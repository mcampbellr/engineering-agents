# Cross · Runtime Validation Capability (Step C4)

> Identify what can actually be MEASURED versus what stays static analysis, and enumerate the profiling each unconfirmed finding needs. NEVER install tools without explicit user authorization. NEVER run a build/dev server or a device profile as part of the default audit — this step only detects capability and defines the validation checklist. It also audits existing performance budgets.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_perf_discovery.md`
for `platform`, `RUNTIME_TOOLS`, `BUILD_TOOLS`.

## 1. Detect available profiling (presence only)

### Web
- **Lighthouse / LHCI** — `lighthouse`, `@lhci/cli` in deps or `lighthouserc.*`.
- **Bundle analyzers** — `webpack-bundle-analyzer`, `@next/bundle-analyzer`,
  `rollup-plugin-visualizer`, `source-map-explorer`, `vite-bundle-visualizer`.
- **Browser APIs** — Chrome DevTools Performance/Coverage, `PerformanceObserver`,
  `web-vitals` package wired to report field data.
- **E2E perf** — Playwright/Puppeteer that could capture traces.
```bash
grep -rniE '"(lighthouse|@lhci/cli|webpack-bundle-analyzer|@next/bundle-analyzer|rollup-plugin-visualizer|source-map-explorer|web-vitals|playwright|puppeteer)"' package.json 2>/dev/null | head
ls lighthouserc* .lighthouserc* 2>/dev/null
```

### Native
- **React DevTools Profiler / RN DevTools**, **Flipper** (`react-native-flipper`),
  **RN Perf Monitor** (built-in), `react-native-performance`, `why-did-you-render`.
- **Platform profilers** — Xcode Instruments (iOS, local only), Android Studio
  Profiler / `systrace`/`perfetto` (Android, local only).
- **Flutter DevTools** for Flutter.
```bash
grep -rniE '"(react-native-flipper|react-native-performance|@shopify/react-native-performance|why-did-you-render|flipper)"' package.json 2>/dev/null | head
```

## 2. Classify each finding as measured vs static

For the report, split findings into:
- **Confirmed by artifact** — a real Lighthouse/trace/profile/analyzer output
  exists in the repo or was provided. Only these may cite numbers.
- **Static — validation required** — everything else. Each MUST name the exact tool
  + action that would confirm it (e.g. "Run `npx @next/bundle-analyzer` to confirm
  chunk weight"; "Capture a React Profiler flame graph while typing in the search
  box to confirm re-render cost"; "Xcode Instruments Allocations to confirm the leak").

Never upgrade a static finding to a numeric claim. This is the enforcement point
for the skill's NO INVENTED METRICS rule.

## 3. Offer measurement (do NOT auto-run)

If profiling tools are present, note in the artifact that the audit CAN be deepened
by running them, and list the exact commands — but do not execute builds, dev
servers, or device profiles unless the user explicitly asks. If tools are absent,
continue with static analysis and recommend which tool to add.

## 4. Performance budgets

Detect existing budgets and audit them; recommend budgets only when justified.
```bash
grep -rniE '(budgets|maximumWarning|maximumError|performance:\s*\{|maxAssetSize|maxEntrypointSize|bundlesize|size-limit)' \
  . --include='*.json' --include='*.js' --include='*.ts' -n 2>/dev/null | grep -v node_modules | head
grep -rniE '"(size-limit|bundlesize|@size-limit/[a-z-]+)"' package.json 2>/dev/null | head
```
- If budgets exist (Angular `budgets`, `size-limit`, `bundlesize`, LHCI assertions):
  check they're realistic and enforced in CI; flag if defined but not run.
- If none exist: recommend budgets ONLY where there's evidence they'd help
  (e.g. a large entry bundle). Do not impose arbitrary universal numbers.

## OUTPUT (mandatory)
Save to `reports/.artifacts/step_c4_runtime.md`:
- `RUNTIME_TOOLS_AVAILABLE` and `MEASUREMENT_PERFORMED=[yes|no]`.
- The validation checklist: for each open question, the tool + command + what to look for.
- Existing budgets found (and whether enforced) + any justified budget recommendations.
