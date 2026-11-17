# Web · Breakpoints & Viewport (Step W2, scored area, base 100)

> Evaluate the viewport meta tag and the breakpoint strategy: whether the app declares a correct responsive viewport, whether breakpoints cover phone→tablet→desktop without gaps or dead bands, and whether zoom is blocked. Web scope only (and desktop web-tech windows). A rendering claim is OBSERVED only with a runtime render across the viewport matrix; otherwise "Static analysis — render at <viewport> to confirm" naming the tool.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_aui_discovery.md` for
`PLATFORMS`, `APPS`, `RESPONSIVE_SYSTEM`, `BREAKPOINTS`, `VIEWPORT_META`, `STYLING`.
Run only for web/desktop-web apps. Skip native. Tag every finding with its app.

## Checks

### 1. Missing or incorrect viewport meta (HIGH)
`<meta name="viewport">` absent → mobile browsers render at ~980px and shrink,
breaking every responsive rule. `maximum-scale=1` / `user-scalable=no` blocks
pinch-zoom (usability + adaptive-a11y defect — cross-ref W4 text scaling). `width`
set to a fixed number instead of `device-width`.
```bash
grep -rniE '<meta[^>]*name=["\x27]viewport' . --include='*.html' --include='*.astro' \
  --include='*.tsx' --include='*.jsx' --include='*.vue' -n 2>/dev/null | grep -v node_modules | head
grep -rniE 'user-scalable\s*=\s*no|maximum-scale\s*=\s*1|width\s*=\s*[0-9]+' . \
  --include='*.html' --include='*.astro' --include='*.tsx' -n 2>/dev/null | grep -v node_modules | head
```
If nothing matches for an SPA, check the framework head config (`app/head`, `Head`,
`index.html`, `nuxt.config`, `next` metadata). Absence in all is the HIGH finding.
Runtime confirm: `document.querySelector('meta[name=viewport]')?.content`.

### 2. No / thin breakpoint strategy — tablet or desktop unstyled (HIGH)
No `@media`/`screens`/`@container` at all (single fixed design); only one
breakpoint; or a gap that leaves the 768–1024 tablet band using phone or desktop
styles unintentionally. Also: desktop-only design with no small-screen breakpoints.
```bash
grep -rniE '@media|@container' . --include='*.css' --include='*.scss' --include='*.vue' -n 2>/dev/null | grep -v node_modules | wc -l
grep -rniE 'screens\s*:' . --include='tailwind.config.*' -n 2>/dev/null | head
# Extract the breakpoint values actually in use to spot gaps
grep -rhoiE 'min-width:\s*[0-9]+px|max-width:\s*[0-9]+px' . --include='*.css' --include='*.scss' 2>/dev/null \
  | grep -v node_modules | sort -u | head -40
```
Runtime confirm: render at 320/360/390/768/1024/1280/1440 and screenshot each;
a band that looks identical to the next-smaller band despite ample width, or a
tablet width that inherits a broken phone/desktop layout, is the OBSERVED finding.

### 3. Conflicting / overlapping media queries & dead bands (MEDIUM)
`min-width` and `max-width` mixed so a width matches two conflicting rules, or a
gap (e.g. `max-width:767px` and `min-width:1024px` with nothing for 768–1023)
leaves a dead band unstyled.
```bash
grep -rniE '@media[^{]*(min-width[^{]*max-width|max-width[^{]*min-width)' . \
  --include='*.css' --include='*.scss' -n 2>/dev/null | grep -v node_modules | head -20
```
Runtime confirm: render exactly at each boundary (767/768/1023/1024) and check
for an unstyled or double-styled result. Screenshot the boundary widths.

### 4. Container queries opportunity / scattered magic-number breakpoints (LOW–MEDIUM)
Components sized off the viewport when they should respond to their container
(sidebar-embedded card) → `@container` would fit. Hardcoded magic-number
breakpoints scattered across files instead of shared tokens/`screens` (light touch
— deep token consistency belongs to the `responsive-consistency` agent).
```bash
grep -rhoiE 'min-width:\s*[0-9]+px' . --include='*.css' --include='*.scss' 2>/dev/null \
  | grep -v node_modules | sort | uniq -c | sort -rn | head
```

## SEVERITY GUIDE
- CRITICAL: viewport meta absent AND app is content-heavy → unusable on phones.
- HIGH: no viewport meta, zoom disabled, or tablet/desktop band left effectively unstyled.
- MEDIUM: dead band / conflicting queries at a boundary; single-breakpoint strategy on a rich app.
- LOW/INFO: scattered magic numbers, container-query opportunities.

## CONFIDENCE GUIDE
- HIGH: viewport content string read; boundary rendered and defect screenshotted.
- MEDIUM: gap inferred from the extracted breakpoint set, not yet rendered.
- LOW: "tablet probably looks wrong" without a render → render across the matrix.

## SCORING HINTS
Base 100. Deduct (× confidence HIGH1.0/MED0.75/LOW0.5): CRITICAL −30, HIGH −20,
MEDIUM −10, LOW −4, INFO 0. Bonus: correct `width=device-width, initial-scale=1`
viewport with zoom allowed +5; breakpoint set covering phone/tablet/desktop with no
gap +5. Clamp 0–100.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_w2_breakpoints_viewport.md`. Every finding: app,
severity, confidence, `file:line`, evidence, and an OBSERVED block or a "Static
analysis — render at <viewport> to confirm" note naming the tool. Record the
resolved viewport-meta string and the breakpoint set for the report. Per-severity count.
