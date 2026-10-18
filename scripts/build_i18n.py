"""Build app/static/i18n/<code>.json: the interface strings machine-translated by OCI.

usage (repo root, real OCI, laptop API key):  py scripts/build_i18n.py <t_en.json> [code ...]
<t_en.json> = {key: English text}: node scripts/dump_ui_strings.js app/static/app.js <t_en.json>
Codes default to every language in app/data/languages.json whose interface is not written
inline in app.js (en, es, ar, zh-CN, zh-TW). Hindi goes through Command A (OCI Language has
no Hindi); every other code through OCI Language.

Placeholders like {pct} must survive translation: each is swapped for {0}, {1}... (which
oci_client already protects), restored after, and checked. A string whose placeholders do
not come back exactly is left out, so the app shows English for that key; the script prints
how many were left out per language. Brand and marker words are protected the same way.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.pop("FAKE_OCI", None)
import oci  # noqa: E402

os.environ.setdefault("OCI_COMPARTMENT_ID", oci.config.from_file()["tenancy"])
os.environ.setdefault("OCI_TEXT_MODEL_ID", "cohere.command-a-03-2025")
from app import oci_client  # noqa: E402

INLINE = {"en", "es", "ar", "zh-CN", "zh-TW"}
KEEP = ["SYNTHETIC DEMO", "SYNTHETIC", "BillScan", "PNG", "JPEG"]
NAMED = re.compile(r"\{([A-Za-z_]\w*)\}")
BATCH = 20  # documents per OCI Language call
# Machine translations whose meaning flipped when translated back to English (OCI Language,
# 2026-10-17): left out so the app shows the English line instead.
DROP = {
    "th": ["notice", "r_decides"],  # notice came back as "the information you entered has been saved"
    "cs": ["r_decides"], "ja": ["r_decides"], "tr": ["r_decides"], "vi": ["r_decides"],  # "the hospital made the final decision"
    "he": ["r_decides", "home_estimate"],
    "hr": ["home_estimate"], "it": ["home_estimate"], "ru": ["home_estimate"], "sk": ["home_estimate"],  # "reduce TO {amt}"
}


def mask(text):
    """'about {pct}% in {year}' -> ('about {0}% in {1}', ['pct', 'year'])"""
    names = []

    def sub(m):
        names.append(m.group(1))
        return "{%d}" % (len(names) - 1)
    return NAMED.sub(sub, text), names


def unmask(text, names):
    return re.sub(r"\{(\d+)\}", lambda m: "{%s}" % names[int(m.group(1))] if int(m.group(1)) < len(names) else m.group(0), text)


def translate(code, texts):
    out = []
    for i in range(0, len(texts), BATCH):
        chunk = texts[i:i + BATCH]
        if code == "hi":
            out += oci_client.translate_genai_many(chunk, code, keep=KEEP)
        else:
            out += oci_client.translate_many(chunk, code, keep=KEEP)
    return out


def build(code, en):
    keys = list(en)
    masked = [mask(en[k]) for k in keys]
    translated = translate(code, [m for m, _ in masked])
    result, dropped = {}, []
    for k, (src, names), tr in zip(keys, masked, translated):
        tr = unmask(tr.strip(), names)
        if sorted(NAMED.findall(tr)) != sorted(names) or not tr:
            dropped.append(k)
            continue
        if k in DROP.get(code, ()):
            dropped.append(k)
            continue
        result[k] = tr
    return result, dropped


def main():
    en = json.load(open(sys.argv[1], encoding="utf-8"))
    langs = json.load(open(os.path.join(ROOT, "app", "data", "languages.json"), encoding="utf-8"))
    codes = sys.argv[2:] or [l["code"] for l in langs if l["code"] not in INLINE]
    outdir = os.path.join(ROOT, "app", "static", "i18n")
    os.makedirs(outdir, exist_ok=True)
    for code in codes:
        result, dropped = build(code, en)
        with open(os.path.join(outdir, code + ".json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(result, f, ensure_ascii=False, indent=0, sort_keys=True)
            f.write("\n")
        print("%-6s kept %3d of %3d  dropped %s" % (code, len(result), len(en), ",".join(dropped) or "-"), flush=True)


if __name__ == "__main__":
    main()
