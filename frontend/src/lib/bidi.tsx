import type { ReactNode } from 'react'

// Team UI rule 7: policy text, citations, phone, email, dates and money stay English and left-to-right inside
// right-to-left pages. These helpers wrap such runs in <bdi dir="ltr"> so Arabic layout cannot reorder them.

/** An English run, isolated from the page direction. */
export function En({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <bdi lang="en" dir="ltr" className={className}>
      {children}
    </bdi>
  )
}

/** Translated template -> nodes; each {var} (and a % right after it) goes in <bdi dir="ltr">. */
export function fillTemplate(tpl: string, vars: Record<string, string | number | null | undefined>): ReactNode[] {
  const out: ReactNode[] = []
  const re = /\{(\w+)\}(%?)/g
  let last = 0
  let m: RegExpExecArray | null
  while ((m = re.exec(tpl)) !== null) {
    if (m.index > last) out.push(tpl.slice(last, m.index))
    out.push(
      <bdi key={m.index} dir="ltr">
        {String(vars[m[1]]) + m[2]}
      </bdi>,
    )
    last = re.lastIndex
  }
  if (last < tpl.length) out.push(tpl.slice(last))
  return out
}

// Emails, money, ISO dates, US phones, account numbers like CGH-00482913, and percents.
const ISOLATE_RE =
  /[\w.+-]+@[\w-]+(?:\.[\w-]+)+|\$\s?\d[\d,]*(?:\.\d+)?|\b\d{4}-\d{2}-\d{2}\b|\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}|\b[A-Z]{2,}-\d+\b|\d+(?:[.,]\d+)*%/g

/** Free translated text -> nodes with every number-like run isolated left-to-right. */
export function isolate(text: string): ReactNode[] {
  const out: ReactNode[] = []
  let last = 0
  let m: RegExpExecArray | null
  ISOLATE_RE.lastIndex = 0
  while ((m = ISOLATE_RE.exec(text)) !== null) {
    if (m.index > last) out.push(text.slice(last, m.index))
    out.push(
      <bdi key={m.index} dir="ltr">
        {m[0]}
      </bdi>,
    )
    last = ISOLATE_RE.lastIndex
  }
  if (last < text.length) out.push(text.slice(last))
  return out
}
