# Native · Touch Ergonomics (Step N4, scored area, base 100)

> React Native / Expo AND Flutter. Evaluate whether touch targets meet platform minimums (iOS 44×44 pt, Android 48×48 dp), whether small controls have `hitSlop`, whether targets are spaced apart, and whether critical actions sit within thumb reach on large phones. NEVER apply web rules. A claim that "the icon button is too small to hit reliably" is OBSERVED only if a device/emulator render + measurement confirms it; otherwise "Static analysis — verify tap target on device" naming the tool. See `references/runtime-validation.md`.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_aui_discovery.md`.
Run only for `platform=native`. Note per app: RN/Expo vs Flutter. Use
version-appropriate APIs. If no native app, write nothing and report that.

## React Native / Expo

### 1. Touch targets below platform minimum (HIGH)
`Pressable`/`TouchableOpacity`/`TouchableWithoutFeedback` wrapping a small icon/text
with no explicit size and no padding, so the tappable box is under 44pt; small
`width`/`height` on the pressable itself.
```bash
grep -rniE "<(TouchableOpacity|TouchableWithoutFeedback|Pressable|TouchableHighlight)\b" . --include='*.tsx' --include='*.jsx' -n 2>/dev/null | grep -v node_modules | head -20
grep -rniE "(width|height):\s*(1[0-9]|2[0-9]|3[0-9])\b" . --include='*.tsx' -n 2>/dev/null | grep -v node_modules | head
```
Inspect the wrapped child + style: an icon (~24) in a `Pressable` with no padding =
~24pt target → HIGH. Flag with `file:line` and the measured/estimated size.

### 2. Small controls without hitSlop (MEDIUM–HIGH)
Small pressables (close "X", stepper +/−, checkbox, inline icon) with no `hitSlop`
to extend the touch area beyond the visual bounds.
```bash
grep -rniE "hitSlop" . --include='*.tsx' --include='*.jsx' -n 2>/dev/null | grep -v node_modules | head || echo "No hitSlop anywhere — small controls likely under-sized targets"
```
HIGH when the undersized control is a primary/frequent action; MEDIUM otherwise.

### 3. Targets too close together (MEDIUM)
Adjacent tappable rows/icons with no gap/margin between hit areas → mis-taps
(delete next to edit, adjacent toolbar icons). Look for rows of `Pressable`s with no
spacing.
```bash
grep -rniE "flexDirection:\s*['\"]row['\"]" . --include='*.tsx' -n 2>/dev/null | grep -v node_modules | head
```
Correlate with adjacent pressables lacking `gap`/`marginHorizontal`.

### 4. Critical actions out of thumb reach (MEDIUM)
Primary action (submit, next, main CTA) pinned to a top corner on a large-phone
layout with no reachable alternative (bottom bar / FAB). Top-left back is fine
(system-standard); flag primary CTAs stranded at the top.
```bash
grep -rniE "(top):\s*0|alignItems:\s*['\"]flex-end['\"]|justifyContent:\s*['\"]flex-start['\"]" . --include='*.tsx' -n 2>/dev/null | grep -v node_modules | head
```

## Flutter

### 5. Undersized / spacing-poor targets in Flutter (MEDIUM–HIGH)
`InkWell`/`GestureDetector` on a small child with no padding/`SizedBox` to reach
48dp; `IconButton` without adequate size (default is usually fine — flag custom tiny
constraints); `ElevatedButton`/`TextButton` with no `minimumSize` while wrapping tiny
content; missing `MaterialTapTargetSize.padded`.
```bash
grep -rniE "InkWell\(|GestureDetector\(|IconButton\(" . --include='*.dart' -n 2>/dev/null | head -20
grep -rniE "minimumSize|MaterialTapTargetSize|Size\(\s*(1[0-9]|2[0-9]|3[0-9])" . --include='*.dart' -n 2>/dev/null | head
```
`GestureDetector` on a bare icon with no `Padding`/`SizedBox` → HIGH. Note Flutter
warns on tap targets under 48dp in debug — cite if `MaterialTapTargetSize.shrinkWrap`
is set on a frequent control.

## SEVERITY GUIDE
- HIGH: a frequently-used / primary control has a tap target well under the platform minimum (iOS 44pt / Android 48dp) with no `hitSlop`/padding to compensate.
- MEDIUM: small control missing `hitSlop`; adjacent targets too close (mis-tap risk); primary CTA out of thumb reach with no reachable alternative.
- LOW/INFO: a rarely-used control slightly under size; cosmetic spacing.

## CONFIDENCE GUIDE
- HIGH: small pressable wrapping a bare icon with no padding/`hitSlop` directly visible in source with its style.
- MEDIUM: size inferred from child + surrounding layout; spacing inferred.
- LOW: exact rendered target size / thumb reach — confirm on device (measure with the platform accessibility inspector / layout bounds overlay).

## SCORING HINTS
Base 100. Deduct (× confidence): CRITICAL −30, HIGH −20, MEDIUM −10, LOW −4, INFO 0;
multiplier HIGH ×1.0 / MEDIUM ×0.75 / LOW ×0.5. Bonus: consistent min-size targets
(≥44/48) + `hitSlop` on small controls +5; primary actions within thumb reach
(bottom bar / FAB) +5. Clamp 0–100.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_n4_touch_ergonomics.md`. Each finding: app tag,
severity, confidence, `file:line`, estimated/measured target size, and the device +
tool needed to confirm. Per-severity count + area score.
