# Performance Audit

> Static-analysis-based unless a profiling artifact is cited. Runtime numbers appear ONLY where a real measurement exists; every other claim is a static hypothesis with a named validation step.

---

## 1. Executive Summary

**Scope:** [Web | Native | Both] · **Apps audited:** [n] · **Profiling performed:** [Yes / No — static analysis only]

**Static Performance Health:** [Score]/100 ([Healthy / Watch / At Risk / Critical])
_Static analysis — not a measured performance score; runtime profiling required to confirm._
**Previous:** [N]/100, Change: [+/-M] ([improving/declining/unchanged])  _(omit if no history)_

**Overall assessment:** [2–4 sentences — the honest state of client/runtime performance.]

**Biggest performance risks:**
- [CRITICAL/HIGH finding — one line]
- [CRITICAL/HIGH finding — one line]
- [CRITICAL/HIGH finding — one line]

**Confidence posture:** [how much rests on direct evidence vs hypotheses needing profiling.]

---

## 2. Project Profile

| Area | Detected |
|------|----------|
| Framework | [..] |
| Runtime | [web / react-native / expo / flutter …] |
| Build system | [vite / webpack / next / metro …] |
| Rendering | [ssr / ssg / islands / csr / hermes …] |
| Platform | [web / native / both] |
| Package manager | [pnpm / npm / yarn / bun] |
| Data fetching | [react-query / swr / fetch-in-effect …] |
| State management | [..] |
| Image solution | [next/image / expo-image / raw …] |
| Styling | [tailwind / nativewind / css-modules …] |
| Third-party | [analytics / maps / chat / ads / none] |

_(Monorepo: add a per-app table — name · platform · framework · rendering.)_

---

## 3. Performance Score

> Scope-conditional. Only areas that apply to the detected platform are scored;
> weights renormalize to 100% for the scope. **Static readiness signal, not a
> measured score.**

**Web scope**

| Area | Weight | Score |
|------|--------|-------|
| Loading & Core Web Vitals | 22% | [Score]/100 |
| Rendering & Hydration | 22% | [Score]/100 |
| JavaScript & Bundles | 20% | [Score]/100 |
| Network & Data Fetching | 20% | [Score]/100 |
| Assets (Images / Fonts / CSS) | 16% | [Score]/100 |
| **Overall (Static Health)** | **100%** | **[Score]/100 ([Posture])** |

**Native scope**

| Area | Weight | Score |
|------|--------|-------|
| Native Rendering & Lists | 55% | [Score]/100 |
| Native Runtime (Startup/Memory/Anim/Nav/State) | 45% | [Score]/100 |
| **Overall (Static Health)** | **100%** | **[Score]/100 ([Posture])** |

**Posture:** Healthy (85–100) · Watch (70–84) · At Risk (50–69) · Critical (0–49)

_(Monorepo: one score line per app + the aggregate method used.)_

---

## 4. Findings

> Ordered by severity → confidence → estimated impact. Root-cause findings list all
> affected locations once.

### PERF-001 — [Short title]
- **Severity:** [CRITICAL|HIGH|MEDIUM|LOW|INFO]
- **Confidence:** [HIGH|MEDIUM|LOW]
- **Area:** [area] · **App:** [name]
- **Location:** `[file:line]`  _(+ affected: `[file]`, `[file]`, … — [N] sites, if root-cause)_
- **Evidence:** [what the code/config shows]
- **Why it matters:** [technical mechanism of the cost]
- **Impact:** [user-perceived metric / resource affected]
- **Recommendation:** [specific fix — what, where, why]
- **Effort:** [LOW|MEDIUM|HIGH]
- **Validation:** [exact tool + action to confirm improvement]

_(Repeat for every finding. If none: "No findings for this scope.")_

---

## 5. Top Priorities

_Max 5, highest impact/confidence first._

1. **[SEVERITY] [Fix X]**
   - Impact: [..]
   - Effort: [Low/Medium/High]
   - Expected outcome: [what should improve]
   - Validation: [tool + action]

---

## 6. Quick Wins

_Small changes, strong impact/effort ratio._
- [Finding ID — one-line action] — Effort: [Low]

---

## 7. Deeper Optimizations

_Architectural changes, or changes that require profiling before acting._
- [Finding ID / theme — what it entails and the profiling prerequisite]

---

## 8. Runtime Validation Required

_Everything static analysis cannot determine on its own. No numbers are asserted above without one of these._

| Open question | Tool / command | What to look for |
|---------------|----------------|------------------|
| [e.g. Actual LCP] | [Lighthouse / WebPageTest] | [LCP element + timing] |
| [e.g. Re-render cost of X] | [React Profiler] | [render count/duration while doing Y] |
| [e.g. Suspected leak in Z] | [Xcode Instruments Allocations] | [growth across mount/unmount cycles] |

---

## 9. Performance Budget Recommendations

_Only when justified. Audit existing budgets first._
- **Existing budgets:** [found + enforced? / none].
- **Recommended (justified):** [budget + the evidence that motivates it], or
  "None recommended — no evidence a budget is needed yet."

---

## 10. Appendix: Detection & Scan Metadata

**Evidence Index (artifacts):**
- `reports/.artifacts/step_00_perf_discovery.md`
- [web: `step_w1_loading.md` … `step_w5_assets.md`]
- [native: `step_n1_rendering.md`, `step_n2_runtime.md`]
- `step_c1_framework.md`, `step_c2_dependencies.md`, `step_c3_antipatterns.md`, `step_c4_runtime.md`

**Scan Metadata:**

| Field | Value |
|-------|-------|
| Scan date | [YYYY-MM-DD] |
| Scope | [web / native / both] |
| Apps | [names] |
| Frameworks / Build | [list] |
| Profiling performed | [Yes/No] · Tools available: [list or none] |
| Findings | [Total] (C:[n] H:[n] M:[n] L:[n] I:[n]) |
| Confidence | H:[n] M:[n] L:[n] |
| Skill | performance-audit |

---
Generated by: [plugin name or "performance-audit"] v[version]
Skill: performance-audit
Date: [YYYY-MM-DD]
---
