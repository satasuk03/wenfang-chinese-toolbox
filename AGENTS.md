# AGENTS.md — 文房 Wénfáng

> File for AI coding agents. This project is an Astro-based static site. Read this before making changes.

---

## Project Overview

**Wénfáng** (文房) is a small, static website that hosts focused, single-purpose tools for students of Chinese. It is built with Astro 5, outputs static HTML/CSS/JS, and is deployed to Cloudflare Pages.

Live site: `https://wenfang.app`

Current tools:
- **Flashcards** (`/tools/flashcards/`) — Interactive 3D-flip cards bound to the Hanyu Jiaocheng 1A vocabulary list (~324 entries). Supports character-first, pinyin-first, or meaning-first modes. Chapter filter with localStorage persistence.
- **Stroke Order** (`/tools/stroke-order/`) — Paste Chinese characters to see stroke-order diagrams fetched from `strokeorder.com`.

The landing page (`/`) features a hero section, a static "Today's word" section, and a principles manifesto. The tools index (`/tools/`) lists available instruments.

**Note on i18n:** The README and internal design docs reference a planned Thai/English bilingual setup with `src/i18n/`, `src/pages/en/`, and a `LangToggle` component. **This infrastructure does not currently exist in the codebase.** All UI text is hardcoded in English inside the Astro components. Do not assume i18n utilities are available.

---

## Technology Stack

| Concern | Choice |
|---|---|
| Framework | Astro 5 (`output: 'static'`) |
| Styling | Tailwind CSS v4 (via `@tailwindcss/vite`) + scoped component `<style>` blocks |
| Language | TypeScript (strict mode) |
| Fonts | `@fontsource/ibm-plex-mono` (self-hosted); system stacks for serif, body, and Chinese |
| Hosting | Cloudflare Pages (static deploy of `dist/`) |
| Quality | ESLint, Prettier, `astro check`, `tsc --noEmit` |

---

## Build & Development Commands

All commands run from the project root.

```bash
# Install dependencies
npm install

# Start dev server (http://localhost:4321)
npm run dev

# Production build (outputs to dist/)
npm run build

# Serve dist/ locally
npm run preview

# Type-check (astro check + tsc --noEmit)
npm run check

# Lint with ESLint
npm run lint

# Format with Prettier
npm run format

# Regenerate vocabulary JSON from CSV
npm run vocab:build
```

**Note:** The README references `npm run i18n:check`, but this script and its associated file (`scripts/check-i18n.ts`) do not exist.

---

## Project Structure

```
wenfang-chinese-toolbox/
├── astro.config.mjs          # Astro config: static output, trailingSlash, sitemap, Tailwind Vite plugin
├── tsconfig.json             # Strict TS, path alias ~/* → src/*
├── eslint.config.js          # ESLint: JS recommended + TS recommended + Astro recommended
├── .prettierrc               # Prettier config with prettier-plugin-astro
├── package.json
├── public/                   # Static assets (favicon.svg, robots.txt)
├── scripts/
│   └── build-vocab.py        # Python script: vocabs/1.csv → src/data/vocab-1a.json
├── vocabs/
│   └── 1.csv                 # Source vocabulary (Hanyu Jiaocheng 1A)
├── src/
│   ├── assets/
│   │   └── hero-inkwash.png  # Hero image; Astro optimizes at build
│   ├── components/
│   │   ├── Masthead.astro    # Site header: wordmark, nav, mobile hamburger menu
│   │   ├── Hero.astro        # Landing hero with image and metadata
│   │   ├── TodaysWord.astro  # Static "Today's word" section
│   │   ├── Landing.astro     # Composes Hero + TodaysWord
│   │   ├── Principles.astro  # Four studio principles
│   │   ├── Footer.astro      # Site footer with social links
│   │   ├── ToolsIndex.astro  # Grid of tool cards on /tools/
│   │   └── ComingSoon.astro  # Simple placeholder (not currently used)
│   ├── data/
│   │   └── vocab-1a.json     # Generated flashcard data (DO NOT EDIT BY HAND)
│   ├── layouts/
│   │   └── BaseLayout.astro  # HTML shell: head meta, OG tags, paper grain overlay, skip link
│   ├── pages/                # File-based routing
│   │   ├── index.astro       # /
│   │   ├── tools/
│   │   │   ├── index.astro   # /tools/
│   │   │   ├── flashcards/
│   │   │   │   └── index.astro   # /tools/flashcards/
│   │   │   └── stroke-order/
│   │   │       └── index.astro   # /tools/stroke-order/
│   └── styles/
│       └── global.css        # Tailwind import, @theme tokens, base resets, container, skip-link
├── design/
│   └── index.html            # Original design reference (hand-crafted HTML)
└── docs/superpowers/
    ├── plans/                # Implementation plans
    └── specs/                # Design specifications
```

---

## Code Style Guidelines

- **Components are `.astro` files** with scoped `<style>` blocks. Most styling is done via raw CSS inside these blocks, using CSS custom properties (`var(--color-*)`, `var(--font-*)`) defined in `src/styles/global.css`.
- **Tailwind is used primarily for theme tokens** (`@theme` in `global.css`), not utility classes in markup.
- **TypeScript strict mode is enabled.** Use proper types; the build will fail on implicit `any`.
- **Path alias:** Use `~/*` to reference `src/*` (e.g., `import BaseLayout from '~/layouts/BaseLayout.astro'`).
- **Prettier:** `semi: true`, `singleQuote: true`, `trailingComma: 'all'`, `printWidth: 100`. Astro files use the `astro` parser.
- **Trailing slashes:** The Astro config sets `trailingSlash: 'always'`. All internal links and hrefs should end with `/`.

---

## Component Patterns

### Page structure
Every page follows this pattern:

```astro
---
import BaseLayout from '../../layouts/BaseLayout.astro';
import Masthead from '../../components/Masthead.astro';
import Footer from '../../components/Footer.astro';
---

<BaseLayout title="Page Title · Wénfáng">
  <Masthead />
  <main id="main">
    <!-- page content -->
  </main>
  <Footer />
</BaseLayout>
```

### Client-side interactivity
Interactive tools use `is:inline` scripts inside Astro components, with `define:vars` to pass server-side data to the browser:

```astro
<script is:inline define:vars={{ entries, allChapters }}>
  // Client-side logic here
</script>
```

Do not use React/Vue/Svelte islands unless explicitly required. The project currently ships zero framework runtime.

### Mobile menu (Masthead)
The masthead includes a hamburger menu controlled by a small inline script. It toggles `data-menu-open` on the header element and manages `aria-expanded`, `hidden`, and body overflow.

---

## Design System

Colors and fonts are defined as Tailwind v4 theme tokens in `src/styles/global.css`.

### Palette (OKLCH)
- `--color-bg`: oklch(96.5% 0.013 80) — page background
- `--color-paper`: oklch(98.5% 0.008 80) — card backgrounds
- `--color-fg`: oklch(18% 0.018 60) — body text
- `--color-ink`: oklch(14% 0.02 60) — headings
- `--color-muted`: oklch(46% 0.014 55) — secondary text
- `--color-border`: oklch(86% 0.014 75) — rules and borders
- `--color-accent`: oklch(50% 0.205 30) — accent red

### Typography
- `--font-display`: Iowan Old Style, Charter, Source Han Serif SC, Georgia, serif
- `--font-body`: system-ui sans stack
- `--font-zh`: Source Han Serif SC, Songti SC, STSong, SimSun, serif
- `--font-mono`: JetBrains Mono, IBM Plex Mono, ui-monospace, Menlo, monospace

### Breakpoints
- `560px` — mobile (hamburger appears)
- `880px` — tablet
- `1080px` — desktop

### Aesthetic notes
- Cream paper aesthetic. No dark mode.
- Subtle paper grain overlay via `body::before` with a radial-gradient dot pattern.
- Tabular numerals on metadata and counters.
- `prefers-reduced-motion: reduce` is respected globally.

---

## Vocabulary Data

Source: `vocabs/1.csv`
Columns: `character, part_of_speech, pinyin, chapter, th_translation`

Generated: `src/data/vocab-1a.json`

To regenerate after editing the CSV:

```bash
npm run vocab:build
```

Entries with an empty `th_translation` display "—" on the flashcard back.

---

## Testing

There are **no automated tests** in this project. Quality is enforced via:

1. `npm run check` — Astro template checking + TypeScript strict type-checking
2. `npm run lint` — ESLint
3. Manual browser testing during `npm run dev` and `npm run preview`

When adding interactive features, test keyboard navigation, touch interactions, and the `prefers-reduced-motion` media query.

---

## Deployment

### Cloudflare Pages (Git integration — current method)
1. Repo is connected to Cloudflare Pages.
2. Build settings:
   - **Framework preset:** Astro
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
   - **Node version:** 20
3. Pushes to `main` deploy automatically. PRs get preview URLs.

### Wrangler CLI (manual)
```bash
npm install -D wrangler
npx wrangler pages deploy dist --project-name=wenfang
```

---

## Security & Privacy Considerations

- **No auth, no accounts, no cookies, no analytics.**
- **Static site:** No server-side execution, no database, no API routes.
- **Client-side storage:** Flashcards use `localStorage` only for user preferences (active tab, selected chapters). No personal data.
- **Third-party resources:** The stroke-order tool loads images from `https://www.strokeorder.com`. This is a runtime dependency; if the service is unavailable, the tool gracefully shows "Not found" for missing characters.
- **No env secrets** are required for the current feature set.

---

## Important Notes for Agents

1. **Do not assume i18n exists.** All text is hardcoded in components. If asked to add Thai translations, you will need to create the i18n infrastructure from scratch.
2. **Do not edit `src/data/vocab-1a.json` by hand.** Always edit `vocabs/1.csv` and run `npm run vocab:build`.
3. **Keep scoped styles.** Prefer adding CSS inside component `<style>` blocks rather than global CSS, unless the style is truly global.
4. **Respect the existing aesthetic.** The design is intentionally quiet and print-like. Avoid flashy animations, popovers, or heavy JS.
5. **Check `design/index.html`** if you need to understand the original visual reference for the landing page.
