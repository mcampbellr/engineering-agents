# Native · Safe Area & Insets (Step N1, scored area, base 100)

> React Native / Expo AND Flutter. Evaluate whether content clears the notch / dynamic island / status bar, the home indicator, and the rounded corners — in portrait AND landscape. NEVER apply web rules here. A claim that content is clipped/hidden under system UI is OBSERVED only if a simulator/emulator render confirms it; otherwise write "Static analysis — verify on <device/orientation>" and name the tool (iOS Simulator, Android emulator, Expo Go). See `references/runtime-validation.md` for the device/orientation matrix.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_aui_discovery.md`.
Run only for apps with `platform=native`. Note per app: RN/Expo vs Flutter, the RN
version, and `SAFE_AREA` (is `react-native-safe-area-context` installed? Flutter
`SafeArea` usage?). Use APIs that exist in the detected version. If no native app,
write nothing and report that.

## React Native / Expo

### 1. No safe-area handling at all (HIGH–CRITICAL)
Top bars / headers / hero content pinned to `top: 0` (or absolute) with no inset,
bottom bars / CTAs pinned to `bottom: 0` under the home indicator; hardcoded
status-bar height instead of measured insets.
```bash
grep -rniE "safe-area-context|SafeAreaProvider|useSafeAreaInsets|SafeAreaView" . --include='*.tsx' --include='*.jsx' -n 2>/dev/null | grep -v node_modules | head
grep -rniE "StatusBar\.currentHeight|Constants\.statusBarHeight|(paddingTop|top):\s*(20|24|44|47|59)\b" . --include='*.tsx' --include='*.jsx' -n 2>/dev/null | grep -v node_modules | head
```
CRITICAL when a primary control (submit, nav, close) sits under system UI and is
unreachable; HIGH when content is merely obscured. If `useSafeAreaInsets`/`SafeAreaView`
(context lib) is entirely absent from a full-screen app, flag the app-level gap.

### 2. Misused / deprecated safe area (MEDIUM–HIGH)
`SafeAreaView` imported from `react-native` (deprecated, iOS-only, no Android inset)
instead of `react-native-safe-area-context`; double-padding (a `SafeAreaView`
wrapping a child that also applies `insets`); insets applied to the wrong edges
(`edges={['top']}` on a bottom bar); full-bleed backgrounds cut off because the
safe-area wrapper shrinks the painted area.
```bash
grep -rniE "SafeAreaView" . --include='*.tsx' --include='*.jsx' -n 2>/dev/null | grep -v node_modules \
  | grep -iE "from ['\"]react-native['\"]" && echo ">> deprecated RN SafeAreaView above"
grep -rniE "edges=\{?\[" . --include='*.tsx' --include='*.jsx' -n 2>/dev/null | grep -v node_modules | head
```

### 3. Landscape / side insets ignored (MEDIUM)
Only `top`/`bottom` insets handled; in landscape the notch/dynamic island moves to
a side, so `left`/`right` insets are needed. Code that reads `insets.top` but never
`insets.left`/`insets.right`, or fixed horizontal padding on full-screen content.
```bash
grep -rniE "insets\.(left|right)" . --include='*.tsx' -n 2>/dev/null | grep -v node_modules | head || echo "No horizontal insets referenced — verify landscape on notched device"
```

## Flutter

### 4. Widgets not protected by SafeArea / MediaQuery padding (HIGH–CRITICAL)
Screen bodies rendered directly under status bar / gesture bar without a `SafeArea`
wrapper and without consuming `MediaQuery.of(context).padding`/`.viewPadding`;
`Scaffold` body with content at the extreme top/bottom edge.
```bash
grep -rniE "SafeArea\(|MediaQuery\.of\(context\)\.(padding|viewPadding)|EdgeInsets\.only\(top:" . --include='*.dart' -n 2>/dev/null | head
grep -rniE "Scaffold\(" . --include='*.dart' -n 2>/dev/null | head
```
Note: `AppBar`/`BottomNavigationBar` inset automatically; flag custom top/bottom
bars, stacked/positioned content, and full-screen bodies. CRITICAL when a tap
target is under the gesture/home indicator.

### 5. Misused SafeArea in Flutter (MEDIUM)
`SafeArea` disabled where it matters (`top:false`/`bottom:false`) leaving content
under system UI, OR nested `SafeArea`s double-insetting; full-bleed background that
should sit behind the inset but is clipped because `SafeArea` wraps the background too.
```bash
grep -rniE "SafeArea\((top:\s*false|bottom:\s*false|left:\s*false|right:\s*false)" . --include='*.dart' -n 2>/dev/null | head
```

## SEVERITY GUIDE
- CRITICAL: an interactive control (submit/nav/close) rendered under the notch, status bar, or home indicator so it is unreachable or mis-tappable.
- HIGH: primary content/text clipped or obscured under system UI; deprecated RN `SafeAreaView` used app-wide with no Android inset.
- MEDIUM: landscape/side insets ignored; wrong-edge insets; nested double-padding.
- LOW/INFO: minor cosmetic gap; full-bleed background slightly shrunk.

## CONFIDENCE GUIDE
- HIGH: absent safe-area lib + top/bottom-pinned content directly visible; RN `SafeAreaView` import from `react-native`.
- MEDIUM: inset usage present but edges/subtree look wrong from source.
- LOW: exact clipping depends on device — confirm on iOS Simulator (iPhone 15 Pro notch) / Android emulator with a cutout, portrait AND landscape.

## SCORING HINTS
Base 100. Deduct (× confidence): CRITICAL −30, HIGH −20, MEDIUM −10, LOW −4, INFO 0;
confidence multiplier HIGH ×1.0 / MEDIUM ×0.75 / LOW ×0.5. Bonus: `SafeAreaProvider`
+ `useSafeAreaInsets` (or context `SafeAreaView`) used consistently with correct
edges +5; Flutter `SafeArea` with intentional per-edge control +5. Clamp 0–100.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_n1_safe_area.md`. Each finding: app tag, severity,
confidence, `file:line`, and the device/orientation needed to confirm any visual
claim. Per-severity count + area score.
