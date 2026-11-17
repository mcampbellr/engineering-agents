# Cross · Dependencies (Step C2, folds into scoring)

> Analyze package manifests for dependencies with performance implications. The rule is always: dependency → bundle/runtime cost → actual usage → alternative. NEVER recommend removing a dependency on size alone — show the cost AND the usage.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_perf_discovery.md`
for `platform`, `PKG_MANAGER`, `FRAMEWORKS`. Read the relevant manifest(s):
`package.json` (per app + shared packages), `pubspec.yaml` (Flutter).

## Checks

### 1. Known-heavy dependencies (MEDIUM–HIGH)
Flag deps with large or runtime-heavy footprints and check how they're imported/used:
- Web bundle-weight: `moment`, `lodash` (full), `three`, `chart.js`/`recharts`/`echarts`,
  rich-text editors (`draft-js`, `slate`, `quill`, `tinymce`), `pdfjs`, `@mui/*`
  full, `rxjs`, `crypto-js`, `firebase` (full SDK vs modular).
- Native: large image libs, heavy nav stacks, unused native modules increasing
  binary/startup cost.
```bash
grep -riE '"(moment|lodash|three|chart\.js|recharts|echarts|draft-js|slate|quill|tinymce|pdfjs-dist|@mui/material|rxjs|crypto-js|firebase)"' \
  package.json 2>/dev/null | head
```
For each hit: (a) confirm it's actually imported (not a stale dep), (b) how much of
it is used, (c) whether a lighter alternative or modular import fits.

### 2. Duplicate functionality (MEDIUM)
Multiple libraries solving the same problem shipped together:
```bash
grep -riE '"(moment|dayjs|date-fns|luxon)"' package.json 2>/dev/null
grep -riE '"(redux|zustand|jotai|recoil|mobx|valtio)"' package.json 2>/dev/null
grep -riE '"(axios|got|ky|node-fetch|superagent)"' package.json 2>/dev/null
grep -riE '"(styled-components|@emotion/styled|@stitches|tailwindcss)"' package.json 2>/dev/null
```
Two+ in the same category on the client → flag with the consolidation recommendation.

### 3. Trivial-use heavy packages (MEDIUM)
A large package pulled in for one small function (e.g. whole `lodash` for `debounce`,
`moment` for one format). Recommend the one-function replacement.

### 4. Duplicate copies / version skew (LOW–MEDIUM, if lockfile present)
Multiple versions of the same package in the lockfile bloating the bundle.
```bash
[ -f pnpm-lock.yaml ] && grep -cE '^\s{2}/?(react|lodash|@babel/runtime)@' pnpm-lock.yaml 2>/dev/null
[ -f package-lock.json ] && echo "(inspect npm ls <pkg> for duplicate versions)"
```

## USAGE VERIFICATION (mandatory before recommending removal)
For every dependency finding, grep for its import to confirm real usage and scope:
```bash
grep -rniE "from ['\"]<pkg>['\"]|require\(['\"]<pkg>['\"]\)" . --include='*.ts' --include='*.tsx' --include='*.js' -n 2>/dev/null | grep -v node_modules | head
```
Unused/stale → recommend removal (LOW, easy win). Used → give the modular-import
or lighter-alternative path, not blanket removal.

## SEVERITY / CONFIDENCE
- HIGH: multi-MB lib in the client entry, heavily used, no split — confirm with analyzer.
- MEDIUM: duplicate-category libs, trivial-use heavy packages.
- LOW: version-skew duplicates, stale deps.
- Confidence HIGH when import + usage are visible; MEDIUM when weight is estimated
  (no analyzer run) — say so.

## SCORING
Findings tag to **W3 (JavaScript & Bundles)** for web apps and to **N2 (Runtime)**
for native apps, and are scored there. The report-generator dedups against W3/N2.
This step has no independent score.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_c2_dependencies.md`. For each finding:
package, target area (W3/N2), severity, confidence, the dep→cost→usage→alternative
chain, and `file:line` of representative imports. Per-severity count.
