"use strict";
// Bill to Help UI. All state lives in this object in memory only: no localStorage, no cookies, no disk.

// UI strings. Every es and ar string is a draft for a human translator.
// TODO-REVIEW: all es/ar strings below (one marker per line).
const T = {
  app_title:   {en: "Bill to Help", es: "Factura a Ayuda", ar: "من الفاتورة إلى المساعدة"}, // TODO-REVIEW es+ar
  notice:      {en: "Nothing you enter is saved. Demo uses synthetic bills only.", es: "Nada de lo que escribe se guarda. La demostración usa solo facturas sintéticas.", ar: "لا يتم حفظ أي شيء تدخله. العرض التجريبي يستخدم فواتير اصطناعية فقط."}, // TODO-REVIEW es+ar
  no_id:       {en: "We do not ask for your name, immigration status, Social Security number, or ID.", es: "No pedimos su nombre, su estatus migratorio, su número de Seguro Social ni su identificación.", ar: "لا نطلب اسمك أو وضعك في الهجرة أو رقم الضمان الاجتماعي أو أي هوية."}, // TODO-REVIEW es+ar
  pick_lang:   {en: "Choose a language", es: "Elija un idioma", ar: "اختر اللغة"}, // TODO-REVIEW es+ar
  for_whom:    {en: "This bill is for:", es: "Esta factura es para:", ar: "هذه الفاتورة لـ:"}, // TODO-REVIEW es+ar
  me:          {en: "Me", es: "Yo", ar: "أنا"}, // TODO-REVIEW es+ar
  family:      {en: "A family member", es: "Un familiar", ar: "أحد أفراد عائلتي"}, // TODO-REVIEW es+ar
  start:       {en: "Start", es: "Comenzar", ar: "ابدأ"}, // TODO-REVIEW es+ar
  bill_title:  {en: "Your bill", es: "Su factura", ar: "فاتورتك"}, // TODO-REVIEW es+ar
  upload:      {en: "Upload or take a photo of the bill", es: "Suba o tome una foto de la factura", ar: "ارفع صورة الفاتورة أو التقطها"}, // TODO-REVIEW es+ar
  reading:     {en: "Reading the bill...", es: "Leyendo la factura...", ar: "جارٍ قراءة الفاتورة..."}, // TODO-REVIEW es+ar
  read_failed: {en: "Photo reading is not available right now. Type the fields in by hand.", es: "La lectura de fotos no está disponible ahora. Escriba los campos a mano.", ar: "قراءة الصورة غير متاحة الآن. اكتب الحقول يدويًا."}, // TODO-REVIEW es+ar
  bill_hint:   {en: "Check each field against your bill, fix mistakes, then confirm each one. A blank field means we could not read it: type it in.", es: "Compare cada campo con su factura, corrija los errores y confirme cada uno. Un campo en blanco significa que no pudimos leerlo: escríbalo.", ar: "قارن كل حقل بفاتورتك وصحح الأخطاء ثم أكّد كل حقل. الحقل الفارغ يعني أننا لم نستطع قراءته: اكتبه."}, // TODO-REVIEW es+ar
  f_hospital:  {en: "Hospital", es: "Hospital", ar: "المستشفى"}, // TODO-REVIEW es+ar
  f_statement: {en: "Statement date", es: "Fecha del estado de cuenta", ar: "تاريخ الكشف"}, // TODO-REVIEW es+ar
  f_account:   {en: "Account number", es: "Número de cuenta", ar: "رقم الحساب"}, // TODO-REVIEW es+ar
  f_amount:    {en: "Amount due (US dollars)", es: "Monto adeudado (dólares)", ar: "المبلغ المستحق (بالدولار)"}, // TODO-REVIEW es+ar
  f_service:   {en: "Date of service", es: "Fecha del servicio", ar: "تاريخ الخدمة"}, // TODO-REVIEW es+ar
  f_insurance: {en: "Insurance", es: "Seguro médico", ar: "التأمين"}, // TODO-REVIEW es+ar
  ins_blank:   {en: "(not set)", es: "(sin definir)", ar: "(غير محدد)"}, // TODO-REVIEW es+ar
  ins_self_pay:{en: "Self-pay (no insurance)", es: "Pago propio (sin seguro)", ar: "دفع شخصي (بدون تأمين)"}, // TODO-REVIEW es+ar
  ins_insured: {en: "Insured", es: "Con seguro", ar: "مؤمَّن"}, // TODO-REVIEW es+ar
  ins_unknown: {en: "Unknown", es: "Desconocido", ar: "غير معروف"}, // TODO-REVIEW es+ar
  unreadable:  {en: "Could not read this. Please type it.", es: "No se pudo leer. Escríbalo, por favor.", ar: "تعذّرت قراءة هذا الحقل. الرجاء كتابته."}, // TODO-REVIEW es+ar
  required:    {en: "Required", es: "Obligatorio", ar: "مطلوب"}, // TODO-REVIEW es+ar
  confirm:     {en: "This is correct", es: "Esto es correcto", ar: "هذا صحيح"}, // TODO-REVIEW es+ar
  continue_:   {en: "Continue", es: "Continuar", ar: "متابعة"}, // TODO-REVIEW es+ar
  back:        {en: "Back", es: "Atrás", ar: "رجوع"}, // TODO-REVIEW es+ar
  q_title:     {en: "Three questions", es: "Tres preguntas", ar: "ثلاثة أسئلة"}, // TODO-REVIEW es+ar
  q_size:      {en: "How many people live in your household (1 to 12)?", es: "¿Cuántas personas viven en su hogar (de 1 a 12)?", ar: "كم عدد الأشخاص في أسرتك (من 1 إلى 12)؟"}, // TODO-REVIEW es+ar
  q_income:    {en: "Total yearly household income before taxes, in US dollars", es: "Ingreso anual total del hogar antes de impuestos, en dólares", ar: "إجمالي دخل الأسرة السنوي قبل الضرائب بالدولار"}, // TODO-REVIEW es+ar
  q_tax:       {en: "Do you file a tax return?", es: "¿Presenta una declaración de impuestos?", ar: "هل تقدّم إقرارًا ضريبيًا؟"}, // TODO-REVIEW es+ar
  yes:         {en: "Yes", es: "Sí", ar: "نعم"}, // TODO-REVIEW es+ar
  no:          {en: "No", es: "No", ar: "لا"}, // TODO-REVIEW es+ar
  see_result:  {en: "See my result", es: "Ver mi resultado", ar: "اعرض نتيجتي"}, // TODO-REVIEW es+ar
  working:     {en: "Working...", es: "Procesando...", ar: "جارٍ المعالجة..."}, // TODO-REVIEW es+ar
  r_title:     {en: "Your result", es: "Su resultado", ar: "نتيجتك"}, // TODO-REVIEW es+ar
  r_percent:   {en: "Your income is about {pct}% of the {year} federal poverty guideline", es: "Su ingreso es aproximadamente el {pct}% de la guía federal de pobreza de {year}", ar: "دخلك يعادل تقريبًا {pct}% من الحد الفيدرالي للفقر لعام {year}"}, // TODO-REVIEW es+ar
  r_tier:      {en: "Under this hospital's policy", es: "Según la política de este hospital", ar: "بحسب سياسة هذا المستشفى"}, // TODO-REVIEW es+ar
  r_deadline:  {en: "Deadline", es: "Fecha límite", ar: "الموعد النهائي"}, // TODO-REVIEW es+ar
  r_about:     {en: "About this bill", es: "Sobre esta factura", ar: "عن هذه الفاتورة"}, // TODO-REVIEW es+ar
  r_docs:      {en: "Documents the hospital asks for", es: "Documentos que pide el hospital", ar: "المستندات التي يطلبها المستشفى"}, // TODO-REVIEW es+ar
  r_contact:   {en: "Where to send the application", es: "Dónde enviar la solicitud", ar: "أين ترسل الطلب"}, // TODO-REVIEW es+ar
  r_payplan:   {en: "Payment plan contact", es: "Contacto para plan de pagos", ar: "جهة الاتصال لخطة السداد"}, // TODO-REVIEW es+ar
  r_phone:     {en: "Phone", es: "Teléfono", ar: "الهاتف"}, // TODO-REVIEW es+ar
  r_email:     {en: "Email", es: "Correo electrónico", ar: "البريد الإلكتروني"}, // TODO-REVIEW es+ar
  r_tn_title:  {en: "Tennessee protections for uninsured patients", es: "Protecciones de Tennessee para pacientes sin seguro", ar: "حمايات ولاية تينيسي للمرضى غير المؤمَّنين"}, // TODO-REVIEW es+ar
  // TODO-CONTENT: no sourced text exists yet. Replace with a short summary that cites a Tennessee source.
  r_tn_body:   {en: "Content pending: a sourced summary will go here. Nothing on this card is legal advice.", es: "Contenido pendiente: aquí irá un resumen con fuente. Nada en esta tarjeta es asesoría legal.", ar: "المحتوى قيد الإعداد: سيُضاف هنا ملخص موثّق بمصدره. لا شيء في هذه البطاقة يُعد استشارة قانونية."}, // TODO-REVIEW es+ar
  r_fallback:  {en: "Shown in English: the translated text did not pass the number check.", es: "Se muestra en inglés: el texto traducido no pasó la verificación de números.", ar: "معروض بالإنجليزية: النص المترجم لم يجتز فحص الأرقام."}, // TODO-REVIEW es+ar
  r_policy_en: {en: "Policy text is shown in English, as the hospital wrote it.", es: "El texto de la política se muestra en inglés, como lo escribió el hospital.", ar: "نص السياسة معروض بالإنجليزية كما كتبه المستشفى."}, // TODO-REVIEW es+ar
  r_see_en:    {en: "Show in English", es: "Ver en inglés", ar: "عرض بالإنجليزية"}, // TODO-REVIEW es+ar
  r_see_native:{en: "Show in my language", es: "Ver en mi idioma", ar: "عرض بلغتي"}, // TODO-REVIEW es+ar
  r_packet:    {en: "Create my application packet", es: "Crear mi paquete de solicitud", ar: "أنشئ حزمة طلبي"}, // TODO-REVIEW es+ar
  r_no_packet: {en: "Not eligible under this policy. No application packet is made. Ask about the payment plan.", es: "No califica según esta política. No se crea un paquete de solicitud. Pregunte por el plan de pagos.", ar: "غير مؤهل بحسب هذه السياسة. لا تُنشأ حزمة طلب. اسأل عن خطة السداد."}, // TODO-REVIEW es+ar
  restart:     {en: "Start over", es: "Empezar de nuevo", ar: "ابدأ من جديد"}, // TODO-REVIEW es+ar
  p_title:     {en: "Your application packet", es: "Su paquete de solicitud", ar: "حزمة طلبك"}, // TODO-REVIEW es+ar
  p_print:     {en: "Print", es: "Imprimir", ar: "طباعة"}, // TODO-REVIEW es+ar
  p_sub:       {en: "You send this yourself. The hospital makes the final decision.", es: "Usted lo envía por su cuenta. El hospital toma la decisión final.", ar: "أنت من يرسله بنفسك. المستشفى هو من يتخذ القرار النهائي."}, // TODO-REVIEW es+ar
  src:         {en: "Source", es: "Fuente", ar: "المصدر"}, // TODO-REVIEW es+ar
  page:        {en: "page", es: "página", ar: "صفحة"}, // TODO-REVIEW es+ar
  effective:   {en: "effective", es: "vigente desde", ar: "ساري من"}, // TODO-REVIEW es+ar
  err_generic: {en: "Something went wrong. Please try again.", es: "Algo salió mal. Inténtelo de nuevo.", ar: "حدث خطأ ما. حاول مرة أخرى."}, // TODO-REVIEW es+ar
  err_invalid: {en: "Check the values: they are missing or not valid.", es: "Revise los valores: faltan o no son válidos.", ar: "تحقق من القيم: فهي ناقصة أو غير صالحة."}, // TODO-REVIEW es+ar
};
const LANG_NAMES = {en: "English", es: "Español", ar: "العربية"};
const FIELD_ORDER = [
  ["hospital_name", "f_hospital"], ["statement_date", "f_statement"], ["account_number", "f_account"],
  ["amount_due_cents", "f_amount"], ["date_of_service", "f_service"], ["insurance_status", "f_insurance"],
];
const REQUIRED = new Set(["statement_date", "amount_due_cents"]); // the engine needs these two

const S = {lang: "en", view: "en", forWhom: "self", bill: null, imageUrl: null, answers: null,
          result: null, explain: null, size: "", income: "", tax: null, busy: false};

// ---------- helpers
function t(key, vars) {
  const row = T[key];
  let s = (row && (row[S.view] || row.en)) || key;
  for (const k in (vars || {})) s = s.replace("{" + k + "}", vars[k]);
  return s;
}
function el(tag, attrs, ...kids) {
  const e = document.createElement(tag);
  for (const k in (attrs || {})) {
    if (k === "class") e.className = attrs[k];
    else if (k.startsWith("on")) e.addEventListener(k.slice(2), attrs[k]);
    else if (attrs[k] !== false && attrs[k] != null) e.setAttribute(k, attrs[k] === true ? "" : attrs[k]);
  }
  for (const kid of kids) if (kid != null) e.append(kid);
  return e;
}
function englishOnly(tag, attrs, text) { // policy text is English: keep it left-to-right
  return el(tag, Object.assign({lang: "en", dir: "ltr"}, attrs || {}), text);
}
function applyDir() {
  document.documentElement.lang = S.view;
  document.documentElement.dir = S.view === "ar" ? "rtl" : "ltr";
  document.getElementById("app-title").textContent = t("app_title");
}
function showMsg(text, info) {
  const m = document.getElementById("msg");
  m.textContent = text || "";
  m.hidden = !text;
  m.className = "msg" + (info ? " info" : "");
}
function show(n) {
  for (let i = 1; i <= 5; i++) document.getElementById("s" + i).hidden = i !== n;
  applyDir();
  [null, renderStart, renderBill, renderQuestions, renderResult, renderPacketShell][n]();
}
async function post(path, body, asText) {
  let r;
  try {
    r = await fetch(path, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)});
  } catch (e) { throw new Error(t("err_generic")); }
  if (!r.ok) {
    let detail = "";
    try { const j = await r.json(); detail = typeof j.detail === "string" ? j.detail : t("err_invalid"); } catch (e) { /* ignore */ }
    throw new Error(detail || t("err_generic"));
  }
  return asText ? r.text() : r.json();
}
// "4812.40" or "$4,812.4" -> 481240 ; invalid -> null. String math, no floats.
function dollarsToCents(s) {
  const m = /^\$?\s*(\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d{1,2}))?$/.exec((s || "").trim());
  if (!m) return null;
  return parseInt(m[1].replace(/,/g, ""), 10) * 100 + parseInt((m[2] || "0").padEnd(2, "0"), 10);
}
function centsToDollars(c) {
  return Math.floor(c / 100) + "." + String(c % 100).padStart(2, "0");
}
function cite(c) {
  if (!c || !c.source) return null;
  let s = t("src") + ": " + c.source;
  if (c.page !== null && c.page !== undefined && c.page !== "") s += ", " + t("page") + " " + c.page;
  if (c.effective_date) s += ", " + t("effective") + " " + c.effective_date;
  if (c.url) return englishOnly("a", {class: "cite", href: c.url, target: "_blank", rel: "noopener"}, s);
  return englishOnly("span", {class: "cite"}, s);
}
function blankBill() {
  const f = {};
  for (const [name] of FIELD_ORDER) f[name] = {value: null, confidence: 0.0, confirmed: false};
  return {contract_version: 1, fields: f};
}

// ---------- screen 1: start
function renderStart() {
  const root = document.getElementById("s1");
  root.replaceChildren(
    el("p", {class: "notice"}, t("notice")),
    el("p", {class: "muted"}, t("no_id")),
    el("h2", null, t("pick_lang")),
    el("div", {class: "row"}, ...["ar", "es", "en"].map(l =>
      el("button", {"aria-pressed": String(S.lang === l), lang: l, onclick: () => { S.lang = l; S.view = l; show(1); }}, LANG_NAMES[l]))),
    el("h2", null, t("for_whom")),
    el("div", {class: "row"}, ...[["self", "me"], ["family", "family"]].map(([v, k]) =>
      el("button", {"aria-pressed": String(S.forWhom === v), onclick: () => { S.forWhom = v; show(1); }}, t(k)))),
    el("div", {class: "row"}, el("button", {class: "primary", onclick: () => { showMsg(""); show(2); }}, t("start"))),
  );
}

// ---------- screen 2: bill
function renderBill() {
  const root = document.getElementById("s2");
  const file = el("input", {type: "file", accept: "image/png,image/jpeg", id: "bill-file"});
  file.addEventListener("change", onFile);
  const left = el("div", null, el("label", {for: "bill-file"}, t("upload")), file);
  if (S.imageUrl) left.append(el("img", {src: S.imageUrl, alt: ""}));
  const right = el("div", {id: "fields"});
  root.replaceChildren(
    el("h2", null, t("bill_title")),
    el("p", {class: "muted"}, t("bill_hint")),
    el("div", {class: "bill-grid"}, left, right),
    el("div", {class: "row"},
      el("button", {onclick: () => show(1)}, t("back")),
      el("button", {class: "primary", id: "bill-next", disabled: true, onclick: () => show(3)}, t("continue_"))));
  if (S.bill) renderFields();
}
async function onFile(ev) {
  const f = ev.target.files[0];
  if (!f) return;
  if (S.imageUrl) URL.revokeObjectURL(S.imageUrl);
  S.imageUrl = URL.createObjectURL(f);
  S.bill = null;
  showMsg(t("reading"), true);
  const fd = new FormData();
  fd.append("file", f);
  try {
    const r = await fetch("/extract", {method: "POST", body: fd});
    if (!r.ok) throw new Error("extract");
    S.bill = await r.json();
    showMsg("");
  } catch (e) {
    S.bill = blankBill();
    showMsg(t("read_failed"));
  }
  renderBill();
}
function readInput(name, node) {
  const v = node.value.trim();
  if (v === "") return null;
  if (name === "amount_due_cents") return dollarsToCents(v);
  return v;
}
function renderFields() {
  const box = document.getElementById("fields");
  const rows = FIELD_ORDER.map(([name, labelKey]) => {
    const f = S.bill.fields[name];
    const id = "f-" + name;
    let input;
    if (name === "insurance_status") {
      input = el("select", {id}, ...[["", "ins_blank"], ["self_pay", "ins_self_pay"], ["insured", "ins_insured"], ["unknown", "ins_unknown"]]
        .map(([v, k]) => el("option", {value: v, selected: (f.value || "") === v}, t(k))));
    } else if (name.endsWith("date") || name === "date_of_service") {
      input = el("input", {type: "date", id, value: f.value || ""});
    } else if (name === "amount_due_cents") {
      input = el("input", {type: "text", id, inputmode: "decimal", value: f.value === null ? "" : centsToDollars(f.value)});
    } else {
      input = el("input", {type: "text", id, value: f.value || "", autocomplete: "off"});
    }
    const cb = el("input", {type: "checkbox", id: id + "-ok"});
    const hint = el("span", {class: "hint"});
    const wrap = el("div", {class: "field"},
      el("label", {for: id}, t(labelKey) + (REQUIRED.has(name) ? " *" : "")), input, hint,
      el("label", {class: "check", for: id + "-ok"}, cb, t("confirm")));
    const sync = () => {
      const blank = f.value === null || f.value === "";
      hint.textContent = blank ? t("unreadable") + (REQUIRED.has(name) ? " (" + t("required") + ")" : "") : "";
      cb.disabled = blank && REQUIRED.has(name);
      cb.checked = f.confirmed;
      wrap.className = "field" + (f.confirmed ? " confirmed" : blank ? " blank" : "");
      document.getElementById("bill-next").disabled = !FIELD_ORDER.every(([n]) => S.bill.fields[n].confirmed);
    };
    const onEdit = () => { f.value = readInput(name, input); f.confirmed = false; f.confidence = null; sync(); };
    input.addEventListener(name === "insurance_status" ? "change" : "input", onEdit);
    cb.addEventListener("change", () => { f.confirmed = cb.checked; sync(); });
    wrap.sync = sync;
    return wrap;
  });
  box.replaceChildren(...rows);
  rows.forEach(r => r.sync());
}

// ---------- screen 3: three questions
function renderQuestions() {
  const root = document.getElementById("s3");
  const size = el("input", {type: "number", id: "q-size", min: "1", max: "12", step: "1", value: S.size});
  const income = el("input", {type: "text", id: "q-income", inputmode: "decimal", value: S.income, autocomplete: "off"});
  const go = el("button", {class: "primary", id: "q-go", onclick: submitAnswers}, t("see_result"));
  const check = () => {
    S.size = size.value; S.income = income.value;
    const n = Number(S.size);
    go.disabled = S.busy || !(Number.isInteger(n) && n >= 1 && n <= 12) || dollarsToCents(S.income) === null || S.tax === null;
  };
  size.addEventListener("input", check);
  income.addEventListener("input", check);
  const taxBtn = (val, key) => el("button", {"aria-pressed": String(S.tax === val), onclick: () => { S.tax = val; renderQuestions(); }}, t(key));
  root.replaceChildren(
    el("h2", null, t("q_title")),
    el("p", {class: "muted"}, t("no_id")),
    el("label", {for: "q-size"}, t("q_size")), size,
    el("p", null), el("label", {for: "q-income"}, t("q_income")), income,
    el("p", null), el("label", null, t("q_tax")), el("div", {class: "row"}, taxBtn(true, "yes"), taxBtn(false, "no")),
    el("div", {class: "row"}, el("button", {onclick: () => show(2)}, t("back")), go));
  check();
}
async function submitAnswers() {
  S.answers = {contract_version: 1, language: S.lang, for_whom: S.forWhom, household_size: Number(S.size),
               annual_income_cents: dollarsToCents(S.income), files_tax_return: S.tax};
  S.busy = true; showMsg(t("working"), true);
  document.getElementById("q-go").disabled = true;
  try {
    S.result = await post("/evaluate", {bill: S.bill, answers: S.answers});
    S.explain = await post("/explain", {bill: S.bill, answers: S.answers, result: S.result});
    S.view = S.lang; showMsg("");
    S.busy = false; show(4);
  } catch (e) {
    S.busy = false; showMsg(e.message); renderQuestions();
  }
}

// ---------- screen 4: result
function renderResult() {
  const r = S.result, root = document.getElementById("s4");
  const english = S.view === "en";
  const textDir = english || S.explain.fallback_used ? "ltr" : (S.view === "ar" ? "rtl" : "ltr");
  const textLang = english || S.explain.fallback_used ? "en" : S.view;
  const lines = (english ? S.explain.text_en : S.explain.text).split("\n");
  const eligible = r.tier.eligible;
  const docs = el("ul", null, ...r.documents.map(d => el("li", null, englishOnly("span", null, d.label_en), cite(d.citation))));
  const c = r.contacts;
  const contactCard = eligible
    ? el("div", {class: "card"}, el("strong", null, t("r_contact")), el("p", null, t("r_email") + ": ", englishOnly("span", null, c.email)),
        el("p", null, t("r_phone") + ": ", englishOnly("span", null, c.phone)), cite(c.citation))
    : el("div", {class: "card"}, el("strong", null, t("r_payplan")),
        el("p", null, t("r_phone") + ": ", englishOnly("span", null, c.payment_plan_phone || c.phone)), cite(c.citation));
  const toggle = S.lang === "en" ? null
    : el("button", {onclick: () => { S.view = english ? S.lang : "en"; show(4); }}, english ? t("r_see_native") : t("r_see_en"));
  root.replaceChildren(
    el("h2", null, t("r_title")),
    toggle ? el("div", {class: "row"}, toggle) : null,
    el("p", {class: "stat"}, t("r_percent", {pct: r.percent_of_fpl, year: r.fpl.year})),
    cite(r.fpl.citation),
    el("div", {class: "card tier"}, el("strong", null, t("r_tier")),
      englishOnly("p", {class: "stat"}, r.tier.label_en), cite(r.tier.citation)),
    el("div", {class: "card"}, el("strong", null, t("r_deadline")),
      englishOnly("p", null, r.deadline.text_en), cite(r.deadline.citation)),
    el("div", {class: "card explain"}, el("strong", null, t("r_about")),
      ...lines.map(l => el("p", {dir: textDir, lang: textLang}, l))),
    S.explain.fallback_used && !english ? el("p", {class: "muted"}, t("r_fallback")) : null,
    el("p", {class: "muted"}, t("r_policy_en")),
    eligible ? el("div", {class: "card"}, el("strong", null, t("r_docs")), docs) : null,
    contactCard,
    el("div", {class: "card"}, el("strong", null, t("r_tn_title")), el("p", null, t("r_tn_body"))),
    eligible ? null : el("p", null, t("r_no_packet")),
    el("div", {class: "row"},
      el("button", {onclick: () => show(3)}, t("back")),
      eligible ? el("button", {class: "primary", onclick: () => { show(5); loadPacket(); }}, t("r_packet")) : null,
      el("button", {onclick: restart}, t("restart"))));
}

// ---------- screen 5: packet
function renderPacketShell() {
  document.getElementById("s5").replaceChildren(
    el("h2", null, t("p_title")), el("p", {class: "muted"}, t("p_sub")),
    el("div", {class: "row"},
      el("button", {onclick: () => show(4)}, t("back")),
      el("button", {class: "primary", id: "print-btn", disabled: true, onclick: () => document.getElementById("packet-frame").contentWindow.print()}, t("p_print")),
      el("button", {onclick: restart}, t("restart"))),
    el("iframe", {id: "packet-frame", title: t("p_title"), sandbox: "allow-modals allow-same-origin"}));
}
async function loadPacket() {
  showMsg(t("working"), true);
  try {
    const page = await post("/packet", {bill: S.bill, answers: S.answers, result: S.result}, true);
    document.getElementById("packet-frame").srcdoc = page;
    document.getElementById("print-btn").disabled = false;
    showMsg("");
  } catch (e) { showMsg(e.message); }
}

function restart() {
  if (S.imageUrl) URL.revokeObjectURL(S.imageUrl);
  Object.assign(S, {bill: null, imageUrl: null, answers: null, result: null, explain: null, size: "", income: "", tax: null, busy: false});
  showMsg(""); show(1);
}

show(1);
