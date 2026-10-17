"""Plain-assert API tests: endpoint functions are called directly (no TestClient / httpx).

Run: py tests/test_api.py   (FAKE_OCI=1 is set here; no network or credentials)
"""
import asyncio
import io
import os
import re
import sys
import time
from types import SimpleNamespace

os.environ["FAKE_OCI"] = "1"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import HTTPException  # noqa: E402
from pydantic import ValidationError  # noqa: E402
from starlette.datastructures import Headers, UploadFile  # noqa: E402
from starlette.requests import Request  # noqa: E402

from app import main, numlock, oci_client  # noqa: E402


PNG_SIG = b"\x89PNG\r\n\x1a\n"
JPEG_SIG = b"\xff\xd8\xff"


def upload(data, mime):
    return UploadFile(file=io.BytesIO(data), filename="bill.png", headers=Headers({"content-type": mime}))


def expect_http(code, fn, *a, **k):
    try:
        fn(*a, **k)
    except HTTPException as e:
        assert e.status_code == code, (e.status_code, e.detail)
        return
    raise AssertionError("expected HTTP %d" % code)


def confirm_all(bill):
    for f in bill["fields"].values():
        f["confirmed"] = True
    return bill


def answers(**over):
    a = {"contract_version": 1, "language": "ar", "for_whom": "family", "household_size": 4,
         "annual_income_cents": 3800000, "files_tax_return": False}
    a.update(over)
    return main.AnswersIn(**a)


# ---- /extract (FAKE_OCI): fields normalized, none confirmed
bill = asyncio.run(main.extract(upload(PNG_SIG + b" fake", "image/png")))
F = bill["fields"]
assert F["statement_date"]["value"] == "2026-10-01"
assert F["amount_due_cents"]["value"] == 481240 and isinstance(F["amount_due_cents"]["value"], int)
assert F["account_number"]["value"] == "CGH-00482913"
assert F["insurance_status"]["value"] == "self_pay"
assert F["date_of_service"]["value"] == "2026-09-12"
assert all(f["confirmed"] is False for f in F.values())
try:
    asyncio.run(main.extract(upload(b"x", "application/pdf")))
    raise AssertionError("pdf accepted")
except HTTPException as e:
    assert e.status_code == 415
try:
    asyncio.run(main.extract(upload(b"", "image/png")))
    raise AssertionError("empty accepted")
except HTTPException as e:
    assert e.status_code == 413

# ---- normalize_bill edge cases
n = main.normalize_bill({"hospital_name": " ", "statement_date": "not a date", "account_number": None,
                         "amount_due": "$1,234.5", "date_of_service": None, "insurance_status": "Aetna PPO"})["fields"]
assert n["hospital_name"]["value"] is None and n["hospital_name"]["confidence"] == 0.0
assert n["statement_date"]["value"] is None
assert n["amount_due_cents"]["value"] == 123450
assert n["insurance_status"]["value"] == "insured"
assert main._norm_insurance("Uninsured") == "self_pay" and main._norm_insurance("Humana-ish?") == "insured"
assert main._norm_insurance("???") == "unknown"
assert main._norm_cents("abc") is None and main._norm_cents(-5) is None and main._norm_cents(4812.40) == 481240

# ---- /evaluate refuses unconfirmed, accepts confirmed
expect_http(422, main.evaluate, main.EvaluateIn(bill=main.BillIn(**bill), answers=answers()))
bill = confirm_all(bill)
res = main.evaluate(main.EvaluateIn(bill=main.BillIn(**bill), answers=answers()))
assert res["percent_of_fpl"] == 115 and res["tier"]["id"] == "free_care" and res["tier"]["eligible"]
assert res["locked_numbers"] == ["115", "4", "38,000", "33,000", "4,812.40", "2027-05-29", "100", "240"], res["locked_numbers"]

# ---- privacy: no way to send extra personal fields
try:
    main.AnswersIn(contract_version=1, language="en", for_whom="self", household_size=1,
                   annual_income_cents=0, files_tax_return=False, ssn="123-45-6789")
    raise AssertionError("extra field accepted")
except ValidationError:
    pass

B = main.BillIn(**bill)
body = main.ResultIn(bill=B, answers=answers(), result=res)

# ---- every number the fixed English text shows is a locked number or derived from it
facts = main._facts_en(B, answers(), res)
assert set(res["locked_numbers"]) <= set(numlock.extract_numbers(facts)), (res["locked_numbers"], facts)

# ---- /explain: en direct; ar via FAKE phrase passes; mismatch falls back
ex_en = main.explain(main.ResultIn(bill=B, answers=answers(language="en"), result=res))
assert ex_en["text"] == ex_en["text_en"] and not ex_en["fallback_used"]
ex_ar = main.explain(body)
assert ex_ar["numbers_match"] and not ex_ar["fallback_used"] and ex_ar["text"]
real_phrase = oci_client.phrase
oci_client.phrase = lambda f, lang: f.replace("38,000", "38,500")
bad = main.explain(body)
assert bad["fallback_used"] and not bad["numbers_match"] and bad["text"] == bad["text_en"]
oci_client.phrase = lambda f, lang: (_ for _ in ()).throw(RuntimeError("down"))
down = main.explain(body)
assert down["fallback_used"] and down["text"] == down["text_en"]
oci_client.phrase = real_phrase
# Arabic-Indic digits for the same numbers pass the lock
oci_client.phrase = lambda f, lang: f.translate({ord(str(i)): chr(0x0660 + i) for i in range(10)})
assert main.explain(body)["numbers_match"]
oci_client.phrase = real_phrase

# ---- /packet: json shape, html page
pk = main.packet(body, format="json")
assert pk["translation_check"] == {"numbers_match": True, "fallback_used": False, "translator": "oci_language"}
assert [c["id"] for c in pk["checklist"]] == ["proof_income", "bill_copy"]      # files_tax_return false
assert pk["cover_letter_en"] and pk["cover_letter_translated"].startswith("[AR draft]")
assert pk["send_to"]["email"] == res["contacts"]["email"] and pk["send_to"]["phone"] == res["contacts"]["phone"]
assert pk["notice_en"].startswith("This is a draft")
assert {f["source"] for f in pk["application_fields"]} == {"bill", "answers", "policy"}
page = main.packet(body)
html = page.body.decode("utf-8")
assert page.status_code == 200 and "<!doctype html>" in html and 'dir="rtl"' in html
assert "CGH-00482913" in html and res["contacts"]["email"] in html and "page 2" in html
tax = main.packet(main.ResultIn(bill=B, answers=answers(files_tax_return=True),
                                result=main.evaluate(main.EvaluateIn(bill=B, answers=answers(files_tax_return=True)))),
                  format="json")
assert [c["id"] for c in tax["checklist"]] == ["proof_income", "tax_return", "bill_copy"]
en_pk = main.packet(main.ResultIn(bill=B, answers=answers(language="en"), result=res), format="json")
assert en_pk["cover_letter_translated"] == "" and not en_pk["translation_check"]["fallback_used"]

# HTML escaping of user-edited fields
evil = main.BillIn(**bill)
evil.fields["hospital_name"].value = "<script>alert(1)</script>"
evil_html = main.packet(main.ResultIn(bill=evil, answers=answers(), result=res)).body.decode("utf-8")
assert "<script>alert(1)" not in evil_html and "&lt;script&gt;" in evil_html

# translation that changes a number -> fallback to English-only
real_tr = oci_client.translate_many
oci_client.translate_many = lambda texts, lang, keep=(): [t.replace("4,812.40", "4,812.04") for t in texts]
fb = main.packet(body, format="json")
assert fb["translation_check"] == {"numbers_match": False, "fallback_used": True}
assert fb["cover_letter_translated"] == ""
oci_client.translate_many = lambda texts, lang, keep=(): (_ for _ in ()).throw(NotImplementedError())
assert main.packet(body, format="json")["translation_check"]["fallback_used"]
oci_client.translate_many = real_tr

# ---- tier 2 languages: AI explanation + letter; Hindi letter is not back-checked
for code in ("zh-CN", "zh-TW", "vi", "fr", "ko", "ru", "de", "hi"):
    a2 = answers(language=code)
    r2 = main.evaluate(main.EvaluateIn(bill=B, answers=a2))
    ex2 = main.explain(main.ResultIn(bill=B, answers=a2, result=r2))
    assert ex2["ai_written"] is True and ex2["numbers_match"] and not ex2["fallback_used"], code
    pk2 = main.packet(main.ResultIn(bill=B, answers=a2, result=r2), format="json")
    assert pk2["translation_check"]["translator"] == ("command_a" if code == "hi" else "oci_language"), code
    assert pk2["translation_check"]["numbers_match"] and not pk2["translation_check"]["fallback_used"], code
    assert pk2["cover_letter_translated"].startswith("[%s draft]" % code.upper()), code
assert pk2["cover_letter_translated"].startswith("[HI draft]")
assert ex_en["ai_written"] is False
try:
    answers(language="ku")
    raise AssertionError("language ku accepted")
except ValidationError:
    pass

# ---- not eligible: honest result, no packet
rich = answers(annual_income_cents=13200100)
res2 = main.evaluate(main.EvaluateIn(bill=B, answers=rich))
assert res2["tier"]["id"] == "not_eligible" and not res2["tier"]["eligible"]
assert res2["contacts"]["payment_plan_phone"]
expect_http(422, main.packet, main.ResultIn(bill=B, answers=rich, result=res2))

# ---- a client-sent result is ignored: the server recomputes it with the engine
fake = dict(res, percent_of_fpl=10, tier=dict(res["tier"], id="free_care", eligible=True))
expect_http(422, main.packet, main.ResultIn(bill=B, answers=rich, result=fake))
assert "115%" in main.explain(main.ResultIn(bill=B, answers=answers(language="en"), result=fake))["text"]

# ---- every UI string row in app.js has zh-CN and zh-TW
js = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "static", "app.js"),
          encoding="utf-8").read()
t_block = js[js.index("const T = {"):js.index("\nconst LANG_NAMES")]
rows = [ln for ln in t_block.splitlines() if re.match(r"^  \w+:\s*\{en:", ln)]
assert len(rows) >= 60, len(rows)
assert all('"zh-CN":' in ln and '"zh-TW":' in ln for ln in rows), [ln[:30] for ln in rows if '"zh-TW":' not in ln]
new_keys = ["step_1", "step_2", "step_3", "step_4", "step_5", "step_of", "load_evaluate", "load_explain", "load_packet",
            "tbl_income", "tbl_result", "band_upto", "band_between", "band_above", "you_tag", "not_affiliated"]
for k in new_keys:
    row = [ln for ln in rows if re.match(r"^  %s:\s*\{en:" % k, ln)]
    assert len(row) == 1 and '"zh-CN":' in row[0] and '"zh-TW":' in row[0], k
assert "working:" not in t_block and 't("working")' not in js     # replaced by the named loading steps
# Result screen: step bar marks the current step; the tier table is read from the engine result
assert "aria-current" in js and "r.tiers" in js
# ---- Command A Vision fences its JSON even in JSON mode (live run 2026-10-17)
fenced = '```json\n{\n  "amount_due": "$4,812.40",\n  "statement_date": "10/01/2026"\n}\n```'
assert oci_client.parse_json_object(fenced) == {"amount_due": "$4,812.40", "statement_date": "10/01/2026"}
assert oci_client.parse_json_object('{"a": 1}') == {"a": 1}

# ---- numbers are shielded from machine translation ("$4,812.40" -> "$4.812,40" seen live)
masked, nums = oci_client.protect_numbers("Amount due: $4,812.40. Account CGH-00482913. Apply by 2027-05-29.")
assert masked == "Amount due: ${0}. Account CGH-{1}. Apply by {2}.", masked
assert nums == ["4,812.40", "00482913", "2027-05-29"]
assert oci_client.restore_numbers("Monto: ${0}. Cuenta CGH-{1}. Antes del {2}.", nums) == \
    "Monto: $4,812.40. Cuenta CGH-00482913. Antes del 2027-05-29."
many = " ".join(str(i) for i in range(12))
assert oci_client.restore_numbers(oci_client.protect_numbers(many)[0], oci_client.protect_numbers(many)[1]) == many

# names are shielded too: the hospital name must not be machine-translated ("(MONOETIC)" seen live)
hosp = "Cumberland General Hospital (SYNTHETIC)"
masked, nums = oci_client.protect_numbers("To %s: due $4,812.40" % hosp, keep=[hosp])
assert masked == "To {0}: due ${1}", masked
assert nums == [hosp, "4,812.40"], nums
assert oci_client.restore_numbers(masked, nums) == "To %s: due $4,812.40" % hosp
assert oci_client.protect_numbers("Due $4,812.40") == ("Due ${0}", ["4,812.40"])      # no keep: unchanged
real_tr = oci_client.translate_many
oci_client.translate_many = lambda texts, lang, keep=(): [t.replace("(SYNTHETIC)", "(MONOETIC)") for t in texts]
mangled = main.packet(body, format="json")
assert mangled["translation_check"]["fallback_used"] is True and mangled["cover_letter_translated"] == ""
oci_client.translate_many = lambda texts, lang, keep=(): list(texts)
intact = main.packet(body, format="json")
assert intact["translation_check"]["fallback_used"] is False and intact["cover_letter_translated"]
oci_client.translate_many = real_tr

# packet layout: <main> landmark, letter columns stack on phones; family wording is unambiguous
ar_html = main.packet(body).body.decode("utf-8")
assert "<main>" in ar_html and "max-width:640px" in ar_html
fam = main.packet(main.ResultIn(bill=B, answers=answers(language="en", for_whom="family"), result=res), format="json")
assert "apply for financial assistance" in fam["cover_letter_en"] and "with this application" not in fam["cover_letter_en"]

# confirm labels carry only the real checkbox (a decorative check icon looked ticked when unconfirmed)
assert 'cb, icon("check")' not in js
# English bill values in RTL pages: inputs pick their own direction; deadline and documents stay one LTR run
assert js.count('dir: "auto"') >= 3
assert 'el("p", {lang: "en", dir: "ltr"}, deadlineLine(' in js

# no placeholder copy may reach a demo screen (pre-mortem T4)
assert "Content pending" not in js and "TODO-CONTENT" not in js

# replaceChildren() prints a null argument as "null": only fill() may call it
assert js.count(".replaceChildren(") == 1 and "function fill(" in js

# ---- B1: the model call runs off the event loop (a 0.3 s call must not stall other requests)
real_extract = oci_client.extract_bill
fake_raw = real_extract(b"", "image/png")


def slow_extract(data, mime):
    time.sleep(0.3)
    return fake_raw


async def ticker():
    t0 = time.perf_counter()
    await asyncio.sleep(0.01)
    return time.perf_counter() - t0


async def concurrent_extracts():
    return await asyncio.gather(main.extract(upload(PNG_SIG + b"1", "image/png")),
                                main.extract(upload(PNG_SIG + b"2", "image/png")), ticker())


oci_client.extract_bill = slow_extract
try:
    t0 = time.perf_counter()
    _a, _b, ticked = asyncio.run(concurrent_extracts())
    whole = time.perf_counter() - t0
finally:
    oci_client.extract_bill = real_extract
assert ticked < 0.2 and whole < 0.55, (ticked, whole)

# ---- B2: a not-eligible household still passes the lock in another language (locked numbers are allowed, not required)
poor_rich = answers(language="es", annual_income_cents=20000000)
res_rich = main.evaluate(main.EvaluateIn(bill=B, answers=poor_rich))
assert res_rich["tier"]["id"] == "not_eligible"
ex_rich = main.explain(main.ResultIn(bill=B, answers=poor_rich))
assert ex_rich["numbers_match"] is True and ex_rich["fallback_used"] is False and ex_rich["ai_written"] is True, ex_rich

# ---- B3: Hindi goes through number/name placeholders; a dropped placeholder fails closed
HOSP = "X (SYNTHETIC)"
SRC = "To X (SYNTHETIC): $4,812.40 on 2026-10-01"
real_fake_fn, real_env, real_chat = oci_client.is_fake, oci_client._env, oci_client._chat


def prompt_text(parts):
    return parts[0].text.split("Text:\n", 1)[1]


try:
    oci_client.is_fake = lambda: False
    oci_client._env = lambda name: "x"
    oci_client._chat = lambda model_id, parts, json_mode, max_tokens=600: prompt_text(parts)
    assert oci_client.translate_genai_many([SRC], "hi", keep=[HOSP]) == [SRC]
    lit = "Account number: {1}. Due $4,812.40 to X (SYNTHETIC)"
    assert oci_client.translate_genai_many([lit], "hi", keep=[HOSP]) == [lit]       # literal {1} stays literal
    assert main.build_packet(B, answers(language="hi"), res)["translation_check"]["fallback_used"] is False
    oci_client._chat = lambda model_id, parts, json_mode, max_tokens=600: prompt_text(parts).replace("{0}", "")
    assert HOSP not in oci_client.translate_genai_many([SRC], "hi", keep=[HOSP])[0]
    dropped = main.build_packet(B, answers(language="hi"), res)
    assert dropped["translation_check"] == {"numbers_match": False, "fallback_used": True}
    assert dropped["cover_letter_translated"] == ""
finally:
    oci_client.is_fake, oci_client._env, oci_client._chat = real_fake_fn, real_env, real_chat

# ---- B4: a cut-off model reply is an error, not a short text
real_env, real_client = oci_client._env, oci_client._genai_client


def chat_reply(finish):
    reply = SimpleNamespace(data=SimpleNamespace(chat_response=SimpleNamespace(
        finish_reason=finish, message=SimpleNamespace(content=[SimpleNamespace(text="cut")]))))
    return SimpleNamespace(chat=lambda detail: reply)


try:
    oci_client._env = lambda name: "x"
    oci_client._genai_client = lambda: chat_reply("MAX_TOKENS")
    try:
        oci_client._chat("m", [], False)
        raise AssertionError("MAX_TOKENS accepted")
    except RuntimeError:
        pass
    oci_client._genai_client = lambda: chat_reply("COMPLETE")
    assert oci_client._chat("m", [], False) == "cut"
finally:
    oci_client._env, oci_client._genai_client = real_env, real_client

# ---- B5: a bill from another hospital is flagged on the packet page
van = main.BillIn(**bill)
van.fields["hospital_name"].value = "Vanderbilt University Medical Center"
res_van = main.evaluate(main.EvaluateIn(bill=van, answers=answers()))
assert res_van["hospital_matches_policy"] is False and res["hospital_matches_policy"] is True
van_html = main.packet(main.ResultIn(bill=van, answers=answers())).body.decode("utf-8")
assert "names a different hospital" in van_html and "Cumberland General Hospital (SYNTHETIC) policy" in van_html
assert "names a different hospital" not in main.packet(body).body.decode("utf-8")

# ---- B6: an upload under the cap stays in memory (Starlette's own parser, ~3 MB body)
boundary = "bth-test-boundary"
payload = PNG_SIG + b"a" * (3 * 1024 * 1024)
mp_body = (("--%s\r\nContent-Disposition: form-data; name=\"file\"; filename=\"bill.png\"\r\n"
            "Content-Type: image/png\r\n\r\n" % boundary).encode() + payload
           + ("\r\n--%s--\r\n" % boundary).encode())


async def parse_upload():
    sent = []

    async def receive():
        if sent:
            return {"type": "http.disconnect"}
        sent.append(1)
        return {"type": "http.request", "body": mp_body, "more_body": False}
    scope = {"type": "http", "method": "POST", "path": "/extract", "query_string": b"", "headers": [
        (b"content-type", ("multipart/form-data; boundary=%s" % boundary).encode()),
        (b"content-length", str(len(mp_body)).encode())]}
    form = await Request(scope, receive).form()
    try:
        up = form["file"]
        assert len(await up.read()) == len(payload)
        return up.file._rolled
    finally:
        await form.close()


assert asyncio.run(parse_upload()) is False
saved_spool = main.MultiPartParser.spool_max_size
main.MultiPartParser.spool_max_size = 1024 * 1024
try:
    assert asyncio.run(parse_upload()) is True      # the check can fail: Starlette's default would spool to disk
finally:
    main.MultiPartParser.spool_max_size = saved_spool

# ---- B7: input limits
main.FieldIn(value="a" * 200)
try:
    main.FieldIn(value="a" * 201)
    raise AssertionError("201-char value accepted")
except ValidationError:
    pass
try:
    main.BillIn(fields={"nickname": {"value": "x"}})
    raise AssertionError("unknown bill field accepted")
except ValidationError:
    pass
main.AnswersIn(contract_version=1, language="en", for_whom="self", household_size=1,
               annual_income_cents=10**12, files_tax_return=False)
for bad in ({"annual_income_cents": 10**12 + 1}, {"contract_version": 2}):
    kw = dict(contract_version=1, language="en", for_whom="self", household_size=1,
              annual_income_cents=0, files_tax_return=False)
    kw.update(bad)
    try:
        main.AnswersIn(**kw)
        raise AssertionError("accepted %r" % bad)
    except ValidationError:
        pass
try:
    main.BillIn(contract_version=2, fields={})
    raise AssertionError("bill contract_version 2 accepted")
except ValidationError:
    pass

main._hits.clear()
try:
    def req(host, xff=None):
        return SimpleNamespace(headers={"x-forwarded-for": xff} if xff else {}, client=SimpleNamespace(host=host))
    for _ in range(40):
        main._rate_limit(req("9.9.9.9"))
    try:
        main._rate_limit(req("9.9.9.9"))
        raise AssertionError("41st request allowed")
    except HTTPException as e:
        assert e.status_code == 429
    main._rate_limit(req("8.8.8.8"))
    for _ in range(40):
        main._rate_limit(req("9.9.9.9", "1.1.1.1, 2.2.2.2"))     # counts as 2.2.2.2, not the client or 1.1.1.1
    expect_http(429, main._rate_limit, req("2.2.2.2"))
    main._rate_limit(req("1.1.1.1"))
finally:
    main._hits.clear()
paid = {r.path for r in main.app.routes if getattr(r, "dependant", None) and r.dependant.dependencies}
assert paid == {"/extract", "/explain", "/packet"}, paid

# ---- B8: amount parsing is strict
for raw_amount, want in (("4,812.40", 481240), ("4812.40", 481240), (4812.4, 481240), ("$4,812.40", 481240),
                         ("4812,40", None), ("4.812,40", None), ("1.234", None), (True, None)):
    assert main._norm_cents(raw_amount) == want, (raw_amount, main._norm_cents(raw_amount))
t0 = time.perf_counter()
assert main._norm_cents("1e999999") is None and main._norm_cents("1E+400000") is None
assert time.perf_counter() - t0 < 0.5

# ---- B12: placeholders for names, numbers and literal {n} come from one pass and round-trip
lit_text = "Account number: {1}. Due $4,812.40 to X (SYNTHETIC)"
for keep_names in (["X (SYNTHETIC)"], []):
    masked_lit, lit_nums = oci_client.protect_numbers(lit_text, keep_names)
    assert "4,812.40" not in masked_lit, masked_lit
    assert oci_client.restore_numbers(masked_lit, lit_nums) == lit_text, (masked_lit, lit_nums)

# ---- B13: no OpenAPI schema; security headers on every response
assert main.app.openapi_url is None


async def echo_next(request):
    return SimpleNamespace(headers={})


hdrs = asyncio.run(main.security_headers(None, echo_next)).headers
assert hdrs == {"X-Content-Type-Options": "nosniff", "Referrer-Policy": "no-referrer",
                "X-Frame-Options": "SAMEORIGIN"}, hdrs

# ---- B14: "1 person", not "1 people"
one = answers(language="en", household_size=1)
res_one = main.evaluate(main.EvaluateIn(bill=B, answers=one))
facts_one = main._facts_en(B, one, res_one)
assert "1 person" in facts_one and "1 people" not in facts_one, facts_one
assert "1 person" in main._letter_en(B, one, res_one) and "1 people" not in main._letter_en(B, one, res_one)
assert "4 people" in main._facts_en(B, answers(), res) and "4 people" in main._letter_en(B, answers(), res)

# ---- B15: the file must really be a PNG or JPEG, and the size cap holds
expect_http(415, lambda: asyncio.run(main.extract(upload(b"this is text, not a picture", "image/png"))))
expect_http(415, lambda: asyncio.run(main.extract(upload(PNG_SIG + b"x", "image/jpeg"))))
assert asyncio.run(main.extract(upload(JPEG_SIG + b"fake", "image/jpeg")))["fields"]["hospital_name"]["value"]
expect_http(413, lambda: asyncio.run(main.extract(
    upload(PNG_SIG + b"a" * (main.MAX_IMAGE_BYTES + 1 - len(PNG_SIG)), "image/png"))))

# ---- B17: the engine and the app format money the same way
from app import engine  # noqa: E402
assert engine._fmt_dollars(3800050) == main._dollars(3800050) == "38,000.50"
assert engine._fmt_dollars(3800000) == main._dollars(3800000) == "38,000"
assert engine._fmt_amount_due(481240) == main._amount_due(481240) == "4,812.40"

# ---- R1: translate_genai_many runs 3 at a time, keeps order, leaves text unchanged
_saved = (oci_client.is_fake, oci_client._env, oci_client._chat)
try:
    oci_client.is_fake = lambda: False
    oci_client._env = lambda name: "x"

    def _slow_chat(model_id, parts, json_mode, max_tokens=600):
        time.sleep(0.3)
        return parts[0].text.split("Text:\n", 1)[1]
    oci_client._chat = _slow_chat
    _texts = ["one 1", "two 2", "three 3", "four 4"]
    _t0 = time.time()
    _out = oci_client.translate_genai_many(_texts, "hi")
    _dt = time.time() - _t0
finally:
    oci_client.is_fake, oci_client._env, oci_client._chat = _saved
assert _out == _texts, _out
assert _dt < 0.9, _dt

# ---- F10 M3/M5: counters (results counted once; explain does not count results)
_saved_counts, _saved_langs = main._counts.copy(), main._langs.copy()
try:
    main._counts.clear()
    main._langs.clear()
    _A = answers()
    main.evaluate(main.EvaluateIn(bill=B, answers=_A))
    assert main._counts["results_free_care"] == 1 and main._langs["ar"] == 1, (main._counts, main._langs)
    main.explain(main.ResultIn(bill=B, answers=_A))
    assert main._counts["results_free_care"] == 1 and main._counts["results_discount"] == 0
    assert main._counts["results_not_eligible"] == 0 and main._langs["ar"] == 1

    # ---- M4: /stats shape, small-number suppression, no content
    main._counts.clear()
    main._counts["photos_read"] = 3
    main._counts["packets"] = 12
    st = main.stats()
    assert st["counts"]["photos_read"] == "<10" and st["counts"]["packets"] == 12, st["counts"]
    assert set(st) == {"contract_version", "since", "counts", "languages", "rules", "rules_review_by"}, set(st)
    assert set(st["counts"]) == {"photos_read", "results_free_care", "results_discount", "results_not_eligible",
                                 "packets", "fallbacks", "household_views"}
    assert st["languages"] == {"ar": "<10"}, st["languages"]
    _dump = str(st)
    assert "CGH-" not in _dump and "4,812" not in _dump
    assert st["rules"] and all(set(r) == {"rule_en", "source", "page", "effective_date"} for r in st["rules"])
    assert st["rules_review_by"] == "2027-01-13"
finally:
    main._counts.clear()
    main._counts.update(_saved_counts)
    main._langs.clear()
    main._langs.update(_saved_langs)

# ---- F10 M2/M5: POST /household
_HA = answers(language="en")
h0 = main.household(main.HouseholdIn(answers=_HA))
assert h0["contract_version"] == 1 and len(h0["bills"]) == 5 and h0["estimate_cents"] == 883765 and h0["eligible"] is True
assert all(b["source"] == "demo" for b in h0["bills"])

_hbill = confirm_all(main.normalize_bill({"hospital_name": "Cumberland General Hospital (SYNTHETIC)",
                                          "statement_date": "2026-10-01", "account_number": "CGH-00482913",
                                          "amount_due": "4812.40", "date_of_service": "2026-09-12",
                                          "insurance_status": "self-pay"}))
h1 = main.household(main.HouseholdIn(answers=_HA, bill=main.BillIn(**_hbill)))
assert len(h1["bills"]) == 5 and h1["bills"][0]["id"] == "bill-01" and h1["bills"][0]["source"] == "yours"
assert [b["source"] for b in h1["bills"][1:]] == ["demo"] * 4
assert main.household(main.HouseholdIn(answers=_HA))["bills"][0]["source"] == "demo"  # demo cache not mutated

_hbill["fields"]["account_number"]["value"] = "CGH-00999999"
h2 = main.household(main.HouseholdIn(answers=_HA, bill=main.BillIn(**_hbill)))
assert len(h2["bills"]) == 6 and h2["bills"][-1]["source"] == "yours" and h2["bills"][-1]["id"] == "yours"
assert h2["estimate_cents"] == 883765 + 481240, h2["estimate_cents"]

h3 = main.household(main.HouseholdIn(answers=answers(language="en", annual_income_cents=20000000)))
assert h3["eligible"] is False and h3["estimate_cents"] == 0

_unconf = main.normalize_bill({"hospital_name": "X", "statement_date": "2026-10-01", "amount_due": "10",
                               "date_of_service": "2026-09-12", "insurance_status": "self-pay"})
_unconf = confirm_all(_unconf)
_unconf["fields"]["amount_due_cents"]["confirmed"] = False
expect_http(422, main.household, main.HouseholdIn(answers=_HA, bill=main.BillIn(**_unconf)))

try:
    main.HouseholdIn(answers=_HA, extra_key=1)
    raise AssertionError("unknown top-level key accepted")
except ValidationError:
    pass

# ---- static UI is mounted
assert any(getattr(r, "path", None) in ("", "/") and getattr(r, "name", "") == "static" for r in main.app.routes)

print("ALL PASS")
