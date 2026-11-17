# Cross · Framework-Specific Adaptive Rules (Step X1)

> An extensible registry of per-framework *adaptive/responsive* idioms: the correct primitive each stack gives you for adapting to viewport/window/orientation, and the anti-idiom to flag when it's ignored. Apply ONLY the block(s) matching the frameworks recorded in discovery. Modular by design: a new framework = a new block here, no other file changes. These findings AUGMENT the scoped areas (W*/N*/D1) and are tagged with their fold-in area for scoring; do NOT double-count a finding a scoped step already raised.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_aui_discovery.md` for
`FRAMEWORKS`, `RESPONSIVE_SYSTEM`, `BREAKPOINTS`, `PLATFORMS`. Run only the blocks whose
framework is detected. If a framework is present but has no block, apply the closest analogous
block and name it explicitly (extensibility path). Fold-in area tags: web → **W1** Layout&Overflow
/ **W2** Breakpoints / **W3** Adaptive Components / **W4** Interaction; native → **N3** Adaptive
Layout / **N4** Touch; desktop → **D1**.

## Tailwind / CSS (any web stack)
Right primitives: `screens` breakpoint tokens (`sm/md/lg`), container queries `@container`,
fluid type/space with `clamp()`, `max-w-*` / `container` for line-length, `min()/max()`.
Anti-idioms to flag:
- Arbitrary fixed layout widths `w-[NNNpx]` / `h-[NNNpx]` on structural elements (not icons). → W1
- Raw `@media` with pixel values that DON'T match the Tailwind `screens` tokens (two systems). → W2
- Static font sizes everywhere, no `clamp()`/fluid scale on headings. → W3
- Container-query-shaped component (card reused in many widths) still keyed off viewport `md:`. → W3
```bash
grep -rniE 'w-\[[0-9]+px\]|h-\[[0-9]+px\]|min-w-\[[0-9]{3,}px\]' src 2>/dev/null | grep -v node_modules | head
grep -rnE '@media|@container' src 2>/dev/null | grep -v node_modules | wc -l
grep -rniE 'screens\s*:|clamp\(' tailwind.config.* src 2>/dev/null | head
```

## Next.js / Nuxt / Astro / SvelteKit / Angular (meta-frameworks)
Right primitives: responsive images with intrinsic `sizes` (`next/image` `sizes=`, Astro/Nuxt
`<Image>`/`<NuxtImg>` with `sizes`), CSS-driven layout over JS width branching, and NOT SSR-ing
viewport-dependent branches that cause hydration mismatch.
Anti-idioms:
- `next/image`/`<NuxtImg>`/`<Image>` without `sizes` (ships one width to all viewports). → W1
- `window.innerWidth`/`matchMedia` read during render/SSR to choose a layout → hydration mismatch, flash. → W2/W4
- `next/dynamic` `ssr:false` used to hide a component that should just be CSS-hidden per breakpoint. → W3
- Angular: layout branches in TS instead of `@angular/cdk/layout` `BreakpointObserver`; no `ngClass` per breakpoint. → W2
```bash
grep -rniE '<Image|next/image|NuxtImg|astro:assets' src 2>/dev/null | grep -v node_modules | head
grep -rniE 'innerWidth|matchMedia|BreakpointObserver|ssr\s*:\s*false' src 2>/dev/null | grep -v node_modules | head
```

## React Native / Expo
Right primitives: `useWindowDimensions()` (re-renders on rotate/resize/foldables) over
`Dimensions.get()` (stale after rotation), NativeWind responsive prefixes, `Platform.select`
for platform-specific layout, `useSafeAreaInsets`, Expo Router large-screen/two-pane `_layout`.
Anti-idioms:
- `Dimensions.get('window')` captured once at module/render top, never updated on rotate. → N3
- Fixed pixel widths/heights for containers instead of flex, `%`, or dimension-derived values. → N3
- No orientation handling (`useWindowDimensions().width > height`) on a tablet-supporting app. → N3
- Touch targets sized in fixed px below 44 with no scaling; hit-slop missing. → N4
```bash
grep -rniE "Dimensions\.get\(" src 2>/dev/null | grep -v node_modules | head
grep -rniE 'useWindowDimensions|useSafeAreaInsets|Platform\.(select|OS)' src 2>/dev/null | grep -v node_modules | head
```

## Flutter
Right primitives: `LayoutBuilder` (constraint-driven), `MediaQuery.of(context).size`/`orientation`,
`OrientationBuilder`, `Flexible`/`Expanded`/`Wrap`/`FractionallySizedBox` over fixed sizes,
`FittedBox` for scale-to-fit, `MediaQuery.textScaler` respected.
Anti-idioms:
- Hardcoded `SizedBox(width: 375...)` / fixed `Container` dims sized to one phone. → N3
- `Row` of many children with no `Flexible`/`Wrap` → overflow (yellow-black stripes) on narrow/rotate. → N3
- Reading `MediaQuery.size` once in `initState` instead of in `build`. → N3
- No `LayoutBuilder`/breakpoint split on a tablet/desktop-target Flutter app. → N3
```bash
grep -rniE 'LayoutBuilder|OrientationBuilder|MediaQuery|Flexible|Expanded|Wrap\(|FittedBox' lib 2>/dev/null | head
grep -rniE 'SizedBox\(\s*width:\s*[0-9]{3,}|width:\s*375|height:\s*812' lib 2>/dev/null | head
```

## Electron / Tauri (desktop shell)
Right primitives: `minWidth`/`minHeight` on `BrowserWindow` / `tauri.conf.json` window config, and
loading the SAME responsive CSS the web build ships (the web UI must react to window drags).
Anti-idioms:
- Window shell present but the loaded web UI has zero small breakpoints (see D1 Check 2). → D1
- Min-size missing so the window drags below the smallest breakpoint. → D1
```bash
grep -rniE 'new BrowserWindow|minWidth|minHeight' -n . 2>/dev/null | grep -v node_modules | head
find . -name 'tauri.conf.json' -not -path '*/node_modules/*' 2>/dev/null | head
```

## SEVERITY / CONFIDENCE
Use the shared 5-level severity and 3-level confidence. An anti-idiom with a runtime-confirmed
visual break (overflow, mismatch flash) rises to HIGH; a static-only signal caps at MEDIUM
confidence and must say "Static analysis — confirm by <tool>" (see `references/runtime-validation.md`).

## SCORING HINTS (folded)
This step has NO independent score. Each finding feeds the scoring of the area it is tagged to
(W1–W4 / N3–N4 / D1) using the shared deduction scheme (CRITICAL −30 / HIGH −20 / MEDIUM −10 /
LOW −4 / INFO 0, ×confidence). The report-generator dedups these against the scoped step's
findings so a defect is counted once.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_x1_framework.md`. Each finding: framework, fold-in area tag,
severity, confidence, `file:line`, OBSERVED-vs-static marker, evidence, and the concrete
right-primitive fix. Record which framework blocks were applied and why (and any analogous-block substitutions).
