"""Vision gate (V1) for the EOB prompt: eob-06, eob-07, eob-08 and a not-an-EOB probe through the real model.

usage (repo root):  py spikes/synthetic-eob/gate.py [--dry-run]
4 real calls (3 EOBs + the probe), one each. --dry-run: no OCI import, no network; canned responses
built from pairs_key.json so the scoring and table code run. If the key is missing it is polled
every 60 s for 15 min, then "key missing" and exit 2. Exit 0 on V1 PASS, 1 on V1 FAIL.
Raw model texts go to the session scratchpad, never into the repo.
"""
import argparse
import base64
import concurrent.futures
import json
import os
import re
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)

from app.eob_prompt import build  # noqa: E402

RAW_DIR = (r"C:\Users\daruw\AppData\Local\Temp\claude\C--ClaudeCode-TNHacks27"
           r"\9de6aac5-e09d-497b-a04a-fb65e2d46bb9\scratchpad\v1_raw")
IDS = ["06", "07", "08"]
PLANTED = ["XYZ-SYNTH-0001", "SYNTH-GRP-01", "Sami Example"]
CALL_TIMEOUT = 60
KEY_POLLS = 15
KEY_POLL_SECONDS = 60
FMT = "%-9s %-7s %-7s %-7s %-8s %-7s"


def to_cents(v):
    if v is None or isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return int(round(float(v) * 100))
    s = str(v).strip().replace("$", "").replace(",", "").replace(" ", "")
    if not s or s.lower() in ("null", "none", "n/a"):
        return None
    try:
        return int(round(float(s) * 100))
    except ValueError:
        return None


def to_date(v):
    if v is None:
        return None
    s = str(v).strip()
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return "%s-%s-%s" % m.groups()
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", s)
    if m:
        return "%s-%02d-%02d" % (m.group(3), int(m.group(1)), int(m.group(2)))
    return s


def to_status(v):
    if v is None:
        return None
    return re.sub(r"[\s-]+", "_", str(v).strip().lower())


def norm_eob(d):
    """Model JSON dict -> comparable form: money in cents, lowercase status, ISO dates."""
    lines = d.get("service_lines")
    lines = lines if isinstance(lines, list) else []
    return {"claim_status": to_status(d.get("claim_status")),
            "patient_owes": to_cents(d.get("patient_owes")),
            "date_of_service": to_date(d.get("date_of_service")),
            "lines": [{"date": to_date(x.get("date")),
                       "amount_billed": to_cents(x.get("amount_billed")),
                       "patient_owes": to_cents(x.get("patient_owes"))}
                      for x in lines if isinstance(x, dict)]}


def key_norm(e):
    return {"claim_status": to_status(e.get("claim_status")),
            "patient_owes": e.get("patient_owes_cents"),
            "lines": [{"amount_billed": x.get("amount_billed_cents")} for x in e.get("service_lines", [])]}


def canned(e):
    """What the model would return, formatted like a model: dollars as floats, MM/DD/YYYY, 'Paid'."""
    def dollars(c):
        return None if c is None else c / 100.0

    def us_date(d):
        if not d:
            return d
        y, mo, da = d.split("-")
        return "%s/%s/%s" % (mo, da, y)
    lines = [{"date": us_date(x.get("date")), "description": x.get("description"),
              "amount_billed": dollars(x.get("amount_billed_cents")),
              "patient_owes": dollars(x.get("patient_owes_cents"))}
             for x in e.get("service_lines", [])]
    return json.dumps({"insurer_name": e.get("insurer_name"), "provider_name": e.get("provider_name"),
                       "date_of_service": us_date(e.get("date_of_service")),
                       "claim_number": e.get("claim_number"),
                       "claim_status": (e.get("claim_status") or "").capitalize() or None,
                       "amount_billed": dollars(e.get("amount_billed_cents")),
                       "plan_discount": dollars(e.get("plan_discount_cents")),
                       "plan_paid": dollars(e.get("plan_paid_cents")),
                       "patient_owes": dollars(e.get("patient_owes_cents")),
                       "denial_reason": e.get("denial_reason"), "appeal_deadline": e.get("appeal_deadline"),
                       "insurer_phone": e.get("insurer_phone"), "service_lines": lines}, indent=1)


def load_key():
    path = os.path.join(HERE, "pairs_key.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def wait_for_key():
    for i in range(KEY_POLLS):
        key = load_key()
        if key is not None:
            return key
        if i < KEY_POLLS - 1:
            time.sleep(KEY_POLL_SECONDS)
    return None


def real_caller():
    import oci
    os.environ.pop("FAKE_OCI", None)
    os.environ.setdefault("OCI_COMPARTMENT_ID", oci.config.from_file()["tenancy"])
    os.environ.setdefault("OCI_VISION_MODEL_ID", "cohere.command-a-vision")
    from app import oci_client
    from oci.generative_ai_inference import models as m
    model = os.environ["OCI_VISION_MODEL_ID"]

    def call(path, date):
        with open(path, "rb") as f:
            uri = "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")
        parts = [m.CohereTextContentV2(text=build(date)),
                 m.CohereImageContentV2(image_url=m.CohereImageUrlV2(url=uri))]
        return oci_client._chat(model, parts, json_mode=True, max_tokens=1500)
    return call, oci_client.parse_json_object


def timed(fn, *args):
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    fut = pool.submit(fn, *args)
    try:
        return fut.result(timeout=CALL_TIMEOUT)
    finally:
        pool.shutdown(wait=False)


def save_raw(tag, text, err, dry):
    os.makedirs(RAW_DIR, exist_ok=True)
    with open(os.path.join(RAW_DIR, "%s%s.txt" % (tag, "_dry" if dry else "")), "w", encoding="utf-8") as f:
        f.write(text if not err else "%s\n%s" % (err, text))


def cell(ok):
    return "ok" if ok else "X"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    key = wait_for_key()
    if key is None:
        print("key missing")
        return 2
    pairs = key["pairs"]

    if args.dry_run:
        def call(path, date):
            name = os.path.basename(path)
            if name.startswith("eob-"):
                return canned(pairs[name[4:6]]["eob"])
            return json.dumps({"not_eob": True})
        parse = json.loads
    else:
        call, parse = real_caller()

    jobs = [("eob-" + i, os.path.join(HERE, pairs[i].get("eob_file", "eob-%s.png" % i)), pairs[i]["bill_date_of_service"], pairs[i]["eob"])
            for i in IDS]
    jobs.append(("probe", os.path.normpath(os.path.join(HERE, key["not_eob_probe"])),
                 key["bill_date_of_service"], None))

    print(FMT % ("doc", "status", "owes", "lines", "amounts", "privacy"))
    failed, demo_safe = [], False
    for tag, path, date, truth in jobs:
        text, err, data = "", None, None
        try:
            text = timed(call, path, date)
            data = parse(text)
            if not isinstance(data, dict):
                raise ValueError("not a JSON object")
        except Exception as ex:  # noqa: BLE001 - record and continue
            err = "ERROR %s" % type(ex).__name__
        save_raw(tag, text, err, args.dry_run)
        leak = any(p in text for p in PLANTED)
        if truth is None:
            ok = bool(data) and data.get("not_eob") is True
            print(FMT % (tag, "not_eob:" + cell(ok), "-", "-", "-", cell(not leak)))
            if not ok:
                failed.append("probe:not_eob")
            if leak:
                failed.append("probe:privacy")
            continue
        want = key_norm(truth)
        if data is None:
            cells = [False] * 4
        else:
            got = norm_eob(data)
            cells = [got["claim_status"] == want["claim_status"],
                     got["patient_owes"] == want["patient_owes"],
                     len(got["lines"]) == len(want["lines"]),
                     Counter(x["amount_billed"] for x in got["lines"])
                     == Counter(x["amount_billed"] for x in want["lines"])]
        print(FMT % tuple([tag, ] + [cell(c) for c in cells] + [cell(not leak)]) + ("  " + err if err else ""))
        for name, c in zip(["status", "owes", "lines", "amounts"], cells):
            if not c:
                failed.append("%s:%s" % (tag, name))
        if leak:
            failed.append("%s:privacy" % tag)
        if tag == "eob-06":
            demo_safe = all(cells)

    if failed:
        print("V1 FAIL: " + ", ".join(failed))
    else:
        print("V1 PASS: all cells ok on eob-06, eob-07, eob-08 and the not-EOB probe")
    print("PAIR 06 DEMO-SAFE" if demo_safe else "PAIR 06 NOT DEMO-SAFE")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
