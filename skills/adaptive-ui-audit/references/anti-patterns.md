# Cross · Anti-Patterns & Over-Responsiveness (Step X3)

> A dual-purpose guard. (a) It emits its OWN findings for over-engineered responsiveness that adds complexity without a real device/user benefit. (b) It is the false-positive filter every other step must pass its findings through: no finding survives unless `pattern → does it actually break for a real device/user? → verdict` holds. This is what keeps the audit honest and prevents "could be more responsive" noise. Run by the desktop-crosscutting-analyzer.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_aui_discovery.md`.
Also read the other step artifacts as they complete, to sanity-check their findings.

## PRINCIPLE

A layout is NOT broken merely because it *could* adapt differently. A finding is
only valid when all hold:
1. **pattern** — the construct is actually present (evidence `file:line`),
2. **break** — a real device / viewport / orientation / OS setting a real user
   hits actually produces a visible defect (overflow, hidden content, unreachable
   control, clipped text, wasted space that harms the experience),
3. **recommendation** — a concrete, plausible adaptive fix exists.
If the "break" link is missing → downgrade to INFO or drop it. When in doubt,
prefer a render (`references/runtime-validation.md`) over asserting a break.

## NOT defects — do NOT flag these

- **Intentional single-column mobile design** that is fine as one column — a
  narrow, stacked layout on a phone is the CORRECT mobile pattern, not a "missing
  multi-column" defect.
- **Deliberate horizontal scroll** — carousels, horizontal snap lists, code blocks
  with `overflow-x:auto`, and wide data tables wrapped in an `overflow-x:auto`
  container. A table that scrolls *inside its own container* is the CORRECT
  responsive pattern; only a table that pushes the whole PAGE wider (body scrolls
  horizontally) is a defect.
- **Breakpoints that legitimately differ** between components — different content
  genuinely needs different reflow points; a component breaking at 900px instead of
  768px is not an inconsistency to normalize unless it produces a real break.
- **Fixed sizes that are correct** — icons, avatars, logos, hairline borders,
  checkbox/radio glyphs, and other intrinsically fixed UI. A `24px` icon is not a
  "fixed dimension that doesn't adapt".
- **A `max-width` content column on desktop** — capping prose to ~65–75ch is good
  typography, not "wasted space". Only flag wide-width gutters when the gap is
  clearly a neglected layout (e.g. a mobile card list left at ~600px inside a
  1440px window with acres of empty space and no design intent).

## Over-engineering to flag (as findings, usually INFO–LOW)

### 1. JS resize listeners where CSS media / container queries would do
`window.addEventListener('resize', …)`, `useWindowDimensions` + manual branching,
or `Dimensions.get` recomputed on every render to drive purely visual layout that
CSS media/container queries (or Tailwind `sm:`/`lg:`) handle declaratively.
→ INFO/LOW (over-engineering, not a break). Escalate only if it causes a real
jank/relayout problem.

### 2. Needless breakpoint proliferation
A dozen bespoke breakpoints where 2–3 would cover every real device; per-pixel
tweaks that add maintenance cost without a user-visible improvement. → INFO/LOW.

### 3. Premature / speculative responsiveness
Elaborate tablet/foldable/ultrawide handling for a product with no such users, or
orientation-specific layouts for an orientation-locked app. → INFO.

### 4. Redundant / conflicting responsive layers
Inline styles + a media query + a JS branch all fighting over the same dimension;
duplicated breakpoint constants. → LOW (staleness/conflict risk).

## FALSE-POSITIVE FILTER (apply to every other step's findings)

When consolidating, re-check each candidate finding from W*/N*/D1/X1/X2:
- Is the horizontal scroll on the PAGE, or is it an intended in-container scroll
  (carousel / `overflow-x:auto` table)? In-container → drop.
- Is the "fixed dimension" an intrinsically fixed element (icon/avatar)? → drop.
- Is the "wasted space" actually a good `max-width` reading measure? → drop or INFO.
- Is the "missing breakpoint" for a device/orientation this app's users actually
  use? If the app is orientation-locked or has no tablet audience → INFO.
- Does the recommended fix add more complexity than the break justifies? → INFO
  with the tradeoff stated.

## SEVERITY / CONFIDENCE
Own findings are almost always INFO or LOW (they are the *opposite* of urgent).
Never mark an over-responsiveness observation as HIGH/CRITICAL. Confidence reflects
how sure you are it is genuinely a no-benefit cost.

## OUTPUT (mandatory)
Save to `reports/.artifacts/step_x3_antipatterns.md`, with two parts:
1. **Own findings** — over-responsiveness observations (INFO/LOW), each with
   `file:line`, the missing "break" link if borderline, and the simpler alternative.
2. **Filter verdicts** — a list of other-step findings you recommend downgrading or
   dropping, with the reason (which link fails). The report-generator applies these
   BEFORE scoring.
