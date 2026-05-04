# Wénfáng Landing Page — Design Spec

**Date:** 2026-05-04
**Status:** Approved (pending final review)
**Scope:** Production-grade landing page only. Tools, About detail pages, and Today's Word backend are out of scope.

## 1. Purpose

Build the public landing page for **文房 Wénfáng**, a small library of focused, single-purpose study tools for learners of Chinese. The page presents the studio's identity, principles, a daily Chinese phrase ("Today's word"), and points visitors at the future Tools section. It is the first surface a Thai or English speaker encounters when they reach `wenfang.{domain}`.

## 2. Goals & Non-Goals

### Goals
- Faithful, production-grade implementation of the existing `design/index.html` reference.
- Pixel-fidelity to the reference at desktop, with intentional, well-tuned mobile behavior.
- Bilingual experience: Thai (default) and English.
- Zero-flicker locale handling for visitors landing at `/`.
- Lighthouse ≥ 95 across Performance, Accessibility, Best Practices, SEO.
- Deploys cleanly to Cloudflare Pages.
- Codebase ready to grow: structure leaves room for `/tools/flashcards`, `/tools/stroke-order`, etc., without rework.

### Non-Goals
- Not implementing any tool yet (flashcards, stroke order). The `/tools` route is a styled "Coming soon" placeholder so the masthead nav doesn't 404.
- No CMS, no dynamic Today's Word backend — the phrase is a static authored entry in the i18n dictionaries.
- No analytics, cookies banner, or auth.
- No dark mode (the design is intrinsically a cream-paper aesthetic).

## 3. Stack

| Concern | Choice | Reason |
|---|---|---|
| Framework | **Astro 5** | Static-first, ships ~0 KB JS by default, ports the existing HTML cleanly, islands available later for interactive tools. |
| Styling | **Tailwind v4** (via `@tailwindcss/vite`) + scoped component CSS | Tailwind covers ~80% via `@theme` tokens; bespoke calligraphic effects stay as raw CSS. |
| Language | **TypeScript** (strict) | Required for `t()` helper type safety and component props. |
| Hosting | **Cloudflare Pages** (static deploy of `dist/`, `output: 'static'`) | Free, fast, global. Static output ships pure HTML/CSS/JS — no adapter or Worker runtime needed. The Cloudflare adapter is only required for SSR/Functions, which we don't use. |
| Tooling | ESLint + Prettier + `astro check` | Standard quality gates. |
| Fonts (latin/serif) | System stacks first, `@fontsource/charter` and `@fontsource/ibm-plex-mono` as fallback | Apple devices already render `Iowan Old Style` / `Songti SC` natively; ship web fonts only for non-Apple visitors. |
| Fonts (zh) | System stacks first; subset `Source Han Serif SC` via `@fontsource-variable` if available, else CDN with `unicode-range` subset | Subset to only the Chinese characters the page actually renders: `文房今日一語学海无涯韩愈苦作舟` + the wordmark. |
| Fonts (th) | System Thai stack: `Sukhumvit Set, Helvetica Neue Thai, Thonburi, sans-serif` appended to body stack | Native rendering on macOS / iOS / Windows; no web font needed for Thai. |

## 4. Routing & i18n

### Locale routing
- **Default locale:** `th` (Thai), no URL prefix.
- **Secondary locale:** `en` (English), prefixed `/en/`.
- **Astro config:**
  ```ts
  i18n: {
    defaultLocale: 'th',
    locales: ['th', 'en'],
    routing: { prefixDefaultLocale: false }
  }
  ```
- **File layout:**
  - `src/pages/index.astro` → Thai landing
  - `src/pages/en/index.astro` → English landing
  - `src/pages/tools/index.astro` → Thai "Coming soon"
  - `src/pages/en/tools/index.astro` → English "Coming soon"

Both locale variants of a page render the same component tree; only the `locale` prop differs. The page file itself is a 5-line wrapper that imports `<Landing locale="..." />`.

### Auto-redirect on `/`
- An inline `<script>` in `BaseLayout.astro` runs **before paint** (placed in `<head>`, no `defer`/`async`).
- Logic, in order:
  1. Read `localStorage.wf_locale`. If `'en'`, `location.replace('/en/')`. If `'th'`, do nothing.
  2. If unset, read `navigator.language`. If it starts with `en`, redirect to `/en/`.
  3. Otherwise stay.
- The script only runs on `/` (and `/tools`). It does NOT run on `/en/*` (those URLs are explicit user choice).
- Total script size: < 300 bytes minified.
- The user's choice via `LangToggle` always overrides — the toggle writes `localStorage.wf_locale` before navigating.

### Translation dictionaries
- `src/i18n/th.json` and `src/i18n/en.json` — flat key-value, dot-notation keys (e.g., `"hero.headline"`).
- `src/i18n/ui.ts` exports:
  ```ts
  export type Locale = 'th' | 'en';
  export const defaultLocale: Locale = 'th';
  export function getLocaleFromUrl(url: URL): Locale;
  export function t(locale: Locale, key: string): string;
  export function localizedPath(locale: Locale, path: string): string;
  ```
- `t()` is purely synchronous; dictionaries are imported, not fetched.
- Missing key behavior: returns the key string itself in dev (so it's visible), throws in CI (so a missing key fails the build).

### Translation surface (final)

**Translated** (both locales):
- Nav: Home / Tools / About / Contact
- Hero eyebrow: "The Studio" / "ห้องเรียน" *(or designer's choice)*
- Hero headline: "Quiet tools for studying *Chinese*."
- Hero deck (full body copy)
- Hero meta `dt` labels (Tools, Levels, Cost) and translatable values (Two → "สอง", None → "ฟรี")
- "Today's word" eyebrow framing
- The translation gloss: "The sea of learning has no shore."
- The note paragraph (about Han Yu and the couplet)
- "Tip 001 · Refreshes daily" label text
- Principles section: eyebrow, h2, all 4 items (heading + body)
- Image caption: "Plate I. — Mountain · Inkwash · 2026"
- Footer: "Free & open", "Made by Zeze", "Wénfáng © 2026" surrounding text

**Verbatim across both locales** (untranslated):
- `文房` (wordmark CN)
- `Wén-fáng` (wordmark EN/transliteration)
- `今` (Today's word watermark)
- `今日一語` (Today's word eyebrow CN)
- `学海无涯` (the four characters of the phrase)
- `xué hǎi wú yá` (pinyin)
- `韩愈` and `Han Yu, 768–824`
- `学海无涯苦作舟` (the full couplet)
- `HSK 1–6`, `Vol. 01`, `Plate I.`
- `@ItsmeZecreto`, `zeze.app`, `X`, `Portfolio`

### `<html lang>` attribute
- `lang="th"` on `/`, `lang="en"` on `/en/*`. Spans containing Chinese receive `lang="zh-Hans"`; spans containing pinyin receive `lang="zh-Latn-pinyin"`.

## 5. Component Architecture

```
src/
├── layouts/
│   └── BaseLayout.astro         # <html><head><body> chrome, fonts, paper grain, slot
├── components/
│   ├── Masthead.astro           # wordmark + nav + LangToggle + header-meta band
│   ├── LangToggle.astro         # EN | ไทย, persists locale, swaps URL
│   ├── Hero.astro               # eyebrow, headline, deck, meta dl, hero image
│   ├── TodaysWord.astro         # 今 watermark, display chars, pinyin, gloss, note
│   ├── Principles.astro         # 4-item ordered list with numeric markers
│   ├── Footer.astro             # copyright + social links
│   └── Landing.astro            # composes Hero + TodaysWord + Principles for both locales
├── i18n/
│   ├── th.json
│   ├── en.json
│   └── ui.ts                    # Locale type, t(), getLocaleFromUrl(), localizedPath()
├── styles/
│   └── global.css               # @theme tokens, body grain, base resets
├── pages/
│   ├── index.astro              # th landing
│   ├── tools/index.astro        # th "coming soon"
│   └── en/
│       ├── index.astro          # en landing
│       └── tools/index.astro    # en "coming soon"
└── assets/
    └── hero-inkwash.png
```

### Component contracts

Every component takes a single `locale: Locale` prop and reads its own strings via `t(locale, '...')`. No global locale context — explicit prop passing keeps SSR deterministic.

| Component | Props | Responsibilities |
|---|---|---|
| `BaseLayout` | `locale`, `title`, `description` | `<html lang>`, meta, font preload, paper grain `::before`, locale-detection script (root pages only), slot for page content. |
| `Masthead` | `locale`, `currentPath` | Wordmark, primary nav (4 links: Home/Tools/About/Contact), `<LangToggle>`, header-meta band. The `Home` link is `href="#top"` (scroll to top of current page). `Tools` is `href="/tools"` or `/en/tools`. `About` is `href="#about"`. `Contact` is `href="#contact"`. `currentPath` is required so the `LangToggle` can compute the mirrored URL. |
| `LangToggle` | `locale`, `currentPath` | Renders `EN / ไทย`. Click writes `localStorage.wf_locale = otherLocale` then navigates to mirrored path. Inert state for current locale. |
| `Hero` | `locale` | Headline (with `<em>` accent on the translated "Chinese" word), deck, hero meta `dl`, hero image with fallback, image caption. |
| `TodaysWord` | `locale` | Renders the watermark, the four `<span class="syl">` characters, pinyin, translation, note (with `<em>` around `韩愈` and `学海无涯苦作舟`), Tip 001 footer. |
| `Principles` | `locale` | Renders the 4-item ordered list. Items pulled from `principles.items[]` array in dictionaries. |
| `Footer` | `locale` | Copyright, social links (X, Portfolio). |
| `Landing` | `locale` | Pure composition of `Hero + TodaysWord + Principles`. Page files render `<BaseLayout locale><Masthead locale currentPath /><main><Landing locale /></main><Footer locale /></BaseLayout>`. The `<main>` wrapper is added for landmark accessibility (not in the source HTML). |

## 6. Styling Strategy

### Tailwind v4 `@theme` tokens
Declared once in `src/styles/global.css` and consumed as utilities everywhere:

```css
@import "tailwindcss";

@theme {
  --color-bg:         oklch(96.5% 0.013 80);
  --color-paper:      oklch(98.5% 0.008 80);
  --color-surface:    oklch(99.2% 0.005 80);
  --color-fg:         oklch(18% 0.018 60);
  --color-ink:        oklch(14% 0.02 60);
  --color-muted:      oklch(46% 0.014 55);
  --color-soft:       oklch(62% 0.012 55);
  --color-border:     oklch(86% 0.014 75);
  --color-rule:       oklch(78% 0.014 70);
  --color-accent:     oklch(50% 0.205 30);
  --color-accent-deep: oklch(40% 0.21 30);
  --color-accent-soft: oklch(94% 0.05 30);

  --font-display: 'Iowan Old Style','Charter','Source Han Serif SC','Songti SC','Times New Roman',Georgia,serif;
  --font-body:    -apple-system,BlinkMacSystemFont,'SF Pro Text','Segoe UI','PingFang SC','Sukhumvit Set',system-ui,sans-serif;
  --font-zh:      'Source Han Serif SC','Songti SC','STSong','SimSun',serif;
  --font-mono:    'JetBrains Mono','IBM Plex Mono',ui-monospace,Menlo,monospace;

  --breakpoint-sm: 560px;
  --breakpoint-md: 880px;
  --breakpoint-lg: 1080px;
}
```

This produces utilities like `bg-bg`, `text-ink`, `text-accent`, `border-border`, `font-display`, `font-zh`, `sm:`, `md:`, `lg:` that match the source CSS exactly.

### What stays as scoped CSS
Tailwind handles spacing, color, typography, layout. Bespoke effects stay as `<style>` blocks in their components:

- **Paper grain** (`body::before` radial-dot pattern) — `BaseLayout.astro`
- **Hero `::before` accent rule** (38px line before eyebrow) — `Hero.astro`
- **Today's word `今` watermark** (240px outlined glyph behind the section) — `TodaysWord.astro`
- **Pulse animation** (the live indicator dot) — `global.css` keyframes. Used on the future Tools section's "live" status indicator; not rendered on the landing page itself but the keyframes are colocated with other base styles for reuse.
- **`tabular-nums` selector cascade** for monospace metadata — `global.css` (matches the source)

### Responsive
Three breakpoints, mobile-first. The component tree renders the same structure at all sizes; only spacing, font-size, grid columns change.

| Breakpoint | Behavior |
|---|---|
| Default (< 560px) | Single column. Hero image above text (`order: -1`). Nav hidden, `LangToggle` remains. Header-meta hidden. Smaller paddings. Tip's `今` watermark scales to 160px. |
| ≥ 560px | Hero meta becomes 3 columns. Container padding 28px. |
| ≥ 880px | Hero becomes 2-column grid `1.15fr 1fr`. Header-meta visible. Principles section becomes `1fr 2fr`. |
| ≥ 1080px | Full desktop spacing (96–120px section padding). Container max-width 1280px, 40px gutter. |

### Hero headline `clamp()`
Preserved verbatim: `clamp(48px, 6.6vw, 104px)`. Same for tip display (`clamp(80px, 11vw, 168px)`) and principles h2 (`clamp(30px, 3.2vw, 44px)`).

## 7. Data / Content Model

### `src/i18n/th.json` (sketch)
```json
{
  "meta": {
    "title": "文房 — Wénfáng · เครื่องมือเงียบ ๆ สำหรับเรียนภาษาจีน",
    "description": "..."
  },
  "nav": { "home": "หน้าแรก", "tools": "เครื่องมือ", "about": "เกี่ยวกับ", "contact": "ติดต่อ" },
  "headerMeta": { "left": "ฟรี · โอเพนซอร์ส", "right": "โดย Zeze" },
  "hero": {
    "eyebrow": "ห้องเรียน",
    "eyebrowVol": "เล่มที่ 01",
    "headlinePre": "เครื่องมือเงียบ ๆ สำหรับเรียน",
    "headlineEm": "ภาษาจีน",
    "deck": "...",
    "metaTools": "เครื่องมือ",
    "metaToolsValue": "สอง",
    "metaLevels": "ระดับ",
    "metaCost": "ค่าใช้จ่าย",
    "metaCostValue": "ฟรี",
    "imageCaption": "..."
  },
  "tip": {
    "eyebrow": "今日一語 · คำของวันนี้",
    "translation": "ทะเลแห่งการเรียนรู้ไม่มีฝั่ง",
    "note": "...",
    "footer": "Tip 001 · เปลี่ยนทุกวัน"
  },
  "principles": {
    "eyebrow": "— เกี่ยวกับสตูดิโอ",
    "headlinePre": "สร้างเหมือนร้านเครื่องเขียน ไม่ใช่",
    "headlineEm": "สตาร์ทอัพ",
    "items": [
      { "title": "หนึ่งเครื่องมือ หนึ่งหน้าที่", "body": "..." },
      { "title": "ตรงกับตำราเรียน", "body": "..." },
      { "title": "ค่าตั้งต้นที่ซื่อสัตย์", "body": "..." },
      { "title": "เงียบบนหน้ากระดาษ", "body": "..." }
    ]
  },
  "footer": { "copyright": "" },
  "comingSoon": { "title": "เร็ว ๆ นี้", "body": "..." }
}
```

`en.json` mirrors the same key structure with the source-fidelity English copy from the reference HTML.

> **Note on copy authoring:** Thai translations in the spec sketches above are illustrative starting points. Final Thai copy is authored by the user (Thai native speaker) before launch; placeholder strings in the dictionaries during implementation are clearly marked `// TODO: th copy`.

## 8. Behavior Details

### Locale toggle
- The toggle is two `<a>` elements: one for the current locale (rendered with `text-ink`, `aria-current="true"`, `pointer-events: none`), one for the other locale (rendered with `text-muted`, links to mirrored path).
- Mirrored path: `/` ↔ `/en/`, `/tools` ↔ `/en/tools/`. A pure-function helper covers this (`localizedPath()`).
- On click of the inactive locale: the link's `href` already points to the mirrored URL. A small click handler runs first to write `localStorage.wf_locale`, then lets navigation proceed. If JS is disabled, the link still works (locale won't persist, but the navigation does).

### Auto-detect script
- Inlined into `<head>` for root pages (`/` and `/tools`) only. Skipped on `/en/*`.
- Reads `localStorage.wf_locale` first (explicit user choice wins). If empty, falls back to `navigator.language`.
- Uses `location.replace()` so the back button doesn't bounce.
- Wrapped in a `try/catch` so storage-blocked browsers (private mode in some contexts) degrade silently.

### Image handling
- The source `design/assets/hero-inkwash.png` is 2.5 MB. The implementation **must** import it through Astro's `<Image>` component (or `<Picture>`) so it gets emitted as optimized variants:
  - AVIF + WebP at widths `[440, 600, 800, 1200]`, served via a `<picture>` source set.
  - `loading="eager"` and `fetchpriority="high"` (it's above the fold; LCP candidate).
  - Aspect ratio `2/3` preserved; `object-fit: cover; object-position: center`.
- The pure-CSS empty-state fallback from the source HTML is preserved as a sibling element shown only if the `<img>` fails to load (via `onerror` or the equivalent Astro pattern). With the optimized pipeline it should rarely trigger.

## 9. Accessibility

- Semantic HTML: `<header>`, `<nav>`, `<main>` (added; not in the source), `<section>` with `aria-labelledby`, `<footer>`. Skip-to-content link as the first focusable element.
- All interactive elements have visible focus states (`outline: 2px solid var(--color-accent); outline-offset: 4px`).
- Locale toggle exposes `aria-current="true"` on the active locale; non-active locale has descriptive `aria-label="Switch to English"` / `"เปลี่ยนเป็นภาษาไทย"`.
- Decorative elements use `aria-hidden="true"` (the seal dot, the `今` watermark, the eyebrow rule).
- Color contrast: all body text against `--color-bg` exceeds 7:1 (AAA). Muted text exceeds 4.5:1 (AA). Verified against the OKLCH palette.
- `prefers-reduced-motion: reduce` disables the pulse animation.

## 10. Performance Budget

| Metric | Target |
|---|---|
| First HTML byte (Cloudflare edge) | < 200 ms |
| LCP (hero image) | < 2.0 s on Slow 4G |
| Total JS shipped | < 5 KB gzipped (the locale-detect script + LangToggle click handler only) |
| Total CSS shipped | < 20 KB gzipped (Tailwind purged + scoped component CSS) |
| Hero image (largest variant) | < 350 KB AVIF |
| Lighthouse | Perf ≥ 95, A11y ≥ 95, BP ≥ 95, SEO ≥ 95 |

## 11. SEO & Metadata

- Per-locale `<title>` and `<meta name="description">`.
- `<link rel="alternate" hreflang="th" href="https://wenfang.app/" />` and the EN equivalent on every page.
- `<link rel="canonical">` on each locale variant pointing to itself.
- Open Graph + Twitter Card tags with the inkwash hero as the preview image.
- `robots.txt` and a generated `sitemap.xml` (Astro's `@astrojs/sitemap` integration).
- Structured data: `WebSite` JSON-LD with `inLanguage` set per page.

## 12. Quality Gates

| Gate | Tool | When |
|---|---|---|
| Type check | `astro check` | Pre-commit + CI |
| Lint | ESLint (`eslint-plugin-astro`) | Pre-commit + CI |
| Format | Prettier (with `prettier-plugin-astro`) | Pre-commit |
| Build | `astro build` produces clean `dist/` | CI |
| Translation completeness | A custom `scripts/check-i18n.ts` ensures `th.json` and `en.json` have identical key sets | CI |
| Accessibility smoke | `axe-core` via Playwright on `/` and `/en/` | CI (optional first pass) |

## 13. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Source Han Serif SC unavailable on a visitor's device → Chinese characters fall back to a sans-serif and the aesthetic breaks | Subset the font to only the ~30 unique CJK glyphs the page renders and self-host. Estimated subset size 20–40 KB; verify during implementation and iterate if larger. |
| Auto-redirect causes a Thai user with English browser locale to land on `/en/` and be confused | The `LangToggle` is on every page; the redirect is a one-time event per browser session unless re-confirmed. The `localStorage` write makes the choice sticky. |
| Hero image is the page's heaviest asset and a Lighthouse blocker | Astro `<Image>` with AVIF/WebP variants + correct `sizes` attribute; preload the chosen variant. |
| Tailwind v4 is new; ecosystem plugin gaps | Stay vanilla — no third-party Tailwind plugins needed. The `@theme` tokens cover the design fully. |
| Translated copy is longer than English in some places (Thai often is) and breaks layout | All section heights are content-driven (no fixed heights). `text-wrap: balance/pretty` is preserved on headlines. Spot-check at 320/375/414 widths during implementation. |

## 14. Out of Scope (future specs)

- `/tools/flashcards` — Hanyu Jiaocheng vocabulary flashcards (consume `vocabs/*.csv`)
- `/tools/stroke-order` — character stroke playback (likely `hanzi-writer` library)
- Daily-rotating Today's Word from a content collection
- Newsletter / RSS feed
- Internationalized URL slugs for tool pages

## 15. Acceptance Criteria

The landing page is "done" when:

1. `/` renders the Thai landing page; `/en/` renders the English landing page; `/tools` and `/en/tools` render styled placeholders.
2. The masthead `LangToggle` switches between locales preserving the current page (e.g., `/tools` → `/en/tools`).
3. A first-time visitor with `navigator.language === 'en-US'` arriving at `/` is redirected to `/en/` before paint (no FOUC).
4. A visitor who clicks the toggle and reloads stays on their chosen locale on subsequent visits.
5. The page passes Lighthouse ≥ 95 on all four axes on a throttled mobile run.
6. Visual regression vs. `design/index.html` is intentional only — i.e. the only differences are i18n surface, the live `LangToggle`, the optimized hero image pipeline, and the auto-redirect script.
7. The page renders correctly at 320, 375, 768, 1024, 1280, 1920 widths.
8. `astro build` produces a deployable `dist/` with no warnings.
9. `scripts/check-i18n.ts` reports identical key sets in both dictionaries.
10. Deployed to Cloudflare Pages on a preview URL; production deploy is the user's call.
