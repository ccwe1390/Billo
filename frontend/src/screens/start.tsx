import { Actions, OptionButton, ScreenTitle } from '@/components/app-shell'
import { Button } from '@/components/ui/button'
import { LANG_NAMES, TIER1, TIER2 } from '@/i18n'
import { useI18n } from '@/i18n/context'
import type { Lang } from '@/lib/api'

export function StartScreen({
  forWhom,
  onLang,
  onForWhom,
  onStart,
}: {
  forWhom: 'self' | 'family'
  onLang: (l: Lang) => void
  onForWhom: (v: 'self' | 'family') => void
  onStart: () => void
}) {
  const { t, lang } = useI18n()
  return (
    <div className="space-y-8">
      <ScreenTitle sub={t('notice')}>{t('app_title')}</ScreenTitle>

      <p className="max-w-prose text-base text-foreground">{t('no_id')}</p>

      <section aria-labelledby="pick-lang" className="space-y-3">
        <h3 id="pick-lang" className="text-lg font-bold">
          {t('pick_lang')}
        </h3>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
          {TIER1.map((l) => (
            <OptionButton key={l} lang={l} selected={lang === l} onClick={() => onLang(l)}>
              {LANG_NAMES[l]}
            </OptionButton>
          ))}
        </div>
        <p lang="en" dir="ltr" className="pt-3 text-sm text-muted-foreground">
          More languages (interface in English)
        </p>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
          {TIER2.map((l) => (
            <OptionButton key={l} lang={l} selected={lang === l} onClick={() => onLang(l)}>
              {LANG_NAMES[l]}
            </OptionButton>
          ))}
        </div>
      </section>

      <section aria-labelledby="for-whom" className="space-y-3">
        <h3 id="for-whom" className="text-lg font-bold">
          {t('for_whom')}
        </h3>
        <div className="grid gap-3 sm:grid-cols-2">
          <OptionButton selected={forWhom === 'self'} onClick={() => onForWhom('self')}>
            {t('me')}
          </OptionButton>
          <OptionButton selected={forWhom === 'family'} onClick={() => onForWhom('family')}>
            {t('family')}
          </OptionButton>
        </div>
      </section>

      <Actions
        start={null}
        end={
          <Button size="lg" onClick={onStart}>
            {t('start')}
          </Button>
        }
      />
    </div>
  )
}
