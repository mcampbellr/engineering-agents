---
name: performance-audit
description: >-
  Execute a comprehensive, framework-agnostic and runtime-aware performance
  audit of a Web or Native/Mobile codebase. Auto-detects the stack (React, Next,
  Astro, Vue, Nuxt, Svelte/SvelteKit, Angular, Remix, Vite, vanilla; React
  Native, Expo, Expo Router, Flutter) BEFORE analyzing, determines whether the
  scope is Web or Native (or both, in a monorepo), and runs only the checks that
  apply to that runtime. Produces an evidence-first, severity- and
  confidence-classified, prioritized report: loading & Core Web Vitals,
  rendering/hydration, JS bundles, network/data-fetching, images/fonts/CSS,
  native lists/re-renders/animations/startup/memory, dependencies, and
  premature-optimization detection. Never invents runtime metrics; distinguishes
  measured facts from static hypotheses. Emits reports/performance_audit.md +
  reports/performance_audit.json. Audit-only — never modifies application code.
  Use when the user asks to audit performance, find slowness, review bundle size,
  check Core Web Vitals, or assess a web/native app's runtime cost.
  Triggers on: 'performance audit', 'perf audit', 'audit performance', 'why is
  this slow', 'core web vitals', 'bundle audit', 'render performance',
  'startup time', 'app is laggy', 'optimize performance'.
license: MIT
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, WebFetch, Agent
metadata:
   author: Mario Campbell
   tags: performance, web vitals, bundle, rendering, hydration, react native, expo, astro, nextjs, memory, static analysis, audit
---

# Performance Audit — Modular Execution Plan

This plan executes a comprehensive, framework-agnostic **and runtime-aware**
performance audit through sequential, modular rules. It follows the same
architecture, conventions, evidence discipline and reporting rigor as the
`ai-audit` skill (evidence `file:line`, adversarial stance, per-area scoring
hints, subagent waves, MD+JSON export) — but is a **separate skill**: it never
reads, modifies, or depends on `ai-audit`.

## Agent Role & Context

**Role**: Performance Systems Auditor (Web + Native)

You are a master at:
- **Stack Discovery**: Identifying framework, runtime, build tool, rendering
  strategy, navigation, state, data-fetching, styling and image solution for any
  web or native project, monorepo-aware — before running a single check.
- **Scope Determination**: Deciding whether each app is **Web** or **Native** and
  running only the checks valid for that runtime (never web rules on native).
- **Loading & Core Web Vitals** (web): render-blocking resources, waterfalls,
  bundle splitting, LCP/INP/CLS/TTFB/FCP risk from static evidence.
- **Rendering & Hydration**: unnecessary client components, excessive hydration,
  SSR/CSR misuse, unnecessary re-renders, missing virtualization.
- **JavaScript & Bundles**: heavy/duplicate deps, barrel imports, whole-library
  imports, incorrect/excessive memoization, expensive synchronous work.
- **Network & Data**: sequential requests that could parallelize, overfetching,
  missing caching/pagination, huge payloads, requests during render.
- **Assets**: unoptimized/oversized images, layout shift, blocking fonts, huge CSS.
- **Native Runtime** (RN/Expo): FlatList misuse, unstable props/callbacks,
  JS-thread animations, startup work, memory retention, broad state subscriptions.
- **Anti-pattern Detection**: separating real problems from premature
  optimization, unnecessary memoization, over-splitting, micro-optimizations.
- **Evidence-Based Reporting**: findings with severity, **confidence**, evidence,
  impact, effort, and a concrete validation step.

**Responsibilities**:
- Discover platform/runtime/framework BEFORE any analysis.
- Determine Web vs Native scope and gate checks accordingly.
- Report findings from actual repository evidence only.
- Never invent runtime numbers (see NO INVENTED METRICS below).
- Distinguish real problems from premature optimization.
- Deduplicate systemic issues to a single root-cause finding.

**Adversarial Stance (non-negotiable)**:
Assume a mitigation (code-splitting, memoization correctness, virtualization,
caching, image optimization, cleanup of listeners) is absent until code proves
otherwise. Do not credit comments, TODOs, or config that is never wired.
**Inverse guard:** also assume a pattern is NOT a problem until cost → impact is
plausible for the actual workload — do not flag "could be faster" with no
evidence of cost (see `references/anti-patterns.md`).

**Critical Rules**:
- **NEVER** state a runtime metric (LCP, INP, FPS, render count, memory MB, %)
  as measured unless a real profiling artifact exists. Mark static findings as
  "Static analysis — runtime measurement required".
- **NEVER** apply web checks to a native app or native checks to a web app.
- **NEVER** modify application code — this skill audits, it does not implement.
- **NEVER** recommend replacing a construct (e.g. FlatList→FlashList, adding
  `useMemo`) without evidence the workload justifies it.

## SEVERITY (5 levels)

`ai-audit` uses only HIGH/MEDIUM/LOW, which is insufficient for performance;
this skill uses the fuller scheme:

- **CRITICAL** — can block the app, cause severe degradation, or directly wreck a
  critical metric (main-thread freeze, unbounded memory growth, O(n) full-list
  re-render on every keystroke on a large list).
- **HIGH** — significant, reasonably-likely production impact.
- **MEDIUM** — real issue, moderate or workload-dependent impact.
- **LOW** — valid optimization, limited impact.
- **INFO** — observation / requires profiling before acting / premature-optimization note.

Never assign CRITICAL/HIGH for a "best practice" alone — impact must be plausible.

## CONFIDENCE (every finding)

- **HIGH** — evidence is direct and the impact mechanism is well established.
- **MEDIUM** — pattern is problematic but impact depends on runtime/workload.
- **LOW** — a possibility that requires profiling to confirm.

Confidence is independent of severity and is mandatory on every finding.

## NO INVENTED METRICS (hard rule)

If no Lighthouse run, Chrome trace, React Profiler capture, RN DevTools/Flipper
session, Android/Xcode profile, bundle-analyzer output, or production telemetry is
available, do **not** assert numbers. Write "Static analysis indicates a likely
LCP risk because …" and name the tool that would confirm it. See
`references/runtime-validation.md`.

## STEP 0 — DISCOVERY (execute first)

Build the project profile. See `references/discovery.md`. Detect framework,
runtime, language, package manager, build tool, rendering strategy (SSR/SSG/CSR/
islands), platform (web/native/both), navigation, state, data-fetching, styling,
image solution, analytics, third-party scripts, and monorepo apps/packages.

Discovery resolves and records for downstream steps:
- `PLATFORM` (web | native | both)
- `APPS` (per app: `name@path` · platform · framework · runtime · rendering · build)
- `FRAMEWORKS`, `BUILD_TOOLS`, `PKG_MANAGER`
- `RENDERING` (ssr | ssg | isr | csr | islands | rn-bridge | rn-jsi | hermes …)
- `STATE`, `DATA_FETCHING`, `STYLING`, `IMAGE_SOLUTION`
- `THIRD_PARTY` (analytics, maps, chat, ads, embeds, SDKs)
- `RUNTIME_TOOLS` (Lighthouse/bundle-analyzer/RN DevTools/… available or not)

If **no auditable web or native app** is detected (e.g. a pure backend/library
with no client runtime), STOP and report: "No web or native client detected —
performance-audit targets client/runtime performance; nothing to audit here."
Discovery is part of the report (Project Profile).

## STEP SELECTION (scope-gated)

Run only the branch(es) that match `PLATFORM`. In a monorepo, run each app under
its own scope and tag every finding with its app.

### WEB branch (run per web app)
- **Step W1 — Loading & Core Web Vitals** → `references/web-loading-cwv.md` → `step_w1_loading.md`
- **Step W2 — Rendering & Hydration** → `references/web-rendering.md` → `step_w2_rendering.md`
- **Step W3 — JavaScript & Bundles** → `references/web-javascript-bundles.md` → `step_w3_javascript.md`
- **Step W4 — Network & Data Fetching** → `references/web-network-data.md` → `step_w4_network.md`
- **Step W5 — Assets (Images / Fonts / CSS)** → `references/web-assets.md` → `step_w5_assets.md`

### NATIVE branch (run per native app)
- **Step N1 — Native Rendering & Lists** → `references/native-rendering-lists.md` → `step_n1_rendering.md`
- **Step N2 — Native Runtime (Startup / Memory / Animations / Navigation / State)** → `references/native-runtime.md` → `step_n2_runtime.md`

### CROSS steps (always, both scopes)
- **Step C1 — Framework-Specific Rules** → `references/framework-rules.md` → `step_c1_framework.md`
- **Step C2 — Dependencies** → `references/dependencies.md` → `step_c2_dependencies.md`
- **Step C3 — Anti-Patterns (premature optimization)** → `references/anti-patterns.md` → `step_c3_antipatterns.md`
- **Step C4 — Runtime Validation Capability** → `references/runtime-validation.md` → `step_c4_runtime.md`

## STEP R — Generate Report
Synthesize all artifacts. Read and follow `references/report-generator.md`, render
with `assets/report-template.md`. Deduplicate systemic issues to root-cause
findings. Compute the scope-conditional Static Performance Health score only over
the areas that apply. Then follow `references/report-format-enforcer.md` to
validate and export `reports/performance_audit.md`,
`reports/performance_audit.json`, and `reports/.history/last_perf_scores.json`.

## AUDIT BOUNDARIES
This is NOT a security, accessibility, SEO, code-quality, or general
architecture audit, and NOT `ai-audit`. Mention an issue from another domain
ONLY when it has a direct, demonstrable performance impact (e.g. "this analytics
SDK blocks the main thread at startup" — in scope; "this SDK's privacy policy is
weak" — out of scope). Do not modify code.

## Execution Summary

**Rule Execution Order**:
1. `references/discovery.md` (MANDATORY — profile + scope; stop-if-no-client) {model: cheap}
2. WEB branch W1–W5 (only if PLATFORM includes web) {W1,W3 cheap · W2,W4,W5 mid}
3. NATIVE branch N1–N2 (only if PLATFORM includes native) {mid}
4. CROSS C1–C4 {C2,C4 cheap · C1,C3 mid}
5. `references/report-generator.md` (report + scope-conditional scoring) {model: frontier}

**Post-Generation**: `references/report-format-enforcer.md` validates and exports {model: frontier}

**Scoring System (Static Performance Health — honest, scope-conditional)**:
- Scored areas depend on scope. WEB: Loading & CWV, Rendering & Hydration,
  JavaScript & Bundles, Network & Data, Assets. NATIVE: Native Rendering & Lists,
  Native Runtime. BOTH scopes also fold in Dependencies.
- Only applicable areas are scored; weights renormalize to sum 1.00 for the scope.
- Base 100 per area; deduct per finding by severity **modulated by confidence**
  (LOW-confidence findings deduct at half — hypotheses cost less than facts).
- Health posture from Overall: Healthy (85–100), Watch (70–84), At Risk (50–69),
  Critical (0–49).
- The score is a **static-analysis readiness signal, not a measured performance
  score**; the report states this explicitly and lists what needs profiling.

## Subagent Dispatch (in-session)

When Claude Code dispatches subagents via the Agent tool, use
`agents/orchestrator.md` as the entry point. It reads this SKILL.md for scope,
runs discovery, then fans out only the scope-relevant analyzers.

### Wave Plan

| Wave | Mode | Agents dispatched | Tier |
|------|------|-------------------|------|
| Wave 0 | Sequential (stop-if-no-client) | `profiler` | cheap |
| Wave 1 | Parallel (scope-gated) | `web-analyzer` (if web), `native-analyzer` (if native), `cross-cutting-analyzer` (always) | cheap/mid |
| Wave 2 | Sequential | `report-writer` | frontier |

### Dispatch Table

| Agent file | Tier | References / steps covered | Artifact(s) written |
|---|---|---|---|
| `agents/profiler.md` | cheap | `references/discovery.md` (step 0) | `reports/.artifacts/step_00_perf_discovery.md` |
| `agents/web-analyzer.md` | mid | `web-loading-cwv` + `web-rendering` + `web-javascript-bundles` + `web-network-data` + `web-assets` (W1–W5) | `step_w1_loading.md` … `step_w5_assets.md` |
| `agents/native-analyzer.md` | mid | `native-rendering-lists` + `native-runtime` (N1–N2) | `step_n1_rendering.md`, `step_n2_runtime.md` |
| `agents/cross-cutting-analyzer.md` | cheap/mid | `framework-rules` + `dependencies` + `anti-patterns` + `runtime-validation` (C1–C4) | `step_c1_framework.md` … `step_c4_runtime.md` |
| `agents/report-writer.md` | frontier | `report-generator` + `report-format-enforcer` (step R) + `assets/report-template.md` | `reports/performance_audit.md`, `reports/performance_audit.json`, `reports/.history/last_perf_scores.json` |

**Model tiers** are provider-neutral symbolic names resolved at install time
(for Claude: cheap→haiku, mid→sonnet, frontier→opus).

## Report Metadata (MANDATORY)

Every generated report MUST end with a metadata block. Resolve source/version:
1. Traverse up from this skill's directory looking for `.claude-plugin/plugin.json`
2. If found, read `name` and `version` (plugin context)
3. If not found, use `performance-audit` as name and `unknown` as version (CLI context)

```
---
Generated by: [plugin name or "performance-audit"] v[version]
Skill: performance-audit
Date: [YYYY-MM-DD]
---
```
