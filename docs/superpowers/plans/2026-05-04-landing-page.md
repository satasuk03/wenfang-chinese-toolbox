# Wénfáng Landing Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a production-grade, bilingual (TH/EN), responsive landing page for 文房 Wénfáng to Cloudflare Pages, faithful to `design/index.html`.

**Architecture:** Astro 5 (static output) + Tailwind v4 + TypeScript. Path-based i18n with Thai at `/`, English at `/en/`. One `BaseLayout`, six discrete components (`Masthead`, `LangToggle`, `Hero`, `TodaysWord`, `Principles`, `Footer`, `Landing`), JSON dictionaries with a typed `t()` helper, inline pre-paint locale-detect script on root URLs.

**Tech Stack:** Astro 5, Tailwind v4 (`@tailwindcss/vite`), TypeScript (strict), ESLint, Prettier, `@astrojs/sitemap`, `astro-icon`-free (no icon lib needed), `@fontsource/...` for self-hosted fonts.

**Spec reference:** `docs/superpowers/specs/2026-05-04-landing-page-design.md`

---

## File Structure

```
wenfang-chinese-toolbox/
├── astro.config.mjs                  # Astro + i18n + sitemap config
├── tsconfig.json                     # TS strict
├── package.json
├── .eslintrc.cjs
├── .prettierrc
├── .gitignore
├── public/
│   └── favicon.svg
├── scripts/
│   └── check-i18n.ts                 # i18n key parity check
├── src/
│   ├── env.d.ts                      # Astro types
│   ├── i18n/
│   │   ├── th.json                   # Thai dictionary
│   │   ├── en.json                   # English dictionary
│   │   └── ui.ts                     # Locale, t(), getLocaleFromUrl(), localizedPath()
│   ├── styles/
│   │   └── global.css                # Tailwind import + @theme tokens + base
│   ├── assets/
│   │   └── hero-inkwash.png          # Copied from design/assets/
│   ├── layouts/
│   │   └── BaseLayout.astro          # html/head/body chrome, paper grain, locale script
│   └── components/
│       ├── Masthead.astro            # wordmark, nav, LangToggle, header-meta
│       ├── LangToggle.astro          # EN | ไทย toggle
│       ├── Hero.astro
│       ├── TodaysWord.astro
│       ├── Principles.astro
│       ├── Footer.astro
│       └── Landing.astro             # composes Hero + TodaysWord + Principles
└── src/pages/
    ├── index.astro                   # th landing
    ├── tools/index.astro             # th coming-soon
    └── en/
        ├── index.astro               # en landing
        └── tools/index.astro         # en coming-soon
```

---

## Task 1: Bootstrap project and install dependencies

**Files:**
- Create: `package.json`, `astro.config.mjs`, `tsconfig.json`, `.gitignore`, `src/env.d.ts`

- [ ] **Step 1: Initialize git and write .gitignore**

```bash
cd /Users/satasuk/Desktop/dev/wenfang-chinese-toolbox
git init
```

Create `.gitignore`:
```gitignore
# build
dist/
.astro/
.cache/

# deps
node_modules/

# env
.env
.env.local
.env.*.local

# editor / os
.DS_Store
.vscode/*
!.vscode/extensions.json
.idea/

# logs
npm-debug.log*
yarn-debug.log*
pnpm-debug.log*
```

- [ ] **Step 2: Initialize package.json**

```bash
npm init -y
```

Then edit `package.json` to set:
```json
{
  "name": "wenfang-chinese-toolbox",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "check": "astro check && tsc --noEmit",
    "lint": "eslint . --ext .ts,.astro",
    "format": "prettier --write .",
    "i18n:check": "tsx scripts/check-i18n.ts"
  }
}
```

- [ ] **Step 3: Install Astro, Tailwind v4, and TypeScript**

```bash
npm install astro@^5
npm install -D typescript @astrojs/check
npm install -D tailwindcss@^4 @tailwindcss/vite@^4
npm install -D @astrojs/sitemap
npm install -D tsx
```

- [ ] **Step 4: Install ESLint and Prettier**

```bash
npm install -D eslint eslint-plugin-astro @typescript-eslint/parser @typescript-eslint/eslint-plugin
npm install -D prettier prettier-plugin-astro
```

- [ ] **Step 5: Install fonts**

```bash
npm install @fontsource/ibm-plex-mono
```

(Source Han Serif SC subsetting is handled in Task 18; for now, system stacks suffice in development.)

- [ ] **Step 6: Create tsconfig.json**

```json
{
  "extends": "astro/tsconfigs/strict",
  "include": [".astro/types.d.ts", "**/*"],
  "exclude": ["dist"],
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "~/*": ["src/*"]
    }
  }
}
```

- [ ] **Step 7: Create src/env.d.ts**

```ts
/// <reference path="../.astro/types.d.ts" />
```

- [ ] **Step 8: Verify install**

```bash
npx astro --version
```

Expected: prints Astro version (5.x.x) without error.

- [ ] **Step 9: Commit**

```bash
git add .
git commit -m "chore: initialize Astro project with TypeScript and Tailwind v4"
```

---

## Task 2: Configure Astro with i18n routing

**Files:**
- Create: `astro.config.mjs`

- [ ] **Step 1: Write astro.config.mjs**

```js
// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://wenfang.app',
  output: 'static',
  trailingSlash: 'always',
  i18n: {
    defaultLocale: 'th',
    locales: ['th', 'en'],
    routing: { prefixDefaultLocale: false },
  },
  vite: {
    plugins: [tailwindcss()],
  },
  integrations: [
    sitemap({
      i18n: {
        defaultLocale: 'th',
        locales: { th: 'th-TH', en: 'en-US' },
      },
    }),
  ],
});
```

- [ ] **Step 2: Verify config parses**

```bash
npx astro check
```

Expected: completes without config errors. May print "no pages yet" — that's fine.

- [ ] **Step 3: Commit**

```bash
git add astro.config.mjs
git commit -m "chore: configure Astro i18n with Thai default and English at /en/"
```

---

## Task 3: Wire up Tailwind v4 with design tokens

**Files:**
- Create: `src/styles/global.css`

- [ ] **Step 1: Create src/styles/global.css**

```css
@import "tailwindcss";

@theme {
  /* Palette — OKLCH from design/index.html */
  --color-bg:           oklch(96.5% 0.013 80);
  --color-paper:        oklch(98.5% 0.008 80);
  --color-surface:      oklch(99.2% 0.005 80);
  --color-fg:           oklch(18% 0.018 60);
  --color-ink:          oklch(14% 0.02 60);
  --color-muted:        oklch(46% 0.014 55);
  --color-soft:         oklch(62% 0.012 55);
  --color-border:       oklch(86% 0.014 75);
  --color-rule:         oklch(78% 0.014 70);
  --color-accent:       oklch(50% 0.205 30);
  --color-accent-deep:  oklch(40% 0.21 30);
  --color-accent-soft:  oklch(94% 0.05 30);

  /* Typography */
  --font-display: 'Iowan Old Style', 'Charter', 'Source Han Serif SC', 'Songti SC', 'Times New Roman', Georgia, serif;
  --font-body:    -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', 'PingFang SC', 'Sukhumvit Set', 'Helvetica Neue Thai', system-ui, sans-serif;
  --font-zh:      'Source Han Serif SC', 'Songti SC', 'STSong', 'SimSun', serif;
  --font-mono:    'JetBrains Mono', 'IBM Plex Mono', ui-monospace, Menlo, monospace;

  /* Breakpoints — match design/index.html exactly */
  --breakpoint-sm: 560px;
  --breakpoint-md: 880px;
  --breakpoint-lg: 1080px;
}

/* Base resets (mirrors design/index.html) */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: var(--color-bg); color: var(--color-fg); }
body {
  font-family: var(--font-body);
  font-size: 17px;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  overflow-x: hidden;
}
img { display: block; max-width: 100%; }
a { color: inherit; text-decoration: none; }

/* Tabular numerals on metadata */
[class*="meta"], [class*="number"], [class*="count"], [class*="foot"],
.nav, .header-meta, .principles-list .num, .footer {
  font-variant-numeric: tabular-nums;
}

/* Visible focus for keyboard users */
:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 4px;
}

/* Skip link */
.skip-link {
  position: absolute;
  top: -100px;
  left: 1rem;
  background: var(--color-ink);
  color: var(--color-bg);
  padding: 0.5rem 1rem;
  z-index: 100;
  transition: top 0.15s ease;
}
.skip-link:focus { top: 1rem; }

/* Pulse animation (used by future Tools section) */
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.45; transform: scale(0.85); }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Container */
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 40px;
}
@media (max-width: 880px) { .container { padding: 0 28px; } }
@media (max-width: 560px) { .container { padding: 0 20px; } }
```

- [ ] **Step 2: Commit**

```bash
git add src/styles/global.css
git commit -m "feat(styles): add Tailwind v4 theme tokens and base styles"
```

---

## Task 4: Build the i18n helper module

**Files:**
- Create: `src/i18n/ui.ts`

- [ ] **Step 1: Write src/i18n/ui.ts**

```ts
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
 * Examples:
 *   localizedPath('en', '/')          -> '/en/'
 *   localizedPath('th', '/en/tools/') -> '/tools/'
 *   localizedPath('en', '/tools/')    -> '/en/tools/'
 */
export function localizedPath(target: Locale, currentPath: string): string {
  const stripped = currentPath.replace(/^\/en(\/|$)/, '/');
  if (target === 'th') return stripped;
  if (stripped === '/') return '/en/';
  return `/en${stripped}`;
}

/**
 * Pretty label for the locale (used in the toggle).
 */
export const localeLabel: Record<Locale, string> = {
  th: 'ไทย',
  en: 'EN',
};

/**
 * `<html lang>` value.
 */
export const htmlLang: Record<Locale, string> = {
  th: 'th',
  en: 'en',
};
```

- [ ] **Step 2: Commit**

```bash
git add src/i18n/ui.ts
git commit -m "feat(i18n): add typed t() helper and locale path utilities"
```

---

## Task 5: Author i18n dictionaries (EN authoritative, TH placeholders)

**Files:**
- Create: `src/i18n/en.json`
- Create: `src/i18n/th.json`

- [ ] **Step 1: Write src/i18n/en.json**

```json
{
  "meta": {
    "title": "文房 — Wénfáng · Quiet tools for studying Chinese.",
    "description": "A small library of focused, single-purpose tools for students of Chinese — Hanyu Jiaocheng flashcards and stroke-order playback."
  },
  "skip": "Skip to main content",
  "nav": {
    "home": "Home",
    "tools": "Tools",
    "about": "About",
    "contact": "Contact"
  },
  "headerMeta": {
    "left": "Free & open",
    "right": "Made by Zeze"
  },
  "hero": {
    "eyebrow": "The Studio",
    "eyebrowVol": "Vol. 01",
    "headlinePre": "Quiet tools for studying ",
    "headlineEm": "Chinese.",
    "deck": "A small library of focused, single-purpose instruments — <b>flashcards bound to the textbook on your shelf</b>, stroke-order playback for any character you can paste in. Built slowly, kept honest, kept free.",
    "metaToolsLabel": "Tools",
    "metaToolsValue": "Two",
    "metaLevelsLabel": "Levels",
    "metaLevelsValue": "HSK 1–6",
    "metaCostLabel": "Cost",
    "metaCostValue": "None",
    "imageAlt": "Inkwash brush painting of a young xian-style scholar standing on a misty mountain peak",
    "imageCaptionLeft": "Plate I.",
    "imageCaptionRight": "Mountain · Inkwash · 2026"
  },
  "tip": {
    "eyebrow": "今日一語 · Today's word",
    "translation": "The sea of learning has no shore.",
    "noteHtml": "From a couplet attributed to the Tang scholar <em>韩愈</em> (Han Yu, 768–824). The full saying — <em>学海无涯苦作舟</em> — \"the sea of learning has no shore; let toil be your boat\" — has been a refrain for Chinese students for a thousand years. A useful thing to keep on the wall above a desk.",
    "footerLeft": "Tip 001",
    "footerRight": "Refreshes daily"
  },
  "principles": {
    "eyebrow": "— On the studio",
    "headlinePre": "Built like a stationery shop, not ",
    "headlineEm": "a startup.",
    "items": [
      {
        "title": "One thing per tool.",
        "body": "Each instrument does a single job and stops. No accounts, no streaks, no leaderboard. The textbook on your shelf already sets the curriculum."
      },
      {
        "title": "Match the textbook.",
        "body": "Cards are bound to the exact vocabulary list of <em>Hanyu Jiaocheng</em> volumes 1A through 3B. The tool follows your study, not its own."
      },
      {
        "title": "Honest defaults.",
        "body": "If we don't have stroke data for a character, we say so plainly. A short, true note is worth more than a generated GIF that's wrong."
      },
      {
        "title": "Quiet on the page.",
        "body": "No popovers, no notifications, no banner ads, no dark patterns. Cream paper, one accent, generous margins. Study in peace."
      }
    ]
  },
  "footer": {
    "year": "2026",
    "linkX": "X",
    "handleX": "@ItsmeZecreto",
    "linkPortfolio": "Portfolio",
    "handlePortfolio": "zeze.app"
  },
  "comingSoon": {
    "title": "Tools — coming soon",
    "body": "The studio is still being arranged. Flashcards and stroke-order playback are next. Check back, or ",
    "back": "return home."
  }
}
```

- [ ] **Step 2: Write src/i18n/th.json with the same key shape**

```json
{
  "meta": {
    "title": "文房 — Wénfáng · เครื่องมือเงียบ ๆ สำหรับเรียนภาษาจีน",
    "description": "ห้องสมุดเล็ก ๆ ของเครื่องมือเฉพาะทางสำหรับผู้เรียนภาษาจีน — แฟลชการ์ด Hanyu Jiaocheng และลำดับการเขียนตัวอักษร"
  },
  "skip": "ข้ามไปยังเนื้อหาหลัก",
  "nav": {
    "home": "หน้าแรก",
    "tools": "เครื่องมือ",
    "about": "เกี่ยวกับ",
    "contact": "ติดต่อ"
  },
  "headerMeta": {
    "left": "ฟรี · โอเพนซอร์ส",
    "right": "โดย Zeze"
  },
  "hero": {
    "eyebrow": "ห้องเรียน",
    "eyebrowVol": "เล่มที่ 01",
    "headlinePre": "เครื่องมือเงียบ ๆ สำหรับเรียน",
    "headlineEm": "ภาษาจีน",
    "deck": "ห้องสมุดเล็ก ๆ ของเครื่องมือเฉพาะทาง — <b>แฟลชการ์ดที่ผูกกับตำราเรียนบนชั้นของคุณ</b> และการเล่นลำดับการเขียนสำหรับตัวอักษรใดก็ตามที่คุณวางลงไป สร้างอย่างช้า ๆ เก็บไว้อย่างซื่อสัตย์ และให้ใช้ฟรี",
    "metaToolsLabel": "เครื่องมือ",
    "metaToolsValue": "สอง",
    "metaLevelsLabel": "ระดับ",
    "metaLevelsValue": "HSK 1–6",
    "metaCostLabel": "ค่าใช้จ่าย",
    "metaCostValue": "ฟรี",
    "imageAlt": "ภาพวาดพู่กันน้ำหมึกของบัณฑิตหนุ่มในชุดเซียนยืนอยู่บนยอดเขาในม่านหมอก",
    "imageCaptionLeft": "ภาพที่ 1",
    "imageCaptionRight": "ภูเขา · ภาพหมึก · 2026"
  },
  "tip": {
    "eyebrow": "今日一語 · คำของวันนี้",
    "translation": "ทะเลแห่งการเรียนรู้ไม่มีฝั่ง",
    "noteHtml": "จากคำกลอนคู่ของบัณฑิตในยุคถัง <em>韩愈</em> (หาน อวี้, 768–824) คำเต็มของบทกวีคือ <em>学海无涯苦作舟</em> — \"ทะเลแห่งการเรียนรู้ไม่มีฝั่ง ให้ความเพียรเป็นเรือของคุณ\" — เป็นคำที่นักเรียนจีนกล่าวซ้ำมาแล้วเป็นพันปี เหมาะที่จะแขวนไว้เหนือโต๊ะทำงาน",
    "footerLeft": "เคล็ดลับ 001",
    "footerRight": "เปลี่ยนทุกวัน"
  },
  "principles": {
    "eyebrow": "— เกี่ยวกับสตูดิโอ",
    "headlinePre": "สร้างเหมือนร้านเครื่องเขียน ไม่ใช่",
    "headlineEm": "สตาร์ทอัพ",
    "items": [
      {
        "title": "หนึ่งเครื่องมือ หนึ่งหน้าที่",
        "body": "เครื่องมือแต่ละชิ้นทำงานเดียวแล้วจบ ไม่มีบัญชี ไม่มีสตรีค ไม่มีลีดเดอร์บอร์ด ตำราเรียนบนชั้นของคุณกำหนดหลักสูตรอยู่แล้ว"
      },
      {
        "title": "ตรงกับตำราเรียน",
        "body": "การ์ดถูกผูกกับรายการคำศัพท์ของ <em>Hanyu Jiaocheng</em> เล่ม 1A ถึง 3B ตรงเป๊ะ เครื่องมือตามการเรียนของคุณ ไม่ใช่ตามของมันเอง"
      },
      {
        "title": "ค่าตั้งต้นที่ซื่อสัตย์",
        "body": "ถ้าเราไม่มีข้อมูลลำดับการเขียนสำหรับตัวอักษรใด เราก็บอกตรง ๆ หมายเหตุสั้น ๆ ที่จริงนั้นมีค่ามากกว่า GIF ที่สร้างขึ้นแต่ผิด"
      },
      {
        "title": "เงียบบนหน้ากระดาษ",
        "body": "ไม่มีป๊อปอัป ไม่มีการแจ้งเตือน ไม่มีโฆษณาแบนเนอร์ ไม่มีดาร์กแพทเทิร์น กระดาษสีครีม สีเน้นเดียว ระยะขอบใจกว้าง อ่านอย่างสงบ"
      }
    ]
  },
  "footer": {
    "year": "2026",
    "linkX": "X",
    "handleX": "@ItsmeZecreto",
    "linkPortfolio": "Portfolio",
    "handlePortfolio": "zeze.app"
  },
  "comingSoon": {
    "title": "เครื่องมือ — เร็ว ๆ นี้",
    "body": "สตูดิโอยังจัดเตรียมไม่เสร็จ แฟลชการ์ดและการเล่นลำดับการเขียนกำลังตามมา กลับมาดูใหม่ได้ หรือ",
    "back": "กลับหน้าแรก"
  }
}
```

> **Note for the implementer:** Thai copy is a faithful first pass. The user (Thai native speaker) will refine before launch. Do not rewrite the Thai copy on your own initiative — flag any phrases you suspect are awkward and let the user adjust.

- [ ] **Step 3: Commit**

```bash
git add src/i18n/en.json src/i18n/th.json
git commit -m "feat(i18n): add Thai and English landing dictionaries"
```

---

## Task 6: i18n key parity check script

**Files:**
- Create: `scripts/check-i18n.ts`

- [ ] **Step 1: Write scripts/check-i18n.ts**

```ts
#!/usr/bin/env tsx
import th from '../src/i18n/th.json' with { type: 'json' };
import en from '../src/i18n/en.json' with { type: 'json' };

type Json = string | number | boolean | null | Json[] | { [k: string]: Json };

function flatten(obj: Json, prefix = ''): string[] {
  if (Array.isArray(obj)) {
    return obj.flatMap((item, i) => flatten(item as Json, `${prefix}[${i}]`));
  }
  if (obj && typeof obj === 'object') {
    return Object.entries(obj).flatMap(([k, v]) =>
      flatten(v as Json, prefix ? `${prefix}.${k}` : k),
    );
  }
  return [prefix];
}

const thKeys = new Set(flatten(th as Json));
const enKeys = new Set(flatten(en as Json));

const missingInTh = [...enKeys].filter((k) => !thKeys.has(k));
const missingInEn = [...thKeys].filter((k) => !enKeys.has(k));

if (missingInTh.length || missingInEn.length) {
  if (missingInTh.length) {
    console.error('Missing in th.json:');
    missingInTh.forEach((k) => console.error(`  ${k}`));
  }
  if (missingInEn.length) {
    console.error('Missing in en.json:');
    missingInEn.forEach((k) => console.error(`  ${k}`));
  }
  process.exit(1);
}

console.log(`✓ i18n parity OK (${thKeys.size} keys × 2 locales)`);
```

- [ ] **Step 2: Run the parity check**

```bash
npm run i18n:check
```

Expected output: `✓ i18n parity OK (NN keys × 2 locales)`

If it fails, fix the dictionary that's missing a key, then re-run until it passes.

- [ ] **Step 3: Commit**

```bash
git add scripts/check-i18n.ts
git commit -m "chore(i18n): add key parity check script"
```

---

## Task 7: BaseLayout with paper grain and locale-detect script

**Files:**
- Create: `src/layouts/BaseLayout.astro`

- [ ] **Step 1: Write src/layouts/BaseLayout.astro**

```astro
---
import '../styles/global.css';
import '@fontsource/ibm-plex-mono/400.css';
import '@fontsource/ibm-plex-mono/500.css';
import { type Locale, htmlLang, t } from '../i18n/ui';

interface Props {
  locale: Locale;
  title?: string;
  description?: string;
  /**
   * If true, embeds the pre-paint locale auto-redirect script.
   * Should only be true on Thai (default) routes.
   */
  enableLocaleDetect?: boolean;
  /**
   * Path on the EN side that mirrors this page (used for hreflang link tags).
   */
  alternates?: { th: string; en: string };
}

const {
  locale,
  title = t(locale, 'meta.title'),
  description = t(locale, 'meta.description'),
  enableLocaleDetect = false,
  alternates,
} = Astro.props;

const canonical = new URL(Astro.url.pathname, Astro.site).toString();
const ogImage = new URL('/og.png', Astro.site).toString();
---

<!doctype html>
<html lang={htmlLang[locale]}>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <meta name="description" content={description} />
    <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
    <link rel="canonical" href={canonical} />
    {alternates && (
      <>
        <link rel="alternate" hreflang="th" href={new URL(alternates.th, Astro.site).toString()} />
        <link rel="alternate" hreflang="en" href={new URL(alternates.en, Astro.site).toString()} />
        <link rel="alternate" hreflang="x-default" href={new URL(alternates.th, Astro.site).toString()} />
      </>
    )}
    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:type" content="website" />
    <meta property="og:url" content={canonical} />
    <meta property="og:image" content={ogImage} />
    <meta name="twitter:card" content="summary_large_image" />

    {enableLocaleDetect && (
      <script is:inline>
        (function(){
          try {
            var stored = localStorage.getItem('wf_locale');
            if (stored === 'en') { location.replace(location.pathname.replace(/^\//, '/en/')); return; }
            if (stored === 'th') return;
            var nav = (navigator.language || navigator.userLanguage || '').toLowerCase();
            if (nav.indexOf('en') === 0) {
              location.replace(location.pathname === '/' ? '/en/' : ('/en' + location.pathname));
            }
          } catch (e) { /* storage blocked — degrade silently */ }
        })();
      </script>
    )}
  </head>
  <body>
    <a href="#main" class="skip-link">{t(locale, 'skip')}</a>
    <slot />

    <style>
      /* Paper grain — fixed on viewport, multiply blend, very subtle */
      body::before {
        content: '';
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image:
          radial-gradient(oklch(30% 0.02 60 / 0.025) 1px, transparent 1.2px);
        background-size: 3px 3px;
        z-index: 1;
        mix-blend-mode: multiply;
      }
    </style>
  </body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add src/layouts/BaseLayout.astro
git commit -m "feat(layout): add BaseLayout with paper grain and locale-detect script"
```

---

## Task 8: LangToggle component

**Files:**
- Create: `src/components/LangToggle.astro`

- [ ] **Step 1: Write src/components/LangToggle.astro**

```astro
---
import { type Locale, localizedPath, localeLabel } from '../i18n/ui';

interface Props {
  locale: Locale;
  currentPath: string;
}

const { locale, currentPath } = Astro.props;
const otherLocale: Locale = locale === 'th' ? 'en' : 'th';
const otherPath = localizedPath(otherLocale, currentPath);
---

<div class="lang-toggle" role="group" aria-label="Language">
  <span class="lang-current" aria-current="true">{localeLabel[locale]}</span>
  <span class="lang-sep" aria-hidden="true">/</span>
  <a
    class="lang-other"
    href={otherPath}
    aria-label={otherLocale === 'en' ? 'Switch to English' : 'เปลี่ยนเป็นภาษาไทย'}
    data-lang-target={otherLocale}
  >
    {localeLabel[otherLocale]}
  </a>
</div>

<script>
  document.querySelectorAll<HTMLAnchorElement>('a.lang-other').forEach((a) => {
    a.addEventListener('click', () => {
      const target = a.dataset.langTarget;
      if (target === 'th' || target === 'en') {
        try { localStorage.setItem('wf_locale', target); } catch {}
      }
    });
  });
</script>

<style>
  .lang-toggle {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
  }
  .lang-current { color: var(--color-ink); }
  .lang-sep    { color: var(--color-border); }
  .lang-other  {
    color: var(--color-muted);
    transition: color 0.15s ease;
  }
  .lang-other:hover { color: var(--color-accent); }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/LangToggle.astro
git commit -m "feat(i18n): add LangToggle component"
```

---

## Task 9: Masthead component (wordmark, nav, header-meta)

**Files:**
- Create: `src/components/Masthead.astro`

- [ ] **Step 1: Write src/components/Masthead.astro**

```astro
---
import LangToggle from './LangToggle.astro';
import { type Locale, t, localizedPath } from '../i18n/ui';

interface Props {
  locale: Locale;
  currentPath: string;
}

const { locale, currentPath } = Astro.props;

// Localize internal links to the active locale
const homeHref = '#top';
const toolsHref = localizedPath(locale, '/tools/');
const aboutHref = '#about';
const contactHref = '#contact';
---

<header class="masthead" id="top">
  <div class="container masthead-inner">
    <a href={localizedPath(locale, '/')} class="wordmark" aria-label="Wénfáng — home">
      <span class="wordmark-cn">文房</span>
      <span class="wordmark-en">Wén<em>fáng</em> · Studio</span>
    </a>
    <nav class="nav" aria-label="Primary">
      <a href={homeHref} class="dot">{t(locale, 'nav.home')}</a>
      <a href={toolsHref}>{t(locale, 'nav.tools')}</a>
      <a href={aboutHref}>{t(locale, 'nav.about')}</a>
      <a href={contactHref}>{t(locale, 'nav.contact')}</a>
      <LangToggle locale={locale} currentPath={currentPath} />
    </nav>
    <div class="nav-mobile">
      <LangToggle locale={locale} currentPath={currentPath} />
    </div>
  </div>
  <div class="header-meta">
    <div class="container header-meta-inner">
      <span>{t(locale, 'headerMeta.left')}</span>
      <div class="right">
        <span>{t(locale, 'headerMeta.right')}</span>
      </div>
    </div>
  </div>
</header>

<style>
  .masthead {
    border-bottom: 1px solid var(--color-border);
    position: relative;
    z-index: 2;
    background: var(--color-bg);
  }
  .masthead-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 22px 0;
  }
  .wordmark { display: flex; align-items: baseline; gap: 14px; }
  .wordmark-cn {
    font-family: var(--font-zh);
    font-size: 28px;
    color: var(--color-ink);
    letter-spacing: 0.04em;
    line-height: 1;
  }
  .wordmark-en {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--color-muted);
    padding-left: 14px;
    border-left: 1px solid var(--color-border);
  }
  .wordmark-en em { font-style: italic; color: var(--color-fg); }

  .nav { display: flex; gap: 36px; align-items: center; }
  .nav a {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--color-fg);
    transition: color 0.15s ease;
  }
  .nav a:hover { color: var(--color-accent); }
  .nav a.dot::before {
    content: '';
    display: inline-block;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--color-accent);
    margin-right: 8px;
    vertical-align: middle;
    transform: translateY(-1px);
  }

  .nav-mobile { display: none; }

  .header-meta {
    border-top: 1px solid var(--color-border);
    border-bottom: 1px solid var(--color-border);
    font-family: var(--font-mono);
    font-size: 10.5px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--color-muted);
    padding: 9px 0;
  }
  .header-meta-inner {
    display: flex;
    justify-content: space-between;
    gap: 24px;
  }

  @media (max-width: 560px) {
    .nav { display: none; }
    .nav-mobile { display: flex; }
    .header-meta { display: none; }
  }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/Masthead.astro
git commit -m "feat(masthead): add header with wordmark, nav, and language toggle"
```

---

## Task 10: Hero component (text + image)

**Files:**
- Create: `src/components/Hero.astro`
- Copy: `design/assets/hero-inkwash.png` → `src/assets/hero-inkwash.png`

- [ ] **Step 1: Copy the hero image into src/assets/**

```bash
mkdir -p src/assets
cp design/assets/hero-inkwash.png src/assets/hero-inkwash.png
```

- [ ] **Step 2: Write src/components/Hero.astro**

```astro
---
import { Image } from 'astro:assets';
import heroImage from '../assets/hero-inkwash.png';
import { type Locale, t } from '../i18n/ui';

interface Props {
  locale: Locale;
}

const { locale } = Astro.props;
---

<section class="hero">
  <div class="container hero-inner">
    <div class="hero-text">
      <p class="hero-eyebrow">
        <span>{t(locale, 'hero.eyebrow')}</span>
        <span>·</span>
        <span class="accent">{t(locale, 'hero.eyebrowVol')}</span>
      </p>
      <h1 class="hero-headline">
        {t(locale, 'hero.headlinePre')}<em>{t(locale, 'hero.headlineEm')}</em>
      </h1>
      <p class="hero-deck" set:html={t(locale, 'hero.deck')} />
      <dl class="hero-meta">
        <div><dt>{t(locale, 'hero.metaToolsLabel')}</dt><dd>{t(locale, 'hero.metaToolsValue')}</dd></div>
        <div><dt>{t(locale, 'hero.metaLevelsLabel')}</dt><dd>{t(locale, 'hero.metaLevelsValue')}</dd></div>
        <div><dt>{t(locale, 'hero.metaCostLabel')}</dt><dd>{t(locale, 'hero.metaCostValue')}</dd></div>
      </dl>
    </div>
    <figure class="hero-image">
      <div class="hero-image-frame">
        <Image
          src={heroImage}
          alt={t(locale, 'hero.imageAlt')}
          widths={[440, 600, 800, 1200]}
          sizes="(max-width: 560px) 90vw, (max-width: 880px) 440px, (max-width: 1080px) 460px, 540px"
          format="avif"
          fallbackFormat="webp"
          loading="eager"
          fetchpriority="high"
          class="hero-img"
        />
      </div>
      <figcaption class="hero-image-caption">
        <span>{t(locale, 'hero.imageCaptionLeft')}</span>
        <span>{t(locale, 'hero.imageCaptionRight')}</span>
      </figcaption>
    </figure>
  </div>
</section>

<style>
  .hero { position: relative; padding: 96px 0 120px; }
  .hero-inner {
    display: grid;
    grid-template-columns: 1.15fr 1fr;
    gap: 72px;
    align-items: end;
  }
  .hero-text { padding-bottom: 18px; max-width: 640px; }
  .hero-eyebrow {
    display: flex;
    align-items: center;
    gap: 14px;
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--color-muted);
    margin-bottom: 36px;
  }
  .hero-eyebrow::before {
    content: '';
    width: 38px;
    height: 1px;
    background: var(--color-accent);
    display: inline-block;
  }
  .hero-eyebrow .accent { color: var(--color-accent); }

  .hero-headline {
    font-family: var(--font-display);
    font-size: clamp(48px, 6.6vw, 104px);
    line-height: 0.96;
    letter-spacing: -0.025em;
    color: var(--color-ink);
    text-wrap: balance;
    margin-bottom: 36px;
    font-weight: 400;
  }
  .hero-headline em {
    font-style: italic;
    color: var(--color-accent);
  }

  .hero-deck {
    font-size: 19px;
    line-height: 1.6;
    color: var(--color-muted);
    max-width: 42ch;
    margin-bottom: 48px;
    text-wrap: pretty;
  }
  .hero-deck :global(b) { color: var(--color-fg); font-weight: 500; }

  .hero-meta {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border-top: 1px solid var(--color-border);
    padding-top: 18px;
    max-width: 480px;
  }
  .hero-meta dt {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--color-muted);
    margin-bottom: 6px;
  }
  .hero-meta dd {
    font-family: var(--font-display);
    font-size: 18px;
    color: var(--color-ink);
    font-style: italic;
  }

  .hero-image { position: relative; align-self: end; }
  .hero-image-frame {
    position: relative;
    background: var(--color-paper);
    border: 1px solid var(--color-border);
    overflow: hidden;
    aspect-ratio: 2 / 3;
  }
  .hero-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center center;
  }
  .hero-image-caption {
    margin-top: 14px;
    font-family: var(--font-mono);
    font-size: 10.5px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--color-muted);
    display: flex;
    justify-content: space-between;
  }

  @media (max-width: 1080px) {
    .hero { padding: 72px 0 96px; }
    .hero-inner { gap: 48px; }
  }
  @media (max-width: 880px) {
    .hero { padding: 56px 0 72px; }
    .hero-inner { grid-template-columns: 1fr; gap: 48px; }
    .hero-image { order: -1; max-width: 440px; }
    .hero-text { padding-bottom: 0; }
  }
  @media (max-width: 560px) {
    .hero-eyebrow { flex-wrap: wrap; gap: 10px; margin-bottom: 24px; }
    .hero-eyebrow::before { width: 24px; }
    .hero-headline { margin-bottom: 24px; }
    .hero-deck { font-size: 17px; margin-bottom: 32px; }
    .hero-meta { grid-template-columns: 1fr 1fr; row-gap: 16px; max-width: none; }
  }
</style>
```

- [ ] **Step 3: Commit**

```bash
git add src/components/Hero.astro src/assets/hero-inkwash.png
git commit -m "feat(hero): add Hero component with optimized inkwash image"
```

---

## Task 11: TodaysWord component (calligraphic tip section)

**Files:**
- Create: `src/components/TodaysWord.astro`

- [ ] **Step 1: Write src/components/TodaysWord.astro**

```astro
---
import { type Locale, t } from '../i18n/ui';

interface Props {
  locale: Locale;
}

const { locale } = Astro.props;
---

<section class="tip" id="tip">
  <div class="container tip-inner">
    <p class="tip-eyebrow">{t(locale, 'tip.eyebrow')}</p>
    <h2 class="tip-display">
      <span class="syl">学</span><span class="syl">海</span><span class="syl">无</span><span class="syl">涯</span>
    </h2>
    <p class="tip-pinyin">xué hǎi wú yá</p>
    <p class="tip-translation">{t(locale, 'tip.translation')}</p>
    <p class="tip-note" set:html={t(locale, 'tip.noteHtml')} />
    <p class="tip-meta">
      <span class="accent-dot" aria-hidden="true"></span>
      {t(locale, 'tip.footerLeft')}
      <span>·</span>
      {t(locale, 'tip.footerRight')}
    </p>
  </div>
</section>

<style>
  .tip {
    position: relative;
    background: var(--color-paper);
    border-top: 1px solid var(--color-border);
    border-bottom: 1px solid var(--color-border);
    padding: 96px 0 104px;
  }
  .tip::before {
    content: '今';
    position: absolute;
    top: 24px;
    left: 50%;
    transform: translateX(-50%);
    font-family: var(--font-zh);
    font-size: 240px;
    line-height: 1;
    color: oklch(40% 0.02 60 / 0.025);
    pointer-events: none;
    z-index: 0;
  }
  .tip-inner {
    position: relative;
    z-index: 1;
    text-align: center;
    max-width: 760px;
    margin: 0 auto;
  }
  .tip-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 14px;
    font-family: var(--font-mono);
    font-size: 10.5px;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: var(--color-accent);
    margin-bottom: 40px;
  }
  .tip-eyebrow::before, .tip-eyebrow::after {
    content: '';
    width: 44px;
    height: 1px;
    background: currentColor;
  }
  .tip-display {
    font-family: var(--font-zh);
    font-size: clamp(80px, 11vw, 168px);
    line-height: 1;
    letter-spacing: 0.06em;
    color: var(--color-ink);
    margin-bottom: 32px;
    font-weight: 400;
  }
  .tip-display .syl { display: inline-block; }
  .tip-pinyin {
    font-family: var(--font-display);
    font-style: italic;
    font-size: clamp(20px, 2vw, 26px);
    color: var(--color-muted);
    margin-bottom: 28px;
    letter-spacing: 0.08em;
  }
  .tip-translation {
    font-family: var(--font-display);
    font-size: clamp(22px, 2.4vw, 30px);
    line-height: 1.35;
    font-style: italic;
    color: var(--color-fg);
    margin-bottom: 36px;
    text-wrap: balance;
  }
  .tip-translation::before, .tip-translation::after {
    color: var(--color-accent);
    font-style: normal;
    font-weight: 500;
  }
  .tip-translation::before { content: '“ '; }
  .tip-translation::after  { content: ' ”'; }
  .tip-note {
    max-width: 54ch;
    margin: 0 auto 32px;
    font-size: 16px;
    line-height: 1.7;
    color: var(--color-muted);
    text-wrap: pretty;
  }
  .tip-note :global(em) {
    font-family: var(--font-zh);
    font-style: normal;
    color: var(--color-fg);
  }
  .tip-meta {
    display: inline-flex;
    gap: 18px;
    align-items: center;
    font-family: var(--font-mono);
    font-size: 10.5px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--color-muted);
    border-top: 1px solid var(--color-border);
    padding-top: 18px;
  }
  .tip-meta .accent-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--color-accent);
    display: inline-block;
  }

  @media (max-width: 880px) {
    .tip { padding: 72px 0 80px; }
    .tip::before { font-size: 160px; }
  }
  @media (max-width: 560px) {
    .tip-display { letter-spacing: 0.04em; }
  }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/TodaysWord.astro
git commit -m "feat(tip): add TodaysWord component with 今 watermark"
```

---

## Task 12: Principles component

**Files:**
- Create: `src/components/Principles.astro`

- [ ] **Step 1: Write src/components/Principles.astro**

```astro
---
import { type Locale, t, tArray } from '../i18n/ui';

interface Props {
  locale: Locale;
}

const { locale } = Astro.props;
const items = tArray<{ title: string; body: string }>(locale, 'principles.items');
---

<section class="principles" id="about">
  <div class="container principles-inner">
    <div>
      <p class="principles-eyebrow">{t(locale, 'principles.eyebrow')}</p>
      <h2>
        {t(locale, 'principles.headlinePre')}<em>{t(locale, 'principles.headlineEm')}</em>
      </h2>
    </div>
    <ol class="principles-list">
      {items.map((item, i) => (
        <li>
          <span class="num">— {String(i + 1).padStart(2, '0')}</span>
          <h4>{item.title}</h4>
          <p set:html={item.body} />
        </li>
      ))}
    </ol>
  </div>
</section>

<style>
  .principles {
    border-top: 1px solid var(--color-border);
    background: var(--color-bg);
    padding: 80px 0;
  }
  .principles-inner {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 80px;
    align-items: start;
  }
  .principles-eyebrow {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--color-accent);
    margin-bottom: 14px;
  }
  .principles h2 {
    font-family: var(--font-display);
    font-size: clamp(30px, 3.2vw, 44px);
    line-height: 1.05;
    letter-spacing: -0.02em;
    color: var(--color-ink);
    font-weight: 400;
    text-wrap: balance;
  }
  .principles h2 em { color: var(--color-accent); font-style: italic; }
  .principles-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    column-gap: 48px;
    row-gap: 40px;
    list-style: none;
  }
  .principles-list li { position: relative; padding-left: 48px; }
  .principles-list .num {
    position: absolute;
    left: 0;
    top: 2px;
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 0.18em;
    color: var(--color-accent);
  }
  .principles-list h4 {
    font-family: var(--font-display);
    font-size: 21px;
    line-height: 1.25;
    color: var(--color-ink);
    margin-bottom: 8px;
    font-weight: 500;
  }
  .principles-list p {
    font-size: 15px;
    line-height: 1.6;
    color: var(--color-muted);
    text-wrap: pretty;
  }
  .principles-list :global(em) {
    font-family: var(--font-zh);
    font-style: normal;
    color: var(--color-fg);
  }

  @media (max-width: 1080px) { .principles-inner { gap: 48px; } }
  @media (max-width: 880px) {
    .principles-inner { grid-template-columns: 1fr; gap: 32px; }
    .principles-list { grid-template-columns: 1fr; row-gap: 28px; }
  }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/Principles.astro
git commit -m "feat(principles): add Principles component"
```

---

## Task 13: Footer component

**Files:**
- Create: `src/components/Footer.astro`

- [ ] **Step 1: Write src/components/Footer.astro**

```astro
---
import { type Locale, t } from '../i18n/ui';

interface Props {
  locale: Locale;
}

const { locale } = Astro.props;
---

<footer class="footer" id="contact">
  <div class="container footer-inner">
    <span class="copyright">
      <span class="small-seal" aria-hidden="true"></span>
      <em>Wénfáng</em>© {t(locale, 'footer.year')}
    </span>
    <div class="footer-social">
      <a href="https://x.com/ItsmeZecreto" target="_blank" rel="noopener noreferrer">
        {t(locale, 'footer.linkX')} — <span class="handle">{t(locale, 'footer.handleX')}</span>
      </a>
      <a href="https://zeze.app/portfolio" target="_blank" rel="noopener noreferrer">
        {t(locale, 'footer.linkPortfolio')} — <span class="handle">{t(locale, 'footer.handlePortfolio')}</span>
      </a>
    </div>
  </div>
</footer>

<style>
  .footer {
    border-top: 1.5px solid var(--color-ink);
    padding: 32px 0;
    font-family: var(--font-mono);
    font-size: 10.5px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--color-muted);
  }
  .footer-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 14px;
  }
  .copyright em {
    font-style: italic;
    color: var(--color-fg);
    text-transform: none;
    letter-spacing: 0;
    font-family: var(--font-display);
    margin-right: 6px;
  }
  .small-seal {
    display: inline-block;
    width: 14px;
    height: 14px;
    background: var(--color-accent);
    margin-right: 8px;
    transform: translateY(2px) rotate(-3deg);
  }
  .footer-social {
    display: flex;
    gap: 28px;
    align-items: center;
  }
  .footer-social a {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: var(--color-muted);
    transition: color 0.15s ease;
  }
  .footer-social a:hover { color: var(--color-accent); }
  .footer-social a::before {
    content: '';
    display: inline-block;
    width: 5px;
    height: 5px;
    background: currentColor;
    transform: rotate(45deg);
    opacity: 0.6;
  }
  .footer-social a span.handle {
    font-family: var(--font-display);
    font-style: italic;
    text-transform: none;
    letter-spacing: 0;
    color: var(--color-fg);
    font-size: 13px;
  }
  .footer-social a:hover span.handle { color: var(--color-accent); }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add src/components/Footer.astro
git commit -m "feat(footer): add Footer with copyright and social links"
```

---

## Task 14: Landing composition + page files

**Files:**
- Create: `src/components/Landing.astro`
- Create: `src/pages/index.astro` (Thai)
- Create: `src/pages/en/index.astro` (English)

- [ ] **Step 1: Write src/components/Landing.astro**

```astro
---
import Hero from './Hero.astro';
import TodaysWord from './TodaysWord.astro';
import Principles from './Principles.astro';
import { type Locale } from '../i18n/ui';

interface Props {
  locale: Locale;
}

const { locale } = Astro.props;
---

<Hero locale={locale} />
<TodaysWord locale={locale} />
<Principles locale={locale} />
```

- [ ] **Step 2: Write src/pages/index.astro (Thai default)**

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import Masthead from '../components/Masthead.astro';
import Footer from '../components/Footer.astro';
import Landing from '../components/Landing.astro';

const locale = 'th' as const;
const currentPath = '/';
---

<BaseLayout
  locale={locale}
  enableLocaleDetect
  alternates={{ th: '/', en: '/en/' }}
>
  <Masthead locale={locale} currentPath={currentPath} />
  <main id="main">
    <Landing locale={locale} />
  </main>
  <Footer locale={locale} />
</BaseLayout>
```

- [ ] **Step 3: Write src/pages/en/index.astro**

```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import Masthead from '../../components/Masthead.astro';
import Footer from '../../components/Footer.astro';
import Landing from '../../components/Landing.astro';

const locale = 'en' as const;
const currentPath = '/en/';
---

<BaseLayout
  locale={locale}
  alternates={{ th: '/', en: '/en/' }}
>
  <Masthead locale={locale} currentPath={currentPath} />
  <main id="main">
    <Landing locale={locale} />
  </main>
  <Footer locale={locale} />
</BaseLayout>
```

- [ ] **Step 4: Run dev server and verify**

```bash
npm run dev
```

Open both URLs in a browser:
- http://localhost:4321/ — Thai landing page
- http://localhost:4321/en/ — English landing page

Manual verification:
- Wordmark `文房` displays in serif Chinese
- Hero headline renders with the colored accent on the translated word
- Hero image loads (no broken icon)
- "Today's word" section shows `学海无涯` with the `今` watermark
- Principles section lists 4 items with — 01, — 02, — 03, — 04 markers
- Footer shows copyright and social links
- Language toggle in masthead nav switches between `/` and `/en/`
- Resize browser to 320, 560, 880, 1080 widths — layout adapts at each breakpoint
- Mobile: nav hides, lang toggle remains visible

Stop the dev server (`Ctrl+C`).

- [ ] **Step 5: Commit**

```bash
git add src/components/Landing.astro src/pages/index.astro src/pages/en/index.astro
git commit -m "feat(landing): wire up th and en landing pages"
```

---

## Task 15: Coming-soon /tools placeholder pages

**Files:**
- Create: `src/pages/tools/index.astro` (Thai)
- Create: `src/pages/en/tools/index.astro` (English)
- Create: `src/components/ComingSoon.astro`

- [ ] **Step 1: Write src/components/ComingSoon.astro**

```astro
---
import { type Locale, t, localizedPath } from '../i18n/ui';

interface Props {
  locale: Locale;
}

const { locale } = Astro.props;
---

<section class="coming-soon">
  <div class="container">
    <h1>{t(locale, 'comingSoon.title')}</h1>
    <p>
      {t(locale, 'comingSoon.body')}
      <a href={localizedPath(locale, '/')}>{t(locale, 'comingSoon.back')}</a>
    </p>
  </div>
</section>

<style>
  .coming-soon {
    padding: 160px 0;
    text-align: center;
  }
  .coming-soon h1 {
    font-family: var(--font-display);
    font-size: clamp(36px, 4vw, 56px);
    color: var(--color-ink);
    font-weight: 400;
    margin-bottom: 24px;
    text-wrap: balance;
  }
  .coming-soon p {
    max-width: 50ch;
    margin: 0 auto;
    font-size: 17px;
    line-height: 1.6;
    color: var(--color-muted);
  }
  .coming-soon a {
    color: var(--color-accent);
    border-bottom: 1px solid currentColor;
  }
  @media (max-width: 880px) {
    .coming-soon { padding: 96px 0; }
  }
</style>
```

- [ ] **Step 2: Write src/pages/tools/index.astro (Thai)**

```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import Masthead from '../../components/Masthead.astro';
import Footer from '../../components/Footer.astro';
import ComingSoon from '../../components/ComingSoon.astro';

const locale = 'th' as const;
const currentPath = '/tools/';
---

<BaseLayout
  locale={locale}
  enableLocaleDetect
  alternates={{ th: '/tools/', en: '/en/tools/' }}
>
  <Masthead locale={locale} currentPath={currentPath} />
  <main id="main">
    <ComingSoon locale={locale} />
  </main>
  <Footer locale={locale} />
</BaseLayout>
```

- [ ] **Step 3: Write src/pages/en/tools/index.astro**

```astro
---
import BaseLayout from '../../../layouts/BaseLayout.astro';
import Masthead from '../../../components/Masthead.astro';
import Footer from '../../../components/Footer.astro';
import ComingSoon from '../../../components/ComingSoon.astro';

const locale = 'en' as const;
const currentPath = '/en/tools/';
---

<BaseLayout
  locale={locale}
  alternates={{ th: '/tools/', en: '/en/tools/' }}
>
  <Masthead locale={locale} currentPath={currentPath} />
  <main id="main">
    <ComingSoon locale={locale} />
  </main>
  <Footer locale={locale} />
</BaseLayout>
```

- [ ] **Step 4: Verify in dev server**

```bash
npm run dev
```

Visit:
- http://localhost:4321/tools/ — Thai placeholder
- http://localhost:4321/en/tools/ — English placeholder
- Click `Tools` link in the masthead from both landing pages — confirm correct placeholder loads.
- Click `LangToggle` from `/tools/` — should land on `/en/tools/` (and vice versa).

Stop dev server.

- [ ] **Step 5: Commit**

```bash
git add src/components/ComingSoon.astro src/pages/tools/index.astro src/pages/en/tools/index.astro
git commit -m "feat(tools): add coming-soon placeholder pages"
```

---

## Task 16: Auto-redirect smoke test

**Files:**
- (No new files; manual + scripted verification)

- [ ] **Step 1: Build the site**

```bash
npm run build
```

Expected: completes without errors. `dist/` contains `index.html`, `tools/index.html`, `en/index.html`, `en/tools/index.html`, `sitemap-index.xml`.

- [ ] **Step 2: Confirm the locale-detect script is inlined only on Thai roots**

```bash
grep -l "wf_locale" dist/index.html dist/tools/index.html dist/en/index.html dist/en/tools/index.html
```

Expected: prints `dist/index.html` and `dist/tools/index.html` only. Does NOT print `dist/en/index.html` or `dist/en/tools/index.html`.

- [ ] **Step 3: Preview and manually verify**

```bash
npm run preview
```

In a browser with English browser language (`navigator.language` starts with `en`):
- Visit http://localhost:4321/ in a fresh incognito window — should `replace`-redirect to `/en/`.
- Set `localStorage.wf_locale = 'th'` from devtools, reload `/` — should stay on `/`.
- Set `localStorage.wf_locale = 'en'`, reload `/` — should redirect to `/en/`.

Stop preview server.

- [ ] **Step 4: Commit (no file changes; this is a verification task)**

No commit needed for this task unless verification reveals a bug requiring a fix. If a fix is needed, commit it under `fix(locale): ...`.

---

## Task 17: Sitemap, robots.txt, favicon

**Files:**
- Create: `public/robots.txt`
- Create: `public/favicon.svg`

- [ ] **Step 1: Write public/robots.txt**

```
User-agent: *
Allow: /

Sitemap: https://wenfang.app/sitemap-index.xml
```

- [ ] **Step 2: Write public/favicon.svg**

A minimal seal-red square mark matching the design's `.small-seal`:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect x="6" y="6" width="20" height="20" fill="oklch(50% 0.205 30)" transform="rotate(-3 16 16)"/>
</svg>
```

- [ ] **Step 3: Verify sitemap generation**

```bash
npm run build
ls dist/sitemap*.xml
```

Expected: `dist/sitemap-index.xml` and `dist/sitemap-0.xml` exist. Open `sitemap-0.xml` and confirm it contains entries for `/`, `/en/`, `/tools/`, `/en/tools/` with `xhtml:link` hreflang alternates.

- [ ] **Step 4: Commit**

```bash
git add public/robots.txt public/favicon.svg
git commit -m "chore: add favicon, robots.txt, and verify sitemap"
```

---

## Task 18: Self-host Source Han Serif SC subset

**Files:**
- Create: `public/fonts/source-han-serif-sc-subset.woff2` (generated)
- Modify: `src/styles/global.css` (add `@font-face`)

- [ ] **Step 1: Install the subsetter**

```bash
npm install -D fonttools-cli
```

(If `fonttools-cli` is unavailable on npm in your environment, fall back to using Python's `pyftsubset` from the `fonttools` package: `pip install fonttools brotli`.)

- [ ] **Step 2: Identify the unique CJK glyphs the page renders**

Set: `文房今日一語学海无涯韩愈苦作舟` (16 unique characters).

Plus the four hero headline characters in case future copy uses them: none additional needed.

- [ ] **Step 3: Generate the subset**

Download `SourceHanSerifSC-Regular.otf` from https://github.com/adobe-fonts/source-han-serif/tree/release/Variable/OTF (or use the variable subset). Place it at `tools/fonts/source-han-serif-sc.otf` (gitignored).

```bash
mkdir -p tools/fonts public/fonts
# Download manually OR:
curl -L -o tools/fonts/source-han-serif-sc.otf \
  https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/SimplifiedChinese/SourceHanSerifSC-Regular.otf

pyftsubset tools/fonts/source-han-serif-sc.otf \
  --text="文房今日一語学海无涯韩愈苦作舟" \
  --flavor=woff2 \
  --output-file=public/fonts/source-han-serif-sc-subset.woff2
```

Expected: `public/fonts/source-han-serif-sc-subset.woff2` is < 50 KB.

- [ ] **Step 4: Add @font-face to src/styles/global.css**

Append to `src/styles/global.css`:

```css
@font-face {
  font-family: 'Source Han Serif SC';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('/fonts/source-han-serif-sc-subset.woff2') format('woff2');
  unicode-range: U+4E00-9FFF, U+3400-4DBF;
}
```

- [ ] **Step 5: Add preload hint in BaseLayout.astro `<head>`**

Edit `src/layouts/BaseLayout.astro`, add inside `<head>` (above the `<script>` block):

```astro
<link
  rel="preload"
  href="/fonts/source-han-serif-sc-subset.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>
```

- [ ] **Step 6: Build and verify**

```bash
npm run build
npm run preview
```

In a non-Apple browser (or with all CJK system fonts disabled), open `/` and confirm `文房` and `学海无涯` render in the served Source Han Serif SC, not a fallback sans-serif.

- [ ] **Step 7: Commit**

```bash
echo "tools/" >> .gitignore
git add .gitignore public/fonts/source-han-serif-sc-subset.woff2 src/styles/global.css src/layouts/BaseLayout.astro
git commit -m "feat(fonts): self-host Source Han Serif SC subset for non-Apple devices"
```

---

## Task 19: ESLint + Prettier configs

**Files:**
- Create: `.eslintrc.cjs`
- Create: `.prettierrc`
- Create: `.prettierignore`

- [ ] **Step 1: Write .eslintrc.cjs**

```js
module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:astro/recommended',
  ],
  overrides: [
    {
      files: ['*.astro'],
      parser: 'astro-eslint-parser',
      parserOptions: {
        parser: '@typescript-eslint/parser',
        extraFileExtensions: ['.astro'],
      },
    },
  ],
  ignorePatterns: ['dist/', '.astro/', 'node_modules/'],
};
```

If `astro-eslint-parser` is missing, install it:

```bash
npm install -D astro-eslint-parser
```

- [ ] **Step 2: Write .prettierrc**

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "plugins": ["prettier-plugin-astro"],
  "overrides": [
    { "files": "*.astro", "options": { "parser": "astro" } }
  ]
}
```

- [ ] **Step 3: Write .prettierignore**

```
dist/
.astro/
public/fonts/
node_modules/
```

- [ ] **Step 4: Run lint and format**

```bash
npm run format
npm run lint
```

Expected: format succeeds; lint reports zero errors. Fix any issues that arise.

- [ ] **Step 5: Commit**

```bash
git add .eslintrc.cjs .prettierrc .prettierignore package.json package-lock.json
git commit -m "chore(lint): configure ESLint and Prettier for Astro/TS"
```

---

## Task 20: Accessibility & responsive verification

**Files:**
- (No new files; verification only)

- [ ] **Step 1: Run astro check + typecheck**

```bash
npm run check
```

Expected: zero errors.

- [ ] **Step 2: Build for production**

```bash
npm run build
```

Expected: zero warnings, zero errors. Confirm `dist/` is populated.

- [ ] **Step 3: Run Lighthouse on the local preview**

```bash
npm run preview
```

In Chrome devtools → Lighthouse, run a mobile audit on:
- http://localhost:4321/
- http://localhost:4321/en/
- http://localhost:4321/tools/

Expected scores per page: Performance ≥ 95, Accessibility ≥ 95, Best Practices ≥ 95, SEO ≥ 95.

If any axis is below 95, address findings before moving on. Common fixes:
- LCP — confirm the chosen `Image` width is preloaded; tighten `sizes`.
- CLS — confirm hero image `width`/`height` attributes are inferred (Astro's `<Image>` adds them automatically).
- A11y — confirm color contrast and focus states; run `axe` extension if scoring fails.
- SEO — confirm `<title>`, `<meta description>`, hreflang alternates render in HTML.

Stop preview.

- [ ] **Step 4: Manual responsive check**

Reopen preview. Use Chrome's responsive device toolbar to test at:
- 320 × 568 (iPhone SE)
- 375 × 812 (iPhone 13)
- 414 × 896 (iPhone 11 Pro Max)
- 768 × 1024 (iPad)
- 1024 × 768 (iPad landscape)
- 1280 × 800 (laptop)
- 1920 × 1080 (desktop)

At each width, verify on `/` and `/en/`:
- No horizontal scroll
- Hero headline fits without overflow
- Hero image either above text (≤ 880px) or beside it (> 880px)
- Header-meta band hidden < 560px
- Primary nav links hidden < 560px; LangToggle stays visible
- Today's word `今` watermark scales appropriately
- Principles list 1-column < 880px, 2-column ≥ 880px
- Footer wraps gracefully on narrow widths

- [ ] **Step 5: Commit any fixes**

If fixes were applied:

```bash
git add <changed files>
git commit -m "fix: <specific issue>"
```

If no fixes were needed, no commit for this task.

---

## Task 21: Cloudflare Pages deployment configuration

**Files:**
- Create: `wrangler.toml` (optional, for Wrangler-based deploys)
- Update: `README.md` with deploy instructions

- [ ] **Step 1: Create README.md**

```markdown
# 文房 Wénfáng — Chinese Toolbox

Quiet tools for studying Chinese.

## Stack
- Astro 5 (static)
- Tailwind v4
- TypeScript
- Cloudflare Pages

## Develop
```bash
npm install
npm run dev
```

## Build & preview
```bash
npm run build
npm run preview
```

## Deploy to Cloudflare Pages

### Option A: Git integration (recommended)
1. Push this repo to GitHub.
2. In Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git.
3. Set:
   - **Framework preset:** Astro
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
   - **Node version:** 20
4. Save. Each push to `main` deploys automatically; PRs get preview URLs.

### Option B: Wrangler CLI
```bash
npm install -D wrangler
npx wrangler pages deploy dist --project-name=wenfang
```

## Quality
- `npm run check` — TS + Astro typecheck
- `npm run lint` — ESLint
- `npm run i18n:check` — translation key parity
- `npm run format` — Prettier

## Project structure
See `docs/superpowers/specs/2026-05-04-landing-page-design.md` for the design spec
and `docs/superpowers/plans/2026-05-04-landing-page.md` for the implementation plan.
```

- [ ] **Step 2: (Optional) Add wrangler.toml**

Only needed for advanced Wrangler usage. Skip unless explicitly required:

```toml
name = "wenfang"
compatibility_date = "2026-05-01"
pages_build_output_dir = "dist"
```

- [ ] **Step 3: Confirm build is deployable**

```bash
npm run build
ls dist/
```

Expected: `dist/index.html`, `dist/en/index.html`, `dist/tools/index.html`, `dist/en/tools/index.html`, `dist/sitemap-index.xml`, `dist/_astro/` directory with hashed asset bundles.

- [ ] **Step 4: Commit**

```bash
git add README.md wrangler.toml
git commit -m "docs: add README with Cloudflare Pages deployment instructions"
```

---

## Task 22: Final verification

**Files:** none

- [ ] **Step 1: Run the full quality suite**

```bash
npm run i18n:check && npm run check && npm run lint && npm run build
```

Expected: every command succeeds with zero errors.

- [ ] **Step 2: Confirm acceptance criteria from the spec**

Walk down section 15 of `docs/superpowers/specs/2026-05-04-landing-page-design.md`. For each of the 10 acceptance criteria, confirm by inspection. If any criterion fails, file a follow-up task and address it before declaring the work done.

- [ ] **Step 3: Summary commit (if anything was tweaked)**

If verification surfaced minor fixes, group them in a single commit:

```bash
git add <files>
git commit -m "chore: final pre-launch polish"
```

If everything passed, no commit required.

- [ ] **Step 4: Report status to the user**

State plainly:
- All 22 tasks complete
- All quality gates green
- Lighthouse scores per page
- Acceptance criteria status (10/10 or list any failed)
- Next step: deploy to Cloudflare Pages (Task 21 instructions) — leave this to the user; do not deploy unilaterally.

---

## Self-Review

**Spec coverage check:**
- §3 Stack → Tasks 1, 2, 3, 18, 19 ✓
- §4 Routing & i18n → Tasks 2, 4, 5, 6, 7, 14, 15, 16 ✓
- §5 Component architecture → Tasks 7, 8, 9, 10, 11, 12, 13, 14, 15 ✓
- §6 Styling strategy → Tasks 3, 18, plus per-component scoped styles ✓
- §7 Content model → Task 5 (dictionaries), Task 6 (parity) ✓
- §8 Behavior (toggle + auto-redirect + image) → Tasks 7 (script), 8 (toggle), 10 (image), 16 (verify) ✓
- §9 Accessibility → Task 3 (skip-link, focus, reduced motion), Task 7 (skip-link in DOM), Task 20 (verify) ✓
- §10 Performance budget → Task 20 (Lighthouse) ✓
- §11 SEO/metadata → Tasks 7 (head meta), 17 (sitemap, robots), 21 (deploy) ✓
- §12 Quality gates → Tasks 6, 19, 20, 22 ✓
- §15 Acceptance criteria → Task 22 ✓

**Placeholder scan:** No "TBD", "fill in details", or unspecified code. Thai copy is explicitly authored as a faithful first pass with a documented expectation that the user (Thai native) will refine — this is documented constraint, not a placeholder.

**Type / signature consistency:**
- `Locale` type defined in Task 4, used identically in Tasks 7–15.
- `t(locale, key)` and `tArray(locale, key)` signatures used consistently.
- `localizedPath(target, currentPath)` argument order consistent across `LangToggle` and `Masthead`.
- `BaseLayout` props (`locale`, `title?`, `description?`, `enableLocaleDetect?`, `alternates?`) match call sites in Tasks 14 and 15.
