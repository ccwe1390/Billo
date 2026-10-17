"""Bill to Help - FastAPI app. Stateless: nothing is written to disk, no request bodies are logged.

Endpoints (shapes in docs/contracts.md): POST /extract, /evaluate, /explain, /packet; static UI at /.
"""
import functools
import html
import os
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any, Dict, Literal, Optional

from fastapi import FastAPI, HTTPException, Query, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

from app import numlock, oci_client

CONTRACT_VERSION = 1
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POLICY_PATH = os.path.join(BASE_DIR, "data", "policy_cumberland_synthetic.json")
FPL_PATH = os.path.join(BASE_DIR, "data", "fpl_2026.json")
MAX_IMAGE_BYTES = 8 * 1024 * 1024
ALLOWED_MIME = ("image/png", "image/jpeg")
NOTICE_EN = "This is a draft you choose to send. The hospital makes the final decision."

app = FastAPI(title="Bill to Help", docs_url=None, redoc_url=None)


# ---------------------------------------------------------------- models

class FieldIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: Any = None
    confidence: Optional[float] = None
    confirmed: bool = False


class BillIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    contract_version: int = CONTRACT_VERSION
    fields: Dict[str, FieldIn]


class AnswersIn(BaseModel):
    # extra="forbid": no way to send immigration status, SSN, ID or a name.
    model_config = ConfigDict(extra="forbid")
    contract_version: int = CONTRACT_VERSION
    language: Literal["en", "es", "ar", "zh-CN", "zh-TW", "vi", "fr", "ko", "ru", "de", "hi"]
    for_whom: Literal["self", "family"]
    household_size: int = Field(ge=1, le=12)
    annual_income_cents: int = Field(ge=0)
    files_tax_return: bool


class EvaluateIn(BaseModel):
    bill: BillIn
    answers: AnswersIn


class ResultIn(EvaluateIn):
    # Accepted for compatibility but never trusted: /explain and /packet
    # recompute the result with the engine (a client could send any numbers).
    result: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------- engine access

@functools.lru_cache(maxsize=1)
def _rules():
    from app import engine  # imported lazily so the UI still serves if the engine is missing
    return engine, engine.load_policy(POLICY_PATH), engine.load_fpl(FPL_PATH)


# ---------------------------------------------------------------- /extract

_DATE_FORMATS = ("%m/%d/%Y", "%Y-%m-%d", "%m/%d/%y", "%B %d, %Y", "%b %d, %Y", "%m-%d-%Y")


def _norm_text(v):
    if v is None:
        return None
    s = str(v).strip()
    return s or None


def _norm_date(v):
    s = _norm_text(v)
    if s is None:
        return None
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            pass
    return None


def _norm_cents(v):
    if v is None or isinstance(v, bool):
        return None
    try:
        d = Decimal(str(v).replace("$", "").replace(",", "").strip())
    except InvalidOperation:
        return None
    if not d.is_finite() or d < 0:
        return None
    return int((d * 100).to_integral_value(rounding=ROUND_HALF_UP))


_SELF_PAY = ("self-pay", "self pay", "selfpay", "uninsured", "no insurance", "not insured", "none", "no coverage")
_INSURED = ("insur", "medicare", "medicaid", "tenncare", "blue cross", "aetna", "cigna", "united", "humana")


def _norm_insurance(v):
    s = _norm_text(v)
    if s is None:
        return None
    t = s.lower()
    if any(k in t for k in _SELF_PAY):
        return "self_pay"
    if any(k in t for k in _INSURED):
        return "insured"
    return "unknown"


def normalize_bill(raw):
    """Model JSON -> BillFields. Dates ISO, amount in cents, every field unconfirmed.

    The model reports no per-field confidence, so confidence is 0.0 for an
    unreadable field and null (not reported) otherwise.
    """
    values = {
        "hospital_name": _norm_text(raw.get("hospital_name")),
        "statement_date": _norm_date(raw.get("statement_date")),
        "account_number": _norm_text(raw.get("account_number")),
        "amount_due_cents": _norm_cents(raw.get("amount_due")),
        "date_of_service": _norm_date(raw.get("date_of_service")),
        "insurance_status": _norm_insurance(raw.get("insurance_status")),
    }
    return {
        "contract_version": CONTRACT_VERSION,
        "fields": {
            k: {"value": v, "confidence": 0.0 if v is None else None, "confirmed": False}
            for k, v in values.items()
        },
    }


@app.post("/extract")
async def extract(file: UploadFile):
    mime = (file.content_type or "").lower()
    if mime not in ALLOWED_MIME:
        raise HTTPException(415, "Upload a PNG or JPEG image.")
    data = await file.read(MAX_IMAGE_BYTES + 1)
    if not data or len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(413, "Image is empty or larger than 8 MB.")
    try:
        raw = oci_client.extract_bill(data, mime)
    except Exception:  # no detail echoed: it could contain request content
        raise HTTPException(502, "Photo reading is unavailable. Enter the fields by hand.")
    return normalize_bill(raw)


# ---------------------------------------------------------------- /evaluate

@app.post("/evaluate")
def evaluate(body: EvaluateIn):
    engine, policy, fpl = _rules()
    try:
        return engine.evaluate(body.bill.model_dump(), body.answers.model_dump(), policy, fpl)
    except ValueError as e:
        raise HTTPException(422, str(e))


# ---------------------------------------------------------------- shared text helpers

def _dollars(cents):
    """Same display format as the engine's locked_numbers: '38,000' or '38,000.50'."""
    whole, rem = divmod(cents, 100)
    s = "{:,}".format(whole)
    return s if rem == 0 else "%s.%02d" % (s, rem)


def _amount_due(cents):
    whole, rem = divmod(cents, 100)
    return "{:,}.{:02d}".format(whole, rem)


def _val(bill, name):
    f = bill.fields.get(name)
    return None if f is None else f.value


def _facts_en(bill, answers, result):
    """The three fixed English lines. Every number in them comes from the engine or a confirmed field."""
    n = answers.household_size
    return "\n".join([
        "This bill is from %s. The statement date is %s and the amount due is $%s."
        % (_val(bill, "hospital_name") or "the hospital", _val(bill, "statement_date"),
           _amount_due(_val(bill, "amount_due_cents"))),
        "Your household has %d people and a yearly income of $%s. The %d poverty guideline for %d people is $%s, "
        "so your income is %d%% of it."
        % (n, _dollars(answers.annual_income_cents), result["fpl"]["year"], n,
           _dollars(result["fpl"]["amount_cents"]), result["percent_of_fpl"]),
        "%s. %s" % (result["tier"]["label_en"], result["deadline"]["text_en"]),
    ])


def _allowed_numbers(result, *texts):
    """Engine locked numbers plus the numbers in the fixed English text built from engine/confirmed values."""
    out = list(result.get("locked_numbers", []))
    for t in texts:
        out.extend(numlock.extract_numbers(t))
    return sorted(set(out))


# ---------------------------------------------------------------- /explain

def _server_result(body):
    return evaluate(EvaluateIn(bill=body.bill, answers=body.answers))


@app.post("/explain")
def explain(body: ResultIn):
    result = _server_result(body)
    lang = body.answers.language
    facts = _facts_en(body.bill, body.answers, result)
    out = {"contract_version": CONTRACT_VERSION, "language": lang, "text_en": facts,
           "text": facts, "numbers_match": True, "fallback_used": False, "ai_written": False}
    if lang == "en":
        return out
    allowed = _allowed_numbers(result, facts)
    try:
        text = oci_client.phrase(facts, lang)
        ok, _missing, _unexpected = numlock.check(text, allowed)
    except Exception:
        text, ok = "", False
    if ok:
        out["text"] = text
        out["ai_written"] = True
    else:  # mismatch or model failure: fixed English template
        out["numbers_match"] = False
        out["fallback_used"] = True
    return out


# ---------------------------------------------------------------- /packet

_INSURANCE_LABEL = {"self_pay": "Self-pay (no insurance)", "insured": "Insured", "unknown": "Unknown"}


def _letter_en(bill, answers, result):
    hospital = _val(bill, "hospital_name") or "the hospital"
    n = answers.household_size
    lines = ["To the Financial Assistance Office, %s:" % hospital, ""]
    lines.append("I am asking for financial assistance for the hospital bill below."
                 + (" I am helping a family member with this application." if answers.for_whom == "family" else ""))
    lines.append("")
    if _val(bill, "account_number"):
        lines.append("Account number: %s" % _val(bill, "account_number"))
    lines.append("Statement date: %s" % _val(bill, "statement_date"))
    lines.append("Amount due: $%s" % _amount_due(_val(bill, "amount_due_cents")))
    lines.append("")
    lines.append("My household has %d people and a yearly income of $%s. By my estimate this is %d%% of the %d "
                 "federal poverty guideline." % (n, _dollars(answers.annual_income_cents),
                                                 result["percent_of_fpl"], result["fpl"]["year"]))
    lines.append("I am sending the documents on your checklist. Please review my application and tell me your "
                 "decision in writing.")
    lines.append("")
    lines.append("Thank you,")
    lines.append("______________________  (signature and printed name)")
    return "\n".join(lines)


def build_packet(bill, answers, result):
    """EngineResult + BillFields + HouseholdAnswers -> Packet (docs/contracts.md shape 4)."""
    if not result["tier"]["eligible"]:
        raise HTTPException(422, "No application packet: not eligible under this policy. Use the payment-plan contact.")
    lang = answers.language
    letter = _letter_en(bill, answers, result)
    fields = []

    def add(label, value, source):
        if value not in (None, ""):
            fields.append({"label_en": label, "value": str(value), "source": source})

    add("Hospital", _val(bill, "hospital_name"), "bill")
    add("Account number", _val(bill, "account_number"), "bill")
    add("Statement date", _val(bill, "statement_date"), "bill")
    add("Amount due", "$" + _amount_due(_val(bill, "amount_due_cents")), "bill")
    add("Date of service", _val(bill, "date_of_service"), "bill")
    add("Insurance", _INSURANCE_LABEL.get(_val(bill, "insurance_status") or ""), "bill")
    add("Household size", answers.household_size, "answers")
    add("Yearly household income", "$" + _dollars(answers.annual_income_cents), "answers")
    add("Files a federal tax return", "Yes" if answers.files_tax_return else "No", "answers")
    add("Estimated percent of %d poverty guideline" % result["fpl"]["year"], "%d%%" % result["percent_of_fpl"], "policy")
    add("Policy tier", result["tier"]["label_en"], "policy")

    checklist = [{"id": d["id"], "label_en": d["label_en"], "label_translated": ""} for d in result["documents"]]
    check = {"numbers_match": True, "fallback_used": False}
    letter_tr = ""
    if lang != "en":
        sources = [letter] + [c["label_en"] for c in checklist]
        try:
            if lang == "hi":  # OCI Language has no Hindi: Command A, no back-check
                translated = oci_client.translate_genai_many(sources, "hi")
            else:
                translated = oci_client.translate_many(sources, lang)
        except Exception:
            translated = None
        if translated is None:
            check = {"numbers_match": False, "fallback_used": True}
        else:
            check["back_checked"] = lang != "hi"
            for i, (src, tr) in enumerate(zip(sources, translated)):
                ok, _m, _u = numlock.check(tr, numlock.extract_numbers(src))
                if not ok:
                    check = {"numbers_match": False, "fallback_used": True}
                    translated[i] = ""
            letter_tr = translated[0]
            for c, tr in zip(checklist, translated[1:]):
                c["label_translated"] = tr
    contacts = result["contacts"]
    return {
        "contract_version": CONTRACT_VERSION,
        "application_fields": fields,
        "checklist": checklist,
        "cover_letter_en": letter,
        "cover_letter_translated": letter_tr,
        "translation_check": check,
        "send_to": {"email": contacts.get("email", ""), "phone": contacts.get("phone", ""),
                    "citation": contacts.get("citation", {})},
        "notice_en": NOTICE_EN,
    }


def _cite(c):
    if not c:
        return ""
    parts = [c.get("source", "")]
    if c.get("page") not in (None, ""):
        parts.append("page %s" % c["page"])
    if c.get("effective_date"):
        parts.append("effective %s" % c["effective_date"])
    if c.get("url"):
        parts.append(c["url"])
    return '<span class="cite">Source: %s</span>' % html.escape(", ".join(p for p in parts if p))


_E = html.escape

_PACKET_CSS = """
body{font-family:system-ui,Segoe UI,Arial,sans-serif;margin:24px;color:#111;line-height:1.45}
h1{font-size:1.4rem;margin:0 0 4px}h2{font-size:1.1rem;margin:22px 0 6px;border-bottom:1px solid #999}
.banner{background:#fff3cd;border:1px solid #c9a227;padding:8px;margin:8px 0}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #bbb;padding:5px 8px;text-align:start;vertical-align:top}
.cite{display:block;font-size:.8rem;color:#444}
.cols{display:flex;gap:16px}.cols>div{flex:1;border:1px solid #bbb;padding:10px;white-space:pre-wrap}
.box{display:inline-block;width:14px;height:14px;border:1.5px solid #111;margin-inline-end:8px;vertical-align:middle}
li{margin:6px 0;list-style:none}
@media print{body{margin:0}.cols{display:block}.cols>div{margin-bottom:10px}}
"""


def render_packet_html(packet, result, lang):
    p, r = packet, result
    d = "rtl" if lang == "ar" else "ltr"
    rows = "".join("<tr><td>%s</td><td>%s</td></tr>" % (_E(f["label_en"]), _E(f["value"]))
                   for f in p["application_fields"])
    items = []
    for doc, c in zip(r["documents"], p["checklist"]):
        tr = '<div dir="%s" lang="%s">%s</div>' % (d, lang, _E(c["label_translated"])) if c["label_translated"] else ""
        items.append('<li><span class="box"></span>%s%s%s</li>' % (_E(c["label_en"]), tr, _cite(doc.get("citation"))))
    tr_block = ""
    if lang != "en":
        if p["cover_letter_translated"]:
            tr_block = '<div dir="%s" lang="%s">%s</div>' % (d, lang, _E(p["cover_letter_translated"]))
        else:
            tr_block = "<div>Translation not available or it failed the number check. Use the English letter.</div>"
    cols = '<div class="cols"><div>%s</div>%s</div>' % (_E(p["cover_letter_en"]), tr_block)
    send = p["send_to"]
    synth = ('<div class="banner">SYNTHETIC DEMO. Fictional hospital and policy. Not a real application.</div>'
             if r.get("hospital_id", "").endswith("synthetic") else "")
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
        'content="width=device-width,initial-scale=1"><title>Financial assistance packet</title>'
        "<style>%s</style></head><body>%s<h1>Financial assistance packet</h1>"
        "<p>%s</p><h2>Estimate</h2><p>%s. Income is about %d%% of the %d poverty guideline.</p>%s"
        "<p>%s</p>%s<h2>Application fields</h2><table>%s</table>"
        "<h2>Documents to include</h2><ul>%s</ul><h2>Cover letter</h2>%s"
        "<h2>Where to send it</h2><p>Email: %s<br>Phone: %s</p>%s</body></html>"
    ) % (_PACKET_CSS, synth, _E(p["notice_en"]), _E(r["tier"]["label_en"]), r["percent_of_fpl"], r["fpl"]["year"],
         _cite(r["tier"].get("citation")), _E(r["deadline"]["text_en"]), _cite(r["deadline"].get("citation")),
         rows, "".join(items), cols, _E(send["email"]), _E(send["phone"]), _cite(send.get("citation")))


@app.post("/packet")
def packet(body: ResultIn, format: str = Query("html", pattern="^(html|json)$")):
    result = _server_result(body)
    pk = build_packet(body.bill, body.answers, result)
    if format == "json":
        return pk
    return HTMLResponse(render_packet_html(pk, result, body.answers.language))


# ---------------------------------------------------------------- static UI (must be mounted last)

app.mount("/", StaticFiles(directory=os.path.join(BASE_DIR, "static"), html=True), name="static")
