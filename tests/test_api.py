"""Plain-assert API tests: endpoint functions are called directly (no TestClient / httpx).

Run: py tests/test_api.py   (FAKE_OCI=1 is set here; no network or credentials)
"""
import asyncio
import io
import os
import re
import sys

os.environ["FAKE_OCI"] = "1"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import HTTPException  # noqa: E402
from pydantic import ValidationError  # noqa: E402
from starlette.datastructures import Headers, UploadFile  # noqa: E402

from app import main, numlock, oci_client  # noqa: E402


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
bill = asyncio.run(main.extract(upload(b"\x89PNG fake", "image/png")))
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
assert pk["translation_check"] == {"numbers_match": True, "fallback_used": False, "back_checked": True}
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
oci_client.translate_many = lambda texts, lang: [t.replace("4,812.40", "4,812.04") for t in texts]
fb = main.packet(body, format="json")
assert fb["translation_check"] == {"numbers_match": False, "fallback_used": True}
assert fb["cover_letter_translated"] == ""
oci_client.translate_many = lambda texts, lang: (_ for _ in ()).throw(NotImplementedError())
assert main.packet(body, format="json")["translation_check"]["fallback_used"]
oci_client.translate_many = real_tr

# ---- tier 2 languages: AI explanation + letter; Hindi letter is not back-checked
for code in ("zh-CN", "zh-TW", "vi", "fr", "ko", "ru", "de", "hi"):
    a2 = answers(language=code)
    r2 = main.evaluate(main.EvaluateIn(bill=B, answers=a2))
    ex2 = main.explain(main.ResultIn(bill=B, answers=a2, result=r2))
    assert ex2["ai_written"] is True and ex2["numbers_match"] and not ex2["fallback_used"], code
    pk2 = main.packet(main.ResultIn(bill=B, answers=a2, result=r2), format="json")
    assert pk2["translation_check"]["back_checked"] is (code != "hi"), code
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
# ---- Command A Vision fences its JSON even in JSON mode (live run 2026-10-17)
fenced = '```json\n{\n  "amount_due": "$4,812.40",\n  "statement_date": "10/01/2026"\n}\n```'
assert oci_client.parse_json_object(fenced) == {"amount_due": "$4,812.40", "statement_date": "10/01/2026"}
assert oci_client.parse_json_object('{"a": 1}') == {"a": 1}

# replaceChildren() prints a null argument as "null": only fill() may call it
assert js.count(".replaceChildren(") == 1 and "function fill(" in js

# ---- static UI is mounted
assert any(getattr(r, "path", None) in ("", "/") and getattr(r, "name", "") == "static" for r in main.app.routes)

print("ALL PASS")
