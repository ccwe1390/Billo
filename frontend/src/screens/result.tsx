import type { ReactNode } from 'react'
import { Actions, Panel, ScreenTitle } from '@/components/app-shell'
import { Button } from '@/components/ui/button'
import { isTier2, template, type StringKey } from '@/i18n'
import { useI18n } from '@/i18n/context'
import type { Citation, EngineResult, Explanation, TierRow } from '@/lib/api'
import { En, fillTemplate, isolate } from '@/lib/bidi'
import { cn } from '@/lib/utils'

/** Numbered footnotes for one screen: same citation = same number, numbered in the order they are created. */
function makeNotes() {
  const items: Citation[] = []
  const index = new Map<string, number>()
  return {
    mark(c: Citation | undefined): ReactNode {
      if (!c || !c.source) return null
      const key = [c.source, c.page, c.effective_date].join('|')
      if (!index.has(key)) {
        items.push(c)
        index.set(key, items.length)
      }
      const n = index.get(key)!
      return (
        <sup className="ms-0.5 font-bold">
          <a href={'#fn-' + n} className="text-primary underline-offset-2 hover:underline">
            <bdi dir="ltr">[{n}]</bdi>
          </a>
        </sup>
      )
    },
    items,
  }
}

function hasPage(c: Citation) {
  return c.page !== null && c.page !== undefined && c.page !== ''
}

export function ResultScreen({
  result: r,
  explanation: ex,
  onToggleView,
  onBack,
  onPacket,
  onRestart,
}: {
  result: EngineResult
  explanation: Explanation
  onToggleView: () => void
  onBack: () => void
  onPacket: () => void
  onRestart: () => void
}) {
  const { t, lang, view } = useI18n()
  const english = view === 'en'
  const tier2 = isTier2(lang)
  const fb = ex.fallback_used
  // Tier 2: English facts first (the interface is English), then the translated text. Tier 1: one or the other.
  const showEn = english || fb || tier2
  const showNative = lang !== 'en' && !fb && (tier2 || !english)
  const eligible = r.tier.eligible
  const tpl = (k: StringKey) => template(view, k)
  const c = r.contacts

  // Build the markers top to bottom so footnote numbers follow reading order.
  const notes = makeNotes()
  const leadMark = notes.mark(r.fpl.citation)
  const tierMark = notes.mark(r.tier.citation)
  const deadlineMark = notes.mark(r.deadline.citation)
  const docMarks = r.documents.map((d) => notes.mark(d.citation))
  const contactMark = notes.mark(c.citation)

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <ScreenTitle>{t('r_title')}</ScreenTitle>
        {lang !== 'en' && !tier2 && (
          <Button variant="outline" onClick={onToggleView}>
            {english ? t('r_see_native') : t('r_see_en')}
          </Button>
        )}
      </div>

      {/* The headline is the engine's number, never the model's. */}
      <Panel className="space-y-5 p-6">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:gap-6">
          <p dir="ltr" className="text-7xl font-bold leading-none text-primary tabular-nums">
            {r.percent_of_fpl}%
          </p>
          <p className="max-w-md text-lg">
            {fillTemplate(tpl('r_percent'), { pct: r.percent_of_fpl, year: r.fpl.year })}
            {leadMark}
          </p>
        </div>
        <p className="border-t border-border pt-3 text-base font-bold">{t('r_decides')}</p>
      </Panel>

      <section aria-labelledby="tier-h" className="space-y-3">
        <h3 id="tier-h" className="text-lg font-bold">
          {t('r_tier')}
        </h3>
        {r.tiers?.length ? (
          <TierTable tiers={r.tiers} pct={r.percent_of_fpl} tpl={tpl} />
        ) : (
          <Panel>
            <p className="text-xl font-bold">
              <En>{r.tier.label_en}</En>
            </p>
          </Panel>
        )}
        <p className="text-sm text-muted-foreground">
          {t('r_policy_en')}
          {tierMark}
        </p>
      </section>

      <Panel className="bg-warning-surface">
        <h3 className="font-bold text-warning">{t('r_deadline')}</h3>
        <p>
          <DeadlineLine text={r.deadline.text_en} date={r.deadline.date} />
          {deadlineMark}
        </p>
      </Panel>

      <Panel>
        <h3 className="font-bold">{t('r_about')}</h3>
        {showEn &&
          ex.text_en.split('\n').map((l, i) => (
            <p key={'en' + i} lang="en" dir="ltr">
              {l}
            </p>
          ))}
        {showNative && (
          <div className={cn('space-y-3', showEn && 'border-t border-border pt-3')}>
            {ex.text.split('\n').map((l, i) => (
              <p key={'n' + i} lang={lang} dir={lang === 'ar' ? 'rtl' : 'ltr'} className="text-lg">
                {isolate(l)}
              </p>
            ))}
            <p className="text-sm text-muted-foreground">{t('ai_note')}</p>
          </div>
        )}
        {fb && (tier2 || !english) && <p className="text-sm text-muted-foreground">{t('r_fallback')}</p>}
      </Panel>

      <div className="grid gap-3 md:grid-cols-2">
        {eligible && (
          <Panel>
            <h3 className="font-bold">{t('r_docs')}</h3>
            <ol className="list-decimal space-y-2 ps-5 marker:font-bold marker:text-primary">
              {r.documents.map((d, i) => (
                <li key={d.id}>
                  <En>{d.label_en}</En>
                  {docMarks[i]}
                </li>
              ))}
            </ol>
          </Panel>
        )}
        <Panel>
          <h3 className="font-bold">{eligible ? t('r_contact') : t('r_payplan')}</h3>
          <dl className="grid grid-cols-[auto_1fr] gap-x-3 gap-y-2">
            {eligible && (
              <>
                <dt className="text-muted-foreground">{t('r_email')}</dt>
                <dd>
                  <En>{c.email}</En>
                </dd>
              </>
            )}
            <dt className="text-muted-foreground">{t('r_phone')}</dt>
            <dd>
              <En>{eligible ? c.phone : c.payment_plan_phone || c.phone}</En>
              {contactMark}
            </dd>
          </dl>
        </Panel>
      </div>

      {!eligible && <Panel className="font-bold">{t('r_no_packet')}</Panel>}

      {notes.items.length > 0 && (
        <ol aria-label={t('src')} className="space-y-2 text-sm text-muted-foreground">
          {notes.items.map((n, i) => {
            const body = (
              <>
                <bdi dir="ltr" className="me-1.5 font-bold text-foreground">
                  [{i + 1}]
                </bdi>
                {t('src')}: <En>{n.source}</En>
                {hasPage(n) && (
                  <>
                    , {t('page')} <En>{String(n.page)}</En>
                  </>
                )}
                {n.effective_date && (
                  <>
                    , {t('effective')} <En>{n.effective_date}</En>
                  </>
                )}
              </>
            )
            return (
              <li key={i} id={'fn-' + (i + 1)} className="scroll-mt-4">
                {n.url ? (
                  <a href={n.url} target="_blank" rel="noopener" className="underline underline-offset-2 hover:text-foreground">
                    {body}
                  </a>
                ) : (
                  body
                )}
              </li>
            )
          })}
        </ol>
      )}

      <Actions
        start={
          <>
            <Button variant="outline" onClick={onBack}>
              {t('back')}
            </Button>
            <Button variant="ghost" onClick={onRestart}>
              {t('restart')}
            </Button>
          </>
        }
        end={
          eligible && (
            <Button size="lg" onClick={onPacket}>
              {t('r_packet')}
            </Button>
          )
        }
      />
    </div>
  )
}

function bandNodes(tier: TierRow, tpl: (k: StringKey) => string) {
  const key = tier.min_percent_exclusive == null ? 'band_upto' : tier.max_percent == null ? 'band_above' : 'band_between'
  return fillTemplate(tpl(key), { min: tier.min_percent_exclusive, max: tier.max_percent })
}

/** The hospital's own tier table; the household's row gets a lighter surface and a "You" tag (text, not colour). */
function TierTable({ tiers, pct, tpl }: { tiers: TierRow[]; pct: number; tpl: (k: StringKey) => string }) {
  const { t } = useI18n()
  return (
    <div className="overflow-x-auto rounded-lg bg-muted">
      <table className="w-full">
        <thead className="text-sm text-muted-foreground">
          <tr>
            <th scope="col" className="px-5 py-3 text-start font-bold">
              {t('tbl_income')}
            </th>
            <th scope="col" className="px-5 py-3 text-start font-bold">
              {t('tbl_result')}
            </th>
          </tr>
        </thead>
        <tbody>
          {tiers.map((tr, i) => (
            <tr
              key={i}
              aria-current={tr.current ? 'true' : undefined}
              className={cn('border-t border-border', tr.current && 'bg-accent font-bold text-accent-foreground')}
            >
              <th scope="row" className={cn('px-5 py-3 text-start align-top', !tr.current && 'font-normal')}>
                {bandNodes(tr, tpl)}
                {tr.current && (
                  <span className="ms-3 inline-block rounded-md bg-primary px-2 py-0.5 text-sm text-primary-foreground">
                    {fillTemplate(tpl('you_tag'), { pct })}
                  </span>
                )}
              </th>
              <td className="px-5 py-3 align-top">
                <En>{tr.label_en}</En>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

/** The English deadline sentence with its date highlighted. */
function DeadlineLine({ text, date }: { text: string; date: string }) {
  const i = text.indexOf(date)
  if (i < 0) return <En>{text}</En>
  return (
    <span lang="en" dir="ltr">
      {text.slice(0, i)}
      <mark className="rounded-sm bg-highlight px-1 font-bold text-highlight-foreground">{date}</mark>
      {text.slice(i + date.length)}
    </span>
  )
}
