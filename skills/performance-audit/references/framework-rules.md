# Cross · Framework-Specific Rules (Step C1)

> An extensible registry of per-framework performance rules. Apply ONLY the block(s) matching the frameworks recorded in discovery. This is deliberately modular: adding a new framework = adding a block here, no other file changes. Findings here augment the scoped areas (W*/N*) and are tagged with their area for scoring; do not double-count a finding already raised by a scoped step.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_perf_discovery.md`
for `FRAMEWORKS`, `RENDERING`, `platform`. Run only the matching blocks below.
When a framework is not in the list but is detected, apply the closest analogous
block and note the framework explicitly (extensibility path).

## React (any renderer)
- Unnecessary re-renders from state placed too high; missing state colocation.
- `key` as array index on dynamic lists; missing keys.
- Effects that run every render (missing/incorrect deps) doing expensive work.
- Context value recreated inline (split state vs updater contexts).
- Expensive computations not memoized where the input is large and stable.
→ Tag to Rendering area (W2 / N1).

## Next.js
- Overuse of `"use client"`; client components that could be Server Components. → W2
- `dynamic()` missing for heavy client-only widgets. → W1/W3
- `next/image` not used; `next/font` not used. → W5
- `fetch` cache misuse: `cache: 'no-store'`/`revalidate: 0` where caching is safe,
  or missing `revalidate` causing over-rendering. → W4
- Missing route-level `loading.tsx`/streaming for slow segments. → W1/W2
- `optimizePackageImports` / `modularizeImports` not configured for big libs. → W3
```bash
grep -rniE '(optimizePackageImports|modularizeImports|images:\s*\{|experimental)' next.config.* 2>/dev/null | head
```

## Astro
- `client:load`/`client:only` where `client:visible`/`client:idle` (or no
  hydration) would do; static content accidentally hydrated. → W2
- Islands too coarse (whole page as one island). → W2
- Not using `astro:assets` `<Image>` for local images. → W5
```bash
grep -rncE 'client:(load|only|visible|idle|media)' . --include='*.astro' 2>/dev/null | grep -v ':0' | head
```

## Vue / Nuxt
- `ssr:false` where SSR/SSG fits; missing `<NuxtImg>`/`@nuxt/image`. → W2/W5
- Non-virtualized large `v-for` lists. → W2
- Heavy computed/watchers running on large reactive data; missing `shallowRef`. → W2/W3
- Missing `defineAsyncComponent` for heavy components. → W1/W3

## Svelte / SvelteKit
- Adapter/prerender misuse (SSR where static works, or vice-versa). → W2
- Large `{#each}` without virtualization. → W2
- Heavy work in reactive `$:` statements. → W2/W3

## Angular
- Default change detection everywhere; missing `OnPush`/signals/zoneless. → W2
- No `trackBy` on `*ngFor` over large lists; no CDK virtual scroll. → W2
- Eagerly-loaded feature modules; missing route-level lazy loading. → W1/W3
```bash
grep -rniE '(ChangeDetectionStrategy\.OnPush|trackBy|loadChildren|provideExperimentalZonelessChangeDetection)' . --include='*.ts' --include='*.html' -n 2>/dev/null | grep -v node_modules | head
```

## Remix
- Loaders not parallelizing independent data; waterfalls across nested routes. → W4
- Missing `defer`/streaming for slow loaders. → W4/W1

## Vite / vanilla / other build systems
- No manual chunking for large vendor libs; no dynamic imports. → W1/W3
- Dev-only config audited as prod (verify `build` config, minify, target). → W3

## Expo / React Native
- Expo Router: heavy layout/`_layout` work; screens doing data load on every focus. → N2
- Not using `expo-image` where image memory/caching matters. → N2
- `Animated` without `useNativeDriver`; Reanimated available but unused for gestures. → N2
- Hermes disabled where it would cut startup/memory; New Architecture considerations. → N2
- NativeWind: large style objects recreated per render in `renderItem`. → N1

## Flutter
- Missing `const` widgets; `ListView(children:)` vs `.builder`; heavy `build()`;
  missing `RepaintBoundary`; oversized images without `cacheWidth`. → N1/N2

## SEVERITY / CONFIDENCE / SCORING
Use the same 5-level severity and 3-level confidence as the scoped areas. These
findings **feed the scoring of the area they are tagged to** (W2, W3, N1, …) — the
report-generator dedups them against the scoped step's findings so nothing is
counted twice. This step itself has no independent score.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_c1_framework.md`. Each finding: framework, the
target area tag (W1–W5 / N1–N2), severity, confidence, `file:line`, evidence,
recommendation. Note which framework blocks were applied and why.
