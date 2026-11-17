# Web · Interaction & Reflow (Step W4, scored area, base 100)

> Evaluate touch/pointer ergonomics and how the UI reflows under text zoom / OS font scaling: tap-target size and spacing, hover-only affordances on touch, focus visibility, and whether fixed px typography and fixed-height text containers break or clip at 200% zoom / large OS fonts. Web scope only (and desktop web-tech windows). A rendering claim is OBSERVED only with a runtime render/measurement; otherwise "Static analysis — render at <viewport>/zoom to confirm" naming the tool.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_aui_discovery.md` for
`PLATFORMS`, `APPS`, `RESPONSIVE_SYSTEM`, `VIEWPORT_META`, `STYLING`. Run only for
web/desktop-web apps. Skip native. Tag every finding with its app.

## Checks

### 1. Touch / pointer target size & spacing (HIGH)
Interactive controls (buttons, links, icon buttons) smaller than ~44×44 CSS px, or
tightly packed tap targets with little spacing → mis-taps on touch. Icon-only
buttons with fixed small px size are the usual offenders.
```bash
grep -rniE '(width|height):\s*(1[0-9]|2[0-9]|3[0-9])px' . \
  --include='*.css' --include='*.scss' --include='*.tsx' --include='*.vue' -n 2>/dev/null | grep -v node_modules | head -30
grep -rniE '<button|role=["\x27]button|IconButton|<a\s' . --include='*.tsx' --include='*.jsx' --include='*.vue' -n 2>/dev/null | grep -v node_modules | wc -l
```
Runtime confirm (see `references/runtime-validation.md`): scan interactive elements'
`getBoundingClientRect()` at a touch viewport (390) and flag any `width<44 || height<44`
or center-to-center spacing below ~8px. Record measured px as OBSERVED.

### 2. Hover-only affordances with no touch equivalent (HIGH)
Menus/tooltips/actions revealed only on `:hover` (or a JS `mouseenter`) with no
click/tap/focus path → invisible/unusable on touch tablets and phones.
```bash
grep -rniE ':hover|onMouseEnter|onMouseOver|mouseenter' . \
  --include='*.css' --include='*.scss' --include='*.tsx' --include='*.jsx' --include='*.vue' -n 2>/dev/null | grep -v node_modules | head -30
```
Flag where the hover reveals *interactive content* (dropdown, action row) with no
`onClick`/`onFocus`/tap equivalent. Cosmetic hover styling is not a finding.
Runtime confirm: emulate touch (no hover) and check the content is reachable.

### 3. Missing focus visibility (MEDIUM)
`outline:none` / `outline:0` on focusable elements with no `:focus-visible`
replacement → keyboard and switch users lose the focus ring.
```bash
grep -rniE 'outline:\s*(none|0)' . --include='*.css' --include='*.scss' -n 2>/dev/null | grep -v node_modules | head
grep -rniE ':focus-visible|:focus\b' . --include='*.css' --include='*.scss' -n 2>/dev/null | grep -v node_modules | head
```

### 4. Fixed px typography that doesn't scale (MEDIUM)
Font sizes in `px` (and layout in `px`) don't respond to browser/OS font-size
settings the way `rem`/`em` do. Heavy `px` typography degrades reflow at large OS
fonts. Report the `px`-vs-`rem` ratio for font sizes as evidence.
```bash
grep -rhoiE 'font-size:\s*[0-9.]+px' . --include='*.css' --include='*.scss' 2>/dev/null | grep -v node_modules | wc -l
grep -rhoiE 'font-size:\s*[0-9.]+(rem|em)' . --include='*.css' --include='*.scss' 2>/dev/null | grep -v node_modules | wc -l
```

### 5. Text clipping in fixed-height containers under zoom (MEDIUM)
Text inside fixed `height`/`max-height` boxes with `overflow:hidden` clips when the
user scales text; buttons/badges with fixed height and centered single-line text
break at 200%.
```bash
grep -rniE '(height|max-height):\s*[0-9]+px[^;]*' . --include='*.css' --include='*.scss' -n 2>/dev/null | grep -v node_modules | head -20
```
Runtime confirm: set browser zoom to 200% (or emulate a large OS font) and render
at 1280 + 390; check whether layout breaks (overlap/overflow) or text is clipped.
Screenshot at 200%. Cross-ref W2 check 1 (`user-scalable=no` compounds this).

### 6. Zoom blocked — cross-reference (HIGH)
If W2 found `user-scalable=no` / `maximum-scale=1`, record it here too as an
interaction defect: users who need to zoom text cannot. Reference the W2 `file:line`.

## SEVERITY GUIDE
- CRITICAL: primary action reachable only via hover on a touch-only context, or unusable at 200% zoom.
- HIGH: sub-44px critical tap targets, hover-only interactive menus, zoom disabled.
- MEDIUM: no focus-visible, all-`px` typography, text clipping under scaling.
- LOW/INFO: minor spacing tweaks, `em`-vs-`rem` preference notes.

## CONFIDENCE GUIDE
- HIGH: measured at runtime (tap-target bbox, 200%-zoom render, touch emulation) with screenshot.
- MEDIUM: missing touch/focus path visible in code but not yet rendered.
- LOW: "might clip when scaled" without a zoom render → render at 200% to confirm.

## SCORING HINTS
Base 100. Deduct (× confidence HIGH1.0/MED0.75/LOW0.5): CRITICAL −30, HIGH −20,
MEDIUM −10, LOW −4, INFO 0. Bonus: tap targets consistently ≥44px +5; `rem`/`em`
typography with layout that reflows cleanly at 200% +5; `:focus-visible` present +5
(cap total bonus at +10). Clamp 0–100.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_w4_web_interaction.md`. Every finding: app,
severity, confidence, `file:line`, evidence, and an OBSERVED block (viewport/zoom,
route, screenshot path, measured value) or a "Static analysis — render at
<viewport>/zoom to confirm" note naming the tool. Per-severity count.
