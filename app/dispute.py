"""Dispute letter (Phase 2). The English letter is a fixed template filled from the bill and the
fixed-rule flags: no AI writes any of it. Translation copies build_packet's loop. No app.main import.

build(bill, answers, check_result, today=None) -> {letter_en, letter_translated, translation_check}
  plus insurer_letter_en, insurer_letter_translated, insurer_send_note_en when
  check_result["insurer_letter"] is a dict (app.eob_checks.run); absent otherwise.
render_html(result, language) -> full HTML page.
bill = {"fields": {name: {"value": ...}}, "lines": {...} | None} (the BillIn shape as a dict);
answers = {"language": code, ...}; check_result = app.checks.run(bill).
Template and banner: plan amendment A5.
"""
import html
import json
import logging
import os
from datetime import date

from app import numlock, ai_client

log = logging.getLogger("billscan")

NOTICE_EN = "This is a draft you choose to send. The hospital makes the final decision."
BANNER_EN = ("DRAFT - you decide whether to send it. Found by fixed rules on the charges you confirmed; "
             "only the hospital can confirm an error. Send it to the billing office address or phone "
             "printed on your bill.")
NOT_AVAILABLE_EN = "Translation not available or it failed the number check. Use the English letter."

_E = html.escape

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "languages.json"),
          encoding="utf-8") as _f:
    _DIR = {x["code"]: x["dir"] for x in json.load(_f)}


def _val(bill, name):
    f = (bill.get("fields") or {}).get(name)
    return f.get("value") if isinstance(f, dict) else None


def _text(v):
    return v.strip() if isinstance(v, str) and v.strip() else None


def _letter_en(bill, check_result, today):
    hospital = _text(_val(bill, "hospital_name"))
    account = _text(_val(bill, "account_number"))
    statement = _text(_val(bill, "statement_date"))
    to_line = "To the Billing Office, %s:" % hospital if hospital else "To the Billing Office:"
    items = "\n".join("- " + f["letter_en"] for f in check_result["flags"]
                      if isinstance(f.get("letter_en"), str) and f["letter_en"])
    return (
        "%s\n\n%s\n\nAccount number: %s\nStatement date: %s\n\n"
        "I am asking you to review my bill. I do not understand these items:\n\n%s\n\n"
        "Please send me an itemized bill and an explanation of each item above, and please do not "
        "send this account to collections while you review it.\n\nThank you,\n\n____________________"
    ) % (today, to_line, account or "not shown", statement or "not shown", items)


def _keep(bill, check_result):
    """The hospital name plus every flagged charge description, verbatim and English."""
    keep = []
    hospital = _text(_val(bill, "hospital_name"))
    if hospital:
        keep.append(hospital)
    lines = bill.get("lines")
    items = (lines.get("items") if isinstance(lines, dict) else None) or []
    for f in check_result["flags"]:
        for i in f.get("line_indexes") or []:
            if 0 <= i < len(items):
                d = _text(items[i].get("description"))
                if d and d not in keep:
                    keep.append(d)
    return keep


def _insurer_letter_en(il):
    name = _text(il.get("insurer_name"))
    claim = _text(il.get("claim_number"))
    when = _text(il.get("date_of_service"))
    provider = _text(il.get("provider_name"))
    reason = _text(il.get("denial_reason"))
    to_line = "To %s:" % name if name else "To my insurance company:"
    denial = "your denial of claim %s" % claim if claim else "your denial of my claim"
    body = "I am asking you to reconsider %s for care%s%s." % (
        denial, " on %s" % when if when else "", " at %s" % provider if provider else "")
    if reason:
        body += ' The reason given was: "%s".' % reason
    body += " Please review the claim again and tell me in writing what you need from me."
    return "%s\n\n%s\n\nThank you,\n\n____________________" % (to_line, body)


def _insurer_send_note_en(il):
    deadline = _text(il.get("appeal_deadline"))
    phone = _text(il.get("insurer_phone"))
    note = "Send this to your insurer"
    if deadline:
        note += " before the appeal deadline printed on your summary: %s" % deadline
    note += "."
    if phone:
        note += " Phone printed on your summary: %s." % phone
    return note


def _insurer_keep(il):
    keep = []
    for k in ("insurer_name", "provider_name", "denial_reason"):
        v = _text(il.get(k))
        if v and v not in keep:
            keep.append(v)
    return keep


def _translate_one(src, lang, keep):
    """Translate one English text. Returns the translation, or None when the translator failed
    or the number lock / kept names did not survive."""
    # shortcut: duplicated from build_packet; merge into one helper after the hackathon
    try:
        if lang == "hi":  # OCI Language has no Hindi: a language model
            translated = ai_client.translate_genai_many([src], "hi", keep=keep)
        else:
            translated = ai_client.translate_many([src], lang, keep=keep)
    except Exception as e:
        log.warning("translation failed: %s", type(e).__name__)
        return None
    if translated is None:
        return None
    tr = translated[0]
    ok, _m, _u = numlock.check(tr, numlock.extract_numbers(src))
    if not ok or any(k in src and k not in tr for k in keep):
        return None
    return tr


def build(bill, answers, check_result, today=None):
    letter = _letter_en(bill, check_result, today or date.today().isoformat())
    il = check_result.get("insurer_letter")
    il = il if isinstance(il, dict) else None
    lang = answers["language"]
    check = {"numbers_match": True, "fallback_used": False}
    letter_tr = None
    il_en = _insurer_letter_en(il) if il else None
    il_tr = None
    if lang != "en":
        letter_tr = _translate_one(letter, lang, _keep(bill, check_result))
        ok = letter_tr is not None
        if il:
            il_tr = _translate_one(il_en, lang, _insurer_keep(il))
            ok = ok and il_tr is not None
            il_tr = il_tr or ""
        if ok:
            check["translator"] = ai_client.translator_name(lang)
        else:
            check = {"numbers_match": False, "fallback_used": True}
        letter_tr = letter_tr or None
    out = {"letter_en": letter, "letter_translated": letter_tr, "translation_check": check}
    if il:
        out["insurer_letter_en"] = il_en
        out["insurer_letter_translated"] = il_tr
        out["insurer_send_note_en"] = _insurer_send_note_en(il)
    return out


_CSS = """
body{font-family:system-ui,Segoe UI,Arial,sans-serif;margin:24px;color:#111;line-height:1.45}
h1{font-size:1.4rem;margin:0 0 4px}h2{font-size:1.1rem;margin:22px 0 6px;border-bottom:1px solid #999}
.banner{background:#fff3cd;border:1px solid #c9a227;padding:8px;margin:8px 0}
.cols{display:flex;gap:16px}.cols>div{flex:1;border:1px solid #bbb;padding:10px;white-space:pre-wrap}
@media (max-width:640px){.cols{display:block}.cols>div{margin-bottom:10px}}
@media print{body{margin:0}.cols{display:block}.cols>div{margin-bottom:10px}}
"""


def _cols(en, translated, language):
    d = _DIR.get(language, "ltr")
    tr_block = ""
    if language != "en":
        if translated:
            tr_block = '<div dir="%s" lang="%s">%s</div>' % (d, _E(language), _E(translated))
        else:
            tr_block = "<div>%s</div>" % _E(NOT_AVAILABLE_EN)
    return '<div class="cols"><div>%s</div>%s</div>' % (_E(en), tr_block)


def render_html(result, language):
    cols = _cols(result["letter_en"], result.get("letter_translated"), language)
    if result.get("insurer_letter_en"):
        cols += "<h2>Letter to your insurer</h2><p>%s</p>%s" % (
            _E(result.get("insurer_send_note_en") or ""),
            _cols(result["insurer_letter_en"], result.get("insurer_letter_translated"), language))
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
        'content="width=device-width,initial-scale=1"><title>Letter to the billing office</title>'
        '<style>%s</style></head><body><div class="banner">%s</div><main>'
        "<h1>Letter to the billing office</h1><p>%s</p><h2>Letter</h2>%s</main></body></html>"
    ) % (_CSS, _E(BANNER_EN), _E(NOTICE_EN), cols)
