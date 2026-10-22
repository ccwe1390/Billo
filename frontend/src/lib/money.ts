// String math only, never floats (docs/contracts.md: money is integer cents). Same rules as app/static/app.js.

/** "4812.40", "$4,812.4" or "38000" -> cents; anything else -> null. */
export function dollarsToCents(s: string): number | null {
  const m = /^\$?\s*(\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d{1,2}))?$/.exec((s || '').trim())
  if (!m) return null
  return parseInt(m[1].replace(/,/g, ''), 10) * 100 + parseInt((m[2] || '0').padEnd(2, '0'), 10)
}

/** 481240 -> "4812.40" (for an editable input). */
export function centsToDollars(c: number): string {
  return Math.floor(c / 100) + '.' + String(c % 100).padStart(2, '0')
}
