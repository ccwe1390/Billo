import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
policy = json.loads((ROOT / "app" / "data" / "policy_cumberland_synthetic.json").read_text(encoding="utf-8"))
html = (ROOT / "app" / "static" / "policy-cumberland.html").read_text(encoding="utf-8")

for tier in policy["tiers"]:
    assert tier["label_en"] in html, "missing tier label: " + tier["label_en"]

for doc in policy["documents"]:
    assert doc["label_en"] in html, "missing document label: " + doc["label_en"]

assert str(policy["application_window"]["days_from_statement"]) in html, "missing days_from_statement"
assert policy["contacts"]["phone"] in html, "missing phone"
assert policy["contacts"]["email"] in html, "missing email"
assert policy["tiers"][0]["citation"]["effective_date"] in html, "missing effective_date"
assert "SYNTHETIC" in html, "missing SYNTHETIC"
assert 'id="page-1"' in html, "missing id page-1"
assert 'id="page-2"' in html, "missing id page-2"

print("ALL PASS")
