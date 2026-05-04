import th from './th.json';
import en from './en.json';

export type Locale = 'th' | 'en';
export const defaultLocale: Locale = 'th';
export const locales = ['th', 'en'] as const satisfies readonly Locale[];

const dictionaries: Record<Locale, Record<string, unknown>> = { th, en };

/**
 * Read a deep-keyed string from the dictionary (e.g. "hero.headline").
 * Throws in production if a key is missing; returns the raw key in dev.
 */
export function t(locale: Locale, key: string): string {
  const dict = dictionaries[locale];
  const value = key.split('.').reduce<unknown>((acc, part) => {
    if (acc && typeof acc === 'object' && part in (acc as object)) {
      return (acc as Record<string, unknown>)[part];
    }
    return undefined;
  }, dict);

  if (typeof value === 'string') return value;

  if (import.meta.env.PROD) {
    throw new Error(`[i18n] Missing key "${key}" for locale "${locale}"`);
  }
  return `⟨${key}⟩`;
}

/**
 * Read a deep-keyed array (used for principles.items[]).
 */
export function tArray<T = string>(locale: Locale, key: string): T[] {
  const dict = dictionaries[locale];
  const value = key.split('.').reduce<unknown>((acc, part) => {
    if (acc && typeof acc === 'object' && part in (acc as object)) {
      return (acc as Record<string, unknown>)[part];
    }
    return undefined;
  }, dict);

  if (Array.isArray(value)) return value as T[];

  if (import.meta.env.PROD) {
    throw new Error(`[i18n] Missing array "${key}" for locale "${locale}"`);
  }
  return [];
}

/**
 * Determine the locale of an Astro request URL.
 */
export function getLocaleFromUrl(url: URL): Locale {
  const segments = url.pathname.split('/').filter(Boolean);
  if (segments[0] === 'en') return 'en';
  return 'th';
}

/**
 * Map a path in one locale to the equivalent in another.
 */
export function localizedPath(target: Locale, currentPath: string): string {
  const stripped = currentPath.replace(/^\/en(\/|$)/, '/');
  if (target === 'th') return stripped;
  if (stripped === '/') return '/en/';
  return `/en${stripped}`;
}

export const localeLabel: Record<Locale, string> = {
  th: 'ไทย',
  en: 'EN',
};

export const htmlLang: Record<Locale, string> = {
  th: 'th',
  en: 'en',
};
