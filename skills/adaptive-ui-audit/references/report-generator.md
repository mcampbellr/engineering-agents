# Adaptive UI Audit Report Generator (Step R)

> Synthesize all step artifacts into the final report using assets/report-template.md. Evidence-first, severity + confidence classified, prioritized by impact/effort, scope-aware (web/native/desktop), monorepo-aware, with root-cause deduplication and an honest static-vs-observed score. Hybrid static+runtime. Never invents visual/pixel observations.

---

Goal: Produce `reports/adaptive_ui_audit.md` from the artifacts under
`reports/.artifacts/`. This skill audits only — the report proposes changes; it
never edits application code.

## READ & INTEGRATE ARTIFACTS
- `step_00_aui_discovery.md` — PLATFORMS, APPS, frameworks, responsive system,
  runtime tools → Project Profile, scope.
  If `PLATFORMS=none`, output ONLY: "No web/native/desktop UI detected —
  adaptive-ui-audit targets responsive/adaptive UI usability; nothing to audit
  here." Stop.
- WEB: `step_w1_layout_overflow.md`, `step_w2_breakpoints_viewport.md`, `step_w3_adaptive_components.md`, `step_w4_web_interaction.md`
- NATIVE: `step_n1_safe_area.md`, `step_n2_keyboard_input.md`, `step_n3_adaptive_layout.md`, `step_n4_touch_ergonomics.md`
- DESKTOP/CROSS: `step_d1_window_resize.md`, `step_x1_framework.md`, `step_x2_responsive_consistency.md`, `step_x3_antipatterns.md`
Only in-scope artifacts exist; missing scope artifacts are expected, not errors.
Desktop reuses the WEB areas (W1–W4) PLUS D1.

## MANDATORY PIPELINE (before writing prose)

**Step A — Collect.** Gather every finding from every artifact with: app, area,
severity, confidence, `file:line` OR viewport/route+screenshot artifact,
evidence, why-it-matters, impact-on-which-device/viewport, recommendation,
effort, validation.

**Step B — Merge cross into areas.** Fold x1 (framework) and x2
(responsive-consistency) findings into their tagged area (W1–W4 / D1 / N1–N4).
Do NOT create separate area scores for x1/x2.

**Step C — Apply the anti-pattern filter (x3).** BEFORE scoring, apply x3's
verdicts: drop or downgrade false positives — intentional single-column layouts,
deliberate `overflow-x:auto` carousels / wide data tables, correct fixed sizes
(hairlines, icons, avatars). Add x3's own premature / over-responsive findings
(INFO/LOW). This runs BEFORE scoring.

**Step D — Deduplicate to root cause.** If many locations share ONE cause (a
shared component, a breakpoint token, a layout util, a missing viewport meta),
emit a SINGLE finding: `root cause → affected locations (list, capped with a
count) → systemic recommendation`. Never emit N near-identical findings. Record
the affected-count. In monorepos, a cause in a shared `package/*` is one finding
spanning apps.

**Step E — Classify OBSERVED vs STATIC (NO-INVENTED-OBSERVATIONS).** A
visual/pixel claim (overflow measured, element covered, empty space at width X)
is stated as OBSERVED only if a real runtime render / screenshot / DOM
measurement backs it — cite the tool + viewport/device/orientation + screenshot
artifact path. Every other visual claim MUST read "Static analysis — render at
<viewport/device/orientation> to confirm" and name the confirming tool. Never
assert scrollWidth/clientWidth, "cut off", or "covered" as fact without a citation.

**Step F — Assign IDs.** `AUI-001`, `AUI-002`, … ordered by (severity desc,
confidence desc, estimated impact desc).

**Step G — Score (scope-conditional Adaptive-UI Health).**
- Determine scored areas from scope:
  - web app → W1 Layout & Overflow, W2 Breakpoints & Viewport, W3 Adaptive Components & Media, W4 Interaction & Reflow
  - desktop app → W1–W4 PLUS D1 Window Resize & Min-Size
  - native app → N1 Safe Area & Insets, N2 Keyboard & Input Visibility, N3 Adaptive Layout (tablet/orientation/scaling), N4 Touch Ergonomics
- Default within-scope weights (renormalize to sum 1.00 for the active scope):
  - WEB: W1 0.30 · W2 0.25 · W3 0.25 · W4 0.20
  - DESKTOP: W1 0.28 · W2 0.18 · W3 0.22 · W4 0.16 · D1 0.16
  - NATIVE: N2 0.28 · N3 0.28 · N1 0.22 · N4 0.22 (keyboard & tablet weighted
    highest — the top real-world pains)
- Per area: base 100, then per surviving finding deduct by severity **×
  confidence factor**: CRITICAL −30, HIGH −20, MEDIUM −10, LOW −4, INFO 0;
  confidence factor HIGH ×1.0, MEDIUM ×0.75, LOW ×0.5. Apply area bonuses from the
  reference SCORING HINTS. Clamp each area 0–100.
- Overall = round(Σ area_score × weight). Posture: Healthy 85–100 · Watch 70–84 ·
  At Risk 50–69 · Critical 0–49.
- **Monorepo:** compute per-app overall; the top-level Overall is the
  min-weighted or evidence-based aggregate — state the method. Show a per-app
  score line.
- **Honesty label (mandatory):** if no runtime render was performed, annotate the
  score "Static analysis — not a rendered/observed score; runtime render required
  to confirm." Never present it as an observed/measured pixel result.

**Step H — Verify.** Every finding has severity + confidence + location
(`file:line` or viewport/route+screenshot or explicit "N/A") + validation. Every
score exists. Then write prose.

## REPORT STRUCTURE (this skill's sections — all mandatory)
1. **Executive Summary** — overall assessment; scope (web/native/desktop); apps;
   whether a runtime render was performed (Yes/No); confidence posture; the
   Adaptive-UI Health score with its honesty label; previous score + delta if
   history exists.
2. **Project Profile** — detection table: Framework, Runtime, Platform,
   Rendering, Responsive system/breakpoints, Viewport meta, Safe-area handling,
   Keyboard handling, Orientation config, UI/design-system, Runtime tools
   available. Per-app rows in a monorepo.
3. **Adaptive-UI Score** — scope-conditional area table + Overall + posture +
   honesty label. Per-app scores in a monorepo.
4. **Findings** — ordered severity → confidence → impact. Each finding uses the
   full block (below). Root-cause findings list affected locations + count.
5. **Top Priorities** — max 5. Each: `[SEVERITY] Fix X` + Impact + Effort +
   Expected outcome + Validation viewport/device.
6. **Quick Wins** — small changes with strong impact/effort ratio.
7. **Deeper Fixes** — architectural changes or ones needing a render pass first.
8. **Runtime Validation Required** — everything static: exact
   viewport/device/orientation + tool + what to look for.
9. **Responsive Coverage Map** — a table of routes/screens × does-it-adapt,
   surfacing neglected screens (the "we forgot tablet on these" view).
10. **Appendix: Detection & Scan Metadata** — evidence index (artifacts), scope
    decision, tools available, per-severity + per-confidence counts.

## FINDING BLOCK FORMAT (Section 4)
```
### AUI-00X — [Short title]
- **Severity:** [CRITICAL|HIGH|MEDIUM|LOW|INFO]
- **Confidence:** [HIGH|MEDIUM|LOW]  ·  **Evidence type:** [Observed (rendered) | Static]
- **Area:** [Layout & Overflow | Breakpoints & Viewport | Adaptive Components & Media | Interaction & Reflow | Window Resize | Safe Area | Keyboard & Input | Adaptive Layout | Touch Ergonomics]  ·  **App:** [name]
- **Affects:** [viewport(s)/device/orientation — e.g. ≤375px phones, 768–1024 tablet, landscape, 200% zoom]
- **Location:** `file:line` (+ affected locations & count if root-cause) (+ screenshot artifact path if observed)
- **Evidence:** [code/config shows … OR rendered measurement: scrollWidth 812 > clientWidth 375]
- **Why it matters:** [what the user experiences — content cut off, must scroll horizontally, input hidden, huge empty space]
- **Recommendation:** [specific — not "make it responsive"; name the primitive/breakpoint/wrapper]
- **Effort:** [LOW|MEDIUM|HIGH]
- **Validation:** [exact viewport/device + tool to confirm the fix]
```
Recommendations must be specific. Bad: "Make it responsive." Good: "The
9-column grid overflows at ≤768px; wrap the `<table>` in an `overflow-x:auto`
container and add a stacked-card layout below `md:` — confirm at 375px in the
browser MCP that `scrollWidth == clientWidth`."

If a finding can't answer what/where/affects/why/how-to-fix/how-to-verify, make
it INFO or drop it.

## FORMATTING
Markdown: `#` headings, `**bold**`, tables, `` `file:line` ``. Severity as
`[CRITICAL]`/`[HIGH]`/`[MEDIUM]`/`[LOW]`/`[INFO]`; confidence as
`[HIGH|MEDIUM|LOW]`; evidence type as `Observed (rendered)` or `Static`. Report
starts with the H1 title, nothing before it. Do NOT leak generator/rubric text or
"SCORING HINTS" into the output.

## JSON EXPORT (mandatory)
After the MD, write `reports/adaptive_ui_audit.json` (run `mkdir -p reports`):
```json
{
  "overallScore": 0,
  "posture": "Healthy|Watch|At Risk|Critical",
  "rendered": false,
  "scope": "web|native|desktop|monorepo",
  "apps": [{ "name": "", "platform": "web|native|desktop", "score": 0 }],
  "areaScores": { "layoutOverflow": null, "breakpointsViewport": null, "adaptiveComponents": null, "interactionReflow": null, "windowResize": null, "safeArea": null, "keyboardInput": null, "adaptiveLayout": null, "touchErgonomics": null },
  "findings": { "critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0 },
  "confidence": { "high": 0, "medium": 0, "low": 0 },
  "frameworks": [], "platforms": [], "runtimeToolsAvailable": [],
  "timestamp": "[ISO8601]"
}
```
`areaScores` for areas outside the active scope MUST be `null` (not 0).

## SCORE HISTORY (mandatory, after MD + JSON)
Write `reports/.history/last_aui_scores.json` (run `mkdir -p reports/.history`)
with `overall`, `timestamp`, `scope`, `areaScores`, `findings`, `frameworks`,
`rendered`. If it already exists, read the previous `overall` + `timestamp` first
and surface "Previous: N, Change: ±M (improving|declining|unchanged)" in Section 1.
