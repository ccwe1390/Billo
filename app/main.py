"""Billow - FastAPI app. Stateless: nothing is written to disk, no request bodies are logged.

Endpoints (shapes in docs/contracts.md): POST /extract, /evaluate, /explain, /packet, /household, /check,
/dispute; GET /stats; static UI at /.
"""
import asyncio
import collections
import functools
import html
import json
import logging
import math
import os
import re
import threading
import time
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Annotated, Any, Dict, List, Literal, Optional

from fastapi import Depends, FastAPI, Form, HTTPException, Query, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, field_validator
from starlette.formparsers import MultiPartParser

from app import checks, dispute, eob_checks, numlock, oci_client

log = logging.getLogger("bill_to_help")

CONTRACT_VERSION = 1
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POLICY_FILES = tuple(os.path.join(BASE_DIR, "data", n) for n in (
    "policy_vumc.json", "policy_ascension_saint_thomas.json", "policy_cumberland_synthetic.json"))
DEFAULT_POLICY_ID = "vumc"  # the household view and a bill that names no known hospital use this policy
FPL_PATH = os.path.join(BASE_DIR, "data", "fpl_2026.json")
LANGUAGES_PATH = os.path.join(BASE_DIR, "data", "languages.json")
MAX_IMAGE_BYTES = 8 * 1024 * 1024
MultiPartParser.spool_max_size = MAX_IMAGE_BYTES  # an allowed upload stays in memory; bigger ones are refused by Content-Length first
MAX_BODY_BYTES = MAX_IMAGE_BYTES + 64 * 1024  # image plus multipart framing
TOO_BIG = "Image is empty or larger than 8 MB."
ALLOWED_MIME = ("image/png", "image/jpeg")
NOTICE_EN = "This is a draft you choose to send. The hospital makes the final decision."

with open(LANGUAGES_PATH, encoding="utf-8") as _f:
    LANGS = {x["code"]: x for x in json.load(_f)}  # the one language list (app/data/languages.json)

app = FastAPI(title="Billow", docs_url=None, redoc_url=None, openapi_url=None)


@app.exception_handler(RequestValidationError)
async def invalid_request(request, exc):
    # The default 422 body echoes each rejected input back; NaN, Infinity or a lone surrogate there cannot be
    # serialised and turned the 422 into a 500. Send only where it failed and why.
    errors = [{"loc": [str(p).encode("utf-8", "replace").decode("utf-8") for p in e["loc"]],
               "msg": e["msg"], "type": e["type"]} for e in exc.errors()]
    return JSONResponse({"detail": errors}, status_code=422)


MAX_JSON_BYTES = 64 * 1024  # every JSON body the app sends is a few KB (security audit 2026-10-18 #1)
TOO_LARGE = "Request is too large."


class _JsonBodyCap:
    """POST bodies other than /extract: 413 once the declared length or the bytes read pass MAX_JSON_BYTES,
    before the body is parsed. Counting the bytes read also caps a chunked body with no Content-Length.
    The 413 is raised as an HTTPException from inside the route, so the security headers still apply. It must be the
    innermost middleware (added first): behind a BaseHTTPMiddleware the error arrives wrapped and becomes a 400."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["method"] != "POST" or scope["path"] == "/extract":
            return await self.app(scope, receive, send)
        declared = dict(scope["headers"]).get(b"content-length", b"")
        seen = 0

        async def capped():
            nonlocal seen
            if declared.isdigit() and int(declared) > MAX_JSON_BYTES:
                raise HTTPException(413, TOO_LARGE)
            message = await receive()
            seen += len(message.get("body", b""))
            if seen > MAX_JSON_BYTES:
                raise HTTPException(413, TOO_LARGE)
            return message

        await self.app(scope, capped, send)


app.add_middleware(_JsonBodyCap)


@app.middleware("http")
async def refuse_big_upload(request, call_next):
    # Runs before FastAPI parses the multipart body, so an oversize file is never spooled to disk.
    # shortcut: a chunked upload with no Content-Length skips this; the 413 in extract() still catches it.
    if request.method == "POST" and request.url.path == "/extract":
        declared = request.headers.get("content-length", "")
        if declared.isdigit() and int(declared) > MAX_BODY_BYTES:
            return JSONResponse({"detail": TOO_BIG}, status_code=413)
    return await call_next(request)


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response


# ---------------------------------------------------------------- rate limit (paid endpoints only)

# shortcut: 60 per IP per minute because a venue's Wi-Fi NAT shares one bucket; a 422 still consumes it (FastAPI
# parses the body before this dependency runs), so the global cap below is the real cost guard.
RATE_LIMIT = 60
RATE_WINDOW_S = 60
GLOBAL_LIMIT_PER_HOUR = 600
GLOBAL_WINDOW_S = 3600
_hits = {}
_global_hits = collections.deque()
_hits_lock = threading.Lock()


def _rate_limit(request: Request):
    # Behind the VM's proxy the last X-Forwarded-For entry is the one the proxy appended.
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        ip = fwd.split(",")[-1].strip()
    else:
        ip = request.client.host if request.client else "unknown"
    now = time.monotonic()
    with _hits_lock:
        for key in list(_hits):
            q = _hits[key]
            while q and now - q[0] > RATE_WINDOW_S:
                q.popleft()
            if not q:
                del _hits[key]
        q = _hits.setdefault(ip, collections.deque())
        if len(q) >= RATE_LIMIT:
            raise HTTPException(429, "Too many requests. Wait a minute and try again.")
        while _global_hits and now - _global_hits[0] > GLOBAL_WINDOW_S:
            _global_hits.popleft()
        if len(_global_hits) >= GLOBAL_LIMIT_PER_HOUR:
            raise HTTPException(429, "Too many requests. Wait a minute and try again.")
        q.append(now)
        _global_hits.append(now)


# ---------------------------------------------------------------- in-memory counters
# Counts only: no request content, IP or time is ever stored. Reset on restart.

_counts = collections.Counter()
_langs = collections.Counter()
_counts_lock = threading.Lock()
_since = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def _count(key, lang=None):
    try:  # counting must never break a request
        with _counts_lock:
            _counts[key] += 1
            if lang:
                _langs[lang] += 1
    except Exception:
        pass


# ---------------------------------------------------------------- models

_CONTROL = re.compile("[\x00-\x1f\x7f\ud800-\udfff]")  # ASCII control characters and lone surrogates


class FieldIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: Any = None
    confidence: Optional[float] = None
    confirmed: bool = False

    @field_validator("value")
    @classmethod
    def _value_is_plain(cls, v):
        if v is not None and not isinstance(v, (str, int, float, bool)):
            raise ValueError("field value must be text or a number")
        if isinstance(v, float) and not math.isfinite(v):
            raise ValueError("field value must be a finite number")
        if isinstance(v, str):
            v = re.sub(" {2,}", " ", _CONTROL.sub(" ", v))  # newlines and tabs too: a value is one line
            if len(v) > 200:
                raise ValueError("field value is too long")
        return v


_BILL_FIELDS = ("hospital_name", "statement_date", "account_number", "amount_due_cents",
                "date_of_service", "insurance_status")


class LineItemIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    date: Optional[str] = None
    description: str
    quantity: Optional[int] = Field(None, ge=1, le=999, strict=True)
    amount_cents: Optional[int] = Field(None, ge=0, le=10**9, strict=True)

    @field_validator("date")
    @classmethod
    def _date_is_iso(cls, v):
        if v is not None:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
                raise ValueError("date must be YYYY-MM-DD")
            datetime.strptime(v, "%Y-%m-%d")  # a ValueError here is a validation error
        return v

    @field_validator("description")
    @classmethod
    def _description_is_one_line(cls, v):
        v = re.sub(" {2,}", " ", _CONTROL.sub(" ", v))  # same cleaning as a field value: it ends up in a letter
        if len(v) > 120:
            raise ValueError("description is too long")
        return v


class LinesIn(BaseModel):
    """The charge lines under the six fields (plan D3). The engine ignores them; checks.run reads them."""
    model_config = ConfigDict(extra="forbid")
    items: List[LineItemIn] = Field(max_length=40)
    total_charges_cents: Optional[int] = Field(None, ge=0, le=10**9, strict=True)
    payments_cents: Optional[int] = Field(None, ge=0, le=10**9, strict=True)
    confirmed: bool = False
    read: bool = False


class BillIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    contract_version: Literal[1] = CONTRACT_VERSION
    fields: Dict[str, FieldIn]
    lines: Optional[LinesIn] = None

    @field_validator("fields")
    @classmethod
    def _known_fields_only(cls, v):
        if any(k not in _BILL_FIELDS for k in v):
            raise ValueError("unknown bill field")
        return v


_EOB_FIELDS = ("insurer_name", "provider_name", "date_of_service", "claim_number", "claim_status",
               "amount_billed_cents", "plan_discount_cents", "plan_paid_cents", "patient_owes_cents",
               "denial_reason", "appeal_deadline", "insurer_phone")


class EobLineIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    date: Optional[str] = None
    description: str
    amount_billed_cents: Optional[int] = Field(None, ge=0, le=10**9, strict=True)
    patient_owes_cents: Optional[int] = Field(None, ge=0, le=10**9, strict=True)

    @field_validator("date")
    @classmethod
    def _date_is_iso(cls, v):
        if v is not None:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
                raise ValueError("date must be YYYY-MM-DD")
            datetime.strptime(v, "%Y-%m-%d")  # a ValueError here is a validation error
        return v

    @field_validator("description")
    @classmethod
    def _description_is_one_line(cls, v):
        v = re.sub(" {2,}", " ", _CONTROL.sub(" ", v))  # same cleaning as a bill line: it ends up in a letter
        if len(v) > 120:
            raise ValueError("description is too long")
        return v


class EobLinesIn(BaseModel):
    """The service lines printed on the insurer's summary (Phase 3). eob_checks.run reads them."""
    model_config = ConfigDict(extra="forbid")
    items: List[EobLineIn] = Field(max_length=40)
    confirmed: bool = False
    read: bool = False


class EobIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    contract_version: Literal[1] = CONTRACT_VERSION
    fields: Dict[str, FieldIn]
    lines: Optional[EobLinesIn] = None

    @field_validator("fields")
    @classmethod
    def _known_fields_only(cls, v):
        if any(k not in _EOB_FIELDS for k in v):
            raise ValueError("unknown insurance summary field")  # no member ID, group number or name field exists
        return v


class AnswersIn(BaseModel):
    # extra="forbid": no way to send immigration status, SSN, ID or a name.
    model_config = ConfigDict(extra="forbid")
    contract_version: Literal[1] = CONTRACT_VERSION
    language: str
    for_whom: Literal["self", "family"]
    household_size: int = Field(ge=1, le=12)
    annual_income_cents: int = Field(ge=0, le=10**12)
    files_tax_return: bool

    @field_validator("language")
    @classmethod
    def _known_language(cls, v):
        if v not in LANGS:
            raise ValueError("unknown language")
        return v


class EvaluateIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    bill: BillIn
    answers: AnswersIn


class HouseholdIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    answers: AnswersIn
    bill: Optional[BillIn] = None


class ResultIn(EvaluateIn):
    model_config = ConfigDict(extra="forbid")
    # Accepted for compatibility but never trusted: /explain and /packet
    # recompute the result with the engine (a client could send any numbers).
    result: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------- engine access

@functools.lru_cache(maxsize=1)
def _rules():
    from app import engine  # imported lazily so the UI still serves if the engine is missing
    policies = {}
    for path in POLICY_FILES:
        policy = engine.load_policy(path)
        policies[policy["hospital_id"]] = policy
    return engine, policies, engine.load_fpl(FPL_PATH)


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
    s = str(v).replace("$", "").strip()
    if len(s) > 15:
        return None
    if re.fullmatch(r".*,\d{1,2}", s):  # decimal comma: ambiguous
        return None
    if re.search(r"\.\d{3,}$", s):  # "1.234" may be a European thousands separator
        return None
    try:
        d = Decimal(s.replace(",", ""))
    except (InvalidOperation, ArithmeticError, ValueError):
        return None
    if not d.is_finite() or d < 0 or d > Decimal(10**9):
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
    if "pending" in t or any(k in t for k in ("no medicaid", "not medicaid", "no tenncare", "not tenncare")):
        return "unknown"  # "Medicaid pending" / "No Medicaid" do not say the person has coverage (O2 #3)
    if "tenncare" in t or "medicaid" in t:  # before the general insured match (plan D4)
        return "medicaid"
    if any(k in t for k in _INSURED):
        return "insured"
    return "unknown"


def _norm_payments(v):
    """Payments and adjustments are often printed as -$200.00 or ($200.00): stored as a positive amount."""
    if v is None or isinstance(v, bool):
        return None
    m = re.fullmatch(r"\s*\$?\s*\(?\s*[-\u2212]?\s*\$?\s*[-\u2212]?\s*([\d.,]+)\s*\)?\s*", str(v))
    return _norm_cents(m.group(1)) if m else None


def _norm_quantity(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    if isinstance(v, str) and v.strip().isdigit():
        v = int(v.strip())
    return v if isinstance(v, int) and 1 <= v <= 999 else None


MAX_LINES = 40
MAX_LINE_CENTS = 10 ** 9  # LinesIn limit: a bigger read becomes None instead of a 422 on every later call (O2 #1)


def _line_cents(c):
    return c if c is not None and c <= MAX_LINE_CENTS else None


def _norm_lines(raw):
    """The model's line_items, total_charges and payments_and_adjustments -> BillIn.lines (unconfirmed).
    No line_items key: None (the reply was from the old six-field prompt or the model left it out)."""
    if "line_items" not in raw:
        return None
    rows = raw.get("line_items")
    rows = rows if isinstance(rows, list) else []
    items = []
    # shortcut: rows past MAX_LINES are dropped (the test bills print 3-7); the person sees the table and the
    # total, and lines_sum flags the gap.
    for row in rows[:MAX_LINES]:
        if not isinstance(row, dict):
            continue
        desc = re.sub(" {2,}", " ", _CONTROL.sub(" ", str(row.get("description") or ""))).strip()[:120]
        items.append({"date": _norm_date(row.get("date")), "description": desc,
                      "quantity": _norm_quantity(row.get("quantity")),
                      "amount_cents": _line_cents(_norm_cents(row.get("amount")))})
    return {"items": items, "total_charges_cents": _line_cents(_norm_cents(raw.get("total_charges"))),
            "payments_cents": _line_cents(_norm_payments(raw.get("payments_and_adjustments"))),
            "confirmed": False, "read": True}


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
        "lines": _norm_lines(raw),
    }


_EOB_STATUSES = ("paid", "partially_paid", "denied", "pending")


def _norm_status(v):
    s = _norm_text(v)
    if s is None:
        return None
    s = re.sub(r"[ -]+", "_", s.lower())
    return s if s in _EOB_STATUSES else None


def _norm_eob_lines(raw):
    """The model's service_lines -> EobIn.lines (unconfirmed). Not a list: None."""
    rows = raw.get("service_lines")
    if not isinstance(rows, list):
        return None
    items = []
    for row in rows[:MAX_LINES]:
        if not isinstance(row, dict):
            continue
        desc = re.sub(" {2,}", " ", _CONTROL.sub(" ", str(row.get("description") or ""))).strip()[:120]
        items.append({"date": _norm_date(row.get("date")), "description": desc,
                      "amount_billed_cents": _line_cents(_norm_cents(row.get("amount_billed"))),
                      "patient_owes_cents": _line_cents(_norm_cents(row.get("patient_owes")))})
    return {"items": items, "confirmed": False, "read": True}


def _eob_text(v):
    """A model-read EOB text, cut to FieldIn's 200-character limit so a long read never 422s /check later."""
    v = _norm_text(v)
    return v[:200] if isinstance(v, str) else v


def normalize_eob(raw):
    """Model JSON -> EobIn shape. Dates ISO, money in cents, every field unconfirmed. Any other key is dropped."""
    values = {
        "insurer_name": _eob_text(raw.get("insurer_name")),
        "provider_name": _eob_text(raw.get("provider_name")),
        "date_of_service": _norm_date(raw.get("date_of_service")),
        "claim_number": _eob_text(raw.get("claim_number")),
        "claim_status": _norm_status(raw.get("claim_status")),
        "amount_billed_cents": _norm_cents(raw.get("amount_billed")),
        "plan_discount_cents": _norm_cents(raw.get("plan_discount")),
        "plan_paid_cents": _norm_cents(raw.get("plan_paid")),
        "patient_owes_cents": _norm_cents(raw.get("patient_owes")),
        "denial_reason": _eob_text(raw.get("denial_reason")),
        "appeal_deadline": _norm_date(raw.get("appeal_deadline")),
        "insurer_phone": _eob_text(raw.get("insurer_phone")),
    }
    return {
        "contract_version": CONTRACT_VERSION,
        "fields": {
            k: {"value": v, "confidence": 0.0 if v is None else None, "confirmed": False}
            for k, v in values.items()
        },
        "lines": _norm_eob_lines(raw),
    }


@app.post("/extract", dependencies=[Depends(_rate_limit)])
async def extract(file: UploadFile, kind: Annotated[str, Form()] = "bill",
                  date_of_service: Annotated[Optional[str], Form()] = None):
    if kind not in ("bill", "eob"):
        raise HTTPException(422, "Unknown kind.")
    mime = (file.content_type or "").lower()
    if mime not in ALLOWED_MIME:
        raise HTTPException(415, "Upload a PNG or JPEG image.")
    data = await file.read(MAX_IMAGE_BYTES + 1)
    if not data or len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(413, TOO_BIG)
    if not data.startswith(b"\x89PNG\r\n\x1a\n" if mime == "image/png" else b"\xff\xd8\xff"):
        raise HTTPException(415, "Upload a PNG or JPEG image.")
    if kind == "eob":
        dos = date_of_service if date_of_service and re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_of_service) else None
        try:
            raw = await asyncio.to_thread(oci_client.extract_eob, data, mime, dos)
        except Exception as e:  # no detail echoed: it could contain request content
            log.warning("photo reading failed: %s", type(e).__name__)
            raise HTTPException(502, "Photo reading is unavailable. Enter the fields by hand.")
        if raw.get("not_eob") is True:
            raise HTTPException(422, "This doesn't look like an insurance summary.")
        out = normalize_eob(raw)
        # V1 gate 2026-10-18: the real model read a hospital bill with the EOB prompt, did not return not_eob, and
        # invented claim_status "pending" with insurer_name and claim_number null. Neither is printed on a real EOB.
        if out["fields"]["insurer_name"]["value"] is None and out["fields"]["claim_number"]["value"] is None:
            raise HTTPException(422, "This doesn't look like an insurance summary.")
        _count("eobs_read")
        return out
    try:
        raw = await asyncio.to_thread(oci_client.extract_bill, data, mime)
    except Exception as e:  # no detail echoed: it could contain request content
        log.warning("photo reading failed: %s", type(e).__name__)
        raise HTTPException(502, "Photo reading is unavailable. Enter the fields by hand.")
    out = normalize_bill(raw)
    _count("photos_read")
    return out


# ---------------------------------------------------------------- /evaluate

def _evaluate(body):
    engine, policies, fpl = _rules()
    policy, matched = engine.select_policy(_val(body.bill, "hospital_name"), policies, DEFAULT_POLICY_ID)
    try:
        result = engine.evaluate(body.bill.model_dump(), body.answers.model_dump(), policy, fpl)
    except ValueError as e:
        raise HTTPException(422, str(e))
    result["hospital_name_missing"] = matched is None  # no name on the bill: treated like a hospital with no policy
    if matched is None:
        result["hospital_matches_policy"] = False
    return result


@app.post("/evaluate")
def evaluate(body: EvaluateIn):
    result = _evaluate(body)
    _count("results_" + result["tier"]["id"], lang=body.answers.language)
    return result


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


def _people(n):
    return "1 person" if n == 1 else "%d people" % n


def _facts_en(bill, answers, result):
    """The three fixed English lines. Every number in them comes from the engine or a confirmed field."""
    n = answers.household_size
    name = _val(bill, "hospital_name")
    name = name.strip() if isinstance(name, str) else ""  # blank, whitespace or a non-text value reads as no name
    first = ("This bill is from %s. The statement date is %s and the amount due is $%s."
             % (name or "the hospital", _val(bill, "statement_date"),
                _amount_due(_val(bill, "amount_due_cents"))))
    if result["hospital_matches_policy"] is False:  # no policy for this hospital: no tier, percent or deadline
        return first
    if result["tier"]["eligible"]:
        last = "%s. %s" % (result["tier"]["label_en"], result["deadline"]["text_en"])
    else:  # no "Apply by": an ineligible family is pointed to the payment-plan contact instead
        last = "%s." % result["tier"]["label_en"]
    return "\n".join([
        first,
        "Your household has %s and a yearly income of $%s. The %d poverty guideline for %s is $%s, "
        "so your income is %d%% of it."
        % (_people(n), _dollars(answers.annual_income_cents), result["fpl"]["year"], _people(n),
           _dollars(result["fpl"]["amount_cents"]), result["percent_of_fpl"]),
        last,
    ])


# ---------------------------------------------------------------- /explain

def _server_result(body):
    return _evaluate(EvaluateIn(bill=body.bill, answers=body.answers))


@app.post("/explain", dependencies=[Depends(_rate_limit)])
def explain(body: ResultIn):
    result = _server_result(body)
    lang = body.answers.language
    facts = _facts_en(body.bill, body.answers, result)
    out = {"contract_version": CONTRACT_VERSION, "language": lang, "text_en": facts,
           "text": facts, "numbers_match": True, "fallback_used": False, "ai_written": False}
    if lang == "en" or result["hospital_matches_policy"] is False:  # no policy for this hospital: English facts, no model call
        return out
    required = numlock.extract_numbers(facts)  # the translation must show these; locked numbers may also appear
    try:
        if LANGS[lang]["explain"] == "oci_language":
            text = oci_client.translate_many([facts], lang)[0]
        else:
            text = oci_client.phrase(facts, lang)
        ok, _missing, _unexpected = numlock.check(text, required, allowed=result["locked_numbers"])
    except Exception as e:
        log.warning("explanation failed: %s", type(e).__name__)
        text, ok = "", False
    if ok:
        out["text"] = text
        out["ai_written"] = True
    else:  # mismatch or model failure: fixed English template
        out["numbers_match"] = False
        out["fallback_used"] = True
        _count("fallbacks")
    return out


# ---------------------------------------------------------------- /packet

_INSURANCE_LABEL = {"self_pay": "Self-pay (no insurance)", "insured": "Insured", "unknown": "Unknown",
                    "medicaid": "TennCare / Medicaid"}


def _letter_en(bill, answers, result):
    hospital = _val(bill, "hospital_name") or "the hospital"
    n = answers.household_size
    lines = ["To the Financial Assistance Office, %s:" % hospital, ""]
    lines.append("I am asking for financial assistance for the hospital bill below."
                 + (" I am helping a family member apply for financial assistance." if answers.for_whom == "family" else ""))
    lines.append("")
    if _val(bill, "account_number"):
        lines.append("Account number: %s" % _val(bill, "account_number"))
    lines.append("Statement date: %s" % _val(bill, "statement_date"))
    lines.append("Amount due: $%s" % _amount_due(_val(bill, "amount_due_cents")))
    lines.append("")
    lines.append("My household has %s and a yearly income of $%s. By my estimate this is about %d%% of the %d "
                 "federal poverty guideline." % (_people(n), _dollars(answers.annual_income_cents),
                                                 result["percent_of_fpl"], result["fpl"]["year"]))
    lines.append("I am sending the documents on your checklist. Please review my application and tell me your "
                 "decision in writing.")
    lines.append("")
    lines.append("Thank you,")
    lines.append("______________________  (signature and printed name)")
    return "\n".join(lines)


def build_packet(bill, answers, result):
    """EngineResult + BillFields + HouseholdAnswers -> Packet (docs/contracts.md shape 4)."""
    if result["hospital_name_missing"]:
        raise HTTPException(422, "No application packet: the bill shows no hospital name.")
    if result["hospital_matches_policy"] is False:
        raise HTTPException(422, "No application packet: this demo has no policy for this hospital.")
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
        hospital = _val(bill, "hospital_name")
        keep = [hospital] if isinstance(hospital, str) and hospital else []
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
@media (max-width:640px){.cols{display:block}.cols>div{margin-bottom:10px}}
@media print{body{margin:0}.cols{display:block}.cols>div{margin-bottom:10px}}
"""


def render_packet_html(packet, result, lang):
    p, r = packet, result
    d = LANGS[lang]["dir"]
    rows = "".join("<tr><td>%s</td><td>%s</td></tr>" % (_E(f["label_en"]), _E(f["value"]))
                   for f in p["application_fields"])
    items = []
    for doc, c in zip(r["documents"], p["checklist"]):
        tr = '<div dir="%s" lang="%s">%s</div>' % (d, lang, _E(c["label_translated"])) if c["label_translated"] else ""
        link = (' <a href="%s" rel="noopener">%s</a>' % (_E(doc["url"]), _E(doc["url"]))) if doc.get("url") else ""
        items.append('<li><span class="box"></span>%s%s%s%s</li>' % (_E(c["label_en"]), link, tr, _cite(doc.get("citation"))))
    checks = "".join("<li>%s%s</li>" % (_E(c["text_en"]), _cite(c.get("citation"))) for c in r.get("conditions") or [])
    checks = "<h2>The hospital also checks</h2><ul>%s</ul>" % checks if checks else ""
    tr_block = ""
    if lang != "en":
        if p["cover_letter_translated"]:
            tr_block = '<div dir="%s" lang="%s">%s</div>' % (d, lang, _E(p["cover_letter_translated"]))
        else:
            tr_block = "<div>Translation not available or it failed the number check. Use the English letter.</div>"
    cols = '<div class="cols"><div>%s</div>%s</div>' % (_E(p["cover_letter_en"]), tr_block)
    send = p["send_to"]
    email_line = "Email: %s<br>" % _E(send["email"]) if send.get("email") else ""  # no email on file: no line
    if r.get("synthetic"):
        synth = '<div class="banner">SYNTHETIC DEMO. Fictional hospital and policy. Not a real application.</div>'
    else:
        synth = ('<div class="banner">DEMO - made from a SYNTHETIC bill. Policy terms are quoted from the hospital\'s '
                 "published policy (see citations). Do not send this packet; apply on the hospital's own form.</div>")
    if r.get("hospital_matches_policy") is False:
        synth += ('<div class="banner">This bill names a different hospital. This estimate uses the %s policy, '
                  "not that hospital's policy.</div>" % _E(r["policy_hospital_name"]))
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
        'content="width=device-width,initial-scale=1"><title>Financial assistance packet</title>'
        "<style>%s</style></head><body>%s<main><h1>Financial assistance packet</h1>"
        "<p>%s</p><h2>Estimate</h2><p>%s. Income is about %d%% of the %d poverty guideline.</p>%s"
        "<p>%s</p>%s<h2>Application fields</h2><table>%s</table>"
        "<h2>Documents to include</h2><ul>%s</ul>%s<h2>Cover letter</h2>%s"
        "<h2>Where to send it</h2><p>%sPhone: %s</p>%s</main></body></html>"
    ) % (_PACKET_CSS, synth, _E(p["notice_en"]), _E(r["tier"]["label_en"]), r["percent_of_fpl"], r["fpl"]["year"],
         _cite(r["tier"].get("citation")), _E(r["deadline"]["text_en"]), _cite(r["deadline"].get("citation")),
         rows, "".join(items), checks, cols, email_line, _E(send["phone"]), _cite(send.get("citation")))


@app.post("/packet", dependencies=[Depends(_rate_limit)])
def packet(body: ResultIn, format: str = Query("html", pattern="^(html|json)$")):
    result = _server_result(body)
    pk = build_packet(body.bill, body.answers, result)
    _count("packets")
    if pk["translation_check"]["fallback_used"] is True:
        _count("fallbacks")
    if format == "json":
        return pk
    return HTMLResponse(render_packet_html(pk, result, body.answers.language))


# ---------------------------------------------------------------- /check and /dispute (Phase 2: fixed rules, no AI)

def _require_confirmed(bill):
    """Same gate as /evaluate for the six fields, plus the charge lines when the bill carries them."""
    if any(f.confirmed is not True for f in bill.fields.values()):
        raise HTTPException(422, "Confirm every bill field first.")
    if bill.lines is not None and bill.lines.confirmed is not True:
        raise HTTPException(422, "Confirm the charge lines first.")


def _require_eob_confirmed(eob):
    """Same gate as the bill: every field, and the service lines when the summary carries them."""
    if any(f.confirmed is not True for f in eob.fields.values()):
        raise HTTPException(422, "Confirm every insurance summary field first.")
    if eob.lines is not None and eob.lines.confirmed is not True:
        raise HTTPException(422, "Confirm the insurance summary lines first.")


def _run_checks(bill, eob, eob_not_yet):
    """Phase 2 (bill-only) rules, then the Phase 3 insurance rules merged on top."""
    if eob is not None:
        _require_eob_confirmed(eob)
    bill_d = bill.model_dump()
    return eob_checks.run(bill_d, None if eob is None else eob.model_dump(), eob_not_yet, checks.run(bill_d))


class CheckIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    bill: BillIn
    eob: Optional[EobIn] = None
    eob_not_yet: bool = False


@app.post("/check")  # free: fixed rules, no model call, so no rate limit (still under the 64 KiB body cap)
def check(body: CheckIn):
    _require_confirmed(body.bill)
    out = _run_checks(body.bill, body.eob, body.eob_not_yet)
    _count("checks_run")
    return {"contract_version": CONTRACT_VERSION, **out}


class DisputeIn(ResultIn):
    model_config = ConfigDict(extra="forbid")
    eob: Optional[EobIn] = None
    eob_not_yet: bool = False


@app.post("/dispute", dependencies=[Depends(_rate_limit)])
def dispute_letter(body: DisputeIn, format: str = Query("html", pattern="^(html|json)$")):
    _require_confirmed(body.bill)
    found = _run_checks(body.bill, body.eob, body.eob_not_yet)
    if not any(f.get("letter_en") for f in found["flags"]):
        raise HTTPException(422, "No letter: no items to ask about.")
    out = dispute.build(body.bill.model_dump(), body.answers.model_dump(), found)
    _count("disputes")
    if (out.get("translation_check") or {}).get("fallback_used") is True:
        _count("fallbacks")
    if format == "json":
        return out
    return HTMLResponse(dispute.render_html(out, body.answers.language))


# ---------------------------------------------------------------- /household

@functools.lru_cache(maxsize=1)
def _demo_bills():
    with open(os.path.join(BASE_DIR, "data", "demo_bills.json"), encoding="utf-8") as f:
        data = json.load(f)
    return tuple({"id": b["id"], "label_en": b["label_en"], "source": "demo", "fields": b["fields"]}
                 for b in data["bills"])


@app.post("/household")
def household(body: HouseholdIn):
    engine, policies, fpl = _rules()
    policy = policies[DEFAULT_POLICY_ID]  # the household is the demo bills' (VUMC) household; other hospitals' bills are listed, not counted
    bills = [dict(b) for b in _demo_bills()]
    if body.bill is not None:
        fields = body.bill.model_dump()["fields"]
        acct = str(fields.get("account_number", {}).get("value") or "").strip()
        match = [b for b in bills if acct and str(b["fields"]["account_number"]["value"]).strip() == acct]
        if match:  # the user's confirmed values win over the demo bill with the same account
            match[0]["fields"] = fields
            match[0]["source"] = "yours"
        else:
            bills.append({"id": "yours", "label_en": "Your bill", "source": "yours", "fields": fields})
    try:
        result = engine.evaluate_many(bills, body.answers.model_dump(), policy, fpl, date.today())
    except ValueError:  # no Python exception text goes to the client
        raise HTTPException(422, "A date or amount is not valid.")
    _count("household_views")
    return {"contract_version": CONTRACT_VERSION, **result}


# ---------------------------------------------------------------- /stats

_STAT_KEYS = ("photos_read", "results_free_care", "results_discount", "results_not_eligible",
              "packets", "fallbacks", "household_views", "checks_run", "disputes", "eobs_read")


def _shown(n):
    return n if n >= 10 else "<10"


def _rule(text, citation):
    return {"rule_en": text, "source": citation.get("source"), "page": citation.get("page"),
            "effective_date": citation.get("effective_date")}


@app.get("/stats")
def stats():
    engine, policies, _fpl = _rules()
    policy = policies[DEFAULT_POLICY_ID]
    with _counts_lock:
        counts = {k: _shown(_counts[k]) for k in _STAT_KEYS}
        languages = {code: _shown(n) for code, n in sorted(_langs.items())}
    rules = [_rule(t["label_en"], t["citation"]) for t in policy["tiers"]]
    win = policy["application_window"]
    rules.append(_rule("Apply within %d days of the first billing statement" % win["days_from_statement"],
                       win["citation"]))
    cov = engine.coverage_of(policy)
    rules.append(_rule(cov["text_en"], cov["citation"]))
    rules.extend(_rule("Document: " + d["label_en"], d["citation"]) for d in policy["documents"])
    return {"contract_version": CONTRACT_VERSION, "since": _since, "counts": counts, "languages": languages,
            "rules": rules,
            "policies": [{"hospital_id": p["hospital_id"], "hospital_name": p["hospital_name"],
                          "rules_review_by": p["rules_review_by"]} for p in policies.values()],
            "rules_review_by": min(p["rules_review_by"] for p in policies.values())}


# ---------------------------------------------------------------- static UI (must be mounted last)

app.mount("/", StaticFiles(directory=os.path.join(BASE_DIR, "static"), html=True), name="static")
