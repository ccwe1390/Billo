"use strict";
// BillScan UI. All state lives in this object in memory only: no localStorage, no cookies, no disk.

// Every language the app offers, in dropdown order. Copied from app/data/languages.json (keep the two in step).
const LANGS = [
  {code: "en", native: "English", dir: "ltr"},
  {code: "es", native: "Español", dir: "ltr"},
  {code: "ar", native: "العربية", dir: "rtl"},
  {code: "zh-CN", native: "简体中文", dir: "ltr"},
  {code: "zh-TW", native: "繁體中文", dir: "ltr"},
  {code: "cs", native: "Čeština", dir: "ltr"},
  {code: "da", native: "Dansk", dir: "ltr"},
  {code: "de", native: "Deutsch", dir: "ltr"},
  {code: "el", native: "Ελληνικά", dir: "ltr"},
  {code: "fr", native: "Français", dir: "ltr"},
  {code: "fr-CA", native: "Français (Canada)", dir: "ltr"},
  {code: "he", native: "עברית", dir: "rtl"},
  {code: "hi", native: "हिन्दी", dir: "ltr"},
  {code: "hr", native: "Hrvatski", dir: "ltr"},
  {code: "it", native: "Italiano", dir: "ltr"},
  {code: "ja", native: "日本語", dir: "ltr"},
  {code: "ko", native: "한국어", dir: "ltr"},
  {code: "hu", native: "Magyar", dir: "ltr"},
  {code: "nl", native: "Nederlands", dir: "ltr"},
  {code: "no", native: "Norsk", dir: "ltr"},
  {code: "pl", native: "Polski", dir: "ltr"},
  {code: "pt", native: "Português", dir: "ltr"},
  {code: "pt-BR", native: "Português (Brasil)", dir: "ltr"},
  {code: "ro", native: "Română", dir: "ltr"},
  {code: "ru", native: "Русский", dir: "ltr"},
  {code: "sk", native: "Slovenčina", dir: "ltr"},
  {code: "sl", native: "Slovenščina", dir: "ltr"},
  {code: "fi", native: "Suomi", dir: "ltr"},
  {code: "sv", native: "Svenska", dir: "ltr"},
  {code: "th", native: "ไทย", dir: "ltr"},
  {code: "tr", native: "Türkçe", dir: "ltr"},
  {code: "vi", native: "Tiếng Việt", dir: "ltr"},
];
const dirOf = c => (LANGS.find(l => l.code === c) || {}).dir || "ltr";

// UI strings. Every es, ar, zh-CN and zh-TW string is a draft for a human translator.
// TODO-REVIEW: all es/ar/zh strings below (one marker per line).
// en, es, ar, zh-CN and zh-TW are inline below. Every other language's interface strings are fetched on demand
// from i18n/<code>.json into I18N (see loadLang); t() falls back to English for any missing key.
const T = {
  app_title:   {en: "BillScan", es: "BillScan", ar: "BillScan", "zh-CN": "BillScan", "zh-TW": "BillScan"}, // brand name: identical in every language
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
  err_too_big: {en: "This photo is larger than 8 MB. Take a smaller photo, or type the fields in by hand.", es: "Esta foto pesa más de 8 MB. Tome una foto más pequeña o escriba los campos a mano.", ar: "حجم هذه الصورة أكبر من 8 ميغابايت. التقط صورة أصغر أو اكتب الحقول يدويًا.", "zh-CN": "这张照片超过 8 MB。请拍一张较小的照片，或手动填写各字段。", "zh-TW": "這張照片超過 8 MB。請拍一張較小的照片，或手動填寫各欄位。"}, // TODO-REVIEW es+ar+zh
  err_type:    {en: "Upload a PNG or JPEG photo, or type the fields in by hand.", es: "Suba una foto PNG o JPEG, o escriba los campos a mano.", ar: "ارفع صورة بصيغة PNG أو JPEG، أو اكتب الحقول يدويًا.", "zh-CN": "请上传 PNG 或 JPEG 照片，或手动填写各字段。", "zh-TW": "請上傳 PNG 或 JPEG 照片，或手動填寫各欄位。"}, // TODO-REVIEW es+ar+zh
  err_busy:    {en: "Too many requests right now. Wait a minute and try again.", es: "Hay demasiadas solicitudes en este momento. Espere un minuto e inténtelo de nuevo.", ar: "هناك طلبات كثيرة الآن. انتظر دقيقة ثم حاول مرة أخرى.", "zh-CN": "目前请求过多。请等一分钟后再试。", "zh-TW": "目前請求過多。請等一分鐘後再試。"}, // TODO-REVIEW es+ar+zh
  r_policy_used:{en: "This estimate uses the policy of {name}.", es: "Esta estimación usa la política de {name}.", ar: "يستخدم هذا التقدير سياسة {name}.", "zh-CN": "此估算使用 {name} 的政策。", "zh-TW": "此估算使用 {name} 的政策。"}, // TODO-REVIEW es+ar+zh
  r_mismatch_title:{en: "Different hospital", es: "Hospital distinto", ar: "مستشفى مختلف", "zh-CN": "不同的医院", "zh-TW": "不同的醫院"}, // TODO-REVIEW es+ar+zh
  r_mismatch:  {en: "Your bill names a different hospital. This demo has only one hospital's policy, and it is synthetic, so this estimate is not about your hospital.", es: "Su factura menciona otro hospital. Esta demostración solo tiene la política de un hospital, y es sintética, así que esta estimación no corresponde a su hospital.", ar: "تذكر فاتورتك مستشفى مختلفًا. يحتوي هذا العرض التجريبي على سياسة مستشفى واحد فقط، وهي اصطناعية، لذا فإن هذا التقدير لا يخص مستشفاك.", "zh-CN": "您的账单上是另一家医院。本演示只有一家医院的政策，而且是合成的，所以此估算与您的医院无关。", "zh-TW": "您的帳單上是另一家醫院。本示範只有一家醫院的政策，而且是合成的，所以此估算與您的醫院無關。"}, // TODO-REVIEW es+ar+zh
  r_deadline_passed:{en: "This date has passed. Ask the hospital whether it will still accept your application.", es: "Esta fecha ya pasó. Pregunte al hospital si todavía aceptará su solicitud.", ar: "لقد مضى هذا التاريخ. اسأل المستشفى هل سيقبل طلبك رغم ذلك.", "zh-CN": "这个日期已经过了。请询问医院是否仍会接受您的申请。", "zh-TW": "這個日期已經過了。請詢問醫院是否仍會接受您的申請。"}, // TODO-REVIEW es+ar+zh
  income_hint: {en: "Type the amount in US dollars, like 38000 or 38,000.50.", es: "Escriba el monto en dólares de EE. UU., como 38000 o 38,000.50.", ar: "اكتب المبلغ بالدولار الأمريكي، مثل 38000 أو 38,000.50.", "zh-CN": "请用美元填写金额，例如 38000 或 38,000.50。", "zh-TW": "請用美元填寫金額，例如 38000 或 38,000.50。"}, // TODO-REVIEW es+ar+zh
  home_open:   {en: "All bills from this visit", es: "Todas las facturas de esta visita", ar: "جميع فواتير هذه الزيارة", "zh-CN": "本次就诊的所有账单", "zh-TW": "本次就診的所有帳單"}, // TODO-REVIEW es+ar+zh
  load_home:   {en: "Adding up all the bills...", es: "Sumando todas las facturas...", ar: "جارٍ جمع كل الفواتير...", "zh-CN": "正在汇总所有账单...", "zh-TW": "正在彙總所有帳單..."}, // TODO-REVIEW es+ar+zh
  home_title:  {en: "All bills from this visit", es: "Todas las facturas de esta visita", ar: "جميع فواتير هذه الزيارة", "zh-CN": "本次就诊的所有账单", "zh-TW": "本次就診的所有帳單"}, // TODO-REVIEW es+ar+zh
  home_estimate:{en: "Up to {amt} could be reduced if the hospital approves.", es: "Hasta {amt} podrían reducirse si el hospital lo aprueba.", ar: "قد يصل التخفيض إلى {amt} إذا وافق المستشفى.", "zh-CN": "如果医院批准，最多可减免 {amt}。", "zh-TW": "如果醫院核准，最多可減免 {amt}。"}, // TODO-REVIEW es+ar+zh
  home_estimate_note:{en: "Estimate. Synthetic bills. The hospital decides.", es: "Estimación. Facturas sintéticas. El hospital decide.", ar: "تقدير. فواتير اصطناعية. المستشفى هو من يقرر.", "zh-CN": "估算。合成账单。由医院决定。", "zh-TW": "估算。合成帳單。由醫院決定。"}, // TODO-REVIEW es+ar+zh
  home_not_eligible:{en: "Not eligible under this policy. Ask the hospital about a payment plan.", es: "No califica según esta política. Pregunte al hospital por un plan de pagos.", ar: "غير مؤهل بحسب هذه السياسة. اسأل المستشفى عن خطة سداد.", "zh-CN": "根据本政策不符合资格。请向医院咨询付款计划。", "zh-TW": "根據本政策不符合資格。請向醫院洽詢付款計畫。"}, // TODO-REVIEW es+ar+zh
  home_one_approval:{en: "One approval may cover all {n} bills.", es: "Una sola aprobación puede cubrir las {n} facturas.", ar: "قد تغطي موافقة واحدة جميع الفواتير الـ {n}.", "zh-CN": "一次批准可能涵盖全部 {n} 份账单。", "zh-TW": "一次核准可能涵蓋全部 {n} 份帳單。"}, // TODO-REVIEW es+ar+zh
  home_yours:  {en: "(your bill)", es: "(su factura)", ar: "(فاتورتك)", "zh-CN": "（您的账单）", "zh-TW": "（您的帳單）"}, // TODO-REVIEW es+ar+zh
  home_bill_line:{en: "{amount}, statement date {date}", es: "{amount}, fecha del estado de cuenta {date}", ar: "{amount}، تاريخ الكشف {date}", "zh-CN": "{amount}，账单日期 {date}", "zh-TW": "{amount}，帳單日期 {date}"}, // TODO-REVIEW es+ar+zh
  home_bill_deadline:{en: "Apply by {date}", es: "Presente la solicitud antes del {date}", ar: "قدّم الطلب قبل {date}", "zh-CN": "请在 {date} 前申请", "zh-TW": "請在 {date} 前申請"}, // TODO-REVIEW es+ar+zh
  home_bill_reduction:{en: "Could be reduced by up to {amount}", es: "Podría reducirse hasta {amount}", ar: "قد ينخفض بما يصل إلى {amount}", "zh-CN": "最多可减免 {amount}", "zh-TW": "最多可減免 {amount}"}, // TODO-REVIEW es+ar+zh
  rem_title:   {en: "Reminders", es: "Recordatorios", ar: "تذكيرات", "zh-CN": "提醒", "zh-TW": "提醒"}, // TODO-REVIEW es+ar+zh
  rem_apply:   {en: "Apply by {date}.", es: "Presente la solicitud antes del {date}.", ar: "قدّم الطلب قبل {date}.", "zh-CN": "请在 {date} 前申请。", "zh-TW": "請在 {date} 前申請。"}, // TODO-REVIEW es+ar+zh
  rem_follow:  {en: "30 days after you apply: if you have no decision yet, call {phone}.", es: "30 días después de presentarla: si aún no tiene una decisión, llame al {phone}.", ar: "بعد 30 يومًا من التقديم: إن لم يصلك قرار، اتصل على {phone}.", "zh-CN": "申请 30 天后：如果还没有决定，请致电 {phone}。", "zh-TW": "申請 30 天後：如果還沒有決定，請致電 {phone}。"}, // TODO-REVIEW es+ar+zh
  rem_reuse:   {en: "Another bill from this hospital? Your answers are reused while this page is open.", es: "¿Otra factura de este hospital? Sus respuestas se reutilizan mientras esta página esté abierta.", ar: "فاتورة أخرى من هذا المستشفى؟ يُعاد استخدام إجاباتك ما دامت هذه الصفحة مفتوحة.", "zh-CN": "这家医院还有其他账单？本页面打开期间，您的回答会被重复使用。", "zh-TW": "這家醫院還有其他帳單？本頁面開啟期間，您的回答會被重複使用。"}, // TODO-REVIEW es+ar+zh
  rem_ics:     {en: "Add to my calendar", es: "Agregar a mi calendario", ar: "أضف إلى تقويمي", "zh-CN": "添加到我的日历", "zh-TW": "加入我的行事曆"}, // TODO-REVIEW es+ar+zh
  ics_deadline:{en: "BillScan: apply for financial assistance by today", es: "BillScan: presente hoy, a más tardar, la solicitud de asistencia financiera", ar: "BillScan: قدّم طلب المساعدة المالية اليوم كحد أقصى", "zh-CN": "BillScan：今天是申请经济援助的最后期限", "zh-TW": "BillScan：今天是申請財務援助的最後期限"}, // TODO-REVIEW es+ar+zh
  ics_follow:  {en: "BillScan: follow up on your financial assistance application", es: "BillScan: dé seguimiento a su solicitud de asistencia financiera", ar: "BillScan: تابع طلب المساعدة المالية", "zh-CN": "BillScan：跟进您的经济援助申请", "zh-TW": "BillScan：追蹤您的財務援助申請"}, // TODO-REVIEW es+ar+zh
  chip_selected:{en: "{name} selected", es: "{name} seleccionado", ar: "تم اختيار {name}", "zh-CN": "已选择 {name}", "zh-TW": "已選擇 {name}"}, // TODO-REVIEW es+ar+zh
  qr_alt:      {en: "QR code that opens BillScan on a phone", es: "Código QR que abre BillScan en un teléfono", ar: "رمز QR يفتح BillScan على الهاتف", "zh-CN": "可在手机上打开 BillScan 的二维码", "zh-TW": "可在手機上開啟 BillScan 的 QR 碼"}, // TODO-REVIEW es+ar+zh
  qr_caption:  {en: "Scan to open on a phone", es: "Escanee para abrir en un teléfono", ar: "امسح الرمز للفتح على الهاتف", "zh-CN": "扫码即可在手机上打开", "zh-TW": "掃描即可在手機上開啟"}, // TODO-REVIEW es+ar+zh
  theme_auto:  {en: "Theme: auto", es: "Tema: automático", ar: "السمة: تلقائي", "zh-CN": "主题：自动", "zh-TW": "主題：自動"}, // TODO-REVIEW es+ar+zh
  theme_light: {en: "Theme: light", es: "Tema: claro", ar: "السمة: فاتح", "zh-CN": "主题：浅色", "zh-TW": "主題：淺色"}, // TODO-REVIEW es+ar+zh
  theme_dark:  {en: "Theme: dark", es: "Tema: oscuro", ar: "السمة: داكن", "zh-CN": "主题：深色", "zh-TW": "主題：深色"}, // TODO-REVIEW es+ar+zh
  q_minus:     {en: "One fewer person", es: "Una persona menos", ar: "شخص واحد أقل", "zh-CN": "减少一人", "zh-TW": "減少一人"}, // TODO-REVIEW es+ar+zh
  q_plus:      {en: "One more person", es: "Una persona más", ar: "شخص واحد إضافي", "zh-CN": "增加一人", "zh-TW": "增加一人"}, // TODO-REVIEW es+ar+zh
  why_bill:    {en: "Confirm {n} more field(s) to continue", es: "Confirme {n} campo(s) más para continuar", ar: "أكّد {n} حقل (حقول) إضافية للمتابعة", "zh-CN": "还需确认 {n} 个字段才能继续", "zh-TW": "還需確認 {n} 個欄位才能繼續"}, // TODO-REVIEW es+ar+zh
  why_q:       {en: "Answer all three questions to continue", es: "Responda las tres preguntas para continuar", ar: "أجب عن الأسئلة الثلاثة للمتابعة", "zh-CN": "请回答全部三个问题后继续", "zh-TW": "請回答全部三個問題後繼續"}, // TODO-REVIEW es+ar+zh
  restart_q:   {en: "Start over? Your answers on this page will be cleared.", es: "¿Empezar de nuevo? Se borrarán sus respuestas en esta página.", ar: "هل تريد البدء من جديد؟ سيتم مسح إجاباتك في هذه الصفحة.", "zh-CN": "重新开始？此页面上的回答将被清除。", "zh-TW": "重新開始？此頁面上的回答將被清除。"}, // TODO-REVIEW es+ar+zh
  retry:       {en: "Try again", es: "Intentar de nuevo", ar: "حاول مرة أخرى", "zh-CN": "重试", "zh-TW": "重試"}, // TODO-REVIEW es+ar+zh
  confirmed_word:{en: "Confirmed", es: "Confirmado", ar: "تم التأكيد", "zh-CN": "已确认", "zh-TW": "已確認"}, // TODO-REVIEW es+ar+zh
  machine_note:{en: "Machine translated by Oracle AI. The English line under important text is what counts.", es: "Traducido automáticamente por Oracle AI. Lo que cuenta es la línea en inglés bajo los textos importantes.", ar: "تمت الترجمة آليًا بواسطة Oracle AI. المعتمد هو السطر الإنجليزي أسفل النصوص المهمة.", "zh-CN": "由 Oracle AI 机器翻译。以重要文字下方的英文为准。", "zh-TW": "由 Oracle AI 機器翻譯。以重要文字下方的英文為準。"}, // TODO-REVIEW es+ar+zh
  steps_label: {en: "Progress", es: "Progreso", ar: "التقدّم", "zh-CN": "进度", "zh-TW": "進度"}, // TODO-REVIEW es+ar+zh
};
const LANG_NAMES = Object.fromEntries(LANGS.map(l => [l.code, l.native]));
const I18N = {}; // other languages' interface strings, fetched on demand from i18n/<code>.json
const FIELD_ORDER = [
  ["hospital_name", "f_hospital"], ["statement_date", "f_statement"], ["account_number", "f_account"],
  ["amount_due_cents", "f_amount"], ["date_of_service", "f_service"], ["insurance_status", "f_insurance"],
];
const REQUIRED = new Set(["statement_date", "amount_due_cents"]); // the engine needs these two

const S = {lang: "en", view: "en", forWhom: "self", bill: null, imageUrl: null, answers: null,
          result: null, explain: null, size: "", income: "", tax: null, busy: false, extractSeq: 0, submitSeq: 0,
          home: null, homeSeq: 0, fromQr: false,
          extracting: false, packetSeq: 0, theme: "auto"}; // theme is in page memory only and survives restart()
let firstShow = true, curScreen = 0;

// ---------- helpers
// Fetch one language's interface strings. The five inline languages need no fetch. Returns false on any failure.
async function loadLang(code) {
  if (T.app_title[code] !== undefined || I18N[code]) return true;
  try {
    const r = await fetch("i18n/" + code + ".json");
    if (!r.ok) return false;
    I18N[code] = await r.json();
    return true;
  } catch (e) {
    return false;
  }
}
// The language the interface is drawn in: the picked one when its strings are available (inline or fetched), else English.
function viewFor(lang) { return (I18N[lang] || T.app_title[lang] !== undefined) ? lang : "en"; }
// True when the interface is drawn in a machine-translated language (strings fetched from i18n/<code>.json, not inline).
function isMachineView() { return !!I18N[S.view] && T.app_title[S.view] === undefined; }
function t(key, vars) {
  const row = T[key];
  let s = (row && row[S.view]) || (I18N[S.view] && I18N[S.view][key]) || (row && row.en) || key;
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
function spinner() { return el("span", {class: "spin", "aria-hidden": "true"}); }
function applyTheme() { // auto follows the phone; light and dark force a theme. In memory only.
  if (S.theme === "auto") document.documentElement.removeAttribute("data-theme");
  else document.documentElement.setAttribute("data-theme", S.theme);
  const b = document.getElementById("theme-btn");
  b.textContent = t("theme_" + S.theme);
  b.setAttribute("aria-label", t("theme_" + S.theme));
}
function applyDir() {
  document.documentElement.lang = S.view;
  document.documentElement.dir = dirOf(S.view);
  document.getElementById("app-title").textContent = t("app_title");
  document.getElementById("stepper").setAttribute("aria-label", t("steps_label"));
  applyTheme();
}
// Errors go to #alert (role=alert); progress and info go to #status (polite). Each call clears the other.
function showMsg(text, info) {
  const st = document.getElementById("status"), al = document.getElementById("alert");
  fill(st); fill(al); // fill() is the only place replaceChildren() is called
  st.hidden = true; al.hidden = true;
  if (!text) return;
  const box = info ? st : al;
  box.textContent = text;
  box.hidden = false;
}
function showBusy(text) { // a named loading step: spinner plus words in #status
  showMsg("");
  const st = document.getElementById("status");
  fill(st, spinner(), text);
  st.hidden = false;
}
// A heading block: h2 (focus target on screen change) plus an optional sub line.
function screenTitle(text, sub) { // sub: a string or an array of nodes
  return el("div", {class: "stack-3"}, el("h2", {tabindex: "-1"}, text), sub ? el("p", {class: "sub"}, ...[].concat(sub)) : null);
}
function panel(cls, ...kids) { // cls: "" or "warn" | "ok" | "hero"
  return el("section", {class: ("panel " + (cls || "")).trim()}, ...kids);
}
function optionButton(label, pressed, onclick, attrs) { // a toggle choice: dot + words, state also in aria-pressed
  return el("button", Object.assign({type: "button", class: "opt", "aria-pressed": String(!!pressed), onclick}, attrs || {}),
    el("span", {class: "dot", "aria-hidden": "true"}), el("span", null, label));
}
function actions(secondary, primary) { // secondary: array of nodes; primary may be null
  return el("div", {class: "actions"}, el("div", {class: "act-sec"}, ...secondary), primary);
}
function setBusy(btn, on) { // spinner before the label, button disabled while its request runs
  if (!btn) return;
  btn.classList.toggle("busy", on);
  btn.disabled = on;
  if (on) btn.setAttribute("aria-busy", "true"); else btn.removeAttribute("aria-busy");
  const sp = btn.querySelector(":scope > .spin");
  if (on && !sp) btn.prepend(spinner());
  else if (!on && sp) sp.remove();
}
function restartAsk() { // every Start over button: confirm first, then clear everything
  if (!confirm(t("restart_q"))) return;
  restart();
}
function ghostRestart() { return el("button", {type: "button", class: "ghost", onclick: restartAsk}, t("restart")); }
// Re-render and put focus back on the control that had it (matched by id), so a re-render does not drop the keyboard user.
function keepFocus(render) {
  const a = document.activeElement, id = a && a.id;
  render();
  const e = id ? document.getElementById(id) : null;
  if (e && !e.disabled) e.focus({preventScroll: true});
}
function show(n) {
  if (n !== 4) { // leaving the questions cancels an in-flight submit
    S.submitSeq = (S.submitSeq || 0) + 1;
    if (S.busy) showMsg("");
    S.busy = false;
  }
  const changed = n !== curScreen;
  const keepId = !changed && document.activeElement ? document.activeElement.id : ""; // same-screen re-render keeps focus
  curScreen = n;
  if (changed) showMsg(""); // a message belongs to the screen that raised it; the new screen shows what it needs
  document.getElementById("main").className = (n === 1 || n === 3) ? "w-narrow" : "w-wide";
  for (let i = 1; i <= 6; i++) document.getElementById("s" + i).hidden = i !== n;
  applyDir();
  const chrome = n !== 6; // the Home screen is not one of the five steps
  document.getElementById("stepper").hidden = !chrome;
  document.getElementById("steps").hidden = !chrome;
  document.getElementById("step-cap").hidden = !chrome;
  if (chrome) renderSteps(n);
  document.getElementById("foot").textContent = t("not_affiliated");
  [null, renderStart, renderBill, renderQuestions, renderResult, renderPacketShell, renderHome][n]();
  if (!firstShow && changed) { // move focus to the new screen's heading so keyboard and screen-reader users land on it
    const h = document.querySelector("#s" + n + " h2");
    if (h) { h.setAttribute("tabindex", "-1"); h.focus(); }
  } else if (keepId) {
    const e = document.getElementById(keepId);
    if (e && !e.disabled) e.focus({preventScroll: true});
  }
  firstShow = false;
}
async function post(path, body, asText) {
  let r;
  try {
    r = await fetch(path, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)});
  } catch (e) { throw new Error(t("err_generic")); }
  if (!r.ok) {
    if (r.status === 429) throw new Error(t("err_busy"));
    let detail = "";
    try {
      const j = await r.json();
      // a 422 detail is English server text: outside English show the translated generic line instead
      detail = (typeof j.detail === "string" && !(r.status === 422 && S.view !== "en")) ? j.detail : t("err_invalid");
    } catch (e) { /* ignore */ }
    throw new Error(detail || t("err_generic"));
  }
  try { return await (asText ? r.text() : r.json()); } // a 200 that is not JSON (captive portal page) must not show a parser error
  catch (e) { throw new Error(t("err_generic")); }
}
// "4812.40" or "$4,812.4" -> 481240 ; invalid -> null. String math, no floats.
function dollarsToCents(s) {
  const norm = (s || "")
    .replace(/[\u0660-\u0669]/g, d => String(d.charCodeAt(0) - 0x0660)) // Arabic-Indic digits
    .replace(/[\u06F0-\u06F9]/g, d => String(d.charCodeAt(0) - 0x06F0)) // Eastern Arabic-Indic digits
    .replace(/[\uFF10-\uFF19]/g, d => String(d.charCodeAt(0) - 0xFF10)) // fullwidth digits
    .replace(/\u066C/g, ",").replace(/\u066B/g, "."); // Arabic thousands and decimal separators
  const m = /^\$?\s*(\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d{1,2}))?$/.exec(norm.trim());
  if (!m) return null;
  const cents = parseInt(m[1].replace(/,/g, ""), 10) * 100 + parseInt((m[2] || "0").padEnd(2, "0"), 10);
  return cents > Number.MAX_SAFE_INTEGER ? null : cents;
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
function tNodes(key, vars) { return tplNodes(t(key), vars); }
// Safety lines (estimate, the hospital decides, nothing saved, no ID asked) in a machine-translated
// language also show the English line under the translation: Oracle's translation changed their
// meaning in some languages (back-translation check 2026-10-17), and the English is what counts.
const SAFETY_KEYS = ["notice", "no_id", "r_decides", "p_sub", "ai_note", "r_mismatch", "home_estimate",
                     "home_estimate_note", "home_one_approval", "home_bill_reduction",
                     "r_packet", "r_no_packet", "home_not_eligible", "rem_follow",
                     "rem_apply", "home_bill_deadline", "r_deadline_passed"];
function machineTranslated(key) {
  return S.view !== "en" && !(T[key] && T[key][S.view]) && !!(I18N[S.view] && I18N[S.view][key]);
}
function tSafe(key, vars) {
  const nodes = tNodes(key, vars);
  if (!SAFETY_KEYS.includes(key) || !machineTranslated(key)) return nodes;
  return [...nodes, el("span", {class: "en-gloss", lang: "en", dir: "ltr"}, ...tplNodes(T[key].en, vars))];
}
function tplNodes(tpl, vars) {
  const out = [];
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
function makeNotes(prefix) { // prefix keeps the anchor ids unique: the Result and Home screens both stay in the DOM
  const items = [], index = new Map(), pre = prefix || "fn";
  return {
    mark(c) {
      if (!c || !c.source) return null;
      const key = [c.source, c.page, c.effective_date].join("|");
      if (!index.has(key)) { items.push(c); index.set(key, items.length); }
      const n = index.get(key);
      return el("sup", {class: "fn-mark"}, el("a", {href: "#" + pre + "-" + n}, el("bdi", {dir: "ltr"}, "[" + n + "]")));
    },
    list() {
      if (!items.length) return null;
      return el("ol", {class: "notes", role: "list", "aria-label": t("src")}, ...items.map((c, i) => {
        const row = [el("span", {class: "fn-num", dir: "ltr"}, "[" + (i + 1) + "]"), el("span", {class: "fn-text"}, ...citeParts(c))];
        return el("li", {id: pre + "-" + (i + 1)}, c.url
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
      el("span", {class: "bar"}),
      el("span", {class: "lbl", "aria-hidden": "true"}, i + ". " + t("step_" + i)),
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
let langPick = 0;
function langSelect() { // one native dropdown with all languages, each named in its own language
  const sel = el("select", {id: "lang-select"}, ...LANGS.map(l =>
    el("option", {value: l.code, lang: l.code, dir: l.dir, selected: l.code === S.lang}, LANG_NAMES[l.code])));
  sel.addEventListener("change", async () => {
    const code = sel.value, mine = ++langPick; // a newer pick cancels this one (focus stays on the select)
    const ok = await loadLang(code);
    if (mine !== langPick) return;
    S.lang = code; S.view = ok ? code : "en";
    if (curScreen !== 1) { applyDir(); return; } // a slow load finished after the user moved on: switch the language, not the screen
    if (!ok) showMsg(t("err_generic"));
    show(1);
  });
  return sel;
}
// Desktop only: a QR code that opens this page on a phone with the hospital preselected. Any failure draws nothing.
function qrFigure() {
  try {
    if (typeof qrcode !== "function" || !window.matchMedia("(min-width: 900px)").matches) return null;
    const q = qrcode(0, "M");
    q.addData(location.origin + "/?hospital=cumberland_synthetic");
    q.make();
    return el("figure", {class: "qr"},
      el("img", {src: q.createDataURL(4, 2), alt: t("qr_alt"), width: "164", height: "164"}),
      el("figcaption", null, t("qr_caption")));
  } catch (e) {
    return null;
  }
}
function renderStart() {
  const root = document.getElementById("s1");
  const title = screenTitle(t("pick_lang"), tSafe("no_id"));
  title.querySelector("h2").id = "pick-lang-label";
  const qr = qrFigure();
  fill(root, el("div", {class: "stack-8"},
    title,
    S.fromQr ? el("p", {class: "chip"}, ...tNodes("chip_selected", {name: "Cumberland General Hospital (SYNTHETIC)"})) : null,
    el("p", {class: "notice"}, ...tSafe("notice")),
    el("div", {class: "stack-3"},
      el("label", {for: "lang-select", class: "sr-only"}, t("pick_lang")),
      langSelect(),
      isMachineView() ? el("p", {class: "muted"}, t("machine_note")) : null),
    el("div", {class: "stack-3"},
      el("h3", {id: "for-whom-label"}, t("for_whom")),
      el("div", {class: "grid-2", role: "group", "aria-labelledby": "for-whom-label"}, ...[["self", "me", "who-me"], ["family", "family", "who-family"]].map(([v, k, id]) =>
        optionButton(t(k), S.forWhom === v, () => { S.forWhom = v; show(1); }, {id})))),
    actions([], el("button", {type: "button", class: "primary", id: "start-btn", onclick: () => { showMsg(""); show(2); }}, t("start"))),
    qr ? panel("", qr) : null,
  ));
}

// ---------- screen 2: bill
function renderBill() {
  const root = document.getElementById("s2");
  const file = el("input", {type: "file", accept: "image/png,image/jpeg", id: "bill-file", class: "sr-only", disabled: S.extracting});
  file.addEventListener("change", onFile);
  const drop = el("label", {class: "drop", "aria-disabled": S.extracting ? "true" : false},
    icon("camera"), el("span", null, t("upload")), el("small", {lang: "en", dir: "ltr"}, "PNG / JPEG"), file);
  const left = el("div", {class: "stack-3"}, drop, S.imageUrl ? el("img", {class: "preview", src: S.imageUrl, alt: ""}) : null);
  const right = el("div", {id: "fields", class: "stack-3"});
  fill(root, el("div", {class: "stack-8"},
    screenTitle(t("bill_title"), t("bill_hint")),
    el("div", {class: "bill-grid"}, left, right),
    el("div", {class: "stack-3"},
      actions([el("button", {type: "button", onclick: () => show(1)}, t("back"))],
        el("button", {type: "button", class: "primary", id: "bill-next", disabled: true, onclick: () => show(3)}, t("continue_"))),
      el("p", {class: "why", id: "bill-why", hidden: true}))));
  if (S.extracting) showBusy(t("reading")); // a re-render while the photo is still being read keeps the spinner
  if (S.bill) renderFields();
  updateBillNext();
}
// Continue is enabled only when a bill exists and every field is confirmed; p.why says what is missing.
function updateBillNext() {
  const next = document.getElementById("bill-next"), why = document.getElementById("bill-why");
  if (!next || !why) return;
  const left = S.bill ? FIELD_ORDER.filter(([n]) => !S.bill.fields[n].confirmed).length : FIELD_ORDER.length;
  next.disabled = S.extracting || !S.bill || left > 0;
  why.hidden = !next.disabled || S.extracting;
  if (why.hidden) fill(why);
  else fill(why, ...(S.bill ? tNodes("why_bill", {n: left}) : [t("upload")]));
}
// Downscale big photos in the browser (long side 2000 px, JPEG 0.85) so phone photos fit the upload cap.
// Any failure returns the original file; the server then accepts or refuses it as before.
async function shrinkImage(file) {
  const small = (file.type === "image/png" || file.type === "image/jpeg") && file.size <= 2 * 1024 * 1024;
  try {
    const bmp = await createImageBitmap(file, {imageOrientation: "from-image"});
    const long = Math.max(bmp.width, bmp.height);
    if (small && long <= 2000) { bmp.close(); return file; }
    const scale = Math.min(1, 2000 / long);
    const cw = Math.round(bmp.width * scale), ch = Math.round(bmp.height * scale);
    const canvas = document.createElement("canvas");
    canvas.width = cw; canvas.height = ch;
    canvas.getContext("2d").drawImage(bmp, 0, 0, cw, ch);
    bmp.close();
    const blob = await new Promise(r => canvas.toBlob(r, "image/jpeg", 0.85));
    if (!blob) return file;
    return new File([blob], "bill.jpg", {type: "image/jpeg"});
  } catch (e) {
    return file;
  }
}
async function onFile(ev) {
  const f = ev.target.files[0];
  if (!f) return;
  const seq = (S.extractSeq = (S.extractSeq || 0) + 1); // a newer upload makes this one stale
  if (S.imageUrl) URL.revokeObjectURL(S.imageUrl);
  S.imageUrl = URL.createObjectURL(f);
  S.bill = null; S.home = null; // a new photo makes the all-bills totals stale
  S.extracting = true; // the file input and Continue stay disabled until the latest read finishes
  renderBill(); // shows the "Reading the bill..." status while S.extracting
  const upload = await shrinkImage(f);
  if (seq !== S.extractSeq) return;
  const fd = new FormData();
  fd.append("file", upload);
  let failMsg = t("read_failed");
  try {
    const r = await fetch("/extract", {method: "POST", body: fd});
    if (seq !== S.extractSeq) return;
    if (!r.ok) {
      if (r.status === 413) failMsg = t("err_too_big");
      else if (r.status === 415) failMsg = t("err_type");
      else if (r.status === 429) failMsg = t("err_busy");
      throw new Error("extract");
    }
    const bill = await r.json();
    if (seq !== S.extractSeq) return;
    S.bill = bill;
    if (curScreen === 2) showMsg(""); // the message box belongs to the screen the user is on
  } catch (e) {
    if (seq !== S.extractSeq) return;
    S.bill = blankBill();
    if (curScreen === 2) showMsg(failMsg);
  }
  S.extracting = false;
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
    const hint = el("p", {class: "hint", id: id + "-hint"});
    const ok = el("span", {class: "state-ok", "aria-hidden": "true"});
    input.setAttribute("aria-describedby", id + "-hint");
    const wrap = el("div", {class: "field panel"},
      el("label", {for: id}, t(labelKey) + (REQUIRED.has(name) ? " *" : "")), input, hint,
      el("label", {class: "check", for: id + "-ok"}, cb, el("span", null, t("confirm"))), ok);
    const sync = () => {
      const blank = f.value === null || f.value === "";
      hint.textContent = blank ? t("unreadable") + (REQUIRED.has(name) ? " (" + t("required") + ")" : "") : "";
      hint.hidden = !hint.textContent;
      ok.textContent = f.confirmed ? t("confirmed_word") : "";
      ok.hidden = !f.confirmed;
      cb.disabled = blank && REQUIRED.has(name);
      cb.checked = f.confirmed;
      wrap.className = "field panel" + (f.confirmed ? " confirmed" : blank ? " blank" : "");
      updateBillNext();
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
  const minus = el("button", {type: "button", class: "sq", id: "q-minus", "aria-label": t("q_minus")}, "\u2212");
  const plus = el("button", {type: "button", class: "sq", id: "q-plus", "aria-label": t("q_plus")}, "+");
  const income = el("input", {type: "text", id: "q-income", inputmode: "decimal", value: S.income, autocomplete: "off", "aria-describedby": "q-income-hint"});
  const incomeHint = el("p", {class: "hint", id: "q-income-hint"});
  const go = el("button", {type: "button", class: "primary", id: "q-go", onclick: submitAnswers}, t("see_result"));
  const why = el("p", {class: "why", id: "q-why"}, t("why_q"));
  const sizeNow = () => { // the household size as typed: an integer, or 0 when empty or not a number
    const n = Number(size.value);
    return size.value.trim() !== "" && Number.isFinite(n) ? Math.trunc(n) : 0;
  };
  const check = () => {
    S.size = size.value; S.income = income.value;
    incomeHint.textContent = (S.income.trim() !== "" && dollarsToCents(S.income) === null) ? t("income_hint") : "";
    incomeHint.hidden = !incomeHint.textContent;
    const n = Number(S.size);
    const wasMinus = document.activeElement === minus, wasPlus = document.activeElement === plus;
    minus.disabled = !(sizeNow() > 1);
    plus.disabled = sizeNow() >= 12;
    if (wasMinus && minus.disabled && !plus.disabled) plus.focus({preventScroll: true}); // keep the keyboard user on a live button
    if (wasPlus && plus.disabled && !minus.disabled) minus.focus({preventScroll: true});
    go.disabled = S.busy || !(Number.isInteger(n) && n >= 1 && n <= 12) || dollarsToCents(S.income) === null || S.tax === null;
    why.hidden = !go.disabled || S.busy;
  };
  const step = d => { size.value = String(Math.min(12, Math.max(1, sizeNow() + d))); check(); };
  minus.addEventListener("click", () => step(-1));
  plus.addEventListener("click", () => step(1));
  size.addEventListener("input", check);
  income.addEventListener("input", check);
  const taxBtn = (val, key, id) => optionButton(t(key), S.tax === val, () => { S.tax = val; keepFocus(renderQuestions); }, {id});
  fill(root, el("div", {class: "stack-8"},
    screenTitle(t("q_title"), tSafe("no_id")),
    el("div", {class: "stack-3"}, el("label", {for: "q-size"}, t("q_size")), el("div", {class: "num-step", dir: "ltr"}, minus, size, plus)),
    el("div", {class: "stack-3"}, el("label", {for: "q-income"}, t("q_income")),
      el("div", {class: "money-in", dir: "ltr"}, el("span", {"aria-hidden": "true"}, "$"), income), incomeHint),
    el("div", {class: "stack-3"}, el("h3", {id: "q-tax-label"}, t("q_tax")),
      el("div", {class: "grid-2", role: "group", "aria-labelledby": "q-tax-label"}, taxBtn(true, "yes", "tax-yes"), taxBtn(false, "no", "tax-no"))),
    el("div", {class: "stack-3"}, actions([el("button", {type: "button", onclick: () => show(2)}, t("back"))], go), why)));
  check();
  if (S.busy) setBusy(go, true);
}
async function submitAnswers() {
  const seq = (S.submitSeq = (S.submitSeq || 0) + 1); // Back or restart bumps S.submitSeq and cancels this submit
  S.answers = {contract_version: 1, language: S.lang, for_whom: S.forWhom, household_size: Number(S.size),
               annual_income_cents: dollarsToCents(S.income), files_tax_return: S.tax};
  S.busy = true; showBusy(t("load_evaluate"));
  setBusy(document.getElementById("q-go"), true);
  document.getElementById("q-why").hidden = true;
  try {
    const result = await post("/evaluate", {bill: S.bill, answers: S.answers});
    if (seq !== S.submitSeq) return;
    showBusy(t("load_explain"));
    const explain = await post("/explain", {bill: S.bill, answers: S.answers, result});
    if (seq !== S.submitSeq) return; // checked BEFORE the assignments: a cancelled submit must not overwrite a newer result
    S.result = result; S.explain = explain;
  } catch (e) {
    if (seq !== S.submitSeq) return;
    S.busy = false; showMsg(e.message); renderQuestions();
    return;
  }
  S.view = viewFor(S.lang); showMsg(""); S.home = null; // new answers: recompute the all-bills totals
  S.busy = false; show(4);
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
function phoneLink(p) { return el("bdi", {lang: "en", dir: "ltr"}, el("a", {href: "tel:" + String(p).replace(/[^\d+]/g, "")}, p)); }
function renderResult() {
  const r = S.result, root = document.getElementById("s4");
  const english = S.view === "en";
  const fb = S.explain.fallback_used;
  // One view at a time: the translated text, or English (the toggle, or when the number check failed).
  const showEn = english || fb;
  const showNative = S.lang !== "en" && !fb && !english;
  const enLines = showEn ? S.explain.text_en.split("\n") : [];
  const nativeLines = showNative ? S.explain.text.split("\n") : [];
  const nativeDir = dirOf(S.lang);
  const eligible = r.tier.eligible;
  // Footnote markers are numbered in the order they are created, so build the page top to bottom.
  const notes = makeNotes();
  const hero = panel("hero",
    el("div", {class: "hero-row"},
      typeof r.percent_of_fpl === "number" ? el("span", {class: "pct", dir: "ltr"}, r.percent_of_fpl + "%") : null,
      el("p", {class: "lead"}, ...tNodes("r_percent", {pct: r.percent_of_fpl, year: r.fpl.year}), notes.mark(r.fpl.citation))),
    el("p", {class: "decides"}, ...tSafe("r_decides")));
  const policyUsed = typeof r.policy_hospital_name === "string" ? el("p", {class: "muted"}, ...tNodes("r_policy_used", {name: r.policy_hospital_name})) : null;
  const mismatch = r.hospital_matches_policy === false
    ? panel("warn", el("h3", null, t("r_mismatch_title")), el("p", null, ...tSafe("r_mismatch")))
    : null;
  if (mismatch) mismatch.setAttribute("role", "note");
  const tierBlock = Array.isArray(r.tiers) && r.tiers.length
    ? [el("p", {class: "excerpt-head"}, t("r_tier")), el("div", {class: "tbl"}, tierTable(r))]
    : [panel("", el("h3", null, t("r_tier")), englishOnly("p", {class: "stat"}, r.tier.label_en))];
  const tierNote = el("p", {class: "muted tbl-note"}, t("r_policy_en"), notes.mark(r.tier.citation));
  const now = new Date();
  const today = now.getFullYear() + "-" + String(now.getMonth() + 1).padStart(2, "0") + "-" + String(now.getDate()).padStart(2, "0");
  const deadline = panel("warn", el("h3", {class: "with-icon"}, icon("calendar"), t("r_deadline")),
    el("p", {lang: "en", dir: "ltr"}, deadlineLine(r.deadline), notes.mark(r.deadline.citation)),
    r.deadline.date < today ? el("p", {class: "warn-text"}, ...tSafe("r_deadline_passed")) : null);
  const explain = panel("explain", el("h3", null, t("r_about")),
    ...enLines.map(l => el("p", {dir: "ltr", lang: "en"}, l)),
    ...nativeLines.map(l => el("p", {dir: nativeDir, lang: S.lang}, ...isolate(l))));
  const docs = el("ol", {class: "docs"}, ...r.documents.map(d => el("li", null, el("span", {lang: "en", dir: "ltr"}, d.label_en, notes.mark(d.citation)))));
  const docsPanel = eligible ? panel("", el("h3", {class: "with-icon"}, icon("file"), t("r_docs")), docs) : null;
  const c = r.contacts;
  const contactPanel = eligible
    ? panel("", el("h3", null, t("r_contact"), notes.mark(c.citation)),
        el("dl", {class: "kv"},
          el("dt", null, t("r_email")), el("dd", null, el("bdi", {lang: "en", dir: "ltr"}, el("a", {href: "mailto:" + c.email}, c.email))),
          el("dt", null, t("r_phone")), el("dd", null, phoneLink(c.phone))))
    : panel("", el("h3", null, t("r_payplan"), notes.mark(c.citation)),
        el("dl", {class: "kv"}, el("dt", null, t("r_phone")), el("dd", null, phoneLink(c.payment_plan_phone || c.phone))));
  const toggle = S.lang === "en" ? null
    : el("button", {type: "button", id: "r-toggle", onclick: () => { S.view = english ? S.lang : "en"; show(4); }}, english ? t("r_see_native") : t("r_see_en"));
  fill(root, el("div", {class: "stack-8"},
    screenTitle(t("r_title")),
    toggle,
    hero,
    policyUsed,
    mismatch,
    el("div", {class: "stack-3"}, ...tierBlock, tierNote),
    eligible ? deadline : null,
    explain,
    showNative ? el("p", {class: "muted"}, ...tSafe("ai_note")) : null,
    fb && !english ? el("p", {class: "muted"}, t("r_fallback")) : null,
    el("div", {class: "grid-md-2"}, docsPanel, contactPanel),
    eligible ? null : el("p", null, ...tSafe("r_no_packet")),
    notes.list(),
    actions([
      el("button", {type: "button", onclick: () => show(3)}, t("back")),
      el("button", {type: "button", onclick: () => show(6)}, t("home_open")),
      ghostRestart()],
      eligible ? el("button", {type: "button", class: "primary", onclick: () => { show(5); loadPacket(); }}, el("span", null, ...tSafe("r_packet"))) : null)));
}

// ---------- screen 6: home (all bills from this visit)
function money(cents) { // 481240 -> "$4,812.40"; integer math only
  const dollars = Math.floor(cents / 100), rest = cents % 100;
  return "$" + String(dollars).replace(/\B(?=(\d{3})+(?!\d))/g, ",") + "." + String(rest).padStart(2, "0");
}
function icsText(s) { // RFC 5545 TEXT escaping
  return String(s).replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\r\n|\r|\n/g, "\\n");
}
function utcStamp(d) { // YYYYMMDDTHHMMSSZ
  return d.toISOString().replace(/[-:]/g, "").replace(/\.\d+Z$/, "Z");
}
// RFC 5545 line folding: at most 75 octets (UTF-8 bytes) per line, never inside a character; each continuation starts with one space.
function foldLine(line) {
  const out = [];
  let cur = "", n = 0, limit = 75;
  for (const ch of line) { // iterates code points, so a surrogate pair is never split
    const cp = ch.codePointAt(0);
    const bytes = cp < 0x80 ? 1 : cp < 0x800 ? 2 : cp < 0x10000 ? 3 : 4;
    if (n + bytes > limit) { out.push(cur); cur = ""; n = 0; limit = 74; } // the leading space counts toward 75
    cur += ch; n += bytes;
  }
  out.push(cur);
  return out.join("\r\n ");
}
// events: [{date: "YYYYMMDD", summary: text}] -> iCalendar text, CRLF line endings (pure: easy to test)
function buildIcs(events, now) {
  const lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//BillScan//Demo//EN"];
  events.forEach((ev, i) => {
    const uid = (typeof crypto !== "undefined" && crypto.randomUUID) ? crypto.randomUUID() : Date.now() + "-" + i;
    lines.push("BEGIN:VEVENT", "UID:" + uid + "@billscan.demo", "DTSTAMP:" + utcStamp(now),
      "DTSTART;VALUE=DATE:" + ev.date, "SUMMARY:" + icsText(ev.summary), "END:VEVENT");
  });
  lines.push("END:VCALENDAR");
  return lines.map(foldLine).join("\r\n") + "\r\n";
}
function downloadIcs(h) {
  const now = new Date();
  const later = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 30); // the user's local today + 30 days
  const ymd = later.getFullYear() + String(later.getMonth() + 1).padStart(2, "0") + String(later.getDate()).padStart(2, "0");
  const ics = buildIcs([
    {date: h.earliest_deadline.date.replace(/-/g, ""), summary: t("ics_deadline")},
    {date: ymd, summary: t("ics_follow")},
  ], now);
  const url = URL.createObjectURL(new Blob([ics], {type: "text/calendar"}));
  const a = el("a", {href: url, download: "billscan-reminders.ics"});
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000); // a moment later, so the download has started
}
function homeActions(primary) { // Back to the result, Start over; primary is the Retry button on a load error, else none
  return actions([
    el("button", {type: "button", onclick: () => { showMsg(""); show(4); }}, t("back")),
    ghostRestart()], primary || null);
}
function renderHome() {
  const root = document.getElementById("s6");
  const h = S.home;
  if (!h) {
    fill(root, el("div", {class: "stack-8"}, screenTitle(t("home_title")), homeActions()));
    showBusy(t("load_home"));
    const seq = (S.homeSeq = (S.homeSeq || 0) + 1);
    post("/household", {answers: S.answers, bill: S.bill}).then(result => {
      if (seq !== S.homeSeq || curScreen !== 6) return;
      S.home = result; showMsg(""); renderHome();
    }, e => {
      if (seq !== S.homeSeq || curScreen !== 6) return;
      showMsg(e.message);
      fill(root, el("div", {class: "stack-8"}, screenTitle(t("home_title")),
        homeActions(el("button", {type: "button", class: "primary", id: "home-retry", onclick: renderHome}, t("retry")))));
    });
    return;
  }
  const notes = makeNotes("home-fn"); // own anchor ids: the Result screen's notes stay in the DOM too
  const eligible = h.eligible === true; // not eligible: no covers panel, no "Apply by", no reminders, no calendar file
  const noneCounted = h.bills.length > 0 && h.bills.every(b => b.hospital_matches_policy === false);
  const headline = eligible && noneCounted
    ? panel("warn", el("h3", null, t("r_mismatch_title")), el("p", null, ...tSafe("r_mismatch")))
    : eligible
    ? panel("hero",
        el("p", {class: "big-money", dir: "ltr"}, money(h.estimate_cents)),
        el("p", {class: "lead"}, ...tSafe("home_estimate", {amt: money(h.estimate_cents)})),
        el("p", {class: "muted"}, ...tSafe("home_estimate_note")))
    : panel("hero", el("p", {class: "lead"}, ...tSafe("home_not_eligible")));
  const covers = eligible && h.one_application_covers_all
    ? panel("ok",
        el("p", null, ...tSafe("home_one_approval", {n: h.bills.length}), notes.mark(h.coverage.citation)),
        englishOnly("p", {class: "muted"}, h.coverage.text_en))
    : null;
  const bills = el("ul", {class: "plain bills"}, ...h.bills.map(b => {
    const other = b.hospital_matches_policy === false; // null = unknown: no warning
    return el("li", {class: "panel"},
    el("div", {class: "bill-top"},
      el("div", null,
        el("p", null, englishOnly("strong", null, b.label_en), b.source === "yours" ? " " + t("home_yours") : null),
        el("p", {class: "muted"}, t("f_statement") + ": ", bdiEn(b.statement_date))),
      el("span", {class: "bill-amt", dir: "ltr"}, money(b.amount_due_cents))),
    other ? el("p", {class: "bill-warn", role: "note"}, t("r_mismatch_title")) : null,
    // another hospital's bill: this policy's deadline and reduction do not apply to it
    eligible && !other ? el("p", {class: "bill-meta"}, ...tSafe("home_bill_deadline", {date: b.deadline.date}),
      " ", ...tSafe("home_bill_reduction", {amount: money(b.reduction_cents)})) : null);
  }));
  const c = h.contacts;
  const payPlan = eligible ? null : panel("",
    el("h3", null, t("r_payplan"), notes.mark(c.citation)),
    el("dl", {class: "kv"}, el("dt", null, t("r_phone")), el("dd", null, phoneLink(c.payment_plan_phone || c.phone))));
  const reminders = !eligible ? null : panel("",
    el("h3", null, t("rem_title")),
    el("p", null, ...tSafe("rem_apply", {date: h.earliest_deadline.date})),
    el("p", null, ...tSafe("rem_follow", {phone: h.contacts.phone})),
    el("p", null, t("rem_reuse")),
    el("div", null, el("button", {type: "button", onclick: () => downloadIcs(h)}, t("rem_ics"))));
  fill(root, el("div", {class: "stack-8"},
    screenTitle(t("home_title")),
    headline,
    covers,
    bills,
    reminders,
    payPlan,
    notes.list(),
    homeActions()));
}

// ---------- screen 5: packet
function packetSkeleton() { return el("div", {class: "skeleton", "aria-hidden": "true"}); }
function renderPacketShell() {
  fill(document.getElementById("s5"), el("div", {class: "stack-8"},
    screenTitle(t("p_title"), tSafe("p_sub")),
    el("div", {class: "paper", id: "packet-paper"}, packetSkeleton()),
    actions([
      el("button", {type: "button", onclick: () => show(4)}, t("back")),
      ghostRestart()],
      el("button", {type: "button", class: "primary", id: "print-btn", disabled: true, onclick: () => document.getElementById("packet-frame").contentWindow.print()}, icon("printer"), t("p_print")))));
}
async function loadPacket() {
  const seq = (S.packetSeq = (S.packetSeq || 0) + 1); // leaving this screen or starting a new packet makes this reply stale
  const paper = document.getElementById("packet-paper"), print = document.getElementById("print-btn");
  showBusy(t("load_packet"));
  setBusy(print, true);
  try {
    const page = await post("/packet", {bill: S.bill, answers: S.answers, result: S.result}, true);
    if (seq !== S.packetSeq || curScreen !== 5) return;
    const frame = el("iframe", {id: "packet-frame", title: t("p_title"), sandbox: "allow-modals allow-same-origin"});
    fill(paper, frame);
    frame.srcdoc = page;
    setBusy(print, false);
    showMsg("");
  } catch (e) {
    if (seq !== S.packetSeq || curScreen !== 5) return;
    setBusy(print, false);
    print.disabled = true;
    showMsg(e.message);
    fill(paper, el("div", {class: "stack-3"},
      el("button", {type: "button", class: "primary", id: "packet-retry", onclick: () => { show(5); loadPacket(); }}, t("retry"))));
  }
}

function restart() {
  if (S.imageUrl) URL.revokeObjectURL(S.imageUrl);
  // theme is deliberately not reset; every request counter is bumped (never reset to 0) so any
  // in-flight reply is dropped and cannot match the next request's number
  Object.assign(S, {view: viewFor(S.lang), bill: null, imageUrl: null, answers: null, result: null, explain: null, size: "", income: "", tax: null, busy: false,
                    extractSeq: S.extractSeq + 1, submitSeq: S.submitSeq + 1, home: null, homeSeq: S.homeSeq + 1, extracting: false, packetSeq: S.packetSeq + 1});
  showMsg(""); show(1);
}

S.fromQr = new URLSearchParams(location.search).get("hospital") === "cumberland_synthetic";
document.getElementById("theme-btn").addEventListener("click", () => {
  S.theme = {auto: "light", light: "dark", dark: "auto"}[S.theme];
  applyTheme();
});
show(1);
