import { createContext, useContext } from 'react'
import type { Lang } from '@/lib/api'
import { makeT, type Translate, type View } from './index'

export interface I18n {
  /** The family's chosen language (decides explanation + letter language). */
  lang: Lang
  /** The interface language actually shown (tier 2 languages show English; the result toggle can switch). */
  view: View
  t: Translate
}

export const I18nContext = createContext<I18n>({ lang: 'en', view: 'en', t: makeT('en') })
export const useI18n = () => useContext(I18nContext)
