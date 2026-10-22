"""Build app/static/i18n/<code>.json: the interface strings machine-translated by OCI.

usage (repo root, real OCI, laptop API key):  py scripts/build_i18n.py <t_en.json> [code ...]
<t_en.json> = {key: English text}: node scripts/dump_ui_strings.js app/static/app.js <t_en.json>
Codes default to every language in app/data/languages.json whose interface is not written
inline in app.js (en, es, ar, zh-CN, zh-TW). Hindi goes through Command A (OCI Language has
no Hindi); every other code through OCI Language.

Placeholders like {pct} must survive translation: each is swapped for {0}, {1}... (which
ai_client already protects), restored after, and checked. A string whose placeholders do
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
os.environ.pop("FAKE_AI", None)
os.environ["AI_PROVIDER"] = "oci"  # the i18n files were built with OCI Language
import oci  # noqa: E402

os.environ.setdefault("OCI_COMPARTMENT_ID", oci.config.from_file()["tenancy"])
os.environ.setdefault("OCI_TEXT_MODEL_ID", "cohere.command-a-03-2025")
from app import ai_client  # noqa: E402

INLINE = {"en", "es", "ar", "zh-CN", "zh-TW"}
KEEP = ["SYNTHETIC DEMO", "SYNTHETIC", "Billo", "PNG", "JPEG"]
NAMED = re.compile(r"\{([A-Za-z_]\w*)\}")
BATCH = 20  # documents per OCI Language call
# Machine translations whose meaning flipped when translated back to English (OCI Language,
# 2026-10-17): left out so the app shows the English line instead.
DROP = {  # meaning changed on back-translation to English (OCI Language, 2026-10-17; audit 2)
    'cs': ['home_not_eligible', 'p_sub', 'r_decides', 'r_no_packet', 'rem_follow'],
    'da': ['home_not_eligible'],
    'de': ['r_deadline', 'r_no_packet', 'r_packet'],
    'fi': ['ai_note', 'home_not_eligible', 'r_no_packet', 'r_packet', 'rem_apply'],
    'fr': ['notice'],
    'fr-CA': ['r_no_packet', 'r_packet'],
    'he': ['home_estimate', 'p_sub', 'r_decides', 'theme_auto', 'theme_dark', 'theme_light'],  # theme: 'tag' (seen in browser)
    'hr': ['home_estimate', 'home_not_eligible', 'r_no_packet', 'theme_auto'],
    'hu': ['home_not_eligible', 'r_no_packet'],
    'it': ['home_estimate', 'notice'],
    'ja': ['home_estimate_note', 'p_sub', 'r_decides'],
    'ko': ['home_estimate_note', 'notice', 'q_minus'],
    'no': ['f_service'],
    'pt': ['r_packet'],
    'pt-BR': ['home_estimate_note', 'r_packet'],
    'ru': ['home_estimate', 'r_fallback', 'theme_auto'],
    'sk': ['home_bill_deadline', 'home_estimate'],
    'sl': ['home_bill_deadline', 'r_packet', 'rem_apply', 'rem_follow', 'theme_auto'],
    'sv': ['r_no_packet', 'r_packet'],
    'th': ['f_service', 'home_estimate_note', 'ins_insured', 'notice', 'p_sub', 'r_deadline', 'r_decides', 'rem_follow'],
    'tr': ['ai_note', 'p_sub', 'r_decides'],
    'vi': ['f_service', 'home_estimate_note', 'notice', 'p_sub', 'r_contact', 'r_decides', 'r_packet', 'rem_follow'],
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
            out += ai_client.translate_genai_many(chunk, code, keep=KEEP)
        else:
            out += ai_client.translate_many(chunk, code, keep=KEEP)
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
    args = sys.argv[1:]
    only = None  # --keys k1,k2: translate just these keys and merge them into the existing files
    if "--keys" in args:
        i = args.index("--keys")
        only = args[i + 1].split(",")
        del args[i:i + 2]
    en = json.load(open(args[0], encoding="utf-8"))
    if only:
        en = {k: en[k] for k in only}
    langs = json.load(open(os.path.join(ROOT, "app", "data", "languages.json"), encoding="utf-8"))
    codes = args[1:] or [l["code"] for l in langs if l["code"] not in INLINE]
    outdir = os.path.join(ROOT, "app", "static", "i18n")
    os.makedirs(outdir, exist_ok=True)
    for code in codes:
        result, dropped = build(code, en)
        if only:
            path = os.path.join(outdir, code + ".json")
            merged = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
            merged.update(result)
            for k in DROP.get(code, ()):
                merged.pop(k, None)
            result = merged
        with open(os.path.join(outdir, code + ".json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(result, f, ensure_ascii=False, indent=0, sort_keys=True)
            f.write("\n")
        print("%-6s kept %3d of %3d  dropped %s" % (code, len(result), len(en), ",".join(dropped) or "-"), flush=True)


if __name__ == "__main__":
    main()
