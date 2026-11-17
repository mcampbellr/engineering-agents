# Project Discovery & Scope (Step 0)

> Profile the project and determine platform scope (web / native / both) BEFORE any analysis. Framework-agnostic, runtime-aware, monorepo-aware. This is the MANDATORY first step; if no web or native client exists, the audit stops here. Never assume the stack — detect it from evidence.

---

Goal: Produce the discovery artifact all downstream steps depend on. Record
platform, per-app profile, frameworks, build tools, rendering strategy, runtime
concerns, and available profiling tools. If no client runtime is detected, report
cleanly and stop.

## PROJECT ROOT, APPS & PATHS (execute first)

- Identify manifests: `package.json`, `pubspec.yaml` (Flutter), `app.json` /
  `app.config.{js,ts}` (Expo), `requirements.txt`, `go.mod`, etc.
- **Monorepo detection:** look for `pnpm-workspace.yaml`, `turbo.json`, `nx.json`,
  `lerna.json`, `rush.json`, or a `workspaces` field in root `package.json`. If
  present, enumerate every app under `apps/*`, `packages/*`, and workspace globs.
  Record each as a separate `APP` with its own platform/framework — audit each app
  under its own scope. Shared `packages/*` are audited once as shared code.

```bash
# Monorepo + app enumeration
ls pnpm-workspace.yaml turbo.json nx.json lerna.json 2>/dev/null
find . -maxdepth 4 -name package.json 2>/dev/null | grep -vE 'node_modules|/dist/|/build/' | head -40
find . -maxdepth 3 \( -name 'app.json' -o -name 'app.config.*' -o -name 'pubspec.yaml' \) 2>/dev/null | grep -v node_modules
```

## PLATFORM DETECTION (web vs native)

Classify EACH app. Do not mix rules across platforms.

```bash
# Native / mobile signals
grep -rniE '"(react-native|expo|expo-router|@react-navigation/[a-z-]+|nativewind|react-native-reanimated|@shopify/flash-list)"' \
  package.json 2>/dev/null && echo "NATIVE:react-native/expo"
test -f pubspec.yaml && grep -qiE '^\s*flutter\s*:' pubspec.yaml && echo "NATIVE:flutter"

# Web framework signals
grep -rniE '"(next|nuxt|@remix-run/[a-z-]+|astro|@sveltejs/kit|svelte|@angular/core|vue|react-dom|vite|gatsby)"' \
  package.json 2>/dev/null && echo "WEB:framework"
```

Resolve `PLATFORM` per app:
- **native** — `react-native`/`expo` present, or Flutter (`pubspec.yaml` with a
  `flutter:` block). Note Expo vs bare RN, and Expo SDK version.
- **web** — a web framework or `react-dom`/DOM bundling present, no RN.
- A monorepo may contain both → project `PLATFORM=both`; each app keeps its own.
- If an app has RN AND `react-native-web`, note it as native-first with web target.

## FRAMEWORK / RENDERING STRATEGY

Identify the framework and its rendering mode from config + code, not guesses:
- **Next.js** — `next.config.*`; App Router (`app/`) vs Pages (`pages/`); RSC usage
  (`"use client"` density); `output: 'export'` (static) vs SSR/ISR.
- **Astro** — `astro.config.*`; client directives (`client:load/idle/visible/only`).
- **Nuxt / Vue** — `nuxt.config.*`; `ssr: true|false`; Vite/webpack.
- **SvelteKit / Svelte** — `svelte.config.*`; adapter (static/node/edge).
- **Remix** — `@remix-run/*`; loaders/actions.
- **Angular** — `angular.json`; SSR (`@angular/ssr`), zoneless, standalone.
- **Vite / vanilla** — `vite.config.*`, `rollup`, `esbuild`, `webpack`.
- **Expo / RN** — Metro config; Hermes on/off; New Architecture (Fabric/TurboModules);
  Expo Router vs React Navigation.
- **Flutter** — build mode (debug vs release relevance), widget tree signals.

Record `RENDERING`: `ssr | ssg | isr | csr | islands | static-export |
rn-hermes | rn-jsc | fabric | bridge`.

## SUPPORTING SYSTEMS

Detect and record (each drives specific checks):
- `PKG_MANAGER` — lockfile: `pnpm-lock.yaml` | `package-lock.json` | `yarn.lock` | `bun.lockb`.
- `BUILD_TOOLS` — vite/webpack/rollup/esbuild/turbopack/metro/rspack.
- `STATE` — redux/zustand/jotai/recoil/mobx/valtio/context-only/signals.
- `DATA_FETCHING` — react-query/swr/apollo/urql/trpc/rtk-query/fetch-in-effect.
- `STYLING` — tailwind/nativewind/css-modules/styled-components/emotion/vanilla-extract/inline.
- `IMAGE_SOLUTION` — next/image, astro `<Image>`, `expo-image`, RN `Image`, `<img>` raw.
- `THIRD_PARTY` — GA/GTM/Segment/Amplitude/Sentry/Intercom/Hotjar/maps/ads/social embeds.
- `PRODUCTION_BUILD` — is there a real prod build config (minify, tree-shake,
  sourcemaps, `NODE_ENV=production`, Hermes/release)? Dev-only config skews everything.

```bash
grep -rniE '"(react-query|@tanstack/react-query|swr|@apollo/client|urql|@trpc/[a-z-]+|@reduxjs/toolkit|zustand|jotai|recoil|mobx)"' package.json 2>/dev/null | head
grep -rniE '(googletagmanager|google-analytics|gtag|segment|amplitude|@sentry|intercom|hotjar|mapbox|google-maps)' . \
  --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx' --include='*.html' -l 2>/dev/null | grep -v node_modules | head
```

## RUNTIME TOOLING CAPABILITY (do not install anything)

Record what profiling is *available* so the report can distinguish measured vs
static. See `references/runtime-validation.md` for how these are used. Just detect
presence here:

```bash
grep -rniE '"(lighthouse|@lhci/cli|webpack-bundle-analyzer|rollup-plugin-visualizer|@next/bundle-analyzer|source-map-explorer|vite-bundle-visualizer|react-native-performance|@shopify/react-native-performance|why-did-you-render)"' package.json 2>/dev/null | head
```

## DECISION

- If NO web app and NO native app is detected (pure backend/library/CLI with no
  client runtime): set `PLATFORM=none`. Write the artifact, then STOP and report:
  "No web or native client detected — performance-audit targets client/runtime
  performance; nothing to audit here."
- Otherwise set `PLATFORM=web|native|both` and continue with the matching branch(es).

## ARTIFACT SAVE (mandatory)

Save to `reports/.artifacts/step_00_perf_discovery.md`. Run first:
`mkdir -p reports/.artifacts`

Output format (downstream steps parse these keys):
```
PLATFORM=[web|native|both|none]
PKG_MANAGER=[..]
BUILD_TOOLS=[comma list]
FRAMEWORKS=[comma list]
RENDERING=[comma list]
STATE=[..]
DATA_FETCHING=[..]
STYLING=[..]
IMAGE_SOLUTION=[..]
THIRD_PARTY=[comma list]
RUNTIME_TOOLS=[comma list or "none available"]
PRODUCTION_BUILD=[yes|no|unknown]
APPS:
- name@path — platform=[web|native] framework=[..] rendering=[..] build=[..]
...
SHARED_PACKAGES:
- name@path — [what it provides]
```
Followed by a short prose summary of the project and the scope decision (which
branches will run, per app).
