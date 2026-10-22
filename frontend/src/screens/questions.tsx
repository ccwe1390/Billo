import { Actions, OptionButton, ScreenTitle } from '@/components/app-shell'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useI18n } from '@/i18n/context'
import { dollarsToCents } from '@/lib/money'

export interface Draft {
  size: string
  income: string
  tax: boolean | null
}

export function draftIsValid(d: Draft) {
  const n = Number(d.size)
  return Number.isInteger(n) && n >= 1 && n <= 12 && dollarsToCents(d.income) !== null && d.tax !== null
}

export function QuestionsScreen({
  draft,
  busy,
  onChange,
  onBack,
  onSubmit,
}: {
  draft: Draft
  busy: boolean
  onChange: (d: Draft) => void
  onBack: () => void
  onSubmit: () => void
}) {
  const { t } = useI18n()
  const n = Number(draft.size) || 0
  const setSize = (v: number) => onChange({ ...draft, size: String(Math.min(12, Math.max(1, v))) })

  return (
    <form
      className="space-y-8"
      onSubmit={(e) => {
        e.preventDefault()
        if (draftIsValid(draft) && !busy) onSubmit()
      }}
    >
      <ScreenTitle sub={t('no_id')}>{t('q_title')}</ScreenTitle>

      <section className="space-y-3">
        <label htmlFor="q-size" className="block text-lg font-bold">
          {t('q_size')}
        </label>
        <div className="flex items-center gap-3" dir="ltr">
          <Button type="button" variant="outline" size="square" aria-label="-1" disabled={n <= 1} onClick={() => setSize(n - 1)}>
            <span aria-hidden>−</span>
          </Button>
          <Input
            id="q-size"
            type="number"
            inputMode="numeric"
            min={1}
            max={12}
            step={1}
            value={draft.size}
            onChange={(e) => onChange({ ...draft, size: e.target.value })}
            className="w-24 text-center text-xl font-bold tabular-nums"
          />
          <Button type="button" variant="outline" size="square" aria-label="+1" disabled={n >= 12} onClick={() => setSize(n + 1)}>
            <span aria-hidden>+</span>
          </Button>
        </div>
      </section>

      <section className="space-y-3">
        <label htmlFor="q-income" className="block text-lg font-bold">
          {t('q_income')}
        </label>
        <div className="relative max-w-xs" dir="ltr">
          <span aria-hidden className="pointer-events-none absolute inset-y-0 left-4 flex items-center text-lg font-bold text-muted-foreground">
            $
          </span>
          <Input
            id="q-income"
            type="text"
            inputMode="decimal"
            autoComplete="off"
            value={draft.income}
            aria-invalid={draft.income !== '' && dollarsToCents(draft.income) === null ? true : undefined}
            onChange={(e) => onChange({ ...draft, income: e.target.value })}
            className="ps-9 text-xl font-bold tabular-nums"
          />
        </div>
      </section>

      <fieldset className="space-y-3">
        <legend className="mb-3 text-lg font-bold">{t('q_tax')}</legend>
        <div className="grid max-w-sm grid-cols-2 gap-3">
          <OptionButton selected={draft.tax === true} onClick={() => onChange({ ...draft, tax: true })}>
            {t('yes')}
          </OptionButton>
          <OptionButton selected={draft.tax === false} onClick={() => onChange({ ...draft, tax: false })}>
            {t('no')}
          </OptionButton>
        </div>
      </fieldset>

      <Actions
        start={
          <Button type="button" variant="outline" onClick={onBack}>
            {t('back')}
          </Button>
        }
        end={
          <Button type="submit" size="lg" disabled={!draftIsValid(draft) || busy}>
            {t('see_result')}
          </Button>
        }
      />
    </form>
  )
}
