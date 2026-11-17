# Native · Keyboard & Input Visibility (Step N2, scored area, base 100)

> React Native / Expo AND Flutter. THE key user pain: the on-screen keyboard covers the focused input or the submit button, so the field can't be seen or the form can't be completed. NEVER apply web rules. A claim that "the input is hidden behind the keyboard" is OBSERVED only if a simulator/emulator render with the keyboard up confirms it; otherwise write "Static analysis — verify on <small device>, focus each input" and name the tool. Confirm step below is mandatory. See `references/runtime-validation.md`.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_aui_discovery.md`.
Run only for `platform=native`. Note per app: RN/Expo vs Flutter and `KEYBOARD_HANDLING`
(is `react-native-keyboard-controller` / `react-native-keyboard-aware-scroll-view`
installed? any `KeyboardAvoidingView`? Flutter `resizeToAvoidBottomInset`?). Use
version-appropriate APIs. If no native app, write nothing and report that.

## React Native / Expo

### 1. Inputs with NO keyboard avoidance (HIGH–CRITICAL)
`TextInput`s in a screen/form with no `KeyboardAvoidingView`, no keyboard-aware
scroll library, and no scrollable that reflows — the keyboard slides over the lower
inputs. Plain `<View>`/`<ScrollView>` forms are the usual offender.
```bash
grep -rniE "<TextInput" . --include='*.tsx' --include='*.jsx' -n 2>/dev/null | grep -v node_modules | head
grep -rniE "KeyboardAvoidingView|keyboard-aware|keyboard-controller|KeyboardAwareScrollView|KeyboardProvider" . --include='*.tsx' --include='*.jsx' -n 2>/dev/null | grep -v node_modules | head
```
CRITICAL when a REQUIRED field or the only submit path is covered and unreachable
(user cannot complete the form). HIGH when a field is merely obscured but scrollable
around. Cross-check: a screen with `TextInput` but zero keyboard-handling hits = flag.

### 2. KeyboardAvoidingView present but misconfigured (MEDIUM–HIGH)
`behavior` not branched per platform (`padding` on iOS, `height`/undefined on
Android — wrong `behavior` no-ops or over-pushes); missing/wrong `keyboardVerticalOffset`
when a header exists; the wrapper wraps the wrong subtree (siblings of the input, or
only part of the form) so the focused field still hides.
```bash
grep -rniE "behavior=\{?['\"]?(padding|height|position)" . --include='*.tsx' -n 2>/dev/null | grep -v node_modules | head
grep -rniE "keyboardVerticalOffset|Platform\.OS\s*===?\s*['\"]ios" . --include='*.tsx' -n 2>/dev/null | grep -v node_modules | head
```
Flag `KeyboardAvoidingView` with a hardcoded `behavior` and no `Platform.OS` branch.

### 3. Bottom-pinned CTA covered / taps dismiss instead of act (MEDIUM–HIGH)
Submit/next button absolutely pinned to `bottom` that the keyboard overlays; scroll
views missing `keyboardShouldPersistTaps="handled"` so the first tap only dismisses
the keyboard instead of hitting the button; long form where the focused field is near
the bottom and nothing auto-scrolls it into view.
```bash
grep -rniE "keyboardShouldPersistTaps" . --include='*.tsx' -n 2>/dev/null | grep -v node_modules | head || echo "No keyboardShouldPersistTaps — taps may dismiss instead of submit"
grep -rniE "position:\s*['\"]absolute['\"]|(bottom):\s*0" . --include='*.tsx' -n 2>/dev/null | grep -v node_modules | head
```

### 4. Modals / bottom-sheets with inputs not adjusting (MEDIUM–HIGH)
Inputs inside a `Modal`, `@gorhom/bottom-sheet`, or custom overlay where the keyboard
handling from the parent screen does not apply (RN `Modal` needs its own avoidance;
bottom-sheet needs its keyboard-aware variant/prop).
```bash
grep -rniE "<Modal|bottom-sheet|BottomSheet|@gorhom" . --include='*.tsx' -n 2>/dev/null | grep -v node_modules | head
```

## Flutter

### 5. resizeToAvoidBottomInset disabled / inputs not scrollable (HIGH–CRITICAL)
`Scaffold(resizeToAvoidBottomInset: false)` (body doesn't shrink for the keyboard),
OR `TextField`/`TextFormField` in a `Column` with no `SingleChildScrollView`/`ListView`
so the field under the keyboard can't scroll into view; not consuming
`MediaQuery.of(context).viewInsets.bottom` for a custom pinned control.
```bash
grep -rniE "resizeToAvoidBottomInset\s*:\s*false" . --include='*.dart' -n 2>/dev/null | head
grep -rniE "TextField|TextFormField" . --include='*.dart' -n 2>/dev/null | head
grep -rniE "SingleChildScrollView|viewInsets\.bottom|ListView" . --include='*.dart' -n 2>/dev/null | head
```
CRITICAL when a required field / the submit button is unreachable with the keyboard up.

## CONFIRM STEP (state this in every finding)
On a small device (iPhone SE / a compact Android), FOCUS each input in the form in
turn and verify: (a) the focused field stays fully visible above the keyboard, (b)
the submit/primary CTA is reachable with the keyboard up, (c) tapping it submits
(does not merely dismiss the keyboard). Repeat in landscape where the keyboard eats
most of the height.

## SEVERITY GUIDE
- CRITICAL: a required input or the only submit control is fully covered/unreachable with the keyboard open → form cannot be completed.
- HIGH: a field/CTA is hidden but recoverable only by awkward manual scrolling; `resizeToAvoidBottomInset:false` on a form screen.
- MEDIUM: misconfigured avoidance that mostly works; missing `keyboardShouldPersistTaps`; modal/sheet inputs not adjusting.
- LOW/INFO: minor offset; cosmetic jump on focus.

## CONFIDENCE GUIDE
- HIGH: `TextInput`/`TextField` form with zero keyboard handling directly visible; `resizeToAvoidBottomInset:false` present.
- MEDIUM: handling exists but behavior/subtree/offset looks wrong from source.
- LOW: exact coverage depends on device height — confirm on smallest target with keyboard up (and landscape).

## SCORING HINTS
Base 100. Deduct (× confidence): CRITICAL −30, HIGH −20, MEDIUM −10, LOW −4, INFO 0;
multiplier HIGH ×1.0 / MEDIUM ×0.75 / LOW ×0.5. Weight this area seriously — hidden
required inputs are the most common and most damaging native adaptive defect. Bonus:
`react-native-keyboard-controller` (or keyboard-aware scroll) used consistently +5;
Flutter forms in a scrollable with `resizeToAvoidBottomInset` left true +5. Clamp 0–100.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_n2_keyboard_input.md`. Each finding: app tag,
severity, confidence, `file:line`, and the confirm step (device + which input).
Per-severity count + area score.
