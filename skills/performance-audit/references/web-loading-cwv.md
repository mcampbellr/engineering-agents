# Web · Loading & Core Web Vitals (Step W1, scored area, base 100)

> Evaluate initial load cost and Core Web Vitals *risk* from static evidence: render-blocking resources, resource waterfalls, preload/prefetch, lazy loading, critical path, and third-party scripts. Web scope only. NEVER state a measured metric (LCP/INP/CLS/TTFB) unless a Lighthouse/trace artifact exists.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_perf_discovery.md`.
Run only for apps with `platform=web`. Skip entirely for native apps.

## Checks

### 1. Render-blocking resources (HIGH)
Synchronous `<script>` in `<head>` without `defer`/`async`, blocking CSS `<link>`
with no critical-CSS strategy, and large synchronous inline scripts. Flag scripts
that block first paint.
```bash
grep -rniE '<script(?![^>]*\b(defer|async|type="module")\b)[^>]*src=' . \
  --include='*.html' --include='*.astro' --include='*.vue' -n 2>/dev/null | grep -v node_modules | head -20 \
  || echo "No obviously render-blocking <script src> in markup"
```

### 2. Third-party scripts on the critical path (HIGH–CRITICAL)
Analytics, tag managers, chat/maps/ads/social embeds loaded eagerly in `<head>`
or without `defer`/`next/script` strategy. Each blocks the main thread during
startup. Cross-reference `THIRD_PARTY` from discovery. CRITICAL if a heavy SDK
(maps, chat widget, tag manager) loads synchronously before interactive content.

### 3. Missing bundle splitting / route-level code splitting (HIGH)
The whole app shipped as one chunk; no dynamic `import()` at route boundaries;
heavy libs (charting, editors, PDF, 3D) imported statically into the entry.
```bash
grep -rniE '\b(import\()|React\.lazy|loadable\(|defineAsyncComponent|dynamic\(' . \
  --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx' --include='*.vue' -l 2>/dev/null \
  | grep -v node_modules | head || echo "No dynamic import()/lazy boundaries found (flag if app is non-trivial)"
```

### 4. Preload / prefetch / preconnect discipline (MEDIUM)
Missing `preconnect`/`dns-prefetch` to critical third-party origins; missing
`preload` for the LCP hero image or critical font; OR over-preloading (many
`preload`s that fight for bandwidth and delay LCP). Both directions are findings.

### 5. Resource / request waterfalls at load (HIGH)
Chained dependencies where each resource is discovered only after the previous
loads (e.g. JS that then fetches config that then fetches data before render).
Note the chain as evidence; verification requires a network trace.

### 6. Eager loading of below-the-fold work (MEDIUM)
Below-the-fold components, images, or data loaded eagerly at first paint instead
of on-demand/viewport. (Above-the-fold must NOT be lazy — see W5.)

## SEVERITY GUIDE
- CRITICAL: heavy third-party SDK synchronously blocking first interactive paint.
- HIGH: render-blocking entry, no code-splitting on a large app, long load waterfall.
- MEDIUM: preload/preconnect gaps, eager below-the-fold work.
- LOW/INFO: micro preload tuning; anything requiring a trace to confirm → INFO + name the tool.

## CONFIDENCE GUIDE
- HIGH: directly visible in markup/config (blocking script, static heavy import).
- MEDIUM: waterfall inferred from code structure.
- LOW: LCP/INP/CLS magnitude — always requires Lighthouse/trace; mark accordingly.

## SCORING HINTS
Base 100. Deduct per finding (modulated by confidence): CRITICAL −30, HIGH −20,
MEDIUM −10, LOW −4, INFO 0; halve the deduction for LOW-confidence findings.
Bonus: route-level code-splitting present +5; disciplined preconnect/preload for
LCP asset +5. Clamp 0–100.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_w1_loading.md`. Every finding: app, severity,
confidence, `file:line`, evidence, why-it-matters, and the validation tool
(Lighthouse / WebPageTest / Chrome trace) needed to confirm any CWV claim.
Per-severity count. Note LCP-candidate and blocking resources for the report.
