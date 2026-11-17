# Adaptive UI Audit

> Static-analysis-based unless a render/screenshot/DOM measurement is cited. Observed pixel/viewport results appear ONLY where a real render exists; every other claim is a static hypothesis with a named render/device validation step.

---

## 1. Executive Summary

**Scope:** [Web | Native | Desktop | Monorepo] · **Apps audited:** [n] · **Runtime render performed:** [Yes / No — static analysis only]

**Adaptive-UI Health:** [Score]/100 ([Healthy / Watch / At Risk / Critical])
_Static analysis — not a rendered/observed score; runtime render required to confirm._
**Previous:** [N]/100, Change: [+/-M] ([improving/declining/unchanged])  _(omit if no history)_

**Overall assessment:** [2–4 sentences — the honest state of adaptive/responsive UI usability across viewports/devices/orientation.]

**Biggest adaptive-UI risks:**
- [CRITICAL/HIGH finding — one line]
- [CRITICAL/HIGH finding — one line]
- [CRITICAL/HIGH finding — one line]

**Confidence posture:** [how much rests on rendered evidence vs static hypotheses needing a render pass.]

---

## 2. Project Profile

| Area | Detected |
|------|----------|
| Framework | [react / next / vue / svelte / react-native / expo / flutter / electron / tauri …] |
| Runtime | [web / react-native / expo / flutter / electron …] |
| Platform | [web / native / desktop] |
| Rendering | [ssr / ssg / islands / csr / native …] |
| Responsive system / breakpoints | [tailwind config / css media queries / MediaQuery / Dimensions …] |
| Viewport meta | [present + content / missing] |
| Safe-area handling | [safe-area-insets / SafeAreaView / none / n/a] |
| Keyboard handling | [KeyboardAvoidingView / adjustResize / none / n/a] |
| Orientation config | [locked portrait / unlocked / responsive …] |
| UI / design-system | [MUI / shadcn / Chakra / RN Paper / custom …] |
| Runtime tools available | [browser MCP / iOS Simulator / Android emulator / none] |

_(Monorepo: add a per-app table — name · platform · framework · responsive system.)_

---

## 3. Adaptive-UI Score

> Scope-conditional. Only areas that apply to the detected platform are scored;
> weights renormalize to 100% for the scope. **Static readiness signal, not a
> rendered/observed score** (unless a render pass was run).

**Web scope**

| Area | Weight | Score |
|------|--------|-------|
| Layout & Overflow | 30% | [Score]/100 |
| Breakpoints & Viewport | 25% | [Score]/100 |
| Adaptive Components & Media | 25% | [Score]/100 |
| Interaction & Reflow | 20% | [Score]/100 |
| **Overall (Adaptive-UI Health)** | **100%** | **[Score]/100 ([Posture])** |

**Desktop scope**

| Area | Weight | Score |
|------|--------|-------|
| Layout & Overflow | 28% | [Score]/100 |
| Breakpoints & Viewport | 18% | [Score]/100 |
| Adaptive Components & Media | 22% | [Score]/100 |
| Interaction & Reflow | 16% | [Score]/100 |
| Window Resize & Min-Size | 16% | [Score]/100 |
| **Overall (Adaptive-UI Health)** | **100%** | **[Score]/100 ([Posture])** |

**Native scope**

| Area | Weight | Score |
|------|--------|-------|
| Keyboard & Input Visibility | 28% | [Score]/100 |
| Adaptive Layout (tablet/orientation/scaling) | 28% | [Score]/100 |
| Safe Area & Insets | 22% | [Score]/100 |
| Touch Ergonomics | 22% | [Score]/100 |
| **Overall (Adaptive-UI Health)** | **100%** | **[Score]/100 ([Posture])** |

**Posture:** Healthy (85–100) · Watch (70–84) · At Risk (50–69) · Critical (0–49)

_(Monorepo: one score line per app + the aggregate method used.)_

---

## 4. Findings

> Ordered by severity → confidence → estimated impact. Root-cause findings list all
> affected locations once.

### AUI-001 — [Short title]
- **Severity:** [CRITICAL|HIGH|MEDIUM|LOW|INFO]
- **Confidence:** [HIGH|MEDIUM|LOW]  ·  **Evidence type:** [Observed (rendered) | Static]
- **Area:** [area] · **App:** [name]
- **Affects:** [viewport(s)/device/orientation — e.g. ≤375px phones, 768–1024 tablet, landscape, 200% zoom]
- **Location:** `[file:line]`  _(+ affected: `[file]`, `[file]`, … — [N] sites, if root-cause)_ _(+ screenshot artifact path if observed)_
- **Evidence:** [code/config shows … OR rendered measurement: scrollWidth 812 > clientWidth 375]
- **Why it matters:** [what the user experiences — content cut off, horizontal scroll, input hidden, wasted space]
- **Recommendation:** [specific fix — name the primitive/breakpoint/wrapper]
- **Effort:** [LOW|MEDIUM|HIGH]
- **Validation:** [exact viewport/device + tool to confirm the fix]

_(Repeat for every finding. If none: "No findings for this scope.")_

---

## 5. Top Priorities

_Max 5, highest impact/confidence first._

1. **[SEVERITY] [Fix X]**
   - Impact: [..]
   - Effort: [Low/Medium/High]
   - Expected outcome: [what should improve]
   - Validation: [viewport/device + tool]

---

## 6. Quick Wins

_Small changes, strong impact/effort ratio._
- [Finding ID — one-line action] — Effort: [Low]

---

## 7. Deeper Fixes

_Architectural changes, or changes that require a render pass before acting._
- [Finding ID / theme — what it entails and the render prerequisite]

---

## 8. Runtime Validation Required

_Everything static analysis cannot determine on its own. No pixel/viewport result is asserted above without one of these._

| Open question | Viewport / device / orientation | Tool | What to look for |
|---------------|--------------------------------|------|------------------|
| [e.g. Horizontal overflow on dashboard] | [320px & 768px] | [browser MCP] | [scrollWidth > clientWidth] |
| [e.g. Login input hidden by keyboard] | [iPhone SE, portrait] | [iOS Simulator] | [focused input covered by keyboard] |
| [e.g. Wasted space on tablet] | [768–1024, landscape] | [Android emulator] | [single-column content stranded at wide width] |

---

## 9. Responsive Coverage Map

_Which routes/screens actually adapt. Surfaces neglected screens ("we forgot tablet on these"). Mark ✅ adapts / ⚠️ partial / ❌ does not / — n/a; render to confirm where static._

| Route/Screen | ≤375 | 768–1024 | ≥1280 | Landscape | Adapts? |
|--------------|------|----------|-------|-----------|---------|
| [/route or Screen] | [✅/⚠️/❌] | [✅/⚠️/❌] | [✅/⚠️/❌] | [✅/⚠️/❌] | [Yes/Partial/No] |

---

## 10. Appendix: Detection & Scan Metadata

**Evidence Index (artifacts):**
- `reports/.artifacts/step_00_aui_discovery.md`
- [web: `step_w1_layout_overflow.md` … `step_w4_web_interaction.md`]
- [native: `step_n1_safe_area.md` … `step_n4_touch_ergonomics.md`]
- [desktop: `step_d1_window_resize.md`]
- `step_x1_framework.md`, `step_x2_responsive_consistency.md`, `step_x3_antipatterns.md`

**Scan Metadata:**

| Field | Value |
|-------|-------|
| Scan date | [YYYY-MM-DD] |
| Scope | [web / native / desktop / monorepo] |
| Apps | [names] |
| Frameworks | [list] |
| Runtime render performed | [Yes/No] · Tools available: [list or none] |
| Findings | [Total] (C:[n] H:[n] M:[n] L:[n] I:[n]) |
| Confidence | H:[n] M:[n] L:[n] |
| Skill | adaptive-ui-audit |

---
Generated by: [plugin name or "adaptive-ui-audit"] v[version]
Skill: adaptive-ui-audit
Date: [YYYY-MM-DD]
---
