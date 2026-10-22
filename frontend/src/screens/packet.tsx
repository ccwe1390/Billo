import { useRef } from 'react'
import { Actions, ScreenTitle } from '@/components/app-shell'
import { Button } from '@/components/ui/button'
import { useI18n } from '@/i18n/context'

/** The server's printable packet page, shown as-is in a sandboxed frame (no scripts run inside it). It stays white:
 *  it is the paper the family prints and hands to the hospital. */
export function PacketScreen({
  html,
  onBack,
  onRestart,
}: {
  html: string | null
  onBack: () => void
  onRestart: () => void
}) {
  const { t } = useI18n()
  const frame = useRef<HTMLIFrameElement>(null)
  return (
    <div className="space-y-8">
      <ScreenTitle sub={t('p_sub')}>{t('p_title')}</ScreenTitle>

      <div className="overflow-hidden rounded-lg bg-white">
        {html ? (
          <iframe
            ref={frame}
            title={t('p_title')}
            sandbox="allow-modals allow-same-origin"
            srcDoc={html}
            className="block h-[75vh] w-full"
          />
        ) : (
          <div className="h-[50vh] bg-muted" />
        )}
      </div>

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
          <Button size="lg" disabled={!html} onClick={() => frame.current?.contentWindow?.print()}>
            {t('p_print')}
          </Button>
        }
      />
    </div>
  )
}
