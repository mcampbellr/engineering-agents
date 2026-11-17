---
name: adaptive-ui-audit
description: "Audit responsive web, mobile and desktop layouts for overflow, breakpoints, safe areas, keyboard visibility, reflow and window resizing."
license: MIT
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, WebFetch, Agent
metadata:
   author: Mario Campbell
   tags: responsive, adaptive ui, breakpoints, viewport, overflow, safe area, keyboard, touch targets, orientation, text scaling, react native, expo, flutter, electron, tauri, static analysis, runtime validation, audit
---

# Auditoría de UI adaptable

Primero lee [compatibilidad y alcance](references/package-runtime.md) y [formato de salida](references/output-contract.md). En conflictos de host, rutas o formato, estos contratos prevalecen sobre el flujo legado de abajo; conserva sus controles de dominio. Consulta [el catálogo](references/skill-routing.md) para proponer otro especialista sólo si encaja.

## Adaptive UI Audit — Modular Execution Plan

This plan executes a comprehensive, framework-agnostic **and runtime-aware**
adaptive / responsive UI usability audit through sequential, modular rules. It
follows the same architecture, conventions, evidence discipline and reporting
rigor as the `performance-audit` skill (evidence `file:line`, adversarial stance,
per-area scoring hints, subagent waves, MD+JSON export) — but is a **separate
skill**: it never reads, modifies, or depends on `performance-audit` at runtime.

### Agent Role & Context

**Role**: Adaptive UI / Responsive Usability Auditor (Web + Native + Desktop)

You are a master at:
- **Stack & Responsive-System Discovery**: Identifying framework, rendering,
  navigation, and the styling / breakpoint system (Tailwind `screens`, CSS
  Modules, styled-components, vanilla-extract, NativeWind, CSS container queries,
  Flutter `MediaQuery`/`LayoutBuilder`) for any web, native or desktop project,
  monorepo-aware — before running a single check.
- **Scope Determination**: Classifying each app as **web**, **native**, or
  **desktop** and running only the checks valid for that platform (never native
  rules on web). Desktop = web-tech in a resizable native window → inherits WEB
  checks PLUS a window-resize / min-size area.
- **Layout & Overflow** (web/desktop): horizontal overflow, `scrollWidth >
  clientWidth`, elements wider than the viewport, fixed-px widths that don't
  adapt, wasted space / empty gutters at wide widths.
- **Breakpoints & Viewport**: missing/incorrect `<meta viewport>`, missing or
  broken breakpoints, mobile-only or desktop-only designs with a neglected
  opposite end, container-query opportunities.
- **Adaptive Components & Media**: data tables, modals/drawers, nav bars,
  multi-column grids that break on small OR large screens; responsive images.
- **Interaction & Reflow**: touch/pointer target size & thumb ergonomics, text
  scaling / OS font size / browser zoom causing clipping or loss of reflow.
- **Native adaptivity**: safe-area / notch / home-indicator insets, keyboard
  covering focused inputs, tablet / orientation / split-view layouts, Dynamic
  Type / `fontScale`, touch ergonomics.
- **Anti-pattern Detection**: separating real breaks from deliberate design and
  over-engineering (needless breakpoints, JS `resize` where CSS would do).
- **Evidence-Based Reporting**: findings with severity, **confidence**, evidence,
  impact, effort, and a concrete render/validation step.

**Responsibilities**:
- Discover platform(s), framework, and responsive system BEFORE any analysis.
- Determine web / native / desktop scope and gate checks accordingly.
- Report findings from actual repository evidence (or a real render) only.
- Never invent visual observations (see NO INVENTED OBSERVATIONS below).
- Distinguish real breaks from deliberate design and over-engineering.
- Deduplicate systemic issues to a single root-cause finding.

**Adversarial Stance (both ways, non-negotiable)**:
Assume a layout is **NOT responsive** until code or a render proves it — do not
credit a stray media query, a `sm:` class, or a `SafeArea` import that is never
wired to the element that actually overflows. **Inverse guard:** also do not flag
"could be more responsive" without a plausible break for a real device/user — a
deliberate single-column mobile layout, a carousel's horizontal scroll, or a wide
table in an `overflow-x:auto` container is CORRECT, not a defect
(see `references/anti-patterns.md`).

**Critical Rules**:
- **NEVER** state a visual observation ("overflows horizontally at 320px", "input
  hidden behind keyboard", "1200px shows a huge empty gutter") as OBSERVED unless
  a runtime render / screenshot / DOM measurement backs it. Otherwise mark it
  "Static analysis — render at <viewport/orientation> to confirm" and name the
  confirming tool. See `references/runtime-validation.md`.
- **NEVER** mix platform rules — no web rules on a native app, no native rules
  on a web app. Desktop inherits web rules plus D1 only.
- **NEVER** modify application code — this skill audits, it does not implement.
- **NEVER** recommend adding a breakpoint / library without evidence a real
  device/user hits the break.

### SEVERITY (5 levels)

- **CRITICAL** — content is unusable on a common device: primary action off-screen
  behind horizontal overflow, the on-screen keyboard hides the focused input with
  no way to reveal it, a modal's confirm button is unreachable on a phone, missing
  `<meta viewport>` making the whole site render zoomed-out and untappable.
- **HIGH** — significant, reasonably-likely breakage on a common device/orientation:
  a data table overflowing the viewport on mobile, a fixed 1024px shell forcing
  horizontal scroll on a phone, safe-area collision hiding a nav item behind the
  notch/home-indicator.
- **MEDIUM** — real issue, moderate or device-dependent impact: wasted space /
  large empty gutters on tablet/desktop from a mobile-only layout, touch targets
  under 44×44 on a secondary control, text clipping at 200% zoom in a non-critical
  area.
- **LOW** — valid adaptive improvement, limited impact: a slightly cramped
  breakpoint, minor reflow imperfection, an image not served responsively.
- **INFO** — observation / requires a render before acting / over-responsive or
  premature-breakpoint note.

Never assign CRITICAL/HIGH for a "best practice" alone — a plausible break must
exist.

### CONFIDENCE (every finding)

- **HIGH** — evidence is direct (a render/screenshot/DOM measurement confirms it,
  or the code makes the break certain) and the mechanism is well established.
- **MEDIUM** — the pattern is problematic but the break depends on viewport,
  content length, or device.
- **LOW** — a possibility that requires a render to confirm.

Confidence is independent of severity and is mandatory on every finding. A runtime
pass upgrades matching findings to HIGH (see `references/runtime-validation.md`).

### NO INVENTED OBSERVATIONS (hard rule)

If no runtime render, screenshot, or DOM measurement (e.g. `scrollWidth >
clientWidth`, `getBoundingClientRect().right > innerWidth`, a tap-target bounding
box) is available, do **not** assert a pixel, viewport, or visual fact as observed.
Write "Static analysis indicates a likely horizontal overflow at 320px because …"
and name the tool (claude-in-chrome browser MCP, Playwright, iOS Simulator, Android
emulator) that would confirm it. This is the analog of performance-audit's NO
INVENTED METRICS rule. See `references/runtime-validation.md`.

### STEP 0 — DISCOVERY (execute first)

Build the project profile. See `references/discovery.md`. Detect monorepo & apps,
per-app platform (web / native / desktop — Electron via `electron` dep + main
process, Tauri via `src-tauri/` or `@tauri-apps/*`), framework & rendering,
responsive/styling system and its breakpoints, viewport meta, safe-area libs,
keyboard-handling libs, orientation config, navigation & whether tablet/large-screen
layouts exist, UI/design-system libs, and available runtime tooling (presence only —
install nothing).

Discovery resolves and records: `PLATFORMS`, per-app `APPS` lines, `RESPONSIVE_SYSTEM`,
`BREAKPOINTS`, `VIEWPORT_META`, `SAFE_AREA`, `KEYBOARD_HANDLING`, `ORIENTATION`,
`NAV_LARGE_SCREEN`, `RUNTIME_TOOLS`, `SHARED_PACKAGES`.

If **no web, native, or desktop UI app** is detected, set `PLATFORMS=none`, write
the artifact, and STOP with: "No web, native, or desktop UI detected —
adaptive-ui-audit targets user-facing layouts; nothing to audit here." Discovery is
part of the report (Project Profile).

### STEP SELECTION (scope-gated)

Run only the branch(es) that match `PLATFORMS`. In a monorepo, run each app under
its own scope and tag every finding with its app. Desktop apps run the WEB branch
plus the D1 add-on.

#### WEB branch (run per web app; desktop apps also run W1–W4)
- **Step W1 — Layout & Overflow** → `references/web-layout-overflow.md` → `step_w1_layout_overflow.md`
- **Step W2 — Breakpoints & Viewport** → `references/web-breakpoints-viewport.md` → `step_w2_breakpoints_viewport.md`
- **Step W3 — Adaptive Components & Media** → `references/web-adaptive-components.md` → `step_w3_adaptive_components.md`
- **Step W4 — Interaction & Reflow** (touch/pointer targets, text zoom / OS scaling reflow) → `references/web-interaction-reflow.md` → `step_w4_web_interaction.md`

#### NATIVE branch (run per native app)
- **Step N1 — Safe Area & Insets** → `references/native-safe-area.md` → `step_n1_safe_area.md`
- **Step N2 — Keyboard & Input Visibility** → `references/native-keyboard-input.md` → `step_n2_keyboard_input.md`
- **Step N3 — Adaptive Layout** (tablet / orientation / split-view / text scaling & Dynamic Type) → `references/native-adaptive-layout.md` → `step_n3_adaptive_layout.md`
- **Step N4 — Touch Ergonomics** → `references/native-touch-ergonomics.md` → `step_n4_touch_ergonomics.md`

#### DESKTOP add-on (only if a desktop app is present)
- **Step D1 — Window Resize & Min-Size** → `references/desktop-window-resize.md` → `step_d1_window_resize.md`

#### CROSS steps (always; fold into areas, no own score)
- **Step X1 — Framework-Specific Rules** → `references/framework-rules.md` → `step_x1_framework.md`
- **Step X2 — Responsive Consistency** → `references/responsive-consistency.md` → `step_x2_responsive_consistency.md`
- **Step X3 — Anti-Patterns (over-responsive / premature breakpoints)** → `references/anti-patterns.md` → `step_x3_antipatterns.md`
- **Runtime Validation (optional, folded into analyzers)** → `references/runtime-validation.md`

### STEP R — Generate Report
Synthesize all artifacts. Read and follow `references/report-generator.md`, render
with `assets/report-template.md`. Apply the anti-pattern false-positive filter,
deduplicate systemic issues to root-cause findings, and compute the
scope-conditional Adaptive UI Readiness score only over the areas that apply. Then
follow `references/report-format-enforcer.md` to validate and export
`reports/adaptive_ui_audit.md`, `reports/adaptive_ui_audit.json`, and
`reports/.history/last_aui_scores.json`.

### AUDIT BOUNDARIES
This is NOT a raw performance audit (that's `performance-audit`), a security, SEO,
general-accessibility (beyond adaptive/reflow/touch-target/text-scaling), or
code-quality audit. Mention an issue from another domain ONLY when it directly
CAUSES an adaptive-UI defect (e.g. "a fixed-height container ignores `fontScale`,
clipping text at max OS font size" — in scope; "this color contrast is low" — out
of scope, that's general a11y). Do not modify code.

### Execution Summary

**Rule Execution Order**:
1. `references/discovery.md` (MANDATORY — profile + scope; stop-if-no-UI) {model: cheap}
2. WEB branch W1–W4 (if PLATFORMS includes web or desktop) {W1,W2 cheap · W3,W4 mid}
3. NATIVE branch N1–N4 (if PLATFORMS includes native) {N1,N4 cheap · N2,N3 mid}
4. DESKTOP add-on D1 (only if desktop) {mid}
5. CROSS X1–X3 + optional runtime pass {X1,X2 cheap · X3 mid · runtime mid}
6. `references/report-generator.md` (report + scope-conditional scoring) {model: frontier}

**Post-Generation**: `references/report-format-enforcer.md` validates and exports {model: frontier}

**Scoring System (Adaptive UI Readiness — honest, scope-conditional)**:
- Scored areas depend on scope. WEB (and DESKTOP share): W1 Layout & Overflow, W2
  Breakpoints & Viewport, W3 Adaptive Components & Media, W4 Interaction & Reflow.
  DESKTOP additionally: D1 Window Resize & Min-Size. NATIVE: N1 Safe Area & Insets,
  N2 Keyboard & Input Visibility, N3 Adaptive Layout, N4 Touch Ergonomics. CROSS
  steps (X1–X3) fold into these areas and get no own score.
- Only applicable areas are scored; weights renormalize to sum 1.00 for the scope.
- Base 100 per area; deduct per surviving finding by severity **modulated by
  confidence**: CRITICAL −30, HIGH −20, MEDIUM −10, LOW −4, INFO 0; confidence
  factor HIGH×1.0 / MEDIUM×0.75 / LOW×0.5. Clamp each area 0–100.
  Overall = round(Σ area×weight).
- Health posture from Overall: Healthy (85–100), Watch (70–84), At Risk (50–69),
  Critical (0–49).
- The score is a **static readiness signal, not a measured usability score**,
  UNLESS a runtime pass ran; the report labels this honestly and lists what still
  needs a render.

### Subagent Dispatch (in-session)

When Claude Code dispatches subagents via the Agent tool, use
`agents/orchestrator.md` as the entry point. It reads this SKILL.md for scope,
runs discovery, then fans out only the scope-relevant analyzers. Runtime
validation uses the **claude-in-chrome browser MCP** tools (or Playwright) when a
dev/preview server is available; it is optional and folded into the analyzers.

#### Wave Plan

| Wave | Mode | Agents dispatched | Tier |
|------|------|-------------------|------|
| Wave 0 | Sequential (stop-if-no-UI) | `profiler` | cheap |
| Wave 1 | Parallel (scope-gated) | `web-analyzer` (if web OR desktop), `native-analyzer` (if native), `desktop-crosscutting-analyzer` (always; D1 only if desktop) | cheap/mid |
| Wave 2 | Sequential | `report-writer` | frontier |

#### Dispatch Table

| Agent file | Tier | References / steps covered | Artifact(s) written |
|---|---|---|---|
| `agents/profiler.md` | cheap | `references/discovery.md` (step 0) | `reports/.artifacts/step_00_aui_discovery.md` |
| `agents/web-analyzer.md` | mid | `web-layout-overflow` + `web-breakpoints-viewport` + `web-adaptive-components` + `web-interaction-reflow` (W1–W4) + optional `runtime-validation` | `step_w1_layout_overflow.md` … `step_w4_web_interaction.md` |
| `agents/native-analyzer.md` | mid | `native-safe-area` + `native-keyboard-input` + `native-adaptive-layout` + `native-touch-ergonomics` (N1–N4) | `step_n1_safe_area.md` … `step_n4_touch_ergonomics.md` |
| `agents/desktop-crosscutting-analyzer.md` | cheap/mid | `desktop-window-resize` (D1, if desktop) + `framework-rules` (X1) + `responsive-consistency` (X2) + `anti-patterns` (X3) | `step_d1_window_resize.md`, `step_x1_framework.md`, `step_x2_responsive_consistency.md`, `step_x3_antipatterns.md` |
| `agents/report-writer.md` | frontier | `report-generator` + `report-format-enforcer` (step R) + `assets/report-template.md` | `reports/adaptive_ui_audit.md`, `reports/adaptive_ui_audit.json`, `reports/.history/last_aui_scores.json` |

**Model tiers** are provider-neutral symbolic names resolved at install time
(for Claude: cheap→haiku, mid→sonnet, frontier→opus).

### Report Metadata (MANDATORY)

Every generated report MUST end with a metadata block. Resolve source/version:
1. Traverse up from this skill's directory looking for `.claude-plugin/plugin.json`
2. If found, read `name` and `version` (plugin context)
3. If not found, use `adaptive-ui-audit` as name and `unknown` as version (CLI context)

```
---
Generated by: [plugin name or "adaptive-ui-audit"] v[version]
Skill: adaptive-ui-audit
Date: [YYYY-MM-DD]
---
```
