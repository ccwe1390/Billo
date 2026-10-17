// Backend contract: docs/contracts.md and app/main.py. Money is integer cents; dates are YYYY-MM-DD.
// Nothing here stores anything: no localStorage, sessionStorage, cookies or IndexedDB (team UI rule 4).

export const LANGS = ['en', 'es', 'ar', 'zh-CN', 'zh-TW', 'vi', 'fr', 'ko', 'ru', 'de', 'hi'] as const
export type Lang = (typeof LANGS)[number]

export const FIELD_NAMES = [
  'hospital_name',
  'statement_date',
  'account_number',
  'amount_due_cents',
  'date_of_service',
  'insurance_status',
] as const
export type FieldName = (typeof FIELD_NAMES)[number]

export interface BillField {
  value: string | number | null
  confidence: number | null
  confirmed: boolean
}

export interface BillFields {
  contract_version: number
  fields: Record<FieldName, BillField>
}

export interface HouseholdAnswers {
  contract_version: 1
  language: Lang
  for_whom: 'self' | 'family'
  household_size: number
  annual_income_cents: number
  files_tax_return: boolean
}

export interface Citation {
  source: string
  url?: string
  page?: number | string | null
  effective_date?: string
}

export interface TierRow {
  id: string
  label_en: string
  discount_percent: number
  eligible: boolean
  min_percent_exclusive: number | null
  max_percent: number | null
  citation: Citation
  current: boolean
}

export interface EngineResult {
  contract_version: number
  hospital_id: string
  fpl: { year: number; household_size: number; amount_cents: number; citation: Citation }
  percent_of_fpl: number
  tier: { id: string; label_en: string; discount_percent: number; eligible: boolean; citation: Citation }
  tiers?: TierRow[]
  deadline: { date: string; text_en: string; citation: Citation }
  documents: { id: string; label_en: string; required_if: string; citation: Citation }[]
  contacts: { phone: string; email: string; payment_plan_phone?: string; citation: Citation }
  locked_numbers: string[]
}

export interface Explanation {
  contract_version: number
  language: Lang
  text_en: string
  text: string
  numbers_match: boolean
  fallback_used: boolean
  ai_written: boolean
}

/** An error whose message is safe to show (the server's own `detail`, or the caller's fallback). */
export class ApiError extends Error {}

async function readError(r: Response, fallback: string, invalid: string): Promise<never> {
  let detail = ''
  try {
    const j = await r.json()
    detail = typeof j.detail === 'string' ? j.detail : invalid
  } catch {
    /* not JSON */
  }
  throw new ApiError(detail || fallback)
}

async function post(path: string, body: unknown, msgs: { generic: string; invalid: string }): Promise<Response> {
  let r: Response
  try {
    r = await fetch(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  } catch {
    throw new ApiError(msgs.generic)
  }
  if (!r.ok) await readError(r, msgs.generic, msgs.invalid)
  return r
}

type Msgs = { generic: string; invalid: string }

/** Photo -> unconfirmed fields. Throws on any failure; the caller falls back to manual entry. */
export async function extractBill(file: File): Promise<BillFields> {
  const fd = new FormData()
  fd.append('file', file)
  const r = await fetch('/extract', { method: 'POST', body: fd })
  if (!r.ok) throw new Error('extract failed')
  return r.json()
}

export async function evaluate(bill: BillFields, answers: HouseholdAnswers, msgs: Msgs): Promise<EngineResult> {
  return (await post('/evaluate', { bill, answers }, msgs)).json()
}

export async function explain(bill: BillFields, answers: HouseholdAnswers, msgs: Msgs): Promise<Explanation> {
  return (await post('/explain', { bill, answers }, msgs)).json()
}

/** The printable packet page (HTML). The server recomputes the result itself, so none is sent. */
export async function packetHtml(bill: BillFields, answers: HouseholdAnswers, msgs: Msgs): Promise<string> {
  return (await post('/packet', { bill, answers }, msgs)).text()
}

export function blankBill(): BillFields {
  const fields = {} as Record<FieldName, BillField>
  for (const name of FIELD_NAMES) fields[name] = { value: null, confidence: 0, confirmed: false }
  return { contract_version: 1, fields }
}
