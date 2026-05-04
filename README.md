# 文房 Wénfáng — Chinese Toolbox

Quiet tools for studying Chinese.

## Stack

- **Astro 5** (static output)
- **Tailwind v4**
- **TypeScript** (strict)
- **Cloudflare Pages**

Bilingual: Thai (default at `/`) and English (at `/en/`).

## Develop

```bash
npm install
npm run dev
```

Open http://localhost:4321/ for Thai, http://localhost:4321/en/ for English.

## Build & preview

```bash
npm run build     # outputs to dist/
npm run preview   # serves dist/ locally
```

## Quality

```bash
npm run check       # astro check + tsc
npm run lint        # ESLint
npm run i18n:check  # translation key parity
npm run format      # Prettier
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

## Project structure

```
src/
├── i18n/             # th.json, en.json, ui.ts (typed t() helper)
├── styles/           # global.css with @theme tokens
├── assets/           # hero-inkwash.png (optimized at build)
├── layouts/          # BaseLayout (chrome + locale-detect)
├── components/       # Masthead, Hero, TodaysWord, Principles, Footer, …
└── pages/
    ├── index.astro              # / (th)
    ├── tools/index.astro        # /tools (th, coming soon)
    └── en/
        ├── index.astro          # /en/
        └── tools/index.astro    # /en/tools/
```

Design spec: `docs/superpowers/specs/2026-05-04-landing-page-design.md`.
Implementation plan: `docs/superpowers/plans/2026-05-04-landing-page.md`.

## Locale behavior

- `/` is Thai. A pre-paint inline script redirects to `/en/` if `localStorage.wf_locale === 'en'` or if the browser's `navigator.language` starts with `en` (and no stored preference exists).
- The masthead `LangToggle` (EN / ไทย) overrides at any time and persists the choice in `localStorage`.
- The toggle preserves the current page when switching locales (`/tools/` ↔ `/en/tools/`).
