# Web · JavaScript & Bundles (Step W3, scored area, base 100)

> Evaluate shipped JS weight: heavy/duplicate dependencies, whole-library and harmful barrel imports, incorrect/excessive memoization, and expensive synchronous work. Web scope only. Prefer a bundle-analyzer artifact for weight claims; otherwise mark size claims as static.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_perf_discovery.md`
for `platform=web`, `BUILD_TOOLS`, `FRAMEWORKS`. Skip native apps.
Cross-reference `references/dependencies.md` (C2) — report dependency *weight*
there; report *how it's imported/used* here.

## Checks

### 1. Whole-library imports that defeat tree-shaking (HIGH)
Default/namespace imports of large libs where a submodule import would ship less.
```bash
grep -rniE "import\s+(\*\s+as\s+\w+|_|moment|dayjs|lodash|rxjs)\s+from\s+['\"](lodash|moment|rxjs|date-fns|@mui/icons-material|antd|react-icons)['\"]" \
  . --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx' -n 2>/dev/null | grep -v node_modules | head -20 \
  || echo "No obvious whole-library imports"
```

### 2. Harmful barrel imports (MEDIUM)
Importing from a package/local `index` barrel that re-exports everything, pulling
unused modules into the bundle when the bundler cannot tree-shake it.
Flag deep barrels imported for one symbol; note `modularizeImports`/`optimizePackageImports` if configured (bonus).

### 3. Heavy dependency imported statically into the entry (HIGH)
Charting, rich-text editors, PDF, 3D (three.js), syntax highlighters, moment,
crypto, markdown, emoji — imported at module top-level in the initial route
instead of dynamically. Cross-reference W1 code-splitting.

### 4. Duplicate / redundant dependencies (MEDIUM)
Multiple libs solving the same problem (moment + date-fns + dayjs; multiple state
libs; multiple HTTP clients), or duplicate copies from version skew.
```bash
grep -riE '"(moment|dayjs|date-fns|luxon)"' package.json 2>/dev/null
ls node_modules 2>/dev/null >/dev/null && echo "(run: npx -y source-map-explorer or bundle analyzer for real weights)"
```

### 5. Incorrect / excessive memoization (LOW–MEDIUM)
`useMemo`/`useCallback`/`React.memo` on trivial values, memo with deps that change
every render (no-op memo), or `React.memo` on a component that always gets new
props. This is *cost without benefit* — flag as INFO/LOW unless it hides a bug.
Defer aggressive claims to `references/anti-patterns.md`.
```bash
grep -rniE '\b(useMemo|useCallback|React\.memo)\b' . --include='*.tsx' --include='*.jsx' -c 2>/dev/null | grep -v node_modules | grep -vE ':0$' | head
```

### 6. Expensive synchronous work on main thread (HIGH)
Large JSON parse, sync crypto/hashing, big loops, or heavy regex run synchronously
during load/interaction where a worker, chunking, or precompute would avoid jank.

### 7. Missing production minify / tree-shake config (HIGH)
Build config that ships un-minified or dev bundles, or disables tree-shaking.
Cross-reference `PRODUCTION_BUILD=no|unknown` from discovery.

## SEVERITY GUIDE
- CRITICAL: multi-MB heavy lib in the initial bundle of a public entry with no split.
- HIGH: whole-library import, static heavy dep, sync heavy work, broken prod build.
- MEDIUM: duplicate deps, harmful barrels.
- LOW/INFO: memoization noise (see anti-patterns).

## CONFIDENCE GUIDE
- HIGH: import statement / config directly shows the issue.
- MEDIUM: bundle *weight* impact estimated from the lib's known size (no analyzer run).
- LOW: "this might be big" — requires a bundle-analyzer run; mark and name it.

## SCORING HINTS
Base 100. Deduct (× confidence): CRITICAL −30, HIGH −20, MEDIUM −10, LOW −4, INFO 0;
LOW-confidence at half. Bonus: dynamic import of heavy libs +5; `optimizePackageImports`/
`modularizeImports` configured +5. Clamp 0–100.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_w3_javascript.md`. Findings with app, severity,
confidence, `file:line`, dependency→cost→usage reasoning, and — for any size
claim — "run [analyzer] to confirm". Per-severity count.
