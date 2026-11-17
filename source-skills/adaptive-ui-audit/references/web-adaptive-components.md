# Web · Adaptive Components & Media (Step W3, scored area, base 100)

> Evaluate whether individual components adapt across sizes: tables, modals/drawers, nav, grids/flex rows, forms/toolbars, sticky headers, and responsive images. These are the components that most often break on small OR large screens. Web scope only (and desktop web-tech windows). A visual claim is OBSERVED only with a runtime render/measurement; otherwise "Static analysis — render at <viewport> to confirm" naming the tool.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_aui_discovery.md` for
`PLATFORMS`, `APPS`, `RESPONSIVE_SYSTEM`, `STYLING`, `IMAGE_SOLUTION`. Run only for
web/desktop-web apps. Skip native. Tag every finding with its app.

## Checks

### 1. Data tables with no responsive strategy (HIGH)
`<table>` with no horizontal-scroll wrapper and no stacked/card mode on small
screens → overflow / horizontal page scroll on mobile (cross-ref W1).
```bash
grep -rniE '<table|role=["\x27]table' . --include='*.html' --include='*.tsx' \
  --include='*.jsx' --include='*.vue' -n 2>/dev/null | grep -v node_modules | head -20
# Look for the mitigation nearby: an overflow-x wrapper or a small-screen card mode
grep -rniE 'overflow-x:\s*auto|overflow-x:\s*scroll' . --include='*.css' --include='*.scss' -n 2>/dev/null | grep -v node_modules | head
```
Runtime confirm: render a table route at 360px; if the table forces page scroll and
there is no scroll wrapper or stacked layout, screenshot and mark OBSERVED.

### 2. Modals / dialogs / drawers fixed-width or overflowing (HIGH)
`role="dialog"` / modal components with fixed px width that exceeds a small
viewport, or tall content with no internal scroll so the actions fall off-screen.
```bash
grep -rniE 'role=["\x27]dialog|Dialog|Modal|Drawer|Sheet' . --include='*.tsx' \
  --include='*.jsx' --include='*.vue' -n 2>/dev/null | grep -v node_modules | head -20
grep -rniE '(Dialog|Modal|Drawer)[^{]*width:\s*[0-9]{3,}px' . --include='*.css' --include='*.scss' -n 2>/dev/null | grep -v node_modules | head
```
Runtime confirm: open the modal at 320/360; check `dialog.getBoundingClientRect()`
width vs `innerWidth` and whether the action row is reachable (internal scroll).

### 3. Nav that doesn't collapse / desktop nav crammed on mobile (HIGH)
A horizontal nav bar with many items and no hamburger/menu collapse on small
screens, or a mobile-first menu with no expanded desktop nav wasting the top bar.
```bash
grep -rniE '<nav|role=["\x27]navigation|Navbar|Header|hamburger|MenuButton' . \
  --include='*.tsx' --include='*.jsx' --include='*.vue' -n 2>/dev/null | grep -v node_modules | head -20
```
Runtime confirm: at 360 check whether nav items overflow or a menu toggle appears;
at 1280 check the nav is not stuck in collapsed mobile mode. Screenshot both.

### 4. Grids / flex rows that don't wrap or reflow (MEDIUM–HIGH)
Fixed column counts, `grid-template-columns` with fixed px tracks, or `flex` rows
with no `flex-wrap` → columns overflow on small screens or stay stuck at N columns
on wide screens. Prefer `repeat(auto-fit, minmax(...))` / responsive column counts.
```bash
grep -rniE 'grid-template-columns:\s*[^;]*px|grid-template-columns:\s*repeat\([0-9]' . \
  --include='*.css' --include='*.scss' --include='*.tsx' --include='*.vue' -n 2>/dev/null | grep -v node_modules | head -20
grep -rniE 'display:\s*flex' . --include='*.css' --include='*.scss' -n 2>/dev/null | grep -v node_modules | wc -l
grep -rniE 'flex-wrap:\s*nowrap' . --include='*.css' --include='*.scss' -n 2>/dev/null | grep -v node_modules | head
```
Runtime confirm: render a grid route at 360 and 1440; measure whether tracks
overflow (child right edge > container) or leave dead columns. Screenshot.

### 5. Long forms / toolbars / sticky headers eating small viewports (MEDIUM)
Toolbars with many controls that overflow instead of wrapping; sticky headers with
fixed large height that consume a big fraction of a short viewport.
```bash
grep -rniE 'position:\s*sticky|position:\s*fixed' . --include='*.css' --include='*.scss' -n 2>/dev/null | grep -v node_modules | head -20
```
Runtime confirm: at 360×640 measure sticky-header height as a fraction of viewport;
flag toolbars whose controls overflow horizontally.

### 6. Responsive images & media (MEDIUM)
`<img>` without `max-width:100%` (overflows container), no `srcset`/`sizes` (ships
one size to every viewport), missing `<picture>` for art direction, non-fluid
`background-image`, and missing `aspect-ratio`/`width`+`height` → layout shift.
```bash
grep -rniE '<img' . --include='*.html' --include='*.tsx' --include='*.jsx' --include='*.vue' -n 2>/dev/null | grep -v node_modules | wc -l
grep -rniE 'srcset|sizes=|<picture|aspect-ratio' . --include='*.html' --include='*.tsx' --include='*.vue' -n 2>/dev/null | grep -v node_modules | head
grep -rniE 'img\s*\{[^}]*max-width:\s*100%|img[^{]*\{[^}]*max-width' . --include='*.css' --include='*.scss' -n 2>/dev/null | grep -v node_modules | head
```
Runtime confirm: at 360 check whether any `<img>` right edge exceeds its container
or the viewport; check for CLS on load where `aspect-ratio`/dimensions are absent.

## SEVERITY GUIDE
- CRITICAL: primary component (table/modal/nav) unusable — actions unreachable — at a common viewport.
- HIGH: table overflow with no wrapper, fixed-width modal off-screen, nav that never collapses.
- MEDIUM: non-wrapping grids/flex, sticky header eating the viewport, images without srcset/max-width.
- LOW/INFO: minor art-direction / aspect-ratio polish.

## CONFIDENCE GUIDE
- HIGH: component rendered at the failing viewport and measured/screenshotted.
- MEDIUM: missing mitigation visible in code (table with no wrapper) but not yet rendered.
- LOW: depends on runtime content volume (row/column count) → render to confirm.

## SCORING HINTS
Base 100. Deduct (× confidence HIGH1.0/MED0.75/LOW0.5): CRITICAL −30, HIGH −20,
MEDIUM −10, LOW −4, INFO 0. Bonus: tables wrapped in `overflow-x:auto` or a stacked
card mode +5; images with `srcset`/`sizes` + `max-width:100%` + `aspect-ratio` +5;
grids using `auto-fit/minmax` +5 (cap total bonus at +10). Clamp 0–100.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_w3_adaptive_components.md`. Every finding: app,
severity, confidence, `file:line`, evidence, and an OBSERVED block (viewport, route,
screenshot path, measured value) or a "Static analysis — render at <viewport> to
confirm" note naming the tool. Per-severity count.
