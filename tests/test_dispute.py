"""Plain-assert tests for app/dispute.py. Run from repo root: FAKE_OCI=1 py tests/test_dispute.py"""
import copy
import json
import os
import sys

os.environ["FAKE_OCI"] = "1"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

from app import checks, dispute

SPIKE = os.path.join(HERE, "..", "spikes", "synthetic-bill")
with open(os.path.join(SPIKE, "lines_key.json"), encoding="utf-8") as fh:
    LINES_KEY = json.load(fh)
with open(os.path.join(SPIKE, "answer_key.json"), encoding="utf-8") as fh:
    ANSWER_KEY = json.load(fh)

TODAY = "2026-10-18"
HOSPITAL = "Cumberland General Hospital (SYNTHETIC)"


def fld(v):
    return {"value": v, "confidence": 0.9, "confirmed": True}


def key_bill(n):
    k = LINES_KEY["bill-%d" % n]
    a = ANSWER_KEY["bill-%d" % n]
    fields = {name: fld(a.get(name)) for name in (
        "hospital_name", "statement_date", "account_number", "amount_due_cents",
        "date_of_service", "insurance_status")}
    fields["amount_due_cents"] = fld(k["amount_due_cents"])
    return {"fields": fields, "lines": {
        "items": copy.deepcopy(k["items"]), "total_charges_cents": k["total_charges_cents"],
        "payments_cents": k["payments_cents"], "confirmed": True, "read": True}}


def make(lang="en", **over):
    bill = key_bill(11)
    for name, v in over.items():
        bill["fields"][name] = fld(v)
    check = checks.run(bill)
    return bill, check, dispute.build(bill, {"language": lang}, check, today=TODAY)


def test_english_letter():
    bill, check, r = make()
    assert set(r) == {"letter_en", "letter_translated", "translation_check"}
    assert r["letter_translated"] is None
    assert r["translation_check"] == {"numbers_match": True, "fallback_used": False}
    L = r["letter_en"]
    assert len(check["flags"]) == 1
    assert "- " + check["flags"][0]["letter_en"] in L
    assert L.startswith(TODAY + "\n\nTo the Billing Office, " + HOSPITAL + ":\n\n"), L[:120]
    assert "Account number: CGH-00582417\nStatement date: 2026-10-16\n\n" in L
    assert "I do not understand these items:\n\n- The charge" in L
    assert L.endswith("collections while you review it.\n\nThank you,\n\n____________________")


def test_arabic_translates_and_passes_lock():
    _, _, r = make("ar")
    assert r["letter_translated"] and r["letter_translated"].startswith("[AR draft]")
    assert r["translation_check"] == {"numbers_match": True, "fallback_used": False,
                                       "translator": "oci_language"}


def test_hindi_uses_command_a():
    _, _, r = make("hi")
    assert r["translation_check"]["translator"] == "command_a"
    assert r["letter_translated"]


def test_dropped_number_falls_back_to_english():
    orig = dispute.oci_client.translate_many
    dispute.oci_client.translate_many = lambda texts, lang, keep=(): [t.replace("1,385.00", "") for t in texts]
    try:
        _, _, r = make("ar")
    finally:
        dispute.oci_client.translate_many = orig
    assert r["letter_translated"] is None
    assert r["translation_check"] == {"numbers_match": False, "fallback_used": True}
    assert "To the Billing Office" in r["letter_en"]
    assert dispute.NOT_AVAILABLE_EN in dispute.render_html(r, "ar")


def test_dropped_description_falls_back():
    orig = dispute.oci_client.translate_many
    dispute.oci_client.translate_many = lambda texts, lang, keep=(): [
        t.replace("CT scan, head, without contrast", "X") for t in texts]
    try:
        _, _, r = make("ar")
    finally:
        dispute.oci_client.translate_many = orig
    assert r["translation_check"]["fallback_used"] is True and r["letter_translated"] is None


def test_translator_error_falls_back():
    orig = dispute.oci_client.translate_many

    def boom(*a, **k):
        raise RuntimeError("down")
    dispute.oci_client.translate_many = boom
    try:
        _, _, r = make("es")
    finally:
        dispute.oci_client.translate_many = orig
    assert r["letter_translated"] is None
    assert r["translation_check"] == {"numbers_match": False, "fallback_used": True}


def test_keep_has_hospital_and_flagged_descriptions():
    bill, check, _ = make()
    assert dispute._keep(bill, check) == [HOSPITAL, "CT scan, head, without contrast"]


def test_no_hospital_name():
    _, _, r = make(hospital_name=None)
    assert "\n\nTo the Billing Office:\n\n" in r["letter_en"]
    assert "To the Billing Office," not in r["letter_en"]


def test_missing_account_number():
    _, _, r = make(account_number=None)
    assert "Account number: not shown\n" in r["letter_en"]


def test_render_html_escapes():
    _, _, r = make(account_number="<script>alert(1)</script>")
    page = dispute.render_html(r, "en")
    assert "<script>" not in page and "&lt;script&gt;" in page
    assert dispute.NOTICE_EN in page
    assert "DRAFT - you decide whether to send it." in page
    r2 = dict(r, letter_translated="<b>x</b>")
    assert "<b>x</b>" not in dispute.render_html(r2, "ar")
    assert 'dir="rtl"' in dispute.render_html(r2, "ar")


def test_no_savings_word():
    for lang in ("en", "ar"):
        _, _, r = make(lang)
        page = dispute.render_html(r, lang)
        assert "savings" not in (r["letter_en"] + (r["letter_translated"] or "") + page).lower()
    with open(dispute.__file__, encoding="utf-8") as fh:
        assert "savings" not in fh.read().lower()


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        fn()
        print("ok", name)
    print("ALL PASS (%d tests)" % len(tests))
