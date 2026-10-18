// node scripts/dump_ui_strings.js app/static/app.js <out.json> : writes {key: English} from the T table,
// the input of scripts/build_i18n.py
const fs = require("fs");
const src = fs.readFileSync(process.argv[2], "utf8");
const block = src.slice(src.indexOf("const T = {"), src.indexOf("\nconst LANG_NAMES"));
const T = new Function(block.replace("const T =", "return") )();
const out = {};
for (const k of Object.keys(T)) out[k] = T[k].en;
fs.writeFileSync(process.argv[3], JSON.stringify(out, null, 1));
console.log("keys", Object.keys(out).length);
