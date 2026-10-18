"""Dispute letter (Phase 2). The English letter is a fixed template filled from the bill and the
fixed-rule flags: no AI writes any of it. Translation copies build_packet's loop. No app.main import.

build(bill, answers, check_result, today=None) -> {letter_en, letter_translated, translation_check}
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

from app import numlock, oci_client

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
    items = "\n".join("- " + f["letter_en"] for f in check_result["flags"])
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


def build(bill, answers, check_result, today=None):
    letter = _letter_en(bill, check_result, today or date.today().isoformat())
    lang = answers["language"]
    check = {"numbers_match": True, "fallback_used": False}
    letter_tr = None
    if lang != "en":
        # shortcut: duplicated from build_packet; merge into one helper after the hackathon
        sources = [letter]
        keep = _keep(bill, check_result)
        try:
            if lang == "hi":  # OCI Language has no Hindi: Command A
                translated = oci_client.translate_genai_many(sources, "hi", keep=keep)
            else:
                translated = oci_client.translate_many(sources, lang, keep=keep)
        except Exception as e:
            log.warning("translation failed: %s", type(e).__name__)
            translated = None
        if translated is None:
            check = {"numbers_match": False, "fallback_used": True}
        else:
            check["translator"] = "command_a" if lang == "hi" else "oci_language"
            for i, (src, tr) in enumerate(zip(sources, translated)):
                ok, _m, _u = numlock.check(tr, numlock.extract_numbers(src))
                if not ok or any(k in src and k not in tr for k in keep):
                    check = {"numbers_match": False, "fallback_used": True}
                    translated[i] = ""
            letter_tr = translated[0] or None
    return {"letter_en": letter, "letter_translated": letter_tr, "translation_check": check}


_CSS = """
body{font-family:system-ui,Segoe UI,Arial,sans-serif;margin:24px;color:#111;line-height:1.45}
h1{font-size:1.4rem;margin:0 0 4px}h2{font-size:1.1rem;margin:22px 0 6px;border-bottom:1px solid #999}
.banner{background:#fff3cd;border:1px solid #c9a227;padding:8px;margin:8px 0}
.cols{display:flex;gap:16px}.cols>div{flex:1;border:1px solid #bbb;padding:10px;white-space:pre-wrap}
@media (max-width:640px){.cols{display:block}.cols>div{margin-bottom:10px}}
@media print{body{margin:0}.cols{display:block}.cols>div{margin-bottom:10px}}
"""


def render_html(result, language):
    d = _DIR.get(language, "ltr")
    tr_block = ""
    if language != "en":
        if result.get("letter_translated"):
            tr_block = '<div dir="%s" lang="%s">%s</div>' % (d, _E(language), _E(result["letter_translated"]))
        else:
            tr_block = "<div>%s</div>" % _E(NOT_AVAILABLE_EN)
    cols = '<div class="cols"><div>%s</div>%s</div>' % (_E(result["letter_en"]), tr_block)
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
        'content="width=device-width,initial-scale=1"><title>Letter to the billing office</title>'
        '<style>%s</style></head><body><div class="banner">%s</div><main>'
        "<h1>Letter to the billing office</h1><p>%s</p><h2>Letter</h2>%s</main></body></html>"
    ) % (_CSS, _E(BANNER_EN), _E(NOTICE_EN), cols)
