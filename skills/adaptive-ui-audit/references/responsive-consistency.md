# Cross · Responsive Consistency (Step X2)

> The "some screens adapt, others were forgotten" defect. Individual checks (W*/N*) ask *is this screen responsive?*; this cross step asks *is the app responsive the SAME way everywhere?* It catches scattered/inconsistent responsiveness: breakpoints defined as tokens in one place but hardcoded as magic numbers elsewhere, two conflicting breakpoint systems, whole routes/screens with zero responsive signal while siblings adapt, mixed units for the same concern, and design-system components that are responsive but consumed inside fixed wrappers. Findings FOLD into the area they belong to (usually W1/W3, or N3 native); no independent score.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_aui_discovery.md` for
`FRAMEWORKS`, `RESPONSIVE_SYSTEM`, `BREAKPOINTS`, `APPS`, `PLATFORMS`. Establish the *canonical*
system first (Tailwind `screens`, a theme/tokens file, RN theme, Flutter breakpoint consts) so
"scattered" is measured against a known source of truth. Multi-app monorepo: scope per app.

## Checks

### 1. Canonical breakpoints vs scattered magic numbers (HIGH)
A single source of truth (theme/tokens/`screens`) exists, yet raw pixel breakpoints are
sprinkled across files that don't reference it — they drift when the token changes.

```bash
# find the canonical set
grep -rniE 'screens\s*:|breakpoints\s*[:=]|--breakpoint|\$screen-' tailwind.config.* src 2>/dev/null | head
# raw @media pixel values scattered in components/styles
grep -rnoE '@media[^{]*\(min-width:\s*[0-9]+px|max-width:\s*[0-9]+px' src 2>/dev/null | grep -v node_modules \
  | sort | uniq -c | sort -rn | head -30
```
Many distinct raw px thresholds that don't match the token set → HIGH (drift risk). Tag W2/W1.

### 2. Conflicting breakpoint systems (HIGH)
Tailwind `screens` AND raw `@media` with DIFFERENT values coexist (e.g. `md=768` in config but
`760`/`800` in CSS), so components jump at different widths — visible seams between adjacent
components at the same viewport.

```bash
grep -rnoE '(min|max)-width:\s*[0-9]+px' src 2>/dev/null | grep -oE '[0-9]+px' | sort | uniq -c | sort -rn | head
# compare that list against the token breakpoints from Check 1 — mismatches are findings
```
Two overlapping-but-unequal threshold sets → HIGH, tag W2. Equal but duplicated → LOW (consolidate).

### 3. Coverage gaps — neglected screens (HIGH)
The signature defect: enumerate every route/screen and grep EACH for ANY responsive signal;
screens with none, while their siblings adapt, are candidates for "forgotten." Coverage-scan:

```bash
# 1) enumerate routes/screens (adapt globs to the stack)
find src -type f \( -path '*app/*/page.tsx' -o -path '*pages/*' -o -path '*routes/*' \
  -o -path '*screens/*' -o -name '*Screen.tsx' -o -name '*.astro' \) -not -path '*/node_modules/*' 2>/dev/null | sort > /tmp/aui_screens.txt
# 2) for each, count responsive signals; zero = candidate
while read f; do
  n=$(grep -cE '@media|@container|sm:|md:|lg:|useWindowDimensions|matchMedia|LayoutBuilder|MediaQuery|Breakpoint' "$f" 2>/dev/null)
  echo "$n  $f"
done < /tmp/aui_screens.txt | sort -n | head -40
```
Screens scoring `0` while the app clearly adapts elsewhere → HIGH (name each file). Runtime-confirm
by rendering the flagged route across the viewport matrix (`references/runtime-validation.md`).
Tag W1/W3 (web) or N3 (native).

### 4. Mixed units for the same concern (MEDIUM)
The same layout concern expressed in `px` in one place, `rem`/`em`/`%`/`vw` in another (web),
or `dp` vs fixed pixels (native) — inconsistent scaling with user font-size / density.

```bash
grep -rnoE '(width|height|padding|margin|font-size):\s*[0-9.]+(px|rem|em|%|vw|vh)' src 2>/dev/null \
  | grep -oE '(px|rem|em|%|vw|vh)$' | sort | uniq -c | sort -rn
```
A layout mixing fixed `px` widths with `rem` type at random → MEDIUM, tag W1/W3.

### 5. Responsive design-system component in a fixed wrapper (MEDIUM)
A shared component is responsive internally, but a consumer wraps it in a fixed-width/height
container that defeats it (`<div style="width:900px"><ResponsiveTable/></div>`, RN fixed-`width`
parent). The primitive is fine; the consumption is the defect.

```bash
grep -rnB2 -E '<[A-Z][A-Za-z]+' src 2>/dev/null | grep -iE 'width:\s*[0-9]{3,}px|w-\[[0-9]{3,}px\]|style=\{\{\s*width:' | head
```
Fixed wrapper around a known-responsive DS component → MEDIUM, tag W3 (native N3).

## SEVERITY / CONFIDENCE GUIDE
- HIGH: coverage gap on a real user route, or conflicting breakpoint systems producing seams.
- MEDIUM: mixed units, fixed wrappers, scattered-but-close thresholds.
- LOW/INFO: duplicated-but-equal thresholds, cosmetic drift with no visible effect.
- CONFIDENCE: HIGH only when the canonical set is unambiguous and the outlier clearly diverges (or a
  render confirms the seam/neglected screen); grep-only inference caps at MEDIUM. Mark
  "Static analysis — confirm by rendering across the viewport matrix" where no render exists.

## SCORING HINTS (folded)
No independent score. Fold each finding into its tagged area (mostly W1/W3, or N3) with the shared
scheme (CRITICAL −30 / HIGH −20 / MEDIUM −10 / LOW −4 / INFO 0, ×confidence HIGH1.0/MED0.75/LOW0.5).
A neglected-screen coverage gap is typically the heaviest contributor here. Dedup against the scoped
step that owns the screen so it isn't counted twice.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_x2_responsive_consistency.md`. Include: the canonical breakpoint
system found; the coverage-scan table (screen → responsive-signal count) with flagged zeros; each
finding with check #, fold-in area tag, severity, confidence, `file:line`, OBSERVED-vs-static marker,
evidence, and the consolidation fix (adopt the token, unify thresholds, add breakpoints to the
neglected screen).
