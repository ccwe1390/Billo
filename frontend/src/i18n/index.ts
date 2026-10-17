import type { Lang } from '@/lib/api'
import { LANG_NAMES, T } from './strings'

export { LANG_NAMES }
export type StringKey = keyof typeof T
export type View = 'en' | 'es' | 'ar' | 'zh-CN' | 'zh-TW'

// Tier 1 has a translated interface. Tier 2 keeps the English interface: only the explanation and the packet
// letter are translated (HANDOFF.md, README_RUN.md).
export const TIER1: Lang[] = ['ar', 'es', 'en', 'zh-CN', 'zh-TW']
export const TIER2: Lang[] = ['vi', 'fr', 'ko', 'ru', 'de', 'hi']
export const isTier2 = (l: Lang) => TIER2.includes(l)
export const viewFor = (l: Lang): View => (isTier2(l) ? 'en' : (l as View))
export const dirFor = (l: Lang | View) => (l === 'ar' ? 'rtl' : 'ltr')

export type Translate = (key: StringKey, vars?: Record<string, string | number>) => string

/** Plain-string lookup in the given interface language, falling back to English. */
export function makeT(view: View): Translate {
  return (key, vars) => {
    const row = T[key] as Record<string, string>
    let s = row[view] ?? row.en ?? key
    for (const k in vars ?? {}) s = s.replace('{' + k + '}', String(vars![k]))
    return s
  }
}

/** The raw template (with {vars}) for building nodes that isolate each value. */
export function template(view: View, key: StringKey): string {
  const row = T[key] as Record<string, string>
  return row[view] ?? row.en ?? key
}
