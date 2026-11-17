# Performance Audit Report Generator (Step R)

> Synthesize all step artifacts into the final report using assets/report-template.md. Evidence-first, severity + confidence classified, prioritized by impact/effort, scope-aware, monorepo-aware, with root-cause deduplication and an honest static-health score. Follows ai-audit's rigor but its OWN section structure (below). Never invents runtime metrics.

---

Goal: Produce `reports/performance_audit.md` from the artifacts under
`reports/.artifacts/`. This skill audits only — the report proposes changes; it
never edits application code.

## READ & INTEGRATE ARTIFACTS
- `step_00_perf_discovery.md` — PLATFORM, APPS, frameworks, tooling → Project Profile, scope.
  If `PLATFORM=none`, output ONLY: "No web or native client detected —
  performance-audit targets client/runtime performance; nothing to audit here." Stop.
- Web: `step_w1_loading.md`, `step_w2_rendering.md`, `step_w3_javascript.md`, `step_w4_network.md`, `step_w5_assets.md`
- Native: `step_n1_rendering.md`, `step_n2_runtime.md`
- Cross: `step_c1_framework.md`, `step_c2_dependencies.md`, `step_c3_antipatterns.md`, `step_c4_runtime.md`
Only web or native artifacts exist per the scope; missing scope artifacts are expected, not errors.

## MANDATORY PIPELINE (before writing prose)

**Step A — Collect.** Gather every finding from every artifact with: app, area
(W1–W5 / N1–N2), severity, confidence, `file:line`, evidence, why-it-matters,
impact, recommendation, effort, validation.

**Step B — Merge cross into areas.** Fold C1 (framework) and C2 (dependencies)
findings into their tagged area (W2/W3/N1/N2…). Do NOT create separate area scores
for C1/C2.

**Step C — Apply the anti-pattern filter (C3).** For each finding, apply C3's
filter verdicts: drop or downgrade findings where `pattern→cost→impact` fails.
Add C3's own premature-optimization findings (INFO/LOW). This runs BEFORE scoring.

**Step D — Deduplicate to root cause.** If many locations share ONE cause (a shared
hook/HOC/list component/util/config), emit a SINGLE finding:
`root cause → affected locations (list, capped with a count) → systemic
recommendation`. Never emit N near-identical findings. Record the affected-count.
In monorepos, a cause in a shared `package/*` is one finding spanning apps.

**Step E — Classify measured vs static (C4).** Only findings backed by a real
profiling artifact may carry numbers; all others are "Static — validation
required" and must name the confirming tool. Enforce NO INVENTED METRICS.

**Step F — Assign IDs.** `PERF-001`, `PERF-002`, … ordered by (severity desc,
confidence desc, estimated impact desc).

**Step G — Score (scope-conditional Static Performance Health).**
- Determine scored areas from scope:
  - web app → Loading & CWV (W1), Rendering & Hydration (W2), JavaScript & Bundles (W3), Network & Data (W4), Assets (W5)
  - native app → Native Rendering & Lists (N1), Native Runtime (N2)
- Default within-scope weights (renormalize to sum 1.00 for the active scope):
  - WEB: W1 0.22 · W2 0.22 · W3 0.20 · W4 0.20 · W5 0.16
  - NATIVE: N1 0.55 · N2 0.45
- Per area: base 100, then per surviving finding deduct by severity **×
  confidence factor**: CRITICAL −30, HIGH −20, MEDIUM −10, LOW −4, INFO 0;
  confidence factor HIGH ×1.0, MEDIUM ×0.75, LOW ×0.5. Apply area bonuses from the
  reference SCORING HINTS. Clamp each area 0–100.
- Overall = round(Σ area_score × weight). Posture: Healthy 85–100 · Watch 70–84 ·
  At Risk 50–69 · Critical 0–49.
- **Monorepo:** compute per-app overall; the top-level Overall is the min-weighted
  or evidence-based aggregate — state the method. Show a per-app score line.
- **Honesty label (mandatory):** if `MEASUREMENT_PERFORMED=no`, annotate the score
  "Static analysis — not a measured performance score; runtime profiling required
  to confirm." Never present it as a measured Lighthouse/FPS number.

**Step H — Verify.** Every finding has severity + confidence + `file:line` (or
explicit "Not found"/"N/A") + validation. Every score exists. Then write prose.

## REPORT STRUCTURE (this skill's sections — all mandatory)
1. **Executive Summary** — overall assessment; biggest risks; web/native scope;
   confidence posture; whether runtime profiling was available; the Static Health
   score with its honesty label; previous score + delta if history exists.
2. **Project Profile** — the detection table (Framework, Runtime, Build system,
   Rendering, Platform, Package manager, Data fetching, State management, + Image
   solution, Styling, Third-party). Per-app rows in a monorepo.
3. **Performance Score** — scope-conditional area table + Overall + posture +
   honesty label. Per-app scores in a monorepo. (Include because ai-audit uses
   scoring; label it static — do not fake precision.)
4. **Findings** — ordered severity → confidence → impact. Each finding uses the
   full block (ID, Severity, Confidence, Area, Location, Evidence, Why it matters,
   Impact, Recommendation, Effort, Validation). Root-cause findings list affected
   locations + count.
5. **Top Priorities** — max 5. Each: `[SEVERITY] Fix X` + Impact + Effort +
   Expected outcome + Validation.
6. **Quick Wins** — small changes with strong impact/effort ratio.
7. **Deeper Optimizations** — architectural changes or ones needing profiling first.
8. **Runtime Validation Required** — everything not determinable by static analysis,
   each with the exact tool/command and what to look for (from C4).
9. **Performance Budget Recommendations** — only when justified; audit existing
   budgets; no arbitrary universal numbers.
10. **Appendix: Detection & Scan Metadata** — evidence index (artifacts), scope
    decision, tools available, per-severity + per-confidence counts.

## FINDING BLOCK FORMAT (Section 4)
```
### PERF-00X — [Short title]
- **Severity:** [CRITICAL|HIGH|MEDIUM|LOW|INFO]
- **Confidence:** [HIGH|MEDIUM|LOW]
- **Area:** [Loading & CWV | Rendering | JavaScript & Bundles | Network & Data | Assets | Native Rendering & Lists | Native Runtime]  ·  **App:** [name]
- **Location:** `file:line` (+ affected locations & count if root-cause)
- **Evidence:** [what the code/config shows]
- **Why it matters:** [technical mechanism of the cost]
- **Impact:** [what user-perceived metric / resource it affects]
- **Recommendation:** [specific fix — not "use memoization"; explain what/where/why]
- **Effort:** [LOW|MEDIUM|HIGH]
- **Validation:** [exact tool + action to confirm the fix improved performance]
```
Recommendations must be specific. Bad: "Use memoization." Good: "`SearchResults`
re-sorts `items` (~2k rows) inline on every keystroke because `query` changes
frequently; hoist the sort or wrap it in `useMemo([items])` so it runs only when
`items` changes — confirm the dropped renders with the React Profiler."

If a finding can't answer what/where/why/impact/how-to-fix/how-to-verify, make it
INFO or drop it.

## FORMATTING
Markdown: `#` headings, `**bold**`, tables, `` `file:line` ``. Severity as
`[CRITICAL]`/`[HIGH]`/`[MEDIUM]`/`[LOW]`/`[INFO]`; confidence as
`[HIGH|MEDIUM|LOW]`. Report starts with the H1 title, nothing before it. Do NOT
leak generator/rubric text or "SCORING HINTS" into the output.

## JSON EXPORT (mandatory)
After the MD, write `reports/performance_audit.json` (run `mkdir -p reports`):
```json
{
  "overallScore": 0,
  "posture": "Healthy|Watch|At Risk|Critical",
  "measured": false,
  "scope": "web|native|both",
  "apps": [{ "name": "", "platform": "web|native", "score": 0 }],
  "areaScores": { "loadingCwv": null, "rendering": null, "javascriptBundles": null, "networkData": null, "assets": null, "nativeRenderingLists": null, "nativeRuntime": null },
  "findings": { "critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0 },
  "confidence": { "high": 0, "medium": 0, "low": 0 },
  "frameworks": [], "buildTools": [], "runtimeToolsAvailable": [],
  "timestamp": "[ISO8601]"
}
```
`areaScores` for areas outside the active scope MUST be `null` (not 0).

## SCORE HISTORY (mandatory, after MD + JSON)
Write `reports/.history/last_perf_scores.json` (run `mkdir -p reports/.history`)
with `overall`, `timestamp`, `scope`, `areaScores`, `findings`, `frameworks`,
`measured`. If it already exists, read the previous `overall` + `timestamp` first
and surface "Previous: N, Change: ±M (improving|declining|unchanged)" in Section 1.
