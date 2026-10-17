"use strict";
// Bill to Help UI. All state lives in this object in memory only: no localStorage, no cookies, no disk.

// UI strings. Every es, ar, zh-CN and zh-TW string is a draft for a human translator.
// TODO-REVIEW: all es/ar/zh strings below (one marker per line).
// Tier 1 (en, es, ar, zh-CN, zh-TW) has a translated interface. Tier 2 (vi, fr, ko, ru, de, hi) keeps the
// English interface (t() falls back to en): only the explanation and the packet letter are translated.
const T = {
  app_title:   {en: "Bill to Help", es: "Factura a Ayuda", ar: "من الفاتورة إلى المساعدة", "zh-CN": "从账单到帮助", "zh-TW": "從帳單到幫助"}, // TODO-REVIEW es+ar+zh
  notice:      {en: "Nothing you enter is saved. Demo uses synthetic bills only.", es: "Nada de lo que escribe se guarda. La demostración usa solo facturas sintéticas.", ar: "لا يتم حفظ أي شيء تدخله. العرض التجريبي يستخدم فواتير اصطناعية فقط.", "zh-CN": "您输入的任何内容都不会被保存。演示仅使用合成账单。", "zh-TW": "您輸入的任何內容都不會被儲存。示範僅使用合成帳單。"}, // TODO-REVIEW es+ar+zh
  no_id:       {en: "We do not ask for your name, immigration status, Social Security number, or ID.", es: "No pedimos su nombre, su estatus migratorio, su número de Seguro Social ni su identificación.", ar: "لا نطلب اسمك أو وضعك في الهجرة أو رقم الضمان الاجتماعي أو أي هوية.", "zh-CN": "我们不会询问您的姓名、移民身份、社会安全号码或身份证件。", "zh-TW": "我們不會詢問您的姓名、移民身分、社會安全號碼或身分證件。"}, // TODO-REVIEW es+ar+zh
  pick_lang:   {en: "Choose a language", es: "Elija un idioma", ar: "اختر اللغة", "zh-CN": "选择语言", "zh-TW": "選擇語言"}, // TODO-REVIEW es+ar+zh
  for_whom:    {en: "This bill is for:", es: "Esta factura es para:", ar: "هذه الفاتورة لـ:", "zh-CN": "这份账单是给：", "zh-TW": "這份帳單是給："}, // TODO-REVIEW es+ar+zh
  me:          {en: "Me", es: "Yo", ar: "أنا", "zh-CN": "我", "zh-TW": "我"}, // TODO-REVIEW es+ar+zh
  family:      {en: "A family member", es: "Un familiar", ar: "أحد أفراد عائلتي", "zh-CN": "家人", "zh-TW": "家人"}, // TODO-REVIEW es+ar+zh
  start:       {en: "Start", es: "Comenzar", ar: "ابدأ", "zh-CN": "开始", "zh-TW": "開始"}, // TODO-REVIEW es+ar+zh
  bill_title:  {en: "Your bill", es: "Su factura", ar: "فاتورتك", "zh-CN": "您的账单", "zh-TW": "您的帳單"}, // TODO-REVIEW es+ar+zh
  upload:      {en: "Upload or take a photo of the bill", es: "Suba o tome una foto de la factura", ar: "ارفع صورة الفاتورة أو التقطها", "zh-CN": "上传或拍摄账单照片", "zh-TW": "上傳或拍攝帳單照片"}, // TODO-REVIEW es+ar+zh
  reading:     {en: "Reading the bill...", es: "Leyendo la factura...", ar: "جارٍ قراءة الفاتورة...", "zh-CN": "正在读取账单...", "zh-TW": "正在讀取帳單..."}, // TODO-REVIEW es+ar+zh
  read_failed: {en: "Photo reading is not available right now. Type the fields in by hand.", es: "La lectura de fotos no está disponible ahora. Escriba los campos a mano.", ar: "قراءة الصورة غير متاحة الآن. اكتب الحقول يدويًا.", "zh-CN": "目前无法读取照片。请手动填写各字段。", "zh-TW": "目前無法讀取照片。請手動填寫各欄位。"}, // TODO-REVIEW es+ar+zh
  bill_hint:   {en: "Check each field against your bill, fix mistakes, then confirm each one. A blank field means we could not read it: type it in.", es: "Compare cada campo con su factura, corrija los errores y confirme cada uno. Un campo en blanco significa que no pudimos leerlo: escríbalo.", ar: "قارن كل حقل بفاتورتك وصحح الأخطاء ثم أكّد كل حقل. الحقل الفارغ يعني أننا لم نستطع قراءته: اكتبه.", "zh-CN": "请对照账单检查每个字段，修正错误，然后逐一确认。字段为空表示我们无法读取：请自行填写。", "zh-TW": "請對照帳單檢查每個欄位，修正錯誤，然後逐一確認。欄位空白表示我們無法讀取：請自行填寫。"}, // TODO-REVIEW es+ar+zh
  f_hospital:  {en: "Hospital", es: "Hospital", ar: "المستشفى", "zh-CN": "医院", "zh-TW": "醫院"}, // TODO-REVIEW es+ar+zh
  f_statement: {en: "Statement date", es: "Fecha del estado de cuenta", ar: "تاريخ الكشف", "zh-CN": "账单日期", "zh-TW": "帳單日期"}, // TODO-REVIEW es+ar+zh
  f_account:   {en: "Account number", es: "Número de cuenta", ar: "رقم الحساب", "zh-CN": "账号", "zh-TW": "帳號"}, // TODO-REVIEW es+ar+zh
  f_amount:    {en: "Amount due (US dollars)", es: "Monto adeudado (dólares)", ar: "المبلغ المستحق (بالدولار)", "zh-CN": "应付金额（美元）", "zh-TW": "應付金額（美元）"}, // TODO-REVIEW es+ar+zh
  f_service:   {en: "Date of service", es: "Fecha del servicio", ar: "تاريخ الخدمة", "zh-CN": "服务日期", "zh-TW": "服務日期"}, // TODO-REVIEW es+ar+zh
  f_insurance: {en: "Insurance", es: "Seguro médico", ar: "التأمين", "zh-CN": "保险", "zh-TW": "保險"}, // TODO-REVIEW es+ar+zh
  ins_blank:   {en: "(not set)", es: "(sin definir)", ar: "(غير محدد)", "zh-CN": "（未设置）", "zh-TW": "（未設定）"}, // TODO-REVIEW es+ar+zh
  ins_self_pay:{en: "Self-pay (no insurance)", es: "Pago propio (sin seguro)", ar: "دفع شخصي (بدون تأمين)", "zh-CN": "自费（无保险）", "zh-TW": "自費（無保險）"}, // TODO-REVIEW es+ar+zh
  ins_insured: {en: "Insured", es: "Con seguro", ar: "مؤمَّن", "zh-CN": "已投保", "zh-TW": "已投保"}, // TODO-REVIEW es+ar+zh
  ins_unknown: {en: "Unknown", es: "Desconocido", ar: "غير معروف", "zh-CN": "未知", "zh-TW": "未知"}, // TODO-REVIEW es+ar+zh
  unreadable:  {en: "Could not read this. Please type it.", es: "No se pudo leer. Escríbalo, por favor.", ar: "تعذّرت قراءة هذا الحقل. الرجاء كتابته.", "zh-CN": "无法读取此项。请手动填写。", "zh-TW": "無法讀取此項。請手動填寫。"}, // TODO-REVIEW es+ar+zh
  required:    {en: "Required", es: "Obligatorio", ar: "مطلوب", "zh-CN": "必填", "zh-TW": "必填"}, // TODO-REVIEW es+ar+zh
  confirm:     {en: "This is correct", es: "Esto es correcto", ar: "هذا صحيح", "zh-CN": "此项正确", "zh-TW": "此項正確"}, // TODO-REVIEW es+ar+zh
  continue_:   {en: "Continue", es: "Continuar", ar: "متابعة", "zh-CN": "继续", "zh-TW": "繼續"}, // TODO-REVIEW es+ar+zh
  back:        {en: "Back", es: "Atrás", ar: "رجوع", "zh-CN": "返回", "zh-TW": "返回"}, // TODO-REVIEW es+ar+zh
  q_title:     {en: "Three questions", es: "Tres preguntas", ar: "ثلاثة أسئلة", "zh-CN": "三个问题", "zh-TW": "三個問題"}, // TODO-REVIEW es+ar+zh
  q_size:      {en: "How many people live in your household (1 to 12)?", es: "¿Cuántas personas viven en su hogar (de 1 a 12)?", ar: "كم عدد الأشخاص في أسرتك (من 1 إلى 12)؟", "zh-CN": "您家有几口人（1 到 12）？", "zh-TW": "您家有幾口人（1 到 12）？"}, // TODO-REVIEW es+ar+zh
  q_income:    {en: "Total yearly household income before taxes, in US dollars", es: "Ingreso anual total del hogar antes de impuestos, en dólares", ar: "إجمالي دخل الأسرة السنوي قبل الضرائب بالدولار", "zh-CN": "家庭税前年总收入（美元）", "zh-TW": "家庭稅前年總收入（美元）"}, // TODO-REVIEW es+ar+zh
  q_tax:       {en: "Do you file a tax return?", es: "¿Presenta una declaración de impuestos?", ar: "هل تقدّم إقرارًا ضريبيًا؟", "zh-CN": "您是否报税？", "zh-TW": "您是否報稅？"}, // TODO-REVIEW es+ar+zh
  yes:         {en: "Yes", es: "Sí", ar: "نعم", "zh-CN": "是", "zh-TW": "是"}, // TODO-REVIEW es+ar+zh
  no:          {en: "No", es: "No", ar: "لا", "zh-CN": "否", "zh-TW": "否"}, // TODO-REVIEW es+ar+zh
  see_result:  {en: "See my result", es: "Ver mi resultado", ar: "اعرض نتيجتي", "zh-CN": "查看我的结果", "zh-TW": "查看我的結果"}, // TODO-REVIEW es+ar+zh
  load_evaluate:{en: "Checking the hospital's policy...", es: "Revisando la política del hospital...", ar: "جارٍ فحص سياسة المستشفى...", "zh-CN": "正在核对医院的政策...", "zh-TW": "正在核對醫院的政策..."}, // TODO-REVIEW es+ar+zh
  load_explain:{en: "Writing your explanation...", es: "Escribiendo su explicación...", ar: "جارٍ كتابة الشرح الخاص بك...", "zh-CN": "正在撰写您的说明...", "zh-TW": "正在撰寫您的說明..."}, // TODO-REVIEW es+ar+zh
  load_packet: {en: "Building your packet...", es: "Creando su paquete...", ar: "جارٍ إنشاء حزمتك...", "zh-CN": "正在生成您的材料包...", "zh-TW": "正在建立您的資料包..."}, // TODO-REVIEW es+ar+zh
  step_1:      {en: "Start", es: "Inicio", ar: "البداية", "zh-CN": "开始", "zh-TW": "開始"}, // TODO-REVIEW es+ar+zh
  step_2:      {en: "Bill", es: "Factura", ar: "الفاتورة", "zh-CN": "账单", "zh-TW": "帳單"}, // TODO-REVIEW es+ar+zh
  step_3:      {en: "Questions", es: "Preguntas", ar: "الأسئلة", "zh-CN": "问题", "zh-TW": "問題"}, // TODO-REVIEW es+ar+zh
  step_4:      {en: "Result", es: "Resultado", ar: "النتيجة", "zh-CN": "结果", "zh-TW": "結果"}, // TODO-REVIEW es+ar+zh
  step_5:      {en: "Packet", es: "Paquete", ar: "الحزمة", "zh-CN": "材料包", "zh-TW": "資料包"}, // TODO-REVIEW es+ar+zh
  step_of:     {en: "Step {n} of {total}", es: "Paso {n} de {total}", ar: "الخطوة {n} من {total}", "zh-CN": "第 {n} 步，共 {total} 步", "zh-TW": "第 {n} 步，共 {total} 步"}, // TODO-REVIEW es+ar+zh
  tbl_income:  {en: "Household income (percent of the poverty guideline)", es: "Ingreso del hogar (porcentaje de la guía de pobreza)", ar: "دخل الأسرة (نسبة من الحد الفيدرالي للفقر)", "zh-CN": "家庭收入（占贫困线的百分比）", "zh-TW": "家庭收入（占貧困線的百分比）"}, // TODO-REVIEW es+ar+zh
  tbl_result:  {en: "Result", es: "Resultado", ar: "النتيجة", "zh-CN": "结果", "zh-TW": "結果"}, // TODO-REVIEW es+ar+zh
  band_upto:   {en: "Up to {max}%", es: "Hasta {max}%", ar: "حتى {max}%", "zh-CN": "不超过 {max}%", "zh-TW": "不超過 {max}%"}, // TODO-REVIEW es+ar+zh
  band_between:{en: "Above {min}% up to {max}%", es: "Más de {min}% hasta {max}%", ar: "أكثر من {min}% حتى {max}%", "zh-CN": "超过 {min}% 至 {max}%", "zh-TW": "超過 {min}% 至 {max}%"}, // TODO-REVIEW es+ar+zh
  band_above:  {en: "Above {min}%", es: "Más de {min}%", ar: "أكثر من {min}%", "zh-CN": "超过 {min}%", "zh-TW": "超過 {min}%"}, // TODO-REVIEW es+ar+zh
  you_tag:     {en: "You: {pct}%", es: "Usted: {pct}%", ar: "أنت: {pct}%", "zh-CN": "您：{pct}%", "zh-TW": "您：{pct}%"}, // TODO-REVIEW es+ar+zh
  not_affiliated:{en: "Independent tool. Not affiliated with any hospital.", es: "Herramienta independiente. No está afiliada a ningún hospital.", ar: "أداة مستقلة. لا ترتبط بأي مستشفى.", "zh-CN": "独立工具，与任何医院均无关联。", "zh-TW": "獨立工具，與任何醫院均無關聯。"}, // TODO-REVIEW es+ar+zh
  r_title:     {en: "Your result", es: "Su resultado", ar: "نتيجتك", "zh-CN": "您的结果", "zh-TW": "您的結果"}, // TODO-REVIEW es+ar+zh
  r_decides:   {en: "This is an estimate. The hospital makes the final decision.", es: "Esto es una estimación. El hospital toma la decisión final.", ar: "هذا تقدير فقط. المستشفى هو من يتخذ القرار النهائي.", "zh-CN": "这只是估算。最终决定由医院做出。", "zh-TW": "這只是估算。最終決定由醫院做出。"}, // TODO-REVIEW es+ar+zh
  r_percent:   {en: "Your income is about {pct}% of the {year} federal poverty guideline", es: "Su ingreso es aproximadamente el {pct}% de la guía federal de pobreza de {year}", ar: "دخلك يعادل تقريبًا {pct}% من الحد الفيدرالي للفقر لعام {year}", "zh-CN": "您的收入约为 {year} 年联邦贫困线的 {pct}%", "zh-TW": "您的收入約為 {year} 年聯邦貧困線的 {pct}%"}, // TODO-REVIEW es+ar+zh
  r_tier:      {en: "Under this hospital's policy", es: "Según la política de este hospital", ar: "بحسب سياسة هذا المستشفى", "zh-CN": "根据本医院的政策", "zh-TW": "根據本醫院的政策"}, // TODO-REVIEW es+ar+zh
  r_deadline:  {en: "Deadline", es: "Fecha límite", ar: "الموعد النهائي", "zh-CN": "截止日期", "zh-TW": "截止日期"}, // TODO-REVIEW es+ar+zh
  r_about:     {en: "About this bill", es: "Sobre esta factura", ar: "عن هذه الفاتورة", "zh-CN": "关于这份账单", "zh-TW": "關於這份帳單"}, // TODO-REVIEW es+ar+zh
  r_docs:      {en: "Documents the hospital asks for", es: "Documentos que pide el hospital", ar: "المستندات التي يطلبها المستشفى", "zh-CN": "医院要求的文件", "zh-TW": "醫院要求的文件"}, // TODO-REVIEW es+ar+zh
  r_contact:   {en: "Where to send the application", es: "Dónde enviar la solicitud", ar: "أين ترسل الطلب", "zh-CN": "申请材料寄送处", "zh-TW": "申請資料寄送處"}, // TODO-REVIEW es+ar+zh
  r_payplan:   {en: "Payment plan contact", es: "Contacto para plan de pagos", ar: "جهة الاتصال لخطة السداد", "zh-CN": "付款计划联系方式", "zh-TW": "付款計畫聯絡方式"}, // TODO-REVIEW es+ar+zh
  r_phone:     {en: "Phone", es: "Teléfono", ar: "الهاتف", "zh-CN": "电话", "zh-TW": "電話"}, // TODO-REVIEW es+ar+zh
  r_email:     {en: "Email", es: "Correo electrónico", ar: "البريد الإلكتروني", "zh-CN": "电子邮件", "zh-TW": "電子郵件"}, // TODO-REVIEW es+ar+zh
  r_fallback:  {en: "Shown in English: the translated text did not pass the number check.", es: "Se muestra en inglés: el texto traducido no pasó la verificación de números.", ar: "معروض بالإنجليزية: النص المترجم لم يجتز فحص الأرقام.", "zh-CN": "以英文显示：翻译后的文字未通过数字检查。", "zh-TW": "以英文顯示：翻譯後的文字未通過數字檢查。"}, // TODO-REVIEW es+ar+zh
  r_policy_en: {en: "Policy text is shown in English, as the hospital wrote it.", es: "El texto de la política se muestra en inglés, como lo escribió el hospital.", ar: "نص السياسة معروض بالإنجليزية كما كتبه المستشفى.", "zh-CN": "政策文本按医院原文以英文显示。", "zh-TW": "政策文本依醫院原文以英文顯示。"}, // TODO-REVIEW es+ar+zh
  r_see_en:    {en: "Show in English", es: "Ver en inglés", ar: "عرض بالإنجليزية", "zh-CN": "显示英文", "zh-TW": "顯示英文"}, // TODO-REVIEW es+ar+zh
  r_see_native:{en: "Show in my language", es: "Ver en mi idioma", ar: "عرض بلغتي", "zh-CN": "显示我的语言", "zh-TW": "顯示我的語言"}, // TODO-REVIEW es+ar+zh
  r_packet:    {en: "Create my application packet", es: "Crear mi paquete de solicitud", ar: "أنشئ حزمة طلبي", "zh-CN": "创建我的申请材料包", "zh-TW": "建立我的申請資料包"}, // TODO-REVIEW es+ar+zh
  r_no_packet: {en: "Not eligible under this policy. No application packet is made. Ask about the payment plan.", es: "No califica según esta política. No se crea un paquete de solicitud. Pregunte por el plan de pagos.", ar: "غير مؤهل بحسب هذه السياسة. لا تُنشأ حزمة طلب. اسأل عن خطة السداد.", "zh-CN": "根据本政策不符合资格，不会生成申请材料包。请咨询付款计划。", "zh-TW": "根據本政策不符合資格，不會產生申請資料包。請洽詢付款計畫。"}, // TODO-REVIEW es+ar+zh
  restart:     {en: "Start over", es: "Empezar de nuevo", ar: "ابدأ من جديد", "zh-CN": "重新开始", "zh-TW": "重新開始"}, // TODO-REVIEW es+ar+zh
  p_title:     {en: "Your application packet", es: "Su paquete de solicitud", ar: "حزمة طلبك", "zh-CN": "您的申请材料包", "zh-TW": "您的申請資料包"}, // TODO-REVIEW es+ar+zh
  p_print:     {en: "Print", es: "Imprimir", ar: "طباعة", "zh-CN": "打印", "zh-TW": "列印"}, // TODO-REVIEW es+ar+zh
  p_sub:       {en: "You send this yourself. The hospital makes the final decision.", es: "Usted lo envía por su cuenta. El hospital toma la decisión final.", ar: "أنت من يرسله بنفسك. المستشفى هو من يتخذ القرار النهائي.", "zh-CN": "由您自行寄出。最终决定由医院做出。", "zh-TW": "由您自行寄出。最終決定由醫院做出。"}, // TODO-REVIEW es+ar+zh
  src:         {en: "Source", es: "Fuente", ar: "المصدر", "zh-CN": "来源", "zh-TW": "來源"}, // TODO-REVIEW es+ar+zh
  page:        {en: "page", es: "página", ar: "صفحة", "zh-CN": "页", "zh-TW": "頁"}, // TODO-REVIEW es+ar+zh
  effective:   {en: "effective", es: "vigente desde", ar: "ساري من", "zh-CN": "生效日期", "zh-TW": "生效日期"}, // TODO-REVIEW es+ar+zh
  err_generic: {en: "Something went wrong. Please try again.", es: "Algo salió mal. Inténtelo de nuevo.", ar: "حدث خطأ ما. حاول مرة أخرى.", "zh-CN": "出了点问题。请重试。", "zh-TW": "出了點問題。請重試。"}, // TODO-REVIEW es+ar+zh
  ai_note:     {en: "Written by AI from the English facts above; every number was checked automatically. The English is what counts.", "zh-CN": "此文本由 AI 根据上方的英文事实撰写；每个数字都已自动核对。以英文为准。", "zh-TW": "此文字由 AI 根據上方的英文事實撰寫；每個數字都已自動核對。以英文為準。", es: "Texto escrito por IA a partir de los datos en inglés; cada número se verificó automáticamente. El texto en inglés es el que vale.", ar: "كتب الذكاء الاصطناعي هذا النص من الحقائق الإنجليزية؛ وتم التحقق من كل رقم تلقائيًا. النص الإنجليزي هو المعتمد."}, // TODO-REVIEW es+ar+zh
  err_invalid: {en: "Check the values: they are missing or not valid.", es: "Revise los valores: faltan o no son válidos.", ar: "تحقق من القيم: فهي ناقصة أو غير صالحة.", "zh-CN": "请检查输入的值：缺失或无效。", "zh-TW": "請檢查輸入的值：缺漏或無效。"}, // TODO-REVIEW es+ar+zh
};
const LANG_NAMES = {en: "English", es: "Español", ar: "العربية", "zh-CN": "简体中文", "zh-TW": "繁體中文",
                    vi: "Tiếng Việt", fr: "Français", ko: "한국어", ru: "Русский", de: "Deutsch", hi: "हिन्दी"};
const TIER1 = ["ar", "es", "en", "zh-CN", "zh-TW"]; // translated interface
const TIER2 = ["vi", "fr", "ko", "ru", "de", "hi"]; // English interface, translated explanation and letter
const viewFor = l => (TIER2.includes(l) ? "en" : l);
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
// replaceChildren() renders a null argument as the text "null"; skip nulls like el() does.
function fill(node, ...kids) { node.replaceChildren(...kids.filter(k => k != null)); }
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
  renderSteps(n);
  document.getElementById("foot").textContent = t("not_affiliated");
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
function bdiEn(text) { return el("bdi", {lang: "en", dir: "ltr"}, String(text)); } // English run, isolated from the page direction
function hasPage(c) { return c.page !== null && c.page !== undefined && c.page !== ""; }
// The pieces of one citation. Translated words (Source, page, effective) sit OUTSIDE every <bdi>; only the English parts are inside.
function citeParts(c) {
  const parts = [t("src") + ": ", bdiEn(c.source)];
  if (hasPage(c)) parts.push(", " + t("page") + " ", bdiEn(c.page));
  if (c.effective_date) parts.push(", " + t("effective") + " ", bdiEn(c.effective_date));
  return parts;
}
function icon(name) { // decorative Phosphor icon, served locally
  return el("img", {src: "icons/" + name + ".svg", alt: "", width: "24", height: "24", class: "icon"});
}
// Translated template -> nodes. Each {var} (and a % right after it) goes in <bdi dir="ltr"> so numbers do not flip in Arabic.
function tNodes(key, vars) {
  const out = [];
  const tpl = t(key);
  const re = /\{(\w+)\}(%?)/g;
  let last = 0, m;
  while ((m = re.exec(tpl)) !== null) {
    if (m.index > last) out.push(tpl.slice(last, m.index));
    out.push(el("bdi", {dir: "ltr"}, String((vars || {})[m[1]]) + m[2]));
    last = re.lastIndex;
  }
  if (last < tpl.length) out.push(tpl.slice(last));
  return out;
}
// Free translated text -> nodes, with emails, money, dates, phones, account numbers and percents isolated in <bdi dir="ltr">.
const ISOLATE_RE = /[\w.+-]+@[\w-]+(?:\.[\w-]+)+|\$\s?\d[\d,]*(?:\.\d+)?|\b\d{4}-\d{2}-\d{2}\b|\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}|\b[A-Z]{2,}-\d+\b|\d+(?:[.,]\d+)*%/g;
function isolate(text) {
  const out = [];
  let last = 0, m;
  ISOLATE_RE.lastIndex = 0;
  while ((m = ISOLATE_RE.exec(text)) !== null) {
    if (m.index > last) out.push(text.slice(last, m.index));
    out.push(el("bdi", {dir: "ltr"}, m[0]));
    last = ISOLATE_RE.lastIndex;
  }
  if (last < text.length) out.push(text.slice(last));
  return out;
}
// Numbered footnotes for one screen: mark(c) returns the [n] marker, list() returns the ONE ordered list. Same citation = same number.
function makeNotes() {
  const items = [], index = new Map();
  return {
    mark(c) {
      if (!c || !c.source) return null;
      const key = [c.source, c.page, c.effective_date].join("|");
      if (!index.has(key)) { items.push(c); index.set(key, items.length); }
      const n = index.get(key);
      return el("sup", {class: "fn-mark"}, el("bdi", {dir: "ltr"}, "[" + n + "]"));
    },
    list() {
      if (!items.length) return null;
      return el("ol", {class: "notes", role: "list", "aria-label": t("src")}, ...items.map((c, i) => {
        const row = [el("span", {class: "fn-num", dir: "ltr"}, "[" + (i + 1) + "]"), el("span", {class: "fn-text"}, ...citeParts(c))];
        return el("li", {id: "fn-" + (i + 1)}, c.url
          ? el("a", {class: "note", href: c.url, target: "_blank", rel: "noopener"}, ...row)
          : el("span", {class: "note"}, ...row));
      }));
    },
  };
}
function renderSteps(n) { // segmented step bar; the current step carries aria-current="step"
  fill(document.getElementById("steps"), ...[1, 2, 3, 4, 5].map(i => {
    const cur = i === n;
    return el("li", {class: cur ? "now" : i < n ? "done" : "", "aria-current": cur ? "step" : false},
      el("span", {class: "sr-only"}, t("step_of", {n: i, total: 5}) + ": " + t("step_" + i)));
  }));
  document.getElementById("step-cap").textContent = t("step_of", {n, total: 5}) + ": " + t("step_" + n);
}
function blankBill() {
  const f = {};
  for (const [name] of FIELD_ORDER) f[name] = {value: null, confidence: 0.0, confirmed: false};
  return {contract_version: 1, fields: f};
}

// ---------- screen 1: start
function langBtn(l) {
  return el("button", {"aria-pressed": String(S.lang === l), lang: l, onclick: () => { S.lang = l; S.view = viewFor(l); show(1); }}, LANG_NAMES[l]);
}
function renderStart() {
  const root = document.getElementById("s1");
  fill(root,
    el("p", {class: "notice"}, t("notice")),
    el("p", {class: "muted"}, t("no_id")),
    el("h2", {class: "with-icon"}, icon("globe"), t("pick_lang")),
    el("div", {class: "row"}, ...TIER1.map(langBtn)),
    el("p", {class: "muted", lang: "en", dir: "ltr"}, "More languages (interface in English)"),
    el("div", {class: "row"}, ...TIER2.map(langBtn)),
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
  const left = el("div", null, el("label", {for: "bill-file", class: "with-icon"}, icon("camera"), t("upload")), file);
  if (S.imageUrl) left.append(el("img", {src: S.imageUrl, alt: ""}));
  const right = el("div", {id: "fields"});
  fill(root,
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
      input = el("input", {type: "date", id, dir: "auto", value: f.value || ""});
    } else if (name === "amount_due_cents") {
      input = el("input", {type: "text", id, dir: "auto", inputmode: "decimal", value: f.value === null ? "" : centsToDollars(f.value)});
    } else {
      input = el("input", {type: "text", id, dir: "auto", value: f.value || "", autocomplete: "off"});
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
  fill(box, ...rows);
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
  fill(root,
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
  S.busy = true; showMsg(t("load_evaluate"), true);
  document.getElementById("q-go").disabled = true;
  try {
    S.result = await post("/evaluate", {bill: S.bill, answers: S.answers});
    showMsg(t("load_explain"), true);
    S.explain = await post("/explain", {bill: S.bill, answers: S.answers, result: S.result});
    S.view = viewFor(S.lang); showMsg("");
    S.busy = false; show(4);
  } catch (e) {
    S.busy = false; showMsg(e.message); renderQuestions();
  }
}

// ---------- screen 4: result
function bandText(tier) { // "Up to 200%", "Above 200% up to 300%", "Above 400%"
  const key = tier.min_percent_exclusive == null ? "band_upto" : tier.max_percent == null ? "band_above" : "band_between";
  return tNodes(key, {min: tier.min_percent_exclusive, max: tier.max_percent});
}
function tierTable(r) { // the hospital's own tier table; the row that matches the household is marked
  const rows = r.tiers.map(tr => el("tr", tr.current ? {class: "you", "aria-current": "true"} : null,
    el("th", {scope: "row"}, ...bandText(tr), tr.current ? el("span", {class: "you-tag"}, ...tNodes("you_tag", {pct: r.percent_of_fpl})) : null),
    el("td", null, englishOnly("span", null, tr.label_en))));
  return el("table", null,
    el("thead", null, el("tr", null, el("th", {scope: "col"}, t("tbl_income")), el("th", {scope: "col"}, t("tbl_result")))),
    el("tbody", null, ...rows));
}
function deadlineLine(d) { // the English sentence with its date highlighted
  const i = d.text_en.indexOf(d.date);
  if (i < 0) return englishOnly("mark", {class: "hl"}, d.text_en);
  return el("span", {lang: "en", dir: "ltr"}, d.text_en.slice(0, i), el("mark", {class: "hl"}, d.date), d.text_en.slice(i + d.date.length));
}
function renderResult() {
  const r = S.result, root = document.getElementById("s4");
  const english = S.view === "en";
  const tier2 = TIER2.includes(S.lang);
  const fb = S.explain.fallback_used;
  // Tier 2: English facts first (the interface is English), then the translated text. Tier 1: one or the other.
  const showEn = english || fb || tier2;
  const showNative = S.lang !== "en" && !fb && (tier2 || !english);
  const enLines = showEn ? S.explain.text_en.split("\n") : [];
  const nativeLines = showNative ? S.explain.text.split("\n") : [];
  const nativeDir = S.lang === "ar" ? "rtl" : "ltr";
  const eligible = r.tier.eligible;
  // Footnote markers are numbered in the order they are created, so build the page top to bottom.
  const notes = makeNotes();
  const lead = el("p", {class: "lead"}, ...tNodes("r_percent", {pct: r.percent_of_fpl, year: r.fpl.year}), notes.mark(r.fpl.citation));
  const tierBlock = Array.isArray(r.tiers) && r.tiers.length
    ? [el("p", {class: "excerpt-head"}, t("r_tier")), tierTable(r)]
    : [el("div", {class: "card"}, el("strong", null, t("r_tier")), englishOnly("p", {class: "stat"}, r.tier.label_en))];
  const tierNote = el("p", {class: "muted tbl-note"}, t("r_policy_en"), notes.mark(r.tier.citation));
  const deadline = el("div", {class: "deadline"}, el("strong", {class: "with-icon"}, icon("calendar"), t("r_deadline")),
    el("p", {lang: "en", dir: "ltr"}, deadlineLine(r.deadline), notes.mark(r.deadline.citation)));
  const docs = el("ul", {class: "plain"}, ...r.documents.map(d => el("li", null, el("span", {lang: "en", dir: "ltr"}, d.label_en, notes.mark(d.citation)))));
  const c = r.contacts;
  const contactCard = eligible
    ? el("div", {class: "card"}, el("strong", null, t("r_contact")), el("p", null, t("r_email") + ": ", englishOnly("span", null, c.email)),
        el("p", null, t("r_phone") + ": ", englishOnly("span", null, c.phone)), notes.mark(c.citation))
    : el("div", {class: "card"}, el("strong", null, t("r_payplan")),
        el("p", null, t("r_phone") + ": ", englishOnly("span", null, c.payment_plan_phone || c.phone)), notes.mark(c.citation));
  const toggle = S.lang === "en" || tier2 ? null
    : el("button", {onclick: () => { S.view = english ? S.lang : "en"; show(4); }}, english ? t("r_see_native") : t("r_see_en"));
  fill(root,
    el("h2", null, t("r_title")),
    toggle ? el("div", {class: "row"}, toggle) : null,
    lead,
    el("p", {class: "decides"}, t("r_decides")),
    ...tierBlock,
    tierNote,
    deadline,
    el("div", {class: "card explain"}, el("strong", null, t("r_about")),
      ...enLines.map(l => el("p", {dir: "ltr", lang: "en"}, l)),
      ...nativeLines.map(l => el("p", {dir: nativeDir, lang: S.lang}, ...isolate(l)))),
    showNative ? el("p", {class: "muted"}, t("ai_note")) : null,
    fb && (tier2 || !english) ? el("p", {class: "muted"}, t("r_fallback")) : null,
    eligible ? el("div", {class: "card"}, el("strong", {class: "with-icon"}, icon("file"), t("r_docs")), docs) : null,
    contactCard,
    eligible ? null : el("p", null, t("r_no_packet")),
    notes.list(),
    el("div", {class: "row"},
      el("button", {onclick: () => show(3)}, t("back")),
      eligible ? el("button", {class: "primary", onclick: () => { show(5); loadPacket(); }}, t("r_packet")) : null,
      el("button", {onclick: restart}, t("restart"))));
}

// ---------- screen 5: packet
function renderPacketShell() {
  fill(document.getElementById("s5"), 
    el("h2", null, t("p_title")), el("p", {class: "muted"}, t("p_sub")),
    el("div", {class: "row"},
      el("button", {onclick: () => show(4)}, t("back")),
      el("button", {class: "primary", id: "print-btn", disabled: true, onclick: () => document.getElementById("packet-frame").contentWindow.print()}, icon("printer"), t("p_print")),
      el("button", {onclick: restart}, t("restart"))),
    el("iframe", {id: "packet-frame", title: t("p_title"), sandbox: "allow-modals allow-same-origin"}));
}
async function loadPacket() {
  showMsg(t("load_packet"), true);
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
