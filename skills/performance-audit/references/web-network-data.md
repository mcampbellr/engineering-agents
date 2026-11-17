# Web · Network & Data Fetching (Step W4, scored area, base 100)

> Evaluate request efficiency: waterfalls, sequential requests that could parallelize, duplicate requests, missing caching, overfetching, huge payloads, requests during render, missing pagination/compression. Web scope (also applies to native data layers — see native-runtime if native). Backend is in scope ONLY where it directly shapes client-perceived latency.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_perf_discovery.md`
for `platform`, `DATA_FETCHING`, `FRAMEWORKS`, `RENDERING`.

## Checks

### 1. Sequential requests that could parallelize (HIGH)
`await` chains where independent requests run one-after-another instead of
`Promise.all`. Classic N+1 in loaders/effects.
```bash
grep -rnB1 -E 'await .*(fetch|axios|\.get\(|\.query\(|\.request\()' . \
  --include='*.ts' --include='*.tsx' --include='*.js' -n 2>/dev/null | grep -v node_modules | head -30 \
  || echo "No obvious await chains"
```
Flag consecutive independent `await`s; confirm they don't depend on each other.

### 2. Client-side request waterfalls (HIGH)
Component fetches → renders child → child fetches, cascading round-trips instead
of hoisting/parallelizing or using a route loader. Cross-reference W1.

### 3. Fetch during render / in effect without dedup (MEDIUM–HIGH)
Fetching directly in render body, or `useEffect` fetches with no caching/dedup so
every mount refetches. Flag absence of a cache layer when `DATA_FETCHING=fetch-in-effect`.
```bash
grep -rniE 'useEffect\([^)]*\)\s*=>\s*\{[^}]*(fetch|axios)' . --include='*.tsx' --include='*.jsx' -n 2>/dev/null | grep -v node_modules | head
```

### 4. Missing / weak caching (MEDIUM)
No HTTP cache headers usage, no query-cache (react-query/swr/apollo) where the app
refetches the same data, or `cache: 'no-store'` / `revalidate: 0` used broadly in
Next where caching is safe. Both missing-cache and cache-disabled are findings.

### 5. Overfetching / huge payloads (MEDIUM–HIGH)
Fetching full objects when a subset is used, GraphQL queries selecting large trees,
list endpoints returning everything with no field selection. Flag `select *`-style
queries and huge response shapes rendered partially.

### 6. Missing pagination / infinite unbounded lists (HIGH)
List endpoints/queries with no `limit`/`cursor`/pagination feeding an ever-growing
client list (also a memory issue). Cross-reference virtualization (W2/N1).

### 7. Duplicate / redundant requests (MEDIUM)
Same endpoint hit multiple times per view (no dedup/shared cache), refetch on every
focus/navigation where stale-while-revalidate would do.

### 8. Missing compression / oversized transfer (LOW–MEDIUM, if detectable)
No gzip/brotli on served assets/API where config is visible; uncompressed large
JSON. Only flag when config evidence exists.

## SEVERITY GUIDE
- CRITICAL: blocking sequential waterfall on the critical render path of the main view.
- HIGH: parallelizable sequential requests, unbounded list, waterfall, big overfetch.
- MEDIUM: missing cache/dedup, duplicate requests.
- LOW/INFO: compression tuning, anything needing a network trace to size.

## CONFIDENCE GUIDE
- HIGH: await chain / missing pagination directly visible.
- MEDIUM: payload size inferred from schema/query, not measured.
- LOW: "might refetch too often" — confirm with Network panel / server logs.

## SCORING HINTS
Base 100. Deduct (× confidence): CRITICAL −30, HIGH −20, MEDIUM −10, LOW −4, INFO 0;
LOW-confidence at half. Bonus: query-cache with sane stale times +5; route loaders
parallelizing data +5; pagination present +5. Clamp 0–100.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_w4_network.md`. Findings with app, severity,
confidence, `file:line`, and the tool to confirm timing/size (Network panel,
server timing, GraphQL tracing). Per-severity count.
