# Web · Layout & Overflow (Step W1, scored area, base 100)

> Evaluate whether the layout adapts across viewport widths without horizontal overflow, wasted space at wide widths, clipping from fixed heights, or avoidable scroll. Web scope only (and desktop apps rendered in a resizable window). A visual claim is OBSERVED only with a runtime render/DOM measurement; otherwise it is "Static analysis — render at <viewport> to confirm" and must name the tool.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_aui_discovery.md` for
`PLATFORMS`, `APPS`, `RESPONSIVE_SYSTEM`, `BREAKPOINTS`, `STYLING`. Run only for apps
tagged web (or desktop web-tech in a resizable window). Skip native apps. In a
monorepo, tag every finding with its app.

## Checks

### 1. Horizontal overflow / unexpected page scroll (HIGH)
Fixed px widths on layout elements, `100vw` used where a scrollbar is present,
`white-space:nowrap` on long text, unconstrained images/iframes/`<pre>`/tables,
negative margins, or absolutely/`fixed`-positioned elements that extend past the
viewport. Any of these can force a horizontal scrollbar on small screens.
```bash
grep -rniE 'width:\s*[0-9]{3,}px|min-width:\s*[0-9]{3,}px' . \
  --include='*.css' --include='*.scss' --include='*.tsx' --include='*.jsx' --include='*.vue' -n 2>/dev/null \
  | grep -v node_modules | head -30
grep -rniE '100vw|white-space:\s*nowrap|overflow-x:\s*(visible|scroll)' . \
  --include='*.css' --include='*.scss' --include='*.tsx' --include='*.vue' -n 2>/dev/null | grep -v node_modules | head -20
```
Runtime confirm (see `references/runtime-validation.md`): at 320/360/390 check
`document.documentElement.scrollWidth > document.documentElement.clientWidth`, then
find the culprit with elements whose `getBoundingClientRect().right > innerWidth`.
Record an OBSERVED block (viewport, route, screenshot path, measured value), confidence HIGH.

### 2. Wasted space / visual gaps at wide widths (HIGH)
The "tablet/desktop was neglected" defect: mobile-first single-column layouts with
no `max-width` container and no wide-screen breakpoint, so content stretches edge to
edge or leaves huge empty gutters at ≥1024/≥1280. Content that never uses the extra
width; giant whitespace beside a phone-width column centered on a 1440 screen.
```bash
# Absence signals: no max-width container, no min-width breakpoints beyond a small cap
grep -rniE 'max-width:|container|@media[^{]*min-width' . \
  --include='*.css' --include='*.scss' --include='*.tsx' --include='*.vue' -n 2>/dev/null | grep -v node_modules | head -20
grep -rniE '@media[^{]*max-width:\s*(4|5|6|7)[0-9]{2}px' . --include='*.css' --include='*.scss' -n 2>/dev/null | grep -v node_modules | head
```
Runtime confirm: render at 1280 and 1440, measure main content width vs viewport
width (empty-gutter ratio), screenshot. Report the gutter fraction as OBSERVED.

### 3. Fixed heights causing clipping / forced inner scroll (MEDIUM)
`height: NNNpx` on containers whose content grows, `overflow:hidden` that clips
overflowing content, and `100vh` bugs on mobile (address-bar / dynamic viewport
cropping) where `100dvh`/`100svh` is the correct unit.
```bash
grep -rniE 'height:\s*[0-9]+px|overflow:\s*hidden|height:\s*100vh|min-height:\s*100vh' . \
  --include='*.css' --include='*.scss' --include='*.tsx' --include='*.vue' -n 2>/dev/null | grep -v node_modules | head -30
```
Runtime confirm: at 360×640 and 390×844 check whether inner content is clipped
(`scrollHeight > clientHeight` on a `overflow:hidden` box) and whether `100vh`
overshoots the visible viewport. Recommend `100dvh` where the address bar clips.

### 4. Vertical layout forcing avoidable scroll on short/wide viewports (LOW–MEDIUM)
Fixed spacing/margins (large fixed `padding`/`margin`/`gap` in px) that push
content off a short or landscape viewport when it should fit — e.g. a login card
that scrolls on a 1024×640 landscape tablet purely from oversized fixed gaps.
```bash
grep -rniE '(margin|padding|gap|top|bottom):\s*[0-9]{2,}px' . \
  --include='*.css' --include='*.scss' -n 2>/dev/null | grep -v node_modules | wc -l
```
Runtime confirm: render at 1024×640 (landscape) and a short viewport; check whether
above-the-fold content that should fit triggers vertical scroll. Screenshot.

## SEVERITY GUIDE
- CRITICAL: primary content unreachable/clipped with no scroll at a common viewport.
- HIGH: horizontal page scroll at ≤390px; desktop/tablet left unstyled with massive empty gutters.
- MEDIUM: fixed-height clipping, `100vh` mobile overshoot, inner forced scroll.
- LOW/INFO: avoidable vertical scroll from oversized fixed spacing; cosmetic only.

## CONFIDENCE GUIDE
- HIGH: measured at runtime (`scrollWidth>clientWidth`, gutter ratio, clipped box) with screenshot.
- MEDIUM: strong static signal (fixed px width on a layout wrapper) not yet rendered.
- LOW: inferred overflow that depends on runtime content length → render to confirm.

## SCORING HINTS
Base 100. Deduct (× confidence HIGH1.0/MED0.75/LOW0.5): CRITICAL −30, HIGH −20,
MEDIUM −10, LOW −4, INFO 0. Bonus: a proper `max-width` container centering content
at wide widths +5; `overflow-x:auto` correctly wrapping wide tables +5. Clamp 0–100.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_w1_layout_overflow.md`. Every finding: app,
severity, confidence, `file:line`, evidence, why-it-matters, and either an OBSERVED
block (viewport, route, screenshot path, measured value) or a "Static analysis —
render at <viewport> to confirm" note naming the tool. Per-severity count.
