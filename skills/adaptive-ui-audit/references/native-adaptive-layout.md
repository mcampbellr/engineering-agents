# Native · Adaptive Layout — Tablet / Orientation / Text Scaling (Step N3, scored area, base 100)

> React Native / Expo AND Flutter. Evaluate whether the layout adapts to large screens (tablets, foldables), to landscape orientation, and to enlarged system text (Dynamic Type / `fontScale` / `textScaler`). NEVER apply web rules. A claim that "the tablet layout is a stretched phone UI" or "text clips at max font size" is OBSERVED only if a 7"/10" tablet + landscape + max-font-scale render confirms it; otherwise "Static analysis — verify on <tablet/orientation/font setting>" naming the tool. See `references/runtime-validation.md`.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_aui_discovery.md`.
Run only for `platform=native`. Note per app: RN/Expo vs Flutter, `RESPONSIVE_SYSTEM`
(NativeWind responsive prefixes? `useWindowDimensions`? Flutter `MediaQuery`/`LayoutBuilder`?),
`ORIENTATION` (locked?), and `NAV_LARGE_SCREEN` (any master-detail / split view). Use
version-appropriate APIs. If no native app, write nothing and report that.

## Tablet / large screen

### 1. Layout keyed only to phone — no breakpoints (HIGH)
No use of `useWindowDimensions`/`Dimensions`, NativeWind `md:`/`lg:` prefixes, Flutter
`LayoutBuilder`/`MediaQuery.size`/`OrientationBuilder` anywhere the layout should
branch — so a tablet gets a single stretched phone column with huge wasted margins
and no master-detail.
```bash
grep -rniE "useWindowDimensions|Dimensions\.get" . --include='*.tsx' --include='*.jsx' -n 2>/dev/null | grep -v node_modules | head
grep -rniE "\b(md|lg|xl):" . --include='*.tsx' --include='*.jsx' -n 2>/dev/null | grep -v node_modules | head
grep -rniE "LayoutBuilder|MediaQuery\.of\(context\)\.size|OrientationBuilder" . --include='*.dart' -n 2>/dev/null | head
```
HIGH for a content app (lists + detail) that never goes master-detail / multi-column
on tablet; MEDIUM for a simple single-purpose app where a centered max-width is enough.

### 2. Fixed pixel dimensions that don't scale (MEDIUM)
Hardcoded `width`/`height` in px on containers, cards, images that look tiny on a
10" tablet or overflow a small phone; full-width elements with no `maxWidth` so lines
stretch unreadably wide on tablet.
```bash
grep -rniE "(width|height):\s*[0-9]{3,}" . --include='*.tsx' -n 2>/dev/null | grep -v node_modules | head
grep -rniE "maxWidth|SizedBox\(width:\s*[0-9]{3,}|ConstrainedBox" . --include='*.tsx' --include='*.dart' -n 2>/dev/null | grep -v node_modules | head
```

## Orientation

### 3. Orientation locked or landscape broken (MEDIUM–HIGH)
Orientation locked to portrait unintentionally (may be deliberate — verify intent),
OR unlocked but the layout never reflows: a portrait-only column that overflows/leaves
huge dead bands in landscape; no `OrientationBuilder`/dimension check to switch to a
row layout.
```bash
grep -rniE "orientation|ScreenOrientation\.lock|lockAsync|SystemChrome\.setPreferredOrientations" . --include='*.tsx' --include='*.ts' --include='*.dart' -n 2>/dev/null | grep -v node_modules | head
grep -rniE "\"orientation\"\s*:\s*\"(portrait|default)\"" ./app.json ./app.config.* 2>/dev/null | head
```
HIGH if landscape is allowed but visibly broken; MEDIUM if locked without a stated
reason. If lock is intentional (games, camera), record INFO.

## Text scaling / Dynamic Type

### 4. Font scaling disabled or clipped (MEDIUM–HIGH)
Blanket `allowFontScaling={false}` (ignores the user's accessibility text-size choice
— bad); fixed-height text containers / one-line labels that clip or overlap at max
`fontScale`; Flutter fixed `fontSize` inside tight boxes ignoring `MediaQuery.textScaler`,
or `TextScaler`/`MediaQuery` clamped to 1.0 app-wide.
```bash
grep -rniE "allowFontScaling\s*=\s*\{?false" . --include='*.tsx' -n 2>/dev/null | grep -v node_modules | head
grep -rniE "maxFontSizeMultiplier|PixelRatio\.getFontScale|useWindowDimensions\(\)\.fontScale" . --include='*.tsx' -n 2>/dev/null | grep -v node_modules | head
grep -rniE "textScaler|textScaleFactor|MediaQuery.*textScal" . --include='*.dart' -n 2>/dev/null | head
```
HIGH when disabling scaling or clipping affects primary content/labels app-wide;
MEDIUM for isolated cases. A single numeric badge with `allowFontScaling={false}` is
defensible — flag the pattern, not every instance. Note: no test at max font size =
"Static analysis — verify at largest Dynamic Type / fontScale".

## SEVERITY GUIDE
- HIGH: content app with no large-screen adaptation at all (stretched phone UI, no master-detail); landscape allowed but broken; font scaling disabled app-wide or primary text clips at max scale.
- MEDIUM: fixed px dimensions that misfit tablets; orientation locked without stated reason; isolated scaling clip.
- LOW/INFO: minor wasted margin; intentional orientation lock; single defensible `allowFontScaling={false}`.

## CONFIDENCE GUIDE
- HIGH: zero responsive-API usage / blanket `allowFontScaling={false}` directly visible in source.
- MEDIUM: responsive hooks present but layout branch looks incomplete.
- LOW: actual tablet/landscape/max-font appearance — confirm on a 10" tablet, in landscape, and at largest system text.

## SCORING HINTS
Base 100. Deduct (× confidence): CRITICAL −30, HIGH −20, MEDIUM −10, LOW −4, INFO 0;
multiplier HIGH ×1.0 / MEDIUM ×0.75 / LOW ×0.5. Bonus: real breakpoint/master-detail
on tablet (`useWindowDimensions`/NativeWind `md:`/`LayoutBuilder`) +5; font scaling
respected with layouts that reflow at max scale +5; deliberate, reasoned orientation
handling +5. Clamp 0–100.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_n3_adaptive_layout.md`. Each finding: app tag,
severity, confidence, `file:line`, and the device/orientation/font setting needed to
confirm. Per-severity count + area score.
