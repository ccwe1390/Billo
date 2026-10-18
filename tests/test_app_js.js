"use strict";
// Executes app/static/app.js (unmodified) inside a minimal fake DOM and tests its logic.
// Run: node tests/test_app_js.js     Plain Node, no npm packages. Prints ALL PASS and exits 0, or exits 1.
// Not a browser: layout, CSS, real events and real fetch are not covered (that stays a manual/phone check).
// Tests tagged "fix N" check the audit-2 fixes (docs/2026-10-17_audit-2.md); on an app.js without that fix they fail.
const assert = require("node:assert");
const fs = require("node:fs");
const path = require("node:path");

// ---------- fake DOM
class FakeNode {
  constructor(tag) {
    this.tag = tag; this.children = []; this.attrs = {}; this.listeners = {}; this.parent = null;
    this.hidden = false; this.disabled = false; this.checked = false; this.className = "";
    this._text = ""; this._v = undefined; this.dataset = {}; this.style = {};
    const self = this;
    this.classList = {
      add(c) { const a = self.className.split(/\s+/).filter(Boolean); if (!a.includes(c)) a.push(c); self.className = a.join(" "); },
      remove(c) { self.className = self.className.split(/\s+/).filter(x => x && x !== c).join(" "); },
      contains(c) { return self.className.split(/\s+/).includes(c); },
      toggle(c, on) { if (on === undefined) on = !this.contains(c); if (on) this.add(c); else this.remove(c); return on; },
    };
  }
  get id() { return this.attrs.id || ""; }
  set id(v) { this.attrs.id = String(v); }
  get value() {
    if (this._v !== undefined) return this._v;
    if (this.tag === "select") {
      const sel = this.children.find(o => o.attrs.selected !== undefined);
      if (sel) return sel.attrs.value || "";
    }
    return this.attrs.value !== undefined ? this.attrs.value : "";
  }
  set value(v) { this._v = String(v); }
  setAttribute(k, v) {
    this.attrs[k] = String(v);
    if (k === "hidden") this.hidden = true;
    if (k === "disabled") this.disabled = true;
    if (k === "class") this.className = String(v);
  }
  removeAttribute(k) {
    delete this.attrs[k];
    if (k === "hidden") this.hidden = false;
    if (k === "disabled") this.disabled = false;
  }
  getAttribute(k) { return this.attrs[k] === undefined ? null : this.attrs[k]; }
  _adopt(k) {
    if (k instanceof FakeNode) { if (k.parent) k.remove(); return k; }
    const n = new FakeNode("#text"); n._text = String(k); return n;
  }
  append(...ks) { for (const k of ks) { const n = this._adopt(k); n.parent = this; this.children.push(n); } }
  prepend(...ks) { for (const k of [...ks].reverse()) { const n = this._adopt(k); n.parent = this; this.children.unshift(n); } }
  remove() { if (this.parent) { this.parent.children = this.parent.children.filter(c => c !== this); this.parent = null; } }
  replaceChildren(...ks) { for (const c of this.children) c.parent = null; this.children = []; this.append(...ks); }
  set textContent(v) { for (const c of this.children) c.parent = null; this.children = []; this._text = String(v); }
  get textContent() { return this._text + this.children.map(c => c.textContent).join(""); }
  addEventListener(type, fn) { (this.listeners[type] = this.listeners[type] || []).push(fn); }
  dispatch(type, ev) { return Promise.all((this.listeners[type] || []).map(f => f(Object.assign({target: this}, ev || {})))); }
  click() { for (const f of (this.listeners.click || [])) f({target: this}); }
  focus() { document.activeElement = this; }
  all() { return this.children.flatMap(c => [c, ...c.all()]); }
  querySelector(sel) {
    const toks = sel.replace(":scope > ", "").trim().split(/\s+/);
    let scopes = [this];
    for (const tok of toks) {
      const next = [];
      for (const s of scopes) for (const n of s.all()) if (matchTok(n, tok)) next.push(n);
      scopes = next;
    }
    return scopes[0] || null;
  }
}
function matchTok(n, tok) {
  if (tok.startsWith("#")) return n.id === tok.slice(1);
  if (tok.startsWith(".")) return n.classList.contains(tok.slice(1));
  return n.tag === tok;
}
const root = new FakeNode("root");
const docEl = new FakeNode("html");
const body = new FakeNode("body");
const mk = (tag, id, attrs) => { const n = new FakeNode(tag); n.attrs.id = id; Object.assign(n, attrs || {}); root.append(n); return n; };
["app-title", "theme-btn", "stepper", "steps", "step-cap", "main", "status", "alert", "foot"].forEach(id => mk("div", id));
for (let i = 1; i <= 7; i++) mk("section", "s" + i);
const doc = {
  activeElement: null, body, documentElement: docEl,
  createElement: tag => new FakeNode(tag),
  getElementById: id => root.all().find(n => n.id === id) || null,
  querySelector: sel => root.querySelector(sel),
  querySelectorAll: sel => root.all().filter(n => matchTok(n, sel)),
};

// ---------- fake browser globals
const fetchQueue = []; // pending requests: {url, opts, resolve, reject}
function fakeResponse(body, status) {
  status = status || 200;
  return {ok: status >= 200 && status < 300, status,
          json: async () => { if (typeof body === "string") throw new SyntaxError("not json"); return body; },
          text: async () => typeof body === "string" ? body : JSON.stringify(body)};
}
function take(urlPart) { // remove and return the oldest pending request whose url contains urlPart
  const i = fetchQueue.findIndex(r => r.url.includes(urlPart));
  if (i < 0) throw new Error("no pending fetch for " + urlPart + " (pending: " + fetchQueue.map(r => r.url).join(", ") + ")");
  return fetchQueue.splice(i, 1)[0];
}
const respond = (req, body, status) => req.resolve(fakeResponse(body, status));
const NO_FLAGS = {contract_version: 1, flags: [], total_to_ask_cents: 0, lines_checked: false};
function answerChecks(body, status) { // the app asks POST /check right after /evaluate succeeds: answer every pending one; returns how many
  let n = 0;
  while (fetchQueue.some(q => q.url.includes("/check"))) { respond(take("/check"), body || NO_FLAGS, status); n++; }
  return n;
}
const flush = async () => { for (let i = 0; i < 6; i++) await new Promise(r => setImmediate(r)); };

let lastBlob = null;
const timers = [];
Object.assign(globalThis, {
  document: doc,
  window: {matchMedia: () => ({matches: false}), addEventListener() {}},
  location: {search: "", origin: "http://x"},
  confirm: () => true,
  fetch: (url, opts) => new Promise((resolve, reject) => {
    fetchQueue.push({url: String(url), opts, resolve, reject});
    if (opts && opts.signal) opts.signal.addEventListener("abort", () => { // like a browser: an aborted fetch rejects with an AbortError
      const e = new Error("The operation was aborted."); e.name = "AbortError"; reject(e);
    });
  }),
  setTimeout: (fn, ms) => { timers.push({fn, ms}); return timers.length; }, // never fires by itself: tests call timers[timers.length - 1].fn()
  clearTimeout: () => {},
});
Object.defineProperty(globalThis, "navigator", {value: {language: "en-US"}, configurable: true, writable: true});
URL.createObjectURL = blob => { lastBlob = blob; return "blob:fake"; };
URL.revokeObjectURL = () => {};

// ---------- load app.js unmodified; export its top-level names by appending one statement
const NAMES = ["S", "T", "I18N", "LANGS", "SAFETY_KEYS", "t", "tSafe", "tNodes", "machineTranslated", "dirOf", "dollarsToCents",
               "money", "buildIcs", "downloadIcs", "submitAnswers", "show", "restart", "loadLang"];
const src = fs.readFileSync(process.env.APP_JS || path.join(__dirname, "..", "app", "static", "app.js"), "utf8"); // APP_JS: test another copy (e.g. a mutant)
const exportSrc = "\n;globalThis.__app = {" +
  NAMES.map(n => `get ${n}() { return typeof ${n} !== "undefined" ? ${n} : undefined; }`).join(",") +
  ", get curScreen() { return curScreen; }};\n";
try {
  new Function(src + exportSrc)();
} catch (e) {
  console.log("FAIL: app.js did not load in the fake DOM: " + (e && e.stack || e));
  process.exit(1);
}
const A = globalThis.__app;
const {S, T, I18N} = A;
for (const n of ["S", "T", "I18N", "LANGS", "t", "tSafe", "dirOf", "dollarsToCents", "money", "buildIcs", "downloadIcs",
                 "submitAnswers", "show", "restart", "loadLang"]) {
  if (A[n] === undefined) { console.log("FAIL: app.js no longer defines " + n); process.exit(1); }
}

// ---------- helpers
const CITE = {source: "Policy", page: 3, effective_date: "2026-01-01", url: "http://u"};
function makeResult(pct, eligible) {
  return {policy_hospital_name: "H", hospital_matches_policy: true, percent_of_fpl: pct, fpl: {year: 2026, citation: CITE},
    tier: {eligible: eligible !== false, label_en: "Tier", citation: CITE},
    tiers: [{min_percent_exclusive: null, max_percent: 200, label_en: "A", current: true}],
    deadline: {date: "2099-01-01", text_en: "Apply by 2099-01-01", citation: CITE},
    documents: [{label_en: "ID", citation: CITE}],
    contacts: {email: "a@b.com", phone: "(555) 123-4567", payment_plan_phone: "(555) 999-0000", citation: CITE}};
}
const makeExplain = tag => ({fallback_used: false, text_en: "EXPLAIN-" + tag, text: "EXPLAIN-" + tag});
function resetApp() {
  fetchQueue.length = 0;
  for (const k of Object.keys(I18N)) delete I18N[k];
  Object.assign(S, {lang: "en", view: "en", forWhom: "self", theme: "auto"});
  A.restart();
  S.bill = null;
}
function fullBill() { // every field present and confirmed, so screen 2 renders if a test goes Back
  const f = {};
  for (const n of ["hospital_name", "statement_date", "account_number", "amount_due_cents", "date_of_service", "insurance_status"])
    f[n] = {value: n === "amount_due_cents" ? 100000 : "x", confidence: 1, confirmed: true};
  return {contract_version: 1, fields: f};
}
function setupQuestions() { // the state a user has when they tap "See my result"
  S.bill = fullBill();
  S.size = "3"; S.income = "38,000"; S.tax = true; S.lang = "en"; S.view = "en";
  A.show(3);
}
const byId = id => doc.getElementById(id);
const textOf = n => typeof n === "string" ? n : n.textContent;
const nodesText = nodes => nodes.map(textOf).join("");
const bodyOf = req => JSON.parse(req.opts.body);
const THAI = "ครอบครัวของคุณสามารถยื่นขอความช่วยเหลือทางการเงินจากโรงพยาบาลได้ภายในวันนี้".repeat(5).slice(0, 150);
const icsEscape = s => s.replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,");
const unfold = s => s.replace(/\r\n[ \t]/g, "");

// ---------- test runner
const tests = [];
const test = (name, fix, fn) => tests.push({name, fix, fn});

// a. dollarsToCents
test("a. dollarsToCents", "", () => {
  const d = A.dollarsToCents;
  const cases = [["38000", 3800000], ["38,000.50", 3800050], ["٣٨٠٠٠", 3800000], ["３８０００", 3800000], ["۳۸۰۰۰", 3800000],
    ["$4,812.4", 481240], ["4812.40", 481240], ["0", 0], ["0.05", 5], ["١٢٫٥", 1250], [" 12 ", 1200],
    ["abc", null], ["", null], [null, null], [undefined, null], ["-5", null], ["1e3", null], ["1,23", null], ["38000.999", null],
    ["12 345", null], ["99999999999999999999", null], ["$", null], [".50", null]];
  for (const [input, want] of cases) assert.strictEqual(d(input), want, "dollarsToCents(" + JSON.stringify(input) + ")");
});

// b. money
test("b. money", "", () => {
  const m = A.money;
  assert.strictEqual(m(481240), "$4,812.40");
  assert.strictEqual(m(0), "$0.00");
  assert.strictEqual(m(5), "$0.05");
  assert.strictEqual(m(99999), "$999.99");
  assert.strictEqual(m(100000), "$1,000.00");
  assert.strictEqual(m(123456789), "$1,234,567.89");
});

// c. buildIcs: 2 events, CRLF, folding at 75 octets
test("c1. buildIcs shape: 2 VEVENT, CRLF only, DTSTAMP", "fix 30", () => {
  const ics = A.buildIcs([{date: "20270529", summary: "one, two; three"}, {date: "20261116", summary: "second"}], new Date("2026-10-17T12:00:00Z"));
  assert.strictEqual(ics.split("BEGIN:VEVENT").length - 1, 2, "BEGIN:VEVENT count");
  assert.strictEqual(ics.split("END:VEVENT").length - 1, 2, "END:VEVENT count");
  assert.strictEqual(ics.split("BEGIN:VCALENDAR").length - 1, 1);
  assert.ok(ics.startsWith("BEGIN:VCALENDAR\r\n") && ics.endsWith("END:VCALENDAR\r\n"), "starts/ends with CRLF-terminated calendar lines");
  const noCrlf = ics.replace(/\r\n/g, "");
  assert.ok(!/[\r\n]/.test(noCrlf), "a bare CR or LF is present");
  assert.ok(ics.includes("DTSTAMP:20261017T120000Z\r\n"), "DTSTAMP");
  assert.ok(ics.includes("DTSTART;VALUE=DATE:20270529\r\n") && ics.includes("DTSTART;VALUE=DATE:20261116\r\n"), "DTSTART");
  assert.ok(unfold(ics).includes("SUMMARY:one\\, two\\; three\r\n"), "TEXT escaping of , and ;");
});
test("c2. buildIcs folds every line to <= 75 octets (long Thai summary)", "fix 30", () => {
  const summary = THAI + ", end; x\\y";
  const ics = A.buildIcs([{date: "20270529", summary}, {date: "20261116", summary: "short"}], new Date("2026-10-17T12:00:00Z"));
  const lines = ics.split("\r\n");
  assert.strictEqual(lines.pop(), "", "output ends with CRLF");
  const longest = Math.max(...lines.map(l => Buffer.byteLength(l, "utf8")));
  assert.ok(longest <= 75, "longest line is " + longest + " octets (limit 75)");
  assert.ok(lines.some(l => l.startsWith(" ")), "no continuation line starts with a space: nothing was folded");
  assert.ok(unfold(ics).includes("SUMMARY:" + icsEscape(summary) + "\r\n"), "unfolded SUMMARY differs from the original text");
  assert.strictEqual(ics.split("BEGIN:VEVENT").length - 1, 2, "VEVENT count after folding");
});
test("c3. buildIcs fold never splits a UTF-8 character (4-byte emoji)", "fix 30", () => {
  const summary = "\u{1F600}".repeat(40); // 160 octets, 80 UTF-16 units
  const ics = A.buildIcs([{date: "20270529", summary}], new Date("2026-10-17T12:00:00Z"));
  for (const line of ics.split("\r\n")) {
    assert.ok(Buffer.byteLength(line, "utf8") <= 75, "line over 75 octets: " + Buffer.byteLength(line, "utf8"));
    assert.ok(!/[\ud800-\udbff](?![\udc00-\udfff])|(?<![\ud800-\udbff])[\udc00-\udfff]/.test(line), "lone surrogate (a character was split)");
  }
  assert.ok(unfold(ics).includes("SUMMARY:" + summary + "\r\n"), "unfolded SUMMARY differs from the original text");
  assert.strictEqual(Buffer.from(ics, "utf8").toString("utf8"), ics, "UTF-8 round trip changed the text");
});
test("c4. downloadIcs (real Home path) with a 150-char Thai ics_deadline", "fix 30", async () => {
  resetApp();
  S.view = "th"; I18N.th = {ics_deadline: THAI};
  lastBlob = null;
  A.downloadIcs({earliest_deadline: {date: "2027-05-29"}});
  assert.ok(lastBlob, "downloadIcs did not create a Blob");
  const ics = await lastBlob.text();
  assert.strictEqual(ics.split("BEGIN:VEVENT").length - 1, 2, "VEVENT count");
  assert.ok(ics.includes("DTSTART;VALUE=DATE:20270529"), "first event is the deadline date");
  assert.ok(!/[\r\n]/.test(ics.replace(/\r\n/g, "")), "bare CR or LF");
  const longest = Math.max(...ics.split("\r\n").map(l => Buffer.byteLength(l, "utf8")));
  assert.ok(longest <= 75, "longest line is " + longest + " octets (limit 75)");
  assert.ok(unfold(ics).includes("SUMMARY:" + THAI + "\r\n"), "unfolded deadline SUMMARY lost text");
});

// d. dirOf and the language table
test("d. dirOf and LANGS", "", () => {
  assert.strictEqual(A.dirOf("ar"), "rtl");
  assert.strictEqual(A.dirOf("he"), "rtl");
  assert.strictEqual(A.dirOf("en"), "ltr");
  assert.strictEqual(A.dirOf("th"), "ltr");
  assert.strictEqual(A.dirOf("zz"), "ltr", "unknown code defaults to ltr");
  assert.deepStrictEqual(A.LANGS.filter(l => l.dir === "rtl").map(l => l.code).sort(), ["ar", "he"]);
  assert.strictEqual(new Set(A.LANGS.map(l => l.code)).size, A.LANGS.length, "duplicate language code");
  assert.strictEqual(A.LANGS.length, 32);
  resetApp(); S.lang = S.view = "ar"; A.show(1);
  assert.strictEqual(doc.documentElement.dir, "rtl", "applyDir did not set dir=rtl for ar");
  assert.strictEqual(doc.documentElement.lang, "ar");
  S.lang = S.view = "en"; A.show(1);
  assert.strictEqual(doc.documentElement.dir, "ltr");
});

// e. t / tSafe / machineTranslated
test("e1. t() fallbacks", "", () => {
  resetApp();
  assert.strictEqual(A.t("start"), "Start");
  S.view = "es"; assert.strictEqual(A.t("start"), "Comenzar");
  S.view = "da"; I18N.da = {start: "Start-da"};
  assert.strictEqual(A.t("start"), "Start-da", "machine-translated string used");
  assert.strictEqual(A.t("back"), "Back", "missing key falls back to English");
  assert.strictEqual(A.t("no_such_key"), "no_such_key", "unknown key returns the key");
  assert.strictEqual(A.t("step_of", {n: 2, total: 5}).replace(/\s+/g, " "), "Step 2 of 5");
});
test("e2. tSafe: machine language shows the English gloss under the translation", "", () => {
  resetApp();
  S.view = "da"; I18N.da = {r_decides: "Dansk tekst"};
  assert.strictEqual(A.machineTranslated("r_decides"), true);
  const nodes = A.tSafe("r_decides");
  const text = nodesText(nodes);
  assert.ok(text.includes("Dansk tekst"), "translation missing");
  assert.ok(text.includes(T.r_decides.en), "English r_decides missing");
  const gloss = nodes.find(n => typeof n !== "string" && n.classList.contains("en-gloss"));
  assert.ok(gloss, "no .en-gloss node");
  assert.strictEqual(gloss.getAttribute("lang"), "en");
  assert.strictEqual(gloss.getAttribute("dir"), "ltr");
  assert.strictEqual(gloss.textContent, T.r_decides.en);
});
test("e3. tSafe: inline languages and English get no gloss", "", () => {
  resetApp();
  for (const v of ["es", "en", "ar", "zh-CN"]) {
    S.view = v;
    const nodes = A.tSafe("r_decides");
    assert.ok(!nodes.some(n => typeof n !== "string" && n.classList.contains("en-gloss")), v + ": unexpected English gloss");
    assert.strictEqual(nodesText(nodes), T.r_decides[v], v + ": text");
    assert.strictEqual(A.machineTranslated("r_decides"), false, v + ": machineTranslated");
  }
  S.view = "da"; I18N.da = {r_decides: "x"};
  assert.strictEqual(A.machineTranslated("start"), false, "key absent from I18N.da is not machine translated");
  assert.ok(!A.tSafe("start").some(n => typeof n !== "string" && n.classList.contains("en-gloss")), "non-safety key got a gloss");
});
test("e4. tSafe gloss covers the new safety keys (r_packet, r_no_packet, home_not_eligible, rem_follow, rem_apply, home_bill_deadline, r_deadline_passed; ics_deadline is plain .ics text, not DOM)", "audit-2 SAFETY_KEYS", () => {
  resetApp();
  S.view = "da";
  for (const key of ["r_packet", "r_no_packet", "home_not_eligible", "rem_follow", "rem_apply", "home_bill_deadline", "r_deadline_passed"]) {
    I18N.da = {[key]: "DA-" + key};
    const nodes = A.tSafe(key, {phone: "555", date: "2027-05-29"});
    const text = nodesText(nodes);
    assert.ok(text.includes("DA-" + key), key + ": translation missing");
    assert.ok(nodes.some(n => typeof n !== "string" && n.classList.contains("en-gloss")), key + ": no English gloss (add it to SAFETY_KEYS)");
  }
});
test("e5. machine_note key exists in the five inline languages", "audit-2 machine_note", () => {
  const row = T.machine_note;
  assert.ok(row, "T.machine_note is missing");
  for (const l of ["en", "es", "ar", "zh-CN", "zh-TW"]) assert.ok(typeof row[l] === "string" && row[l].length > 10, "machine_note." + l);
  assert.ok(/machine/i.test(row.en) && /English/.test(row.en), "machine_note.en should say machine translated / English counts");
});
test("e6. every T row has English and consistent {placeholders}", "", () => {
  const vars = s => [...String(s).matchAll(/\{(\w+)\}/g)].map(m => m[1]).sort().join(",");
  for (const [key, row] of Object.entries(T)) {
    assert.strictEqual(typeof row.en, "string", key + ": no English");
    for (const [lang, s] of Object.entries(row)) assert.strictEqual(vars(s), vars(row.en), key + "." + lang + ": placeholders differ from English");
  }
});

// f. submitAnswers: stale replies never land
test("f0. submitAnswers happy path sends the right payload and lands the result", "", async () => {
  resetApp(); setupQuestions();
  const p = A.submitAnswers();
  const ev = take("/evaluate");
  const b = bodyOf(ev);
  assert.strictEqual(b.answers.household_size, 3);
  assert.strictEqual(typeof b.answers.household_size, "number");
  assert.strictEqual(b.answers.annual_income_cents, 3800000);
  assert.strictEqual(b.answers.files_tax_return, true);
  assert.strictEqual(b.answers.language, "en");
  assert.strictEqual(b.answers.for_whom, "self");
  respond(ev, makeResult(115)); await flush();
  const ex = take("/explain");
  assert.ok(!("result" in bodyOf(ex)) && bodyOf(ex).answers.household_size === 3, "/explain must send bill + answers only (the server recomputes the result)");
  respond(ex, makeExplain("A")); answerChecks(); await p;
  assert.strictEqual(S.result.percent_of_fpl, 115);
  assert.strictEqual(A.curScreen, 4);
  assert.strictEqual(S.busy, false);
  const pct = byId("s4").all().find(n => n.className === "pct");
  assert.ok(pct && pct.textContent === "115%", "result screen should show 115%");
  assert.ok(byId("s4").textContent.includes("EXPLAIN-A"));
});
test("f5. Result screen, not eligible: no Deadline panel and no 'Apply by'; eligible still shows it", "audit-3 #1", async () => {
  resetApp(); setupQuestions();
  let p = A.submitAnswers();
  let ev = take("/evaluate");
  respond(ev, makeResult(400, false)); await flush();
  let ex = take("/explain");
  respond(ex, makeExplain("N")); answerChecks(); await p;
  assert.ok(!byId("s4").textContent.includes("Apply by"), "ineligible result shows 'Apply by'");
  assert.ok(!byId("s4").textContent.includes("Deadline"), "ineligible result shows the Deadline panel");
  resetApp(); setupQuestions();
  p = A.submitAnswers();
  ev = take("/evaluate");
  respond(ev, makeResult(115)); await flush();
  ex = take("/explain");
  respond(ex, makeExplain("E")); answerChecks(); await p;
  assert.ok(byId("s4").textContent.includes("Apply by"), "eligible result lost the 'Apply by' line");
});
test("f1. a stale /evaluate reply (older submit) never replaces the newer result", "fix 10", async () => {
  resetApp(); setupQuestions();
  const p1 = A.submitAnswers();
  const e1 = take("/evaluate"); // first submit: reply held back
  A.show(2); A.show(3); // Back, then forward again: cancels submit 1
  const p2 = A.submitAnswers();
  const e2 = take("/evaluate");
  respond(e2, makeResult(60)); await flush();
  respond(take("/explain"), makeExplain("B")); answerChecks(); await p2;
  assert.strictEqual(S.result.percent_of_fpl, 60, "second submit did not land");
  respond(e1, makeResult(115)); await p1; await flush(); // the older reply arrives last
  assert.strictEqual(S.result.percent_of_fpl, 60, "stale /evaluate reply overwrote S.result (115 instead of 60)");
  assert.strictEqual(S.explain.text_en, "EXPLAIN-B");
  assert.strictEqual(A.curScreen, 4);
  const pct = byId("s4").all().find(n => n.className === "pct");
  assert.strictEqual(pct && pct.textContent, "60%", "screen shows the wrong percent");
});
test("f2. a stale /explain reply (older submit) never replaces the newer explanation", "fix 10", async () => {
  resetApp(); setupQuestions();
  const p1 = A.submitAnswers();
  respond(take("/evaluate"), makeResult(115)); await flush();
  const x1 = take("/explain"); // first submit: explain reply held back
  A.show(2); A.show(3);
  const p2 = A.submitAnswers();
  respond(take("/evaluate"), makeResult(60)); await flush();
  respond(take("/explain"), makeExplain("B")); answerChecks(); await p2;
  respond(x1, makeExplain("A")); await p1; await flush();
  assert.strictEqual(S.explain.text_en, "EXPLAIN-B", "stale /explain reply overwrote S.explain");
  assert.strictEqual(S.result.percent_of_fpl, 60, "S.result changed");
  assert.ok(byId("s4").textContent.includes("EXPLAIN-B") && !byId("s4").textContent.includes("EXPLAIN-A"));
});
test("f3. submit cancelled by Back: a late reply does not move the user to the result", "fix 10", async () => {
  resetApp(); setupQuestions();
  const p = A.submitAnswers();
  const e = take("/evaluate");
  A.show(2);
  respond(e, makeResult(115)); await p; await flush();
  assert.strictEqual(A.curScreen, 2, "late reply changed the screen");
  assert.ok(S.result === null, "late reply stored a result after Back");
});
test("f4. errors: busy shows a message and stays on Questions; a stale error is silent", "", async () => {
  resetApp(); setupQuestions();
  const p = A.submitAnswers();
  respond(take("/evaluate"), {detail: "x"}, 429); await p;
  assert.strictEqual(A.curScreen, 3);
  assert.strictEqual(S.busy, false);
  assert.strictEqual(byId("alert").hidden, false, "alert not shown");
  assert.strictEqual(byId("alert").textContent, T.err_busy.en);
  assert.strictEqual(byId("q-go").disabled, false, "See my result should be usable again");
  resetApp(); setupQuestions();
  const p2 = A.submitAnswers();
  const e = take("/evaluate");
  A.show(2);
  respond(e, {detail: "server error text"}, 500); await p2; await flush();
  assert.strictEqual(A.curScreen, 2);
  assert.strictEqual(byId("alert").hidden, true, "a cancelled submit's error leaked onto another screen");
});

// g. language change mid-flow
test("g1. slow language load does not pull the user back from screen 2 to Start", "fix 11", async () => {
  resetApp(); A.show(1);
  const sel = byId("lang-select");
  assert.ok(sel, "no #lang-select on the Start screen");
  sel.value = "th";
  const done = sel.dispatch("change");
  const req = take("i18n/th.json");
  byId("start-btn").click(); // the user taps Start while the language file is loading
  assert.strictEqual(A.curScreen, 2);
  respond(req, {start: "TH-start"}); await done; await flush();
  assert.strictEqual(A.curScreen, 2, "language load re-rendered the Start screen over screen 2");
});
test("g2. language change on Start applies the language and re-renders Start", "", async () => {
  resetApp(); A.show(1);
  const sel = byId("lang-select");
  sel.value = "th";
  const done = sel.dispatch("change");
  respond(take("i18n/th.json"), {start: "TH-start", pick_lang: "TH-pick"}); await done; await flush();
  assert.strictEqual(A.curScreen, 1);
  assert.strictEqual(S.lang, "th"); assert.strictEqual(S.view, "th");
  assert.strictEqual(doc.documentElement.lang, "th");
  assert.strictEqual(byId("start-btn").textContent, "TH-start");
});
test("g3. a failed language load falls back to English with a message", "", async () => {
  resetApp(); A.show(1);
  const sel = byId("lang-select");
  sel.value = "vi";
  const done = sel.dispatch("change");
  respond(take("i18n/vi.json"), {}, 404); await done; await flush();
  assert.strictEqual(S.view, "en");
  assert.strictEqual(byId("alert").hidden, false, "no error shown");
});
test("g4. a newer language pick cancels an older slow one", "", async () => {
  resetApp(); A.show(1);
  const sel = byId("lang-select");
  sel.value = "th";
  const d1 = sel.dispatch("change");
  const req = take("i18n/th.json");
  sel.value = "es"; // inline language: no fetch
  await sel.dispatch("change"); await flush();
  assert.strictEqual(S.lang, "es");
  respond(req, {start: "TH-start"}); await d1; await flush();
  assert.strictEqual(S.lang, "es", "the older pick (th) overwrote the newer one (es)");
  assert.strictEqual(S.view, "es");
});

// h. questions screen gating (kills the income / tax / size mutants)
test("h. questions screen: See my result needs size 1-12, a valid income and a tax answer", "", () => {
  resetApp(); S.bill = fullBill(); A.show(3);
  const go = () => byId("q-go");
  const type = (id, v) => { const n = byId(id); n.value = v; n.listeners.input.forEach(f => f({target: n})); };
  assert.strictEqual(go().disabled, true, "disabled with nothing entered");
  type("q-size", "4"); type("q-income", "38,000.50");
  assert.strictEqual(go().disabled, true, "disabled until a tax answer is chosen");
  byId("tax-yes").click();
  assert.strictEqual(S.tax, true, "Yes must set tax true");
  assert.strictEqual(byId("tax-yes").getAttribute("aria-pressed"), "true");
  assert.strictEqual(byId("tax-no").getAttribute("aria-pressed"), "false");
  assert.strictEqual(byId("q-size").value, "4", "size lost on re-render");
  assert.strictEqual(byId("q-income").value, "38,000.50", "income lost on re-render");
  assert.strictEqual(go().disabled, false, "all three answered: should be enabled");
  byId("tax-no").click();
  assert.strictEqual(S.tax, false, "No must set tax false");
  assert.strictEqual(byId("tax-no").getAttribute("aria-pressed"), "true");
  for (const bad of ["13", "0", "", "-2", "abc"]) { type("q-size", bad); assert.strictEqual(go().disabled, true, "size " + JSON.stringify(bad) + " should disable"); }
  type("q-size", "12"); assert.strictEqual(go().disabled, false); assert.strictEqual(byId("q-plus").disabled, true, "plus at 12");
  type("q-size", "1"); assert.strictEqual(byId("q-minus").disabled, true, "minus at 1");
  byId("q-plus").click(); assert.strictEqual(byId("q-size").value, "2", "plus from 1");
  byId("q-minus").click(); assert.strictEqual(byId("q-size").value, "1", "minus from 2");
  type("q-income", "abc");
  assert.strictEqual(go().disabled, true, "invalid income should disable");
  assert.strictEqual(byId("q-income-hint").hidden, false, "income hint should show");
  type("q-income", "");
  assert.strictEqual(go().disabled, true, "empty income should disable");
});

// i. Home screen: ineligible family is not told to apply
function makeHome(eligible) {
  return {eligible, estimate_cents: eligible ? 12345 : 0, one_application_covers_all: eligible,
    bills: [{label_en: "Bill A", source: "yours", statement_date: "2026-10-01", amount_due_cents: 100000, reduction_cents: eligible ? 12345 : 0, deadline: {date: "2099-01-01"}, hospital_matches_policy: true},
            {label_en: "Bill B", source: "demo", statement_date: "2026-10-02", amount_due_cents: 5000, reduction_cents: 0, deadline: {date: "2099-01-01"}, hospital_matches_policy: true}],
    coverage: {text_en: "One application covers all bills.", citation: CITE},
    earliest_deadline: {date: "2099-01-01"},
    contacts: {email: "a@b.com", phone: "(555) 123-4567", payment_plan_phone: "(555) 999-0000", citation: CITE}};
}
test("i1. Home, eligible: shows estimate, one approval, reminders and calendar", "", () => {
  resetApp(); S.answers = {}; S.bill = {}; S.home = makeHome(true); A.show(6);
  const txt = byId("s6").textContent;
  assert.ok(txt.includes("$123.45"), "estimate");
  assert.ok(txt.includes("One approval may cover all 2 bills"), "one approval line");
  assert.ok(txt.includes("Reminders") && txt.includes("Add to my calendar"), "reminders and calendar button");
  assert.ok(txt.includes("$1,000.00") && txt.includes("$50.00"), "bill amounts");
});
test("i2. Home, not eligible: no 'one approval', no reminders, no calendar; payment-plan contact shown", "fix 6", () => {
  resetApp(); S.answers = {}; S.bill = {}; S.home = makeHome(false); A.show(6);
  const txt = byId("s6").textContent;
  assert.ok(txt.includes("Not eligible"), "not-eligible headline");
  assert.ok(!txt.includes("One approval"), "ineligible Home still says one approval may cover all bills");
  assert.ok(!txt.includes("Reminders"), "ineligible Home still shows Reminders");
  assert.ok(!txt.includes("Add to my calendar"), "ineligible Home still offers the calendar file");
  assert.ok(txt.includes("(555) 999-0000"), "payment-plan phone missing on ineligible Home");
  assert.ok(txt.includes("Financial assistance office") && !txt.includes("Payment plan contact"), "ineligible Home contact label must be r_fa_office (audit-4 #12)");
});
test("i3. Home, every bill from another hospital: no 'Up to $0.00', the different-hospital note instead", "audit 2 landing-check", () => {
  resetApp(); S.answers = {}; S.bill = {};
  const h = makeHome(true); h.estimate_cents = 0;
  h.bills.forEach(b => { b.hospital_matches_policy = false; b.reduction_cents = 0; });
  S.home = h; A.show(6);
  const txt = byId("s6").textContent;
  assert.ok(!txt.includes("$0.00"), "Home shows an estimate of $0.00");
  assert.ok(txt.includes("Different hospital"), "different-hospital note missing");
});

function homeBill(label, source, matches) {
  const b = {label_en: label, source, statement_date: "2026-10-01", amount_due_cents: 100000, reduction_cents: 100, deadline: {date: "2099-01-01"}};
  if (matches !== undefined) b.hospital_matches_policy = matches;
  return b;
}
test("i4. Home, the user's own bill is from a no-policy hospital: no one-approval line, no reminders, no calendar button", "audit-4 #3", () => {
  resetApp(); S.answers = {}; S.bill = {};
  const h = makeHome(true);
  h.bills = [homeBill("Bill A", "yours", false), homeBill("Bill B", "demo", true)];
  S.home = h; A.show(6);
  const s6 = byId("s6"), txt = s6.textContent;
  assert.ok(!txt.includes("One approval"), "one-approval line shown for a user bill with no policy");
  assert.ok(!txt.includes("Reminders"), "reminders shown for a user bill with no policy");
  assert.ok(!txt.includes("Add to my calendar") && !s6.all().some(n => n.tag === "button" && n.textContent === T.rem_ics.en), "calendar button shown for a user bill with no policy");
  assert.ok(txt.includes("Different hospital"), "the no-policy bill should still be flagged");
});
test("i7. Home, the user's own bill shows no hospital name: no one-approval line, reminders, calendar; the no-name note, not 'Different hospital'", "landing check B2", () => {
  resetApp(); S.answers = {}; S.bill = {};
  const h = makeHome(true);
  h.bills = [homeBill("Bill A", "yours", null), homeBill("Bill B", "demo", true)];
  S.home = h; A.show(6);
  const txt = byId("s6").textContent;
  assert.ok(!txt.includes("One approval"), "one-approval line shown for a user bill with no hospital name");
  assert.ok(!txt.includes("Reminders") && !txt.includes("Add to my calendar"), "reminders or calendar shown for a user bill with no hospital name");
  assert.ok(txt.includes(T.r_no_hospital.en) && !txt.includes("Different hospital"), "no-name bill should carry the no-name note");
});
test("i8. Home, not eligible and the user's own bill has no policy here: no contact from this policy", "landing check #3", () => {
  resetApp(); S.answers = {}; S.bill = {};
  const h = makeHome(false);
  h.bills = [homeBill("Bill A", "yours", false), homeBill("Bill B", "demo", true)];
  S.home = h; A.show(6);
  const txt = byId("s6").textContent;
  assert.ok(!txt.includes("(555) 999-0000") && !txt.includes("Financial assistance office"), "another policy's contact shown for a no-policy user bill");
});
test("i5. Home, the user's own bill matches: one-approval line, reminders and calendar shown; n = rows that match", "audit-4 #3", () => {
  resetApp(); S.answers = {}; S.bill = {};
  const h = makeHome(true);
  h.bills = [homeBill("Bill A", "yours", true), homeBill("Bill B", "demo", true), homeBill("Bill C", "demo", false)];
  S.home = h; A.show(6);
  const txt = byId("s6").textContent;
  assert.ok(txt.includes("One approval may cover all 2 bills"), "n must be the matching-row count (2 of 3), got: " + txt.slice(0, 400));
  assert.ok(!txt.includes("all 3 bills"), "n counted a non-matching row");
  assert.ok(txt.includes("Reminders") && txt.includes("Add to my calendar"), "reminders and calendar button missing");
});
test("i6. Home, no 'yours' bill in the list: one-approval line, reminders and calendar shown", "audit-4 #3", () => {
  resetApp(); S.answers = {}; S.bill = {};
  const h = makeHome(true);
  h.bills = [homeBill("Bill A", "demo", true), homeBill("Bill B", "demo", false)];
  S.home = h; A.show(6);
  const txt = byId("s6").textContent;
  assert.ok(txt.includes("One approval may cover all 1 bills"), "one-approval line missing or wrong n");
  assert.ok(txt.includes("Reminders") && txt.includes("Add to my calendar"), "reminders and calendar button missing");
});

// j. real-policies UI (plan D5, D8, D10, D11, D12, D13, D15, D16, D17)
const CITE2 = {source: "VUMC FAP", page: 9, effective_date: "2026-07-01", url: "http://u2"};
let lastCheckCount = 0; // how many /check requests the last landResult answered
async function landResult(result, check, checkStatus) { // drive the real submit path and return the Result screen node
  resetApp(); setupQuestions();
  const p = A.submitAnswers();
  respond(take("/evaluate"), result); await flush();
  if (result.hospital_matches_policy !== false) respond(take("/explain"), makeExplain("X")); // no policy: the app must not ask for one
  lastCheckCount = answerChecks(check, checkStatus); // default: a check with no flags
  await p;
  assert.strictEqual(A.curScreen, 4, "did not reach the Result screen");
  return byId("s4");
}
const links = node => node.all().filter(n => n.tag === "a");
const hrefs = node => links(node).map(n => n.getAttribute("href"));
const items = node => node.all().filter(n => n.tag === "li").map(n => n.textContent);
const NO_ROUTE = "Ask the hospital about the catastrophic route.";
function otherRouteResult() {
  const r = makeResult(400, false);
  r.tier.other_route_en = NO_ROUTE;
  return r;
}
test("j1. conditions panel: heading, English items with footnote marks, between the tier note and the deadline", "plan D8", async () => {
  const r = makeResult(115);
  r.conditions = [{text_en: "Income is adjusted gross income.", citation: CITE2}, {text_en: "Clarksville has its own terms.", citation: CITE}];
  const s4 = await landResult(r);
  const txt = s4.textContent;
  assert.ok(txt.includes(T.r_conditions.en), "conditions heading missing");
  const li = s4.all().filter(n => n.tag === "li" && n.textContent.includes("Income is adjusted gross income."))[0];
  assert.ok(li, "condition item missing");
  assert.ok(li.all().some(n => n.classList.contains("fn-mark")), "condition has no footnote mark");
  assert.ok(li.all().some(n => n.getAttribute("lang") === "en" && n.textContent === "Income is adjusted gross income."), "condition text is not English-only");
  assert.ok(items(s4).some(x => x.startsWith("Clarksville has its own terms.")), "second condition missing");
  const iCond = txt.indexOf(T.r_conditions.en), iTier = txt.indexOf(T.r_policy_en.en), iDead = txt.indexOf("Apply by");
  assert.ok(iTier >= 0 && iTier < iCond && iCond < iDead, "order must be tier note, conditions, deadline (" + [iTier, iCond, iDead] + ")");
  assert.ok(s4.all().some(n => n.tag === "ol" && n.classList.contains("notes") && n.textContent.includes("VUMC FAP")), "condition citation not in the footnotes");
});
test("j2. conditions absent, empty or missing: no conditions heading", "plan D8", async () => {
  let s4 = await landResult(makeResult(115));
  assert.ok(!s4.textContent.includes(T.r_conditions.en), "heading shown with no conditions field");
  const r = makeResult(115); r.conditions = [];
  s4 = await landResult(r);
  assert.ok(!s4.textContent.includes(T.r_conditions.en), "heading shown for an empty list");
});
test("j3. no policy for the hospital: only the title, the warning and the help card (no office line)", "plan D5", async () => {
  const r = makeResult(250);
  r.hospital_matches_policy = false;
  r.documents = [{label_en: "DOCLABEL", citation: CITE}];
  r.conditions = [{text_en: "CONDTEXT", citation: CITE}];
  const s4 = await landResult(r);
  const txt = s4.textContent;
  assert.ok(txt.includes(T.r_mismatch_any.en), "r_mismatch_any missing");
  assert.ok(txt.includes(T.help_title.en) && txt.includes(T.help_note.en), "help card missing");
  assert.ok(txt.includes("Dollar For") && txt.includes("Tennessee Justice Center") && txt.includes("dial 211"), "help items missing");
  assert.ok(!txt.includes("financial assistance office"), "hospital-office line must be omitted");
  assert.ok(!txt.includes("(555) 123-4567") && !hrefs(s4).some(h => h.startsWith("tel:555")), "hospital phone shown");
  for (const gone of ["%", "Deadline", "Apply by", "EXPLAIN-X", "DOCLABEL", "CONDTEXT", "a@b.com", "Tier", T.r_tier.en, T.r_docs.en, T.r_contact.en, T.r_about.en])
    assert.ok(!txt.includes(gone), "no-policy screen still shows: " + gone);
  assert.ok(!s4.all().some(n => n.className === "pct"), "percent shown");
  assert.ok(!s4.all().some(n => n.tag === "table"), "tier table shown");
  assert.ok(!s4.all().some(n => n.tag === "button" && n.classList.contains("primary")), "packet button shown");
  assert.ok(s4.all().some(n => n.classList.contains("warn")), "warning is not a warn panel");
});
test("j4. other route: r_other_route plus the hospital's English text, deadline kept, no r_no_packet, still no packet button", "plan D10", async () => {
  const s4 = await landResult(otherRouteResult());
  const txt = s4.textContent;
  assert.ok(txt.includes(T.r_other_route.en), "r_other_route missing");
  assert.ok(txt.includes(NO_ROUTE), "tier.other_route_en missing");
  assert.ok(s4.all().some(n => n.getAttribute("lang") === "en" && n.textContent === NO_ROUTE), "other_route_en is not English-only");
  assert.ok(txt.includes("Apply by"), "deadline panel must stay for the other route");
  assert.ok(!txt.includes(T.r_no_packet.en), "r_no_packet shown with an other route");
  assert.ok(!s4.all().some(n => n.tag === "button" && n.classList.contains("primary")), "packet button shown");
  const plain = await landResult(makeResult(400, false)); // ineligible, no other route: unchanged
  assert.ok(plain.textContent.includes(T.r_no_packet.en) && !plain.textContent.includes("Apply by"), "plain ineligible result changed");
});
test("j5. Home, not eligible with an other route: r_other_route instead of home_not_eligible", "plan D10", () => {
  resetApp(); S.answers = {}; S.bill = {};
  const h = makeHome(false); h.tier = {eligible: false, other_route_en: NO_ROUTE};
  S.home = h; A.show(6);
  let txt = byId("s6").textContent;
  assert.ok(txt.includes(T.r_other_route.en), "Home lacks r_other_route");
  assert.ok(!txt.includes(T.home_not_eligible.en), "Home still shows home_not_eligible");
  resetApp(); S.answers = {}; S.bill = {};
  const h2 = makeHome(false); h2.tier = {eligible: false};
  S.home = h2; A.show(6);
  txt = byId("s6").textContent;
  assert.ok(txt.includes(T.home_not_eligible.en) && !txt.includes(T.r_other_route.en), "no other route: Home must keep home_not_eligible");
});
test("j6. help card on eligible, ineligible and no-policy results; TJC shows its verified number", "plan D15", async () => {
  const noPolicy = makeResult(250); noPolicy.hospital_matches_policy = false;
  for (const [name, r] of [["eligible", makeResult(115)], ["ineligible", makeResult(400, false)], ["other route", otherRouteResult()], ["no policy", noPolicy]]) {
    const s4 = await landResult(r);
    const its = items(s4);
    assert.ok(s4.textContent.includes(T.help_title.en), name + ": no help title");
    assert.ok(its.includes("Dollar For (free help applying, English and Spanish): dollarfor.org"), name + ": Dollar For line: " + JSON.stringify(its));
    assert.ok(hrefs(s4).includes("https://dollarfor.org"), name + ": Dollar For link");
    assert.ok(its.includes("Tennessee Justice Center (TennCare help): (615) 255-0331"), name + ": TJC line must carry the verified number: " + JSON.stringify(its));
    assert.ok(its.includes("211: dial 211 for local help") && hrefs(s4).includes("tel:211"), name + ": 211 line");
    const office = its.filter(x => x.startsWith("The hospital's financial assistance office: "));
    if (name === "no policy") assert.strictEqual(office.length, 0, "office line on a no-policy result");
    else {
      assert.strictEqual(office.length, 1, name + ": office line count");
      assert.ok(office[0].includes("(555) 123-4567") && hrefs(s4).includes("tel:5551234567"), name + ": office phone link");
    }
    const card = s4.all().filter(n => n.tag === "li" && n.textContent.startsWith("Dollar For"))[0];
    assert.strictEqual(card.getAttribute("lang"), "en", name + ": help items are English-only");
  }
});
test("j7. contacts.email null: no email row, phone row kept", "plan D16", async () => {
  const r = makeResult(115); r.contacts.email = null;
  let s4 = await landResult(r);
  assert.ok(!s4.textContent.includes(T.r_email.en), "email label shown");
  assert.ok(!hrefs(s4).some(h => h.startsWith("mailto:")), "mailto link shown");
  assert.ok(s4.textContent.includes("(555) 123-4567"), "phone missing");
  s4 = await landResult(makeResult(115));
  assert.ok(hrefs(s4).includes("mailto:a@b.com") && s4.textContent.includes(T.r_email.en), "email row lost when present");
});
test("j8. a document with a url shows its label followed by a link; unsafe urls are not linked", "plan D11", async () => {
  const r = makeResult(115);
  r.documents = [{label_en: "Application form", url: "https://vumc.example/form.pdf", citation: CITE},
                 {label_en: "Bad form", url: "javascript:alert(1)", citation: CITE}, {label_en: "Plain doc", citation: CITE}];
  const s4 = await landResult(r);
  const li = s4.all().filter(n => n.tag === "li" && n.textContent.startsWith("Application form"))[0];
  assert.ok(li, "document item missing");
  const a = links(li).find(n => n.getAttribute("href") === "https://vumc.example/form.pdf");
  assert.ok(a && a.textContent === "https://vumc.example/form.pdf", "document link missing");
  assert.ok(li.textContent.indexOf("Application form") < li.textContent.indexOf("https://vumc.example/form.pdf"), "link must follow the label");
  assert.ok(!hrefs(s4).some(h => h.startsWith("javascript:")), "javascript: url was linked");
  assert.ok(!hrefs(s4).includes(undefined), "link without href");
});
test("j9. Start chip names the hospital from S.fromQr (string key or null); the QR points at ?hospital=vumc", "plan D13", () => {
  resetApp(); S.fromQr = null; A.show(1);
  assert.ok(!byId("s1").all().some(n => n.classList.contains("chip")), "chip shown with no hospital");
  S.fromQr = "vumc"; A.show(1);
  assert.ok(byId("s1").textContent.includes("Vanderbilt University Medical Center selected"), "chip text: " + byId("s1").textContent);
  S.fromQr = "ascension_saint_thomas"; A.show(1);
  assert.ok(byId("s1").textContent.includes("Ascension Saint Thomas selected"), "AST chip");
  S.fromQr = "cumberland_synthetic"; A.show(1);
  assert.ok(byId("s1").textContent.includes("Cumberland General Hospital (SYNTHETIC) selected"), "Cumberland chip");
  S.fromQr = null;
  assert.ok(/location\.origin \+ "\/\?hospital=vumc"/.test(src), "Start-screen QR must encode origin + /?hospital=vumc");
});
test("j10. SAFETY_KEYS has r_mismatch_any and r_other_route; the new T rows are in the five inline languages", "plan D12", () => {
  assert.ok(A.SAFETY_KEYS.includes("r_mismatch_any") && A.SAFETY_KEYS.includes("r_other_route") && A.SAFETY_KEYS.includes("r_no_hospital"));
  for (const k of ["r_conditions", "r_mismatch_any", "r_other_route", "r_no_hospital", "r_fa_office", "r_payplan", "help_title", "help_note"])
    for (const l of ["en", "es", "ar", "zh-CN", "zh-TW"]) assert.ok(typeof T[k][l] === "string" && T[k][l].length > 5, k + "." + l);
  resetApp();
  S.view = "da";
  for (const key of ["r_mismatch_any", "r_other_route"]) {
    I18N.da = {[key]: "DA-" + key};
    const nodes = A.tSafe(key);
    assert.ok(nodesText(nodes).includes("DA-" + key) && nodes.some(n => typeof n !== "string" && n.classList.contains("en-gloss")), key + ": no English gloss");
  }
});
test("j16. /evaluate says no policy: /explain is never requested, S.explain stays null, the no-policy screen renders", "audit-4 #10", async () => {
  resetApp(); setupQuestions();
  const p = A.submitAnswers();
  const r = makeResult(250); r.hospital_matches_policy = false;
  respond(take("/evaluate"), r); await flush();
  assert.ok(!fetchQueue.some(q => q.url.includes("/explain")), "/explain was requested for a no-policy result (pending: " + fetchQueue.map(q => q.url).join(", ") + ")");
  answerChecks();
  await p;
  assert.strictEqual(S.explain, null, "S.explain should be null");
  assert.strictEqual(A.curScreen, 4);
  assert.strictEqual(S.busy, false);
  assert.ok(byId("s4").textContent.includes(T.r_mismatch_title.en), "no-policy screen not rendered");
});
test("j17. hospital_name_missing: r_no_hospital replaces r_mismatch_any under the same title", "audit-4 #2", async () => {
  const r = makeResult(250); r.hospital_matches_policy = false; r.hospital_name_missing = true;
  let txt = (await landResult(r)).textContent;
  assert.ok(txt.includes(T.r_no_hospital.en), "r_no_hospital missing");
  assert.ok(!txt.includes(T.r_mismatch_any.en), "r_mismatch_any shown with a missing hospital name");
  assert.ok(txt.includes(T.r_mismatch_title.en), "title lost");
  const r2 = makeResult(250); r2.hospital_matches_policy = false; // flag absent: the old text
  txt = (await landResult(r2)).textContent;
  assert.ok(txt.includes(T.r_mismatch_any.en) && !txt.includes(T.r_no_hospital.en), "flag absent: must keep r_mismatch_any");
});
test("j18. Result, not eligible: the contact panel is labelled 'Financial assistance office', not 'Payment plan contact'", "audit-4 #12", async () => {
  const txt = (await landResult(makeResult(400, false))).textContent;
  assert.ok(txt.includes("Financial assistance office"), "r_fa_office label missing");
  assert.ok(!txt.includes("Payment plan contact"), "old r_payplan label still shown");
  assert.ok(txt.includes("(555) 999-0000"), "payment-plan phone changed or missing");
});
test("j11. timeout: a timed-out /evaluate shows the generic error and stays on Questions (20 s)", "plan D17", async () => {
  resetApp(); setupQuestions();
  const p = A.submitAnswers();
  take("/evaluate"); // the request stays pending; only the timer fires
  assert.strictEqual(timers[timers.length - 1].ms, 20000, "/evaluate timeout");
  timers[timers.length - 1].fn();
  await p; await flush();
  assert.strictEqual(A.curScreen, 3, "left the Questions screen");
  assert.strictEqual(S.busy, false);
  assert.ok(S.result === null, "a result was stored");
  assert.strictEqual(byId("alert").hidden, false, "no error shown");
  assert.strictEqual(byId("alert").textContent, T.err_generic.en);
  assert.strictEqual(byId("q-go").disabled, false, "See my result should be usable again");
});
test("j12. timeout: a timed-out /explain (45 s) lands on the same error path", "plan D17", async () => {
  resetApp(); setupQuestions();
  const p = A.submitAnswers();
  respond(take("/evaluate"), makeResult(115)); await flush();
  take("/explain");
  assert.strictEqual(timers[timers.length - 1].ms, 45000, "/explain timeout");
  timers[timers.length - 1].fn();
  await p; await flush();
  assert.strictEqual(A.curScreen, 3);
  assert.ok(S.result === null && S.explain === null, "half a result was stored");
  assert.strictEqual(byId("alert").textContent, T.err_generic.en);
});
test("j13. timeout: a timed-out /packet (45 s) shows the error and a retry button", "plan D17", async () => {
  const s4 = await landResult(makeResult(115));
  const btn = s4.all().find(n => n.tag === "button" && n.classList.contains("primary"));
  assert.ok(btn, "no packet button");
  btn.click();
  assert.strictEqual(A.curScreen, 5);
  const pk = take("/packet");
  assert.ok(!("result" in bodyOf(pk)) && bodyOf(pk).bill && bodyOf(pk).answers, "/packet must send bill + answers only");
  assert.strictEqual(timers[timers.length - 1].ms, 45000, "/packet timeout");
  timers[timers.length - 1].fn();
  await flush();
  assert.strictEqual(byId("alert").textContent, T.err_generic.en);
  assert.ok(byId("packet-retry"), "no retry button");
});
test("j14. timeout: a language file that does not arrive in 20 s falls back to English with the error", "plan D17", async () => {
  resetApp(); A.show(1);
  const sel = byId("lang-select");
  sel.value = "th";
  const done = sel.dispatch("change");
  take("i18n/th.json");
  assert.strictEqual(timers[timers.length - 1].ms, 20000, "i18n timeout");
  timers[timers.length - 1].fn();
  await done; await flush();
  assert.strictEqual(S.view, "en");
  assert.strictEqual(byId("alert").hidden, false, "no error shown");
});
test("j15. timeout: /extract gets 60 s and a timeout lands on the 'could not read' path", "plan D17", async () => {
  resetApp(); A.show(2);
  const file = new File([new Uint8Array(10)], "bill.png", {type: "image/png"});
  const done = byId("bill-file").dispatch("change", {target: {files: [file]}});
  await flush();
  take("/extract");
  assert.strictEqual(timers[timers.length - 1].ms, 60000, "/extract timeout");
  timers[timers.length - 1].fn();
  await done; await flush();
  assert.ok(S.bill && S.bill.fields.hospital_name.value === null, "a blank bill should be shown after the timeout");
  assert.strictEqual(S.extracting, false);
  assert.strictEqual(byId("alert").textContent, T.read_failed.en);
});

// k. Phase 2 "find errors" UI: charge lines on the Bill screen, /check, the result card, the letter (plan D8, A3, A4, A8)
const typeIn = (id, v) => { const n = byId(id); n.value = v; n.dispatch("input"); };
const tick = (id, on) => { const n = byId(id); n.checked = on; n.dispatch("change"); };
const CTL = (n) => ({date: null, description: n, quantity: 1, amount_cents: 138500});
function readLines() {
  return {items: [CTL("CT scan, head, without contrast"), CTL("CT scan, head, without contrast"),
                  {date: null, description: "IV fluids, first hour", quantity: 1, amount_cents: 37500}],
          total_charges_cents: 314500, payments_cents: 0, confirmed: false, read: true};
}
function openBill(lines) { // the Bill screen with all six fields confirmed, and the given charge lines (undefined = none)
  resetApp(); S.bill = fullBill();
  if (lines !== undefined) S.bill.lines = lines;
  A.show(2);
}
const DUP_TEXT = "This charge appears 2 times with the same description and amount: CT scan, head, without contrast ($1,385.00 each). Ask whether it was billed more than once.";
const INS_TEXT = "The bill lists insurance but shows no insurance payment. Ask whether the bill was sent to your insurer.";
const MCD_CITE = {source: "42 CFR 438.106 (eCFR, current to 2026-10-15)", url: "https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-438/subpart-C/section-438.106"};
function flagsCheck(total) {
  return {contract_version: 1, lines_checked: true, total_to_ask_cents: total === undefined ? 138500 : total, flags: [
    {id: "duplicate", text_en: DUP_TEXT, letter_en: "dup", amount_cents: 138500, line_indexes: [0, 1], citation: null},
    {id: "insurance_unpaid", text_en: INS_TEXT, letter_en: "ins", amount_cents: null, line_indexes: [], citation: null},
    {id: "medicaid", text_en: "TennCare text.", letter_en: "mcd", amount_cents: null, line_indexes: [], citation: MCD_CITE}]};
}
test("k1. Bill screen: charge lines render; Continue is blocked until 'These charges match my bill' is ticked", "plan D8", () => {
  openBill(readLines());
  assert.strictEqual(byId("line-0-desc").value, "CT scan, head, without contrast", "row 0 description");
  assert.strictEqual(byId("line-0-amt").value, "1385.00", "row 0 amount in dollars");
  assert.strictEqual(byId("line-2-amt").value, "375.00");
  assert.strictEqual(byId("lines-total").value, "3145.00");
  assert.strictEqual(byId("lines-paid").value, "0.00");
  assert.strictEqual(byId("bill-next").disabled, true, "Continue enabled with unconfirmed lines");
  assert.ok(byId("bill-why").textContent.includes(T.why_lines.en) && byId("bill-why").hidden === false, "no reason shown: " + byId("bill-why").textContent);
  tick("lines-ok", true);
  assert.strictEqual(S.bill.lines.confirmed, true);
  assert.strictEqual(byId("bill-next").disabled, false, "Continue still disabled after confirming the lines");
  assert.strictEqual(byId("bill-why").hidden, true);
  tick("lines-ok", false);
  assert.strictEqual(byId("bill-next").disabled, true, "unticking must block Continue again");
  assert.ok(T.lines_ok.en === "These charges match my bill");
});
test("k2. Bill screen: any edit unticks the confirmation (description, amount, total, payments) and converts dollars to cents", "plan D8", () => {
  openBill(readLines());
  const edits = [["line-0-desc", "CT head", () => assert.strictEqual(S.bill.lines.items[0].description, "CT head")],
                 ["line-1-amt", "1,200.50", () => assert.strictEqual(S.bill.lines.items[1].amount_cents, 120050)],
                 ["lines-total", "$3,000", () => assert.strictEqual(S.bill.lines.total_charges_cents, 300000)],
                 ["lines-paid", "250.5", () => assert.strictEqual(S.bill.lines.payments_cents, 25050)]];
  for (const [id, v, check] of edits) {
    tick("lines-ok", true);
    assert.strictEqual(byId("bill-next").disabled, false, id + ": setup");
    typeIn(id, v);
    check();
    assert.strictEqual(S.bill.lines.confirmed, false, id + ": edit did not untick");
    assert.strictEqual(byId("lines-ok").checked, false, id + ": checkbox still shows ticked");
    assert.strictEqual(byId("bill-next").disabled, true, id + ": Continue stayed enabled after an edit");
  }
  typeIn("lines-paid", "");
  assert.strictEqual(S.bill.lines.payments_cents, null, "empty payments should be null");
  typeIn("line-0-amt", "abc");
  assert.strictEqual(S.bill.lines.items[0].amount_cents, null, "a bad amount must not become a number");
  assert.strictEqual(byId("line-0-amt-hint").hidden, false, "no hint for a bad amount");
  assert.strictEqual(byId("line-0-amt").getAttribute("aria-invalid"), "true");
  typeIn("line-0-amt", "10");
  assert.strictEqual(byId("line-0-amt-hint").hidden, true);
  typeIn("line-0-amt", "99999999999"); // over the server's 10^9 cents cap
  assert.strictEqual(S.bill.lines.items[0].amount_cents, null, "over-cap amount must not be sent");
  assert.strictEqual(byId("line-0-amt-hint").hidden, false);
});
test("k3. Bill screen: remove a line and add a line; both untick and reindex the rows", "plan D8", () => {
  openBill(readLines());
  tick("lines-ok", true);
  byId("line-1-rm").click();
  assert.strictEqual(S.bill.lines.items.length, 2, "remove did not drop the row");
  assert.deepStrictEqual(S.bill.lines.items.map(i => i.description), ["CT scan, head, without contrast", "IV fluids, first hour"]);
  assert.strictEqual(byId("line-2-desc"), null, "rows were not re-rendered");
  assert.strictEqual(byId("line-1-desc").value, "IV fluids, first hour");
  assert.strictEqual(S.bill.lines.confirmed, false, "remove did not untick");
  assert.strictEqual(byId("lines-ok").checked, false);
  assert.strictEqual(byId("bill-next").disabled, true);
  tick("lines-ok", true);
  byId("line-add").click();
  assert.strictEqual(S.bill.lines.items.length, 3, "add did not add a row");
  assert.deepStrictEqual(S.bill.lines.items[2], {date: null, description: "", quantity: null, amount_cents: null});
  assert.ok(byId("line-2-desc") && byId("line-2-amt") && byId("line-2-rm"), "new row not rendered");
  assert.strictEqual(S.bill.lines.confirmed, false, "add did not untick");
  assert.strictEqual(byId("bill-next").disabled, true);
});
test("k4. Bill screen: with no lines only 'Add a line' shows; adding one creates hand-typed lines that must be confirmed; 40 lines is the cap", "plan D8", () => {
  for (const none of [undefined, null]) {
    openBill(none);
    assert.ok(byId("line-add") && byId("line-add").textContent === "Add a line", "Add a line missing");
    for (const gone of ["lines-ok", "lines-total", "lines-paid", "line-0-desc"]) assert.strictEqual(byId(gone), null, gone + " shown with no lines");
    assert.strictEqual(byId("bill-next").disabled, false, "Continue blocked with no lines");
  }
  byId("line-add").click();
  assert.deepStrictEqual(S.bill.lines, {items: [{date: null, description: "", quantity: null, amount_cents: null}],
                                        total_charges_cents: null, payments_cents: null, confirmed: false, read: false});
  assert.ok(byId("lines-ok") && byId("lines-total") && byId("lines-paid") && byId("line-0-desc"), "table not shown after Add a line");
  assert.strictEqual(byId("bill-next").disabled, true, "hand-typed lines must be confirmed before Continue");
  for (let i = 1; i < 40; i++) byId("line-add").click();
  assert.strictEqual(S.bill.lines.items.length, 40);
  assert.strictEqual(byId("line-add").disabled, true, "Add a line stays enabled at 40 lines");
});
test("k5. /check is requested after /evaluate succeeds, with {bill} only and a 20 s timeout; the answer is stored", "plan A4", async () => {
  resetApp(); setupQuestions();
  S.bill.lines = Object.assign(readLines(), {confirmed: true});
  const p = A.submitAnswers();
  assert.ok(!fetchQueue.some(q => q.url.includes("/check")), "/check was requested before /evaluate answered");
  const mark = timers.length;
  respond(take("/evaluate"), makeResult(115)); await flush();
  const ck = take("/check");
  assert.deepStrictEqual(Object.keys(bodyOf(ck)), ["bill"], "/check body must be {bill}");
  assert.deepStrictEqual(bodyOf(ck).bill, JSON.parse(JSON.stringify(S.bill)));
  assert.strictEqual(bodyOf(ck).bill.lines.items.length, 3, "lines missing from the /check body");
  assert.strictEqual(timers[mark].ms, 20000, "/check timeout");
  respond(take("/explain"), makeExplain("C"));
  respond(ck, flagsCheck()); await p;
  assert.strictEqual(S.check.total_to_ask_cents, 138500);
  assert.strictEqual(S.check.flags.length, 3);
  assert.strictEqual(A.curScreen, 4);
});
test("k6. Result: the card sits right after the hero and lists each flag (text, amount via money(), citation), the total line, the safety line", "plan D8, A3", async () => {
  const s4 = await landResult(makeResult(115), flagsCheck());
  const txt = s4.textContent;
  assert.ok(txt.includes(T.chk_title.en), "card title missing");
  const ul = s4.all().find(n => n.tag === "ul" && n.classList.contains("flags"));
  assert.ok(ul, "no flags list");
  const lis = ul.children;
  assert.strictEqual(lis.length, 3, "one line per flag");
  assert.ok(lis[0].textContent.includes(DUP_TEXT) && lis[0].textContent.includes("$1,385.00"), "duplicate flag line: " + lis[0].textContent);
  assert.ok(lis[0].all().some(n => n.getAttribute("lang") === "en" && n.textContent === DUP_TEXT), "flag text is not English-only");
  assert.ok(lis[1].textContent === INS_TEXT && !lis[1].textContent.includes("$"), "a null amount must show no amount: " + lis[1].textContent);
  assert.ok(lis[2].all().some(n => n.classList.contains("fn-mark")), "medicaid flag has no footnote mark");
  assert.ok(s4.all().some(n => n.tag === "ol" && n.classList.contains("notes") && n.textContent.includes("42 CFR 438.106")), "citation not in the footnotes");
  assert.ok(hrefs(s4).includes(MCD_CITE.url), "citation link missing");
  assert.ok(txt.includes("Up to $1,385.00 to ask the hospital about"), "total line missing");
  assert.ok(txt.includes("Found by fixed rules on the charges you confirmed, not by AI. Only the hospital can confirm an error."), "safety line missing");
  const iHero = txt.indexOf("poverty guideline"), iCard = txt.indexOf(T.chk_title.en), iTier = txt.indexOf(T.r_policy_en.en);
  assert.ok(iHero >= 0 && iHero < iCard && iCard < iTier, "card must come right after the hero (" + [iHero, iCard, iTier] + ")");
  const zero = (await landResult(makeResult(115), flagsCheck(0))).textContent;
  assert.ok(zero.includes(T.chk_title.en) && !/Up to \$/.test(zero), "a zero total must not show the total line");
});
test("k7. the word 'savings' is nowhere in app.js, its strings, or a rendered flags card", "plan D5", async () => {
  assert.ok(T.chk_total && T.chk_safety && T.chk_none, "new chk_* strings missing");
  assert.ok(!/savings/i.test(src), "app.js contains 'savings'");
  for (const [k, row] of Object.entries(T)) for (const [l, s] of Object.entries(row)) assert.ok(!/savings/i.test(s), k + "." + l + " says savings");
  const s4 = await landResult(makeResult(115), flagsCheck());
  assert.ok(s4.textContent.includes(T.chk_title.en) && !/savings/i.test(s4.textContent), "rendered card says savings");
});
test("k8. Result: lines_checked true and no flags shows the no-repeats sentence; lines_checked false, or no check, shows nothing", "plan D8", async () => {
  const none = {contract_version: 1, flags: [], total_to_ask_cents: 0, lines_checked: true};
  let s4 = await landResult(makeResult(115), none);
  assert.ok(s4.textContent.includes("Our checks found no repeated charges, and the math adds up. Simple checks can't prove a bill is right."), "no-flags sentence missing");
  assert.ok(!s4.textContent.includes(T.chk_title.en) && !s4.all().some(n => n.getAttribute("id") === "letter-btn"), "card or letter button shown with no flags");
  s4 = await landResult(makeResult(115), Object.assign({}, none, {lines_checked: false}));
  assert.ok(!s4.textContent.includes(T.chk_none.en), "no-flags sentence shown although no lines were checked");
  s4 = await landResult(makeResult(115), {detail: "nope"}, 500); // /check fails
  assert.ok(!s4.textContent.includes(T.chk_none.en) && !s4.textContent.includes(T.chk_title.en));
});
test("k9. Result: the letter button shows whenever there are flags, eligible or not; never without flags", "plan D8", async () => {
  const btn = s4 => s4.all().find(n => n.tag === "button" && n.textContent === "Create a letter asking the hospital to check this bill");
  let s4 = await landResult(makeResult(400, false), flagsCheck());
  assert.ok(btn(s4), "no letter button on a not-eligible result with flags");
  assert.ok(!s4.all().some(n => n.tag === "button" && n.classList.contains("primary")), "ineligible result must still have no packet button");
  s4 = await landResult(makeResult(115), flagsCheck());
  assert.ok(btn(s4), "no letter button on an eligible result with flags");
  assert.ok(s4.all().some(n => n.tag === "button" && n.classList.contains("primary")), "packet button lost");
  s4 = await landResult(makeResult(115), {contract_version: 1, flags: [], total_to_ask_cents: 0, lines_checked: true});
  assert.ok(!btn(s4), "letter button shown without flags");
});
test("k10. No policy for the hospital: /check still runs and the card shows after the warning; /explain is never requested", "plan D7, A4", async () => {
  const r = makeResult(250); r.hospital_matches_policy = false;
  const s4 = await landResult(r, flagsCheck());
  assert.strictEqual(lastCheckCount, 1, "/check was not requested on the no-policy branch");
  const txt = s4.textContent;
  assert.ok(txt.includes(T.chk_title.en) && txt.includes(DUP_TEXT) && txt.includes("$1,385.00"), "card missing on the no-policy screen");
  const iWarn = txt.indexOf(T.r_mismatch_any.en), iCard = txt.indexOf(T.chk_title.en), iHelp = txt.indexOf(T.help_title.en);
  assert.ok(iWarn >= 0 && iWarn < iCard && iCard < iHelp, "order must be warning, card, help (" + [iWarn, iCard, iHelp] + ")");
  assert.ok(s4.all().some(n => n.tag === "button" && n.textContent === T.chk_letter.en), "letter button missing on the no-policy screen");
  assert.ok(s4.all().some(n => n.tag === "ol" && n.classList.contains("notes") && n.textContent.includes("42 CFR 438.106")), "citation list missing on the no-policy screen");
  assert.ok(!s4.all().some(n => n.tag === "button" && n.classList.contains("primary")), "packet button shown");
});
test("k11. Screen 5 in dispute mode posts /dispute (not /packet) with {bill, answers}; the packet button still posts /packet", "plan D8, A4", async () => {
  const s4 = await landResult(makeResult(115), flagsCheck());
  s4.all().find(n => n.tag === "button" && n.textContent === T.chk_letter.en).click();
  assert.strictEqual(S.doc, "dispute");
  assert.strictEqual(A.curScreen, 5);
  assert.ok(!fetchQueue.some(q => q.url.includes("/packet")), "/packet requested in dispute mode");
  const d = take("/dispute");
  assert.deepStrictEqual(Object.keys(bodyOf(d)).sort(), ["answers", "bill"], "/dispute body must be {bill, answers}");
  assert.strictEqual(bodyOf(d).answers.household_size, 3);
  assert.strictEqual(timers[timers.length - 1].ms, 45000, "/dispute timeout");
  assert.ok(byId("s5").textContent.includes(T.d_title.en) && !byId("s5").textContent.includes(T.p_title.en), "screen 5 title should be the letter's");
  respond(d, "<html><body>LETTER</body></html>"); await flush();
  const frame = byId("packet-paper").all().find(n => n.tag === "iframe");
  assert.ok(frame && frame.srcdoc === "<html><body>LETTER</body></html>", "letter page not in the iframe");
  assert.strictEqual(frame.getAttribute("title"), T.d_title.en);
  assert.strictEqual(byId("print-btn").disabled, false, "print button not enabled");
  A.show(4); // Back keeps the card
  assert.ok(byId("s4").textContent.includes(T.chk_title.en), "Back lost the check card");
  byId("s4").all().find(n => n.tag === "button" && n.classList.contains("primary")).click();
  assert.strictEqual(S.doc, "packet");
  assert.ok(!fetchQueue.some(q => q.url.includes("/dispute")), "/dispute requested in packet mode");
  take("/packet");
  assert.ok(byId("s5").textContent.includes(T.p_title.en) && !byId("s5").textContent.includes(T.d_title.en), "packet title lost");
});
test("k12. Screen 5, dispute mode: a failed /dispute shows the error and a retry that posts /dispute again", "plan D8", async () => {
  const s4 = await landResult(makeResult(400, false), flagsCheck());
  s4.all().find(n => n.tag === "button" && n.textContent === T.chk_letter.en).click();
  respond(take("/dispute"), {detail: "x"}, 500); await flush();
  assert.strictEqual(byId("alert").hidden, false, "no error shown");
  assert.ok(byId("packet-retry"), "no retry button");
  byId("packet-retry").click();
  take("/dispute");
});
test("k13. a /check failure (500, network error, 20 s timeout) never blocks the result and shows no error", "plan A4", async () => {
  for (const how of ["500", "reject", "timeout"]) {
    resetApp(); setupQuestions();
    const p = A.submitAnswers();
    const mark = timers.length;
    respond(take("/evaluate"), makeResult(115)); await flush();
    const ck = take("/check");
    if (how === "500") respond(ck, {detail: "boom"}, 500);
    else if (how === "reject") ck.reject(new Error("network down"));
    else timers[mark].fn();
    respond(take("/explain"), makeExplain("F")); await p; await flush();
    assert.strictEqual(A.curScreen, 4, how + ": result did not land");
    assert.strictEqual(S.check, null, how + ": S.check should be null");
    assert.strictEqual(byId("alert").hidden, true, how + ": an error was shown for a /check failure");
    assert.ok(byId("s4").textContent.includes("EXPLAIN-F") && !byId("s4").textContent.includes(T.chk_title.en), how + ": result content wrong");
  }
  resetApp(); setupQuestions(); // the no-policy branch too
  const p2 = A.submitAnswers();
  const r = makeResult(250); r.hospital_matches_policy = false;
  respond(take("/evaluate"), r); await flush();
  respond(take("/check"), {detail: "boom"}, 500); await p2;
  assert.strictEqual(A.curScreen, 4); assert.strictEqual(S.check, null);
  assert.ok(byId("s4").textContent.includes(T.r_mismatch_title.en) && byId("alert").hidden === true);
});
test("k14. /extract returning insurance_status 'medicaid' shows the TennCare / Medicaid option, selected, and keeps it on re-render", "plan A8", async () => {
  resetApp(); A.show(2);
  const file = new File([new Uint8Array(10)], "bill.png", {type: "image/png"});
  const done = byId("bill-file").dispatch("change", {target: {files: [file]}});
  await flush();
  const bill = fullBill();
  for (const f of Object.values(bill.fields)) f.confirmed = false;
  bill.fields.insurance_status = {value: "medicaid", confidence: 0.9, confirmed: false};
  respond(take("/extract"), bill); await done; await flush();
  const sel = byId("f-insurance_status");
  assert.deepStrictEqual(sel.children.map(o => o.getAttribute("value")), ["", "self_pay", "insured", "medicaid", "unknown"]);
  assert.strictEqual(sel.children.find(o => o.getAttribute("value") === "medicaid").textContent, "TennCare / Medicaid");
  assert.strictEqual(sel.value, "medicaid", "the read value is not the selected option");
  assert.strictEqual(S.bill.fields.insurance_status.value, "medicaid");
  A.show(2);
  assert.strictEqual(byId("f-insurance_status").value, "medicaid", "option lost on re-render");
  assert.strictEqual(S.bill.fields.insurance_status.value, "medicaid");
});
test("k15. new strings: ins_medicaid and the chk_/lines_ rows exist in all five inline languages; chk_safety is a SAFETY key with an English gloss; en text is exact", "plan D9, A3", () => {
  const keys = ["ins_medicaid", "lines_title", "lines_hint", "line_desc", "line_amt", "line_remove", "line_add", "lines_total", "lines_paid",
                "lines_ok", "why_lines", "chk_title", "chk_total", "chk_none", "chk_safety", "chk_letter", "load_dispute", "d_title"];
  for (const k of keys) for (const l of ["en", "es", "ar", "zh-CN", "zh-TW"]) assert.ok(T[k] && typeof T[k][l] === "string" && T[k][l].length >= 2, k + "." + l);
  assert.strictEqual(T.ins_medicaid.en, "TennCare / Medicaid");
  assert.strictEqual(T.chk_safety.en, "Found by fixed rules on the charges you confirmed, not by AI. Only the hospital can confirm an error.");
  assert.strictEqual(T.chk_total.en, "Up to {amount} to ask the hospital about");
  assert.ok(A.SAFETY_KEYS.includes("chk_safety"), "chk_safety is not a SAFETY key");
  resetApp(); S.view = "da"; I18N.da = {chk_safety: "DA-safety"};
  const nodes = A.tSafe("chk_safety");
  assert.ok(nodesText(nodes).includes("DA-safety") && nodes.some(n => typeof n !== "string" && n.classList.contains("en-gloss")), "no English gloss in a machine language");
});

// m. Insurance-summary (EOB) step: screen 7 between Bill and Questions when the bill says "insured"
const EOB_NAMES = ["insurer_name", "provider_name", "date_of_service", "claim_number", "claim_status", "amount_billed_cents",
                   "plan_discount_cents", "plan_paid_cents", "patient_owes_cents", "denial_reason", "appeal_deadline", "insurer_phone"];
function eobRead(withLines) { // what POST /extract returns for an insurance summary
  const v = {insurer_name: "Acme Health", provider_name: "VUMC", date_of_service: "2026-03-04", claim_number: "C123", claim_status: "partially_paid",
             amount_billed_cents: 500000, plan_discount_cents: 200000, plan_paid_cents: 150000, patient_owes_cents: 12345, denial_reason: null,
             appeal_deadline: "2026-09-01", insurer_phone: "800-555-0100"};
  const fields = {};
  for (const n of EOB_NAMES) fields[n] = {value: v[n], confidence: 0.9, confirmed: false};
  return {contract_version: 1, fields, lines: withLines === false ? null : {read: true, confirmed: false, items: [
    {date: "2026-03-04", description: "Office visit", amount_billed_cents: 30000, patient_owes_cents: 2500},
    {date: "2026-03-04", description: "Lab panel", amount_billed_cents: 20000, patient_owes_cents: 9845}]}};
}
function openEobAsk(ins, dos) { // the Bill screen with the given insurance and service date, then Continue
  resetApp(); S.bill = fullBill();
  S.bill.fields.insurance_status.value = ins;
  S.bill.fields.date_of_service.value = dos === undefined ? "2026-03-04" : dos;
  A.show(2);
  byId("bill-next").click();
}
async function uploadEob(reply, status) { // pick a photo on the ask state and answer /extract; returns the request
  const file = new File([new Uint8Array(10)], "eob.png", {type: "image/png"});
  const done = byId("eob-file").dispatch("change", {target: {files: [file]}});
  await flush();
  const req = take("/extract");
  if (reply === undefined) return req; // left pending
  respond(req, reply, status);
  await done; await flush();
  return req;
}
async function openEobConfirm(withLines) { openEobAsk("insured"); await uploadEob(eobRead(withLines)); }
function tickAllEob() { for (const n of EOB_NAMES) tick("e-" + n + "-ok", true); }
function setAnswers() { S.size = "3"; S.income = "38,000"; S.tax = true; }

test("m1. Continue on the Bill screen shows the insurance-summary screen for 'insured' only; self_pay and medicaid go straight to the questions", "eob", () => {
  openEobAsk("insured");
  assert.strictEqual(A.curScreen, 7, "insured did not go to screen 7");
  const txt = byId("s7").textContent;
  assert.ok(txt.includes("Your insurance summary") && txt.includes("Do you have your insurer's summary for this visit? It usually says 'This is not a bill.'"), txt);
  assert.ok(txt.includes("Add a photo") && txt.includes("Not yet"), "ask buttons missing");
  assert.ok(byId("eob-file") && byId("eob-file").getAttribute("accept") === "image/png,image/jpeg", "file input missing");
  byId("eob-back").click();
  assert.strictEqual(A.curScreen, 2, "Back did not return to the Bill screen");
  for (const ins of ["self_pay", "medicaid", "unknown"]) {
    openEobAsk(ins);
    assert.strictEqual(A.curScreen, 3, ins + " must skip the insurance-summary step");
  }
});
test("m2. 'Not yet' goes to the questions; /check carries eob_not_yet true and no eob; /dispute too", "eob", async () => {
  openEobAsk("insured");
  byId("eob-notyet").click();
  assert.strictEqual(A.curScreen, 3);
  assert.strictEqual(S.eobNotYet, true); assert.strictEqual(S.eob, null);
  setAnswers();
  const p = A.submitAnswers();
  respond(take("/evaluate"), makeResult(115)); await flush();
  const ck = take("/check");
  assert.strictEqual(bodyOf(ck).eob_not_yet, true, "eob_not_yet missing from /check");
  assert.ok(!("eob" in bodyOf(ck)), "eob must not be sent after Not yet");
  respond(take("/explain"), makeExplain("N")); respond(ck, flagsCheck()); await p;
  byId("s4").all().find(n => n.tag === "button" && n.textContent === T.chk_letter.en).click();
  const d = bodyOf(take("/dispute"));
  assert.strictEqual(d.eob_not_yet, true); assert.ok(!("eob" in d));
});
test("m3. Upload posts /extract with kind=eob, the bill's date_of_service and a 60 s timeout; no date means the key is omitted", "eob", async () => {
  openEobAsk("insured", "2026-03-04");
  const mark = timers.length;
  const file = new File([new Uint8Array(10)], "eob.png", {type: "image/png"});
  const done = byId("eob-file").dispatch("change", {target: {files: [file]}});
  await flush();
  assert.strictEqual(S.eobExtracting, true);
  assert.ok(byId("status").textContent.includes("Reading the insurance summary"), "no reading status");
  assert.strictEqual(byId("eob-file").disabled, true, "file input stays enabled while reading");
  const req = take("/extract");
  assert.strictEqual(timers[mark].ms, 60000, "timeout");
  const fd = req.opts.body;
  assert.strictEqual(fd.get("kind"), "eob"); assert.strictEqual(fd.get("date_of_service"), "2026-03-04");
  assert.ok(fd.get("file"), "no file part");
  respond(req, eobRead()); await done; await flush();
  assert.ok(byId("e-insurer_name"), "confirm state not shown after the read");
  openEobAsk("insured", null);
  const r2 = await uploadEob(undefined);
  assert.strictEqual(r2.opts.body.get("kind"), "eob"); assert.strictEqual(r2.opts.body.has("date_of_service"), false, "blank date must be omitted");
});
test("m4. A 422 shows the not-an-insurance-summary message and the ask state again; other failures show the read-failed message", "eob", async () => {
  openEobAsk("insured");
  await uploadEob({detail: "This doesn't look like an insurance summary."}, 422);
  assert.strictEqual(A.curScreen, 7);
  assert.ok(byId("alert").textContent === "This doesn't look like an insurance summary. Try another photo, or tap Not yet.", byId("alert").textContent);
  assert.strictEqual(S.eobDraft, null);
  assert.ok(byId("eob-file") && byId("eob-file").disabled === false && byId("eob-notyet").disabled === false, "ask state not restored");
  await uploadEob("<html>gateway</html>", 502);
  assert.strictEqual(byId("alert").textContent, T.eob_read_failed.en);
  assert.ok(byId("eob-file") && S.eobExtracting === false);
  await uploadEob({contract_version: 1}, 200); // 200 with no fields is a failed read
  assert.strictEqual(byId("alert").textContent, T.eob_read_failed.en);
  assert.strictEqual(S.eobDraft, null);
});
test("m5. Confirm state: Continue stays disabled until every field and the lines are confirmed; any edit unticks", "eob", async () => {
  await openEobConfirm();
  assert.strictEqual(byId("e-patient_owes_cents").value, "123.45", "money not shown in dollars");
  assert.strictEqual(byId("e-insurer_name").value, "Acme Health");
  assert.strictEqual(byId("e-claim_status").value, "partially_paid");
  assert.deepStrictEqual(byId("e-claim_status").children.map(o => o.getAttribute("value")), ["", "paid", "partially_paid", "denied", "pending"]);
  assert.strictEqual(byId("e-appeal_deadline").getAttribute("type"), "date");
  assert.strictEqual(byId("eline-0-desc").value, "Office visit");
  assert.strictEqual(byId("eline-1-owes").value, "98.45");
  assert.strictEqual(byId("eob-next").disabled, true);
  for (const n of EOB_NAMES.slice(0, 11)) tick("e-" + n + "-ok", true);
  assert.strictEqual(byId("eob-next").disabled, true, "enabled with one field open");
  tick("e-" + EOB_NAMES[11] + "-ok", true);
  assert.strictEqual(byId("eob-next").disabled, true, "enabled with the lines unconfirmed");
  assert.ok(byId("eob-why").textContent.includes(T.why_lines.en), "no reason: " + byId("eob-why").textContent);
  tick("eob-lines-ok", true);
  assert.strictEqual(byId("eob-next").disabled, false, "still disabled with everything confirmed");
  assert.ok(S.eob && S.eob.fields.insurer_name.confirmed === true && S.eob.lines.confirmed === true, "S.eob not set when confirmed");
  const edits = [["e-insurer_name", "Acme", "input"], ["e-patient_owes_cents", "99.50", "input"], ["e-claim_status", "denied", "change"], ["e-appeal_deadline", "2026-10-01", "input"]];
  for (const [id, v, ev] of edits) {
    byId(id).value = v; byId(id).dispatch(ev);
    assert.strictEqual(byId(id + "-ok").checked, false, id + ": field still ticked after an edit");
    assert.strictEqual(byId("eob-next").disabled, true, id + ": Continue stayed enabled");
    assert.strictEqual(S.eob, null, id + ": S.eob stays set while a field is unconfirmed");
    tick(id + "-ok", true);
    assert.strictEqual(byId("eob-next").disabled, false, id + ": re-ticking should re-enable");
  }
  assert.strictEqual(S.eobDraft.fields.patient_owes_cents.value, 9950);
  assert.strictEqual(S.eobDraft.fields.claim_status.value, "denied");
  for (const [id, v, check] of [["eline-0-desc", "Visit", () => assert.strictEqual(S.eobDraft.lines.items[0].description, "Visit")],
                                ["eline-0-date", "2026-03-05", () => assert.strictEqual(S.eobDraft.lines.items[0].date, "2026-03-05")],
                                ["eline-1-billed", "250", () => assert.strictEqual(S.eobDraft.lines.items[1].amount_billed_cents, 25000)],
                                ["eline-1-owes", "$1.5", () => assert.strictEqual(S.eobDraft.lines.items[1].patient_owes_cents, 150)]]) {
    tick("eob-lines-ok", true);
    assert.strictEqual(byId("eob-next").disabled, false, id + ": setup");
    typeIn(id, v);
    check();
    assert.strictEqual(S.eobDraft.lines.confirmed, false, id + ": edit did not untick");
    assert.strictEqual(byId("eob-lines-ok").checked, false, id + ": checkbox still ticked");
    assert.strictEqual(byId("eob-next").disabled, true, id + ": Continue stayed enabled after a line edit");
  }
  tick("eob-lines-ok", true);
  byId("eline-0-rm").click();
  assert.strictEqual(S.eobDraft.lines.items.length, 1); assert.strictEqual(byId("eline-1-desc"), null, "rows not re-rendered");
  assert.strictEqual(byId("eob-next").disabled, true, "removing a row must untick");
  tick("eob-lines-ok", true);
  byId("eob-next").click();
  assert.strictEqual(A.curScreen, 3);
  assert.strictEqual(S.eobNotYet, false);
});
test("m6. A summary read with no lines needs no lines checkbox; 'Use a different photo' returns to the ask state", "eob", async () => {
  await openEobConfirm(false);
  assert.strictEqual(byId("eob-lines-ok"), null, "lines checkbox shown with no lines");
  tickAllEob();
  assert.strictEqual(byId("eob-next").disabled, false, "blocked with no lines to confirm");
  byId("eob-retake").click();
  assert.strictEqual(S.eobDraft, null); assert.strictEqual(S.eob, null);
  assert.ok(byId("eob-file"), "ask state not shown");
});
test("m7. /check and /dispute carry the confirmed eob (and no eob_not_yet); /packet is unchanged", "eob", async () => {
  await openEobConfirm();
  tickAllEob(); tick("eob-lines-ok", true);
  byId("eob-next").click();
  setAnswers();
  const p = A.submitAnswers();
  respond(take("/evaluate"), makeResult(115)); await flush();
  const ck = take("/check");
  const b = bodyOf(ck);
  assert.deepStrictEqual(Object.keys(b).sort(), ["bill", "eob"], "/check body keys");
  assert.deepStrictEqual(b.eob, JSON.parse(JSON.stringify(S.eob)));
  assert.strictEqual(b.eob.fields.patient_owes_cents.value, 12345);
  assert.strictEqual(b.eob.fields.insurer_name.confirmed, true);
  assert.strictEqual(b.eob.lines.confirmed, true); assert.strictEqual(b.eob.lines.items.length, 2);
  respond(take("/explain"), makeExplain("E")); respond(ck, flagsCheck()); await p;
  byId("s4").all().find(n => n.tag === "button" && n.textContent === T.chk_letter.en).click();
  const d = bodyOf(take("/dispute"));
  assert.deepStrictEqual(Object.keys(d).sort(), ["answers", "bill", "eob"], "/dispute body keys");
  assert.strictEqual(d.eob.fields.claim_status.value, "partially_paid");
  A.show(4);
  byId("s4").all().find(n => n.tag === "button" && n.classList.contains("primary")).click();
  assert.deepStrictEqual(Object.keys(bodyOf(take("/packet"))).sort(), ["answers", "bill"], "/packet body must not gain eob");
});
test("m8. restart, a new bill photo, and switching insurance away from 'insured' clear the summary; a reply after a restart is dropped", "eob", async () => {
  await openEobConfirm(); tickAllEob(); tick("eob-lines-ok", true);
  assert.ok(S.eob, "setup");
  A.restart();
  assert.strictEqual(S.eob, null); assert.strictEqual(S.eobDraft, null); assert.strictEqual(S.eobNotYet, false);
  openEobAsk("insured");
  const file = new File([new Uint8Array(10)], "eob.png", {type: "image/png"});
  const done = byId("eob-file").dispatch("change", {target: {files: [file]}});
  await flush();
  const req = take("/extract");
  A.restart();
  respond(req, eobRead()); await done; await flush();
  assert.strictEqual(S.eobDraft, null, "a stale reply landed after restart"); assert.strictEqual(S.eobExtracting, false);
  await openEobConfirm(); tickAllEob(); tick("eob-lines-ok", true);
  A.show(2);
  const sel = byId("f-insurance_status");
  sel.value = "self_pay"; sel.dispatch("change");
  assert.strictEqual(S.eob, null, "switching to self_pay kept S.eob"); assert.strictEqual(S.eobDraft, null);
  openEobAsk("insured"); byId("eob-notyet").click(); A.show(2);
  assert.strictEqual(S.eobNotYet, true);
  const f2 = new File([new Uint8Array(10)], "bill.png", {type: "image/png"});
  const d2 = byId("bill-file").dispatch("change", {target: {files: [f2]}});
  await flush();
  assert.strictEqual(S.eobNotYet, false, "a new bill photo kept eobNotYet");
  respond(take("/extract"), fullBill()); await d2;
});
test("m9. new strings: every eob_ key and eob_f_<field> exists in all five inline languages; en text is exact", "eob", () => {
  const keys = ["eob_title", "eob_ask", "eob_add", "eob_not_yet", "eob_reading", "eob_not_eob", "eob_hint", "eob_blank", "eob_retake", "eob_lines_title",
                "eob_l_date", "eob_billed", "eob_owes", "eob_lines_ok", "eob_st_paid", "eob_st_partially_paid", "eob_st_denied", "eob_st_pending"]
    .concat(EOB_NAMES.map(n => "eob_f_" + n));
  for (const k of keys) for (const l of ["en", "es", "ar", "zh-CN", "zh-TW"]) assert.ok(T[k] && typeof T[k][l] === "string" && T[k][l].length >= 2, k + "." + l);
  assert.strictEqual(T.eob_lines_ok.en, "These match my insurance summary.");
  assert.strictEqual(T.eob_not_eob.en, "This doesn't look like an insurance summary. Try another photo, or tap Not yet.");
});

test("n1. Sources: the citation list sits in a closed dropdown; a footnote mark opens it", "Evan 2026-10-18", async () => {
  const s4 = await landResult(makeResult(115));
  const box = s4.all().find(n => n.tag === "details" && n.classList.contains("notes-box"));
  assert.ok(box, "no Sources dropdown");
  assert.ok(!box.open && box.getAttribute("open") === null, "Sources must start closed");
  const sum = box.children.find(n => n.tag === "summary");
  assert.ok(sum && sum.textContent.startsWith(T.srcs.en + " ("), "summary text: " + (sum && sum.textContent));
  assert.ok(box.all().some(n => n.tag === "ol" && n.classList.contains("notes")), "the list must be inside the dropdown");
  const mark = s4.all().find(n => n.tag === "a" && n.parent && n.parent.classList.contains("fn-mark"));
  assert.ok(mark, "no footnote mark");
  mark.click();
  assert.strictEqual(box.open, true, "a footnote mark must open the dropdown");
});
test("n2. Remove photo: drops the photo and every field read from it; a read still in flight is ignored", "Evan 2026-10-18", async () => {
  resetApp(); A.show(2);
  const file = new File([new Uint8Array(10)], "bill.png", {type: "image/png"});
  const done = byId("bill-file").dispatch("change", {target: {files: [file]}});
  await flush();
  const req = take("/extract");
  const btn = byId("s2").all().find(n => n.tag === "button" && n.textContent === T.photo_remove.en);
  assert.ok(btn, "no Remove photo button while a photo is shown");
  btn.click();
  assert.strictEqual(S.imageUrl, null, "photo not removed");
  assert.strictEqual(S.bill, null, "fields from the photo must be dropped");
  assert.strictEqual(S.extracting, false, "still marked as reading");
  assert.ok(!byId("s2").all().some(n => n.tag === "button" && n.textContent === T.photo_remove.en), "button still shown with no photo");
  respond(req, {contract_version: 1, fields: {}}); await done; await flush();
  assert.strictEqual(S.bill, null, "a stale read brought the removed photo's fields back");
});

test("n3. a card whose only flag has no letter line (different visit) shows no letter button", "O1 review #1", async () => {
  const only = {contract_version: 1, flags: [{id: "different_visit", kind: "insurance", text_en: "This insurance summary is for a different visit.", letter_en: null, amount_cents: null, line_indexes: [], citation: null}], total_to_ask_cents: 0, lines_checked: false};
  const s4 = await landResult(makeResult(115), only);
  assert.ok(s4.textContent.includes("different visit"), "flag not shown");
  assert.ok(!s4.all().some(n => n.tag === "button" && n.textContent === T.chk_letter.en), "letter button shown with no letter line");
});

// ---------- run
let finished = false; // a test whose promise never settles empties the event loop: Node would exit 0 with no ALL PASS
process.on("exit", code => { if (!finished && code === 0) { console.log("FAIL: the run stopped before every test finished"); process.exitCode = 1; } });
(async () => {
  let failed = 0;
  for (const tc of tests) {
    try {
      await tc.fn();
      console.log("ok   " + tc.name);
    } catch (e) {
      failed++;
      console.log("FAIL " + tc.name + (tc.fix ? "  [checks " + tc.fix + "]" : "") + "\n     " + String(e && e.message || e).split("\n").join("\n     "));
    }
  }
  if (failed) { console.log(failed + " of " + tests.length + " tests FAILED"); process.exit(1); }
  finished = true;
  console.log("ALL PASS");
  process.exit(0);
})();
