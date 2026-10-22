import { Direction } from 'radix-ui'
import { useEffect, useMemo, useState } from 'react'
import { Footer, Header, StatusLine, Stepper, type Status } from '@/components/app-shell'
import { dirFor, makeT, viewFor, type View } from '@/i18n'
import { I18nContext } from '@/i18n/context'
import {
  ApiError,
  blankBill,
  evaluate,
  explain,
  extractBill,
  packetHtml,
  type BillFields,
  type EngineResult,
  type Explanation,
  type HouseholdAnswers,
  type Lang,
} from '@/lib/api'
import { dollarsToCents } from '@/lib/money'
import { cn } from '@/lib/utils'
import { BillScreen } from '@/screens/bill'
import { PacketScreen } from '@/screens/packet'
import { QuestionsScreen, type Draft } from '@/screens/questions'
import { ResultScreen } from '@/screens/result'
import { StartScreen } from '@/screens/start'

type Step = 1 | 2 | 3 | 4 | 5
const EMPTY_DRAFT: Draft = { size: '', income: '', tax: null }

// All state lives in memory only: nothing is written to localStorage, sessionStorage, cookies or IndexedDB
// (team UI rule 4). Restart and closing the tab both forget everything.
function App() {
  const [step, setStep] = useState<Step>(1)
  const [lang, setLang] = useState<Lang>('en')
  const [view, setView] = useState<View>('en')
  const [forWhom, setForWhom] = useState<'self' | 'family'>('self')
  const [bill, setBill] = useState<BillFields | null>(null)
  const [readCount, setReadCount] = useState(0)
  const [imageUrl, setImageUrl] = useState<string | null>(null)
  const [draft, setDraft] = useState<Draft>(EMPTY_DRAFT)
  const [answers, setAnswers] = useState<HouseholdAnswers | null>(null)
  const [result, setResult] = useState<EngineResult | null>(null)
  const [explanation, setExplanation] = useState<Explanation | null>(null)
  const [packet, setPacket] = useState<string | null>(null)
  const [status, setStatus] = useState<Status>(null)
  const [busy, setBusy] = useState(false)

  const i18n = useMemo(() => ({ lang, view, t: makeT(view) }), [lang, view])
  const { t } = i18n
  const msgs = { generic: t('err_generic'), invalid: t('err_invalid') }
  const dir = dirFor(view)

  useEffect(() => {
    document.documentElement.lang = view
    document.documentElement.dir = dir
    document.title = t('app_title')
  }, [view, dir, t])

  const go = (s: Step) => {
    setStatus(null)
    setStep(s)
    window.scrollTo({ top: 0 })
  }

  const chooseLang = (l: Lang) => {
    setLang(l)
    setView(viewFor(l))
  }

  const onFile = async (f: File) => {
    if (imageUrl) URL.revokeObjectURL(imageUrl)
    setImageUrl(URL.createObjectURL(f))
    setBill(null)
    setBusy(true)
    setStatus({ kind: 'busy', text: t('reading') })
    try {
      setBill(await extractBill(f))
      setStatus(null)
    } catch {
      setBill(blankBill()) // photo reading off: the same fields, typed by hand
      setStatus({ kind: 'error', text: t('read_failed') })
    } finally {
      setReadCount((n) => n + 1)
      setBusy(false)
    }
  }

  const submitAnswers = async () => {
    if (!bill) return
    const a: HouseholdAnswers = {
      contract_version: 1,
      language: lang,
      for_whom: forWhom,
      household_size: Number(draft.size),
      annual_income_cents: dollarsToCents(draft.income)!,
      files_tax_return: draft.tax!,
    }
    setAnswers(a)
    setBusy(true)
    setStatus({ kind: 'busy', text: t('load_evaluate') })
    try {
      const r = await evaluate(bill, a, msgs)
      setStatus({ kind: 'busy', text: t('load_explain') })
      const ex = await explain(bill, a, msgs)
      setResult(r)
      setExplanation(ex)
      setView(viewFor(lang))
      go(4)
    } catch (e) {
      setStatus({ kind: 'error', text: e instanceof ApiError ? e.message : t('err_generic') })
    } finally {
      setBusy(false)
    }
  }

  const openPacket = async () => {
    if (!bill || !answers) return
    setPacket(null)
    go(5)
    setStatus({ kind: 'busy', text: t('load_packet') })
    try {
      setPacket(await packetHtml(bill, answers, msgs))
      setStatus(null)
    } catch (e) {
      setStatus({ kind: 'error', text: e instanceof ApiError ? e.message : t('err_generic') })
    }
  }

  const restart = () => {
    if (imageUrl) URL.revokeObjectURL(imageUrl)
    setBill(null)
    setImageUrl(null)
    setDraft(EMPTY_DRAFT)
    setAnswers(null)
    setResult(null)
    setExplanation(null)
    setPacket(null)
    setBusy(false)
    go(1)
  }

  return (
    <I18nContext.Provider value={i18n}>
      <Direction.Provider dir={dir}>
        <div className="flex min-h-dvh flex-col">
          <Header />
          <Stepper step={step} />
          <main className={cn('mx-auto w-full flex-1 space-y-4 px-4 py-6 sm:px-6', step === 2 || step >= 4 ? 'max-w-5xl' : 'max-w-2xl')}>
            <StatusLine status={status} />
            <div className="rounded-xl border border-border bg-card p-5 sm:p-8">
              {step === 1 && (
                <StartScreen forWhom={forWhom} onLang={chooseLang} onForWhom={setForWhom} onStart={() => go(2)} />
              )}
              {step === 2 && (
                <BillScreen
                  bill={bill}
                  readCount={readCount}
                  imageUrl={imageUrl}
                  busy={busy}
                  onFile={onFile}
                  onChange={setBill}
                  onBack={() => go(1)}
                  onNext={() => go(3)}
                />
              )}
              {step === 3 && (
                <QuestionsScreen draft={draft} busy={busy} onChange={setDraft} onBack={() => go(2)} onSubmit={submitAnswers} />
              )}
              {step === 4 && result && explanation && (
                <ResultScreen
                  result={result}
                  explanation={explanation}
                  onToggleView={() => setView(view === 'en' ? viewFor(lang) : 'en')}
                  onBack={() => go(3)}
                  onPacket={openPacket}
                  onRestart={restart}
                />
              )}
              {step === 5 && <PacketScreen html={packet} onBack={() => go(4)} onRestart={restart} />}
            </div>
          </main>
          <Footer />
        </div>
      </Direction.Provider>
    </I18nContext.Provider>
  )
}

export default App
