import { LoaderCircle } from 'lucide-react'
import { useEffect, useRef, type ComponentProps, type ReactNode } from 'react'
import { useI18n } from '@/i18n/context'
import type { StringKey } from '@/i18n'
import { cn } from '@/lib/utils'

// Spacing system, used everywhere (no one-off values): page gutter px-4 / sm:px-6; between sections of a screen
// space-y-8; inside a section space-y-3; panel padding p-5; gaps between controls gap-3; action row pt-6 border-t.
// Panels are a solid surface step (bg-muted), never a coloured border.

export function Header() {
  const { t } = useI18n()
  return (
    <header className="border-b border-border bg-card">
      <div className="mx-auto flex max-w-5xl items-center justify-between gap-3 px-4 py-4 sm:px-6">
        <h1 className="min-w-0 truncate text-xl font-bold">{t('app_title')}</h1>
        {/* Team UI rule 5: the synthetic-demo label stays visible on every screen. */}
        <span lang="en" dir="ltr" className="shrink-0 rounded-md bg-warning px-2.5 py-1 text-xs font-bold text-highlight-foreground">
          SYNTHETIC DEMO
        </span>
      </div>
    </header>
  )
}

export function Stepper({ step }: { step: number }) {
  const { t } = useI18n()
  return (
    <nav aria-label={t('step_of', { n: step, total: 5 })} className="mx-auto w-full max-w-5xl px-4 pt-6 sm:px-6">
      <ol className="grid grid-cols-5 gap-3">
        {[1, 2, 3, 4, 5].map((i) => {
          const state = i === step ? 'now' : i < step ? 'done' : 'todo'
          return (
            <li key={i} aria-current={state === 'now' ? 'step' : undefined} className="space-y-2">
              <span className={cn('block h-1 rounded-full', state === 'todo' ? 'bg-border' : 'bg-primary')} />
              <span
                className={cn(
                  'hidden text-sm sm:block',
                  state === 'now' ? 'font-bold text-foreground' : state === 'done' ? 'text-foreground' : 'text-muted-foreground',
                )}
              >
                <span className="tabular-nums">{i}.</span> {t(('step_' + i) as StringKey)}
              </span>
            </li>
          )
        })}
      </ol>
      <p className="mt-2 text-sm font-bold sm:hidden">
        {t('step_of', { n: step, total: 5 })}: {t(('step_' + step) as StringKey)}
      </p>
    </nav>
  )
}

export type Status = { kind: 'busy' | 'error'; text: string } | null

/** One live region for loading steps and errors (team UI rule 9: loading states name the step). */
export function StatusLine({ status }: { status: Status }) {
  return (
    <div aria-live="polite" role="status">
      {status && (
        <p
          className={cn(
            'flex items-center gap-3 rounded-lg bg-muted px-5 py-3 text-base',
            status.kind === 'error' ? 'font-bold text-destructive' : 'text-foreground',
          )}
        >
          {status.kind === 'busy' && <LoaderCircle aria-hidden className="size-5 shrink-0 animate-spin text-primary" />}
          <span>{status.text}</span>
        </p>
      )}
    </div>
  )
}

/** A screen's heading; it takes focus when the screen opens so screen readers announce the new step. */
export function ScreenTitle({ children, sub }: { children: ReactNode; sub?: ReactNode }) {
  const ref = useRef<HTMLHeadingElement>(null)
  useEffect(() => {
    ref.current?.focus()
  }, [])
  return (
    <div className="space-y-3">
      <h2 ref={ref} tabIndex={-1} className="text-2xl font-bold outline-none sm:text-3xl">
        {children}
      </h2>
      {sub && <p className="max-w-prose text-base text-muted-foreground">{sub}</p>}
    </div>
  )
}

/** A section surface: one step lighter than the card, no border. */
export function Panel({ children, className, ...rest }: ComponentProps<'section'>) {
  return (
    <section className={cn('space-y-3 rounded-lg bg-muted p-5', className)} {...rest}>
      {children}
    </section>
  )
}

export function Footer() {
  const { t } = useI18n()
  return (
    <footer className="mx-auto w-full max-w-5xl px-4 pb-8 pt-2 text-sm text-muted-foreground sm:px-6">
      {t('not_affiliated')}
    </footer>
  )
}

/** Single-choice option. Selected = filled radio dot + teal surface + bold, so it never relies on colour alone. */
export function OptionButton({
  selected,
  onClick,
  children,
  lang,
}: {
  selected: boolean
  onClick: () => void
  children: ReactNode
  lang?: string
}) {
  return (
    <button
      type="button"
      lang={lang}
      aria-pressed={selected}
      onClick={onClick}
      className={cn(
        'flex min-h-12 items-center gap-3 rounded-lg px-4 py-3 text-start text-base transition-colors duration-150',
        selected ? 'bg-accent font-bold text-accent-foreground' : 'bg-muted text-foreground hover:bg-muted-hover',
      )}
    >
      <span
        aria-hidden
        className={cn(
          'grid size-5 shrink-0 place-items-center rounded-full border-2',
          selected ? 'border-primary' : 'border-input',
        )}
      >
        {selected && <span className="size-2.5 rounded-full bg-primary" />}
      </span>
      <span>{children}</span>
    </button>
  )
}

/** The bottom row of a screen: secondary actions at the start, the main action at the end. */
export function Actions({ start, end }: { start: ReactNode; end?: ReactNode }) {
  return (
    <div className="flex flex-col-reverse gap-3 border-t border-border pt-6 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex flex-col gap-3 sm:flex-row">{start}</div>
      {end}
    </div>
  )
}
