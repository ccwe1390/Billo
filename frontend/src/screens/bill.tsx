import { useState } from 'react'
import { Actions, ScreenTitle } from '@/components/app-shell'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import type { StringKey } from '@/i18n'
import { useI18n } from '@/i18n/context'
import { FIELD_NAMES, type BillField, type BillFields, type FieldName } from '@/lib/api'
import { centsToDollars, dollarsToCents } from '@/lib/money'
import { cn } from '@/lib/utils'

const LABELS: Record<FieldName, StringKey> = {
  hospital_name: 'f_hospital',
  statement_date: 'f_statement',
  account_number: 'f_account',
  amount_due_cents: 'f_amount',
  date_of_service: 'f_service',
  insurance_status: 'f_insurance',
}
const REQUIRED = new Set<FieldName>(['statement_date', 'amount_due_cents']) // the engine needs these two
const INSURANCE: [string, StringKey][] = [
  ['', 'ins_blank'],
  ['self_pay', 'ins_self_pay'],
  ['insured', 'ins_insured'],
  ['unknown', 'ins_unknown'],
]

export function BillScreen({
  bill,
  readCount,
  imageUrl,
  busy,
  onFile,
  onChange,
  onBack,
  onNext,
}: {
  bill: BillFields | null
  readCount: number
  imageUrl: string | null
  busy: boolean
  onFile: (f: File) => void
  onChange: (bill: BillFields) => void
  onBack: () => void
  onNext: () => void
}) {
  const { t } = useI18n()
  const allConfirmed = !!bill && FIELD_NAMES.every((n) => bill.fields[n].confirmed)
  const setField = (name: FieldName, f: BillField) => bill && onChange({ ...bill, fields: { ...bill.fields, [name]: f } })

  return (
    <div className="space-y-8">
      <ScreenTitle sub={t('bill_hint')}>{t('bill_title')}</ScreenTitle>

      <div className="grid gap-8 lg:grid-cols-[minmax(0,5fr)_minmax(0,6fr)]">
        <div className="space-y-3">
          <label
            className={cn(
              'flex min-h-36 flex-col items-center justify-center gap-3 rounded-lg border-2 border-dashed border-input bg-muted p-5 text-center transition-colors duration-150 hover:border-primary hover:bg-muted-hover',
              'has-[input:focus-visible]:outline-3 has-[input:focus-visible]:outline-offset-2 has-[input:focus-visible]:outline-ring',
              busy && 'pointer-events-none',
            )}
          >
            <input
              type="file"
              accept="image/png,image/jpeg"
              className="sr-only"
              disabled={busy}
              onChange={(e) => {
                const f = e.target.files?.[0]
                if (f) onFile(f)
                e.target.value = '' // let the same photo be picked again
              }}
            />
            <span className="text-lg font-bold">{t('upload')}</span>
            <span lang="en" dir="ltr" className="text-sm text-muted-foreground">
              PNG / JPEG
            </span>
          </label>
          {imageUrl && <img src={imageUrl} alt="" className="max-h-[28rem] w-full rounded-lg bg-white object-contain" />}
        </div>

        <div className="space-y-3">
          {bill ? (
            FIELD_NAMES.map((name) => (
              // keyed on the read count so a new photo resets the draft text of each field
              <FieldRow key={readCount + name} name={name} field={bill.fields[name]} onChange={(f) => setField(name, f)} />
            ))
          ) : (
            <p className="rounded-lg bg-muted p-5 text-muted-foreground">{t('upload')}</p>
          )}
        </div>
      </div>

      <Actions
        start={
          <Button variant="outline" onClick={onBack}>
            {t('back')}
          </Button>
        }
        end={
          <Button size="lg" disabled={!allConfirmed || busy} onClick={onNext}>
            {t('continue_')}
          </Button>
        }
      />
    </div>
  )
}

function FieldRow({ name, field, onChange }: { name: FieldName; field: BillField; onChange: (f: BillField) => void }) {
  const { t } = useI18n()
  const id = 'f-' + name
  const required = REQUIRED.has(name)
  // The amount is typed as dollars; keep the typed text so "48" is not reformatted while typing.
  const [draft, setDraft] = useState(() =>
    name === 'amount_due_cents' ? (typeof field.value === 'number' ? centsToDollars(field.value) : '') : String(field.value ?? ''),
  )
  const blank = field.value === null || field.value === ''
  const edit = (text: string) => {
    setDraft(text)
    const v = text.trim()
    const value = v === '' ? null : name === 'amount_due_cents' ? dollarsToCents(v) : v
    onChange({ value, confidence: null, confirmed: false }) // any edit needs a fresh confirmation
  }

  const control =
    name === 'insurance_status' ? (
      <select
        id={id}
        value={draft}
        onChange={(e) => edit(e.target.value)}
        className="h-12 w-full rounded-[var(--radius)] border-2 border-input bg-background px-3 text-base text-foreground outline-none focus-visible:border-primary"
      >
        {INSURANCE.map(([v, k]) => (
          <option key={v} value={v}>
            {t(k)}
          </option>
        ))}
      </select>
    ) : (
      <Input
        id={id}
        type={name === 'statement_date' || name === 'date_of_service' ? 'date' : 'text'}
        inputMode={name === 'amount_due_cents' ? 'decimal' : undefined}
        autoComplete="off"
        dir={name === 'hospital_name' ? undefined : 'ltr'}
        value={draft}
        aria-invalid={blank && required ? true : undefined}
        aria-describedby={blank ? id + '-hint' : undefined}
        onChange={(e) => edit(e.target.value)}
      />
    )

  // State is shown by the surface and by words, never by a coloured border.
  return (
    <div className={cn('space-y-3 rounded-lg p-5', blank ? 'bg-warning-surface' : field.confirmed ? 'bg-success-surface' : 'bg-muted')}>
      <label htmlFor={id} className="block font-bold">
        {t(LABELS[name])}
        {required && <span aria-hidden> *</span>}
      </label>
      {control}
      {blank && (
        <p id={id + '-hint'} className="text-sm font-bold text-warning">
          {t('unreadable')}
          {required && ' (' + t('required') + ')'}
        </p>
      )}
      <label
        htmlFor={id + '-ok'}
        className={cn(
          'flex min-h-12 items-center gap-3',
          field.confirmed ? 'font-bold text-success' : 'text-foreground',
          blank && required && 'cursor-not-allowed text-muted-foreground',
        )}
      >
        <Checkbox
          id={id + '-ok'}
          checked={field.confirmed}
          disabled={blank && required}
          onCheckedChange={(c) => onChange({ ...field, confirmed: c === true })}
        />
        {t('confirm')}
      </label>
    </div>
  )
}
