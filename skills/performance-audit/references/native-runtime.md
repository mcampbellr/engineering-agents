# Native · Runtime — Startup, Memory, Animations, Navigation, State (Step N2, scored area, base 100)

> React Native / Expo runtime cost outside rendering: app startup work, memory retention/leaks, animation threading, navigation lifecycle, and state-management breadth. NEVER apply web rules. NEVER state startup ms / memory MB / FPS as measured without a real profile (Xcode Instruments, Android Studio Profiler, RN Perf Monitor, Flipper).

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_perf_discovery.md`.
Run only for `platform=native`. Respect the detected Expo SDK / RN version and
whether Reanimated, Hermes, and the New Architecture are present — use APIs that
exist in the detected version; do not assume legacy or newer APIs.

## Startup

### 1. Heavy synchronous work at startup (HIGH)
Root `App`/entry doing sync work before first frame: many providers, analytics
init, storage hydration, large JSON parse, font/asset preloading blocking splash,
synchronous `require` of heavy modules, network requests gating render.
```bash
grep -rniE '(AppRegistry|registerRootComponent|export default function App|SplashScreen\.preventAutoHide)' . \
  --include='*.tsx' --include='*.ts' -n 2>/dev/null | grep -v node_modules | head
grep -rniE '(analytics|amplitude|segment|Sentry\.init|mixpanel)\.' . --include='*.tsx' --include='*.ts' -n 2>/dev/null | grep -v node_modules | head
```
Flag work that could be deferred/lazy/post-interactive.

### 2. Splash held too long / no deferral (MEDIUM)
`SplashScreen.preventAutoHideAsync` without hiding promptly, or gating first paint
on non-critical startup requests.

## Images (native)

### 3. Memory-heavy / unoptimized native images (HIGH)
Loading full-resolution remote images into small views, no caching, no
downsampling, or a memory-heavy image path where `expo-image`/`react-native-fast-image`
(with `recyclingKey`, `contentFit`, cache policy) would help — only if available/warranted.
```bash
grep -rniE "from ['\"](expo-image|react-native-fast-image)['\"]" . -n 2>/dev/null | grep -v node_modules | head
grep -rniE "<Image\b" . --include='*.tsx' --include='*.jsx' -n 2>/dev/null | grep -v node_modules | head
```

## Animations

### 4. JS-thread-driven animations (HIGH)
`Animated` without `useNativeDriver: true`, or state-driven (`setState`) animation
loops that run on the JS thread and drop frames; heavy work inside animated frames.
```bash
grep -rniE 'useNativeDriver' . --include='*.tsx' --include='*.ts' -n 2>/dev/null | grep -v node_modules | head
grep -rniE '(Animated\.(timing|spring|loop)|LayoutAnimation)' . --include='*.tsx' -n 2>/dev/null | grep -v node_modules | head
```
Prefer Reanimated (UI-thread) ONLY where the project uses/supports it — record as
recommendation, not a mandate.

## Navigation

### 5. Expensive screen mount / work on every focus (MEDIUM)
Heavy init in screen bodies, data reload on every `useFocusEffect`/focus without
caching, many navigation listeners, heavy work during transitions. Cross-reference
`react-navigation`/`expo-router` from discovery.
```bash
grep -rniE '(useFocusEffect|navigation.addListener|useIsFocused)' . --include='*.tsx' -n 2>/dev/null | grep -v node_modules | head
```

## State management

### 6. Overly broad subscriptions / missing selectors (MEDIUM)
Global store consumed without selectors so unrelated updates re-render screens;
excessive Context; unnecessary persistence of large state; expensive rehydration
on launch (couples to Startup).

## Memory / leaks (report as *potential* unless provable)

### 7. Uncleaned subscriptions / listeners / timers (HIGH, confidence-gated)
`addEventListener`/`addListener`/`setInterval`/`setTimeout`/subscriptions created
in effects/mount with no cleanup (`removeListener`, `clearInterval`, unsubscribe,
`AbortController`). Retained closures over large objects; ever-growing caches/arrays.
```bash
grep -rniE '(addEventListener|addListener|setInterval|setTimeout|subscribe\()' . --include='*.tsx' --include='*.ts' -n 2>/dev/null | grep -v node_modules | head -20
grep -rniE '(removeEventListener|removeListener|clearInterval|clearTimeout|unsubscribe|AbortController)' . --include='*.tsx' --include='*.ts' -n 2>/dev/null | grep -v node_modules | head -20
```
If a leak cannot be *proven* statically, report as **potential leak**, confidence
LOW/MEDIUM, and name the profiler + repro needed (heap snapshot, Instruments
Leaks/Allocations, Android Studio Memory Profiler).

## SEVERITY GUIDE
- CRITICAL: unbounded memory growth (retained listener/timer per mount on a
  frequently-mounted screen) — but only HIGH+ confidence if provable; else HIGH "potential".
- HIGH: heavy sync startup, JS-thread animation jank, uncleaned subscriptions, memory-heavy images.
- MEDIUM: focus refetch, broad state subscriptions, splash deferral.
- LOW/INFO: micro-tuning; anything needing a profile to confirm.

## CONFIDENCE GUIDE
- HIGH: missing cleanup / `useNativeDriver:false` / sync startup directly visible.
- MEDIUM: memory pressure inferred from image/state usage.
- LOW: leak/jank magnitude — always requires a device profile.

## SCORING HINTS
Base 100. Deduct (× confidence): CRITICAL −30, HIGH −20, MEDIUM −10, LOW −4, INFO 0;
LOW-confidence at half. Bonus: native-driver/Reanimated animations +5; deferred
startup work +5; listeners consistently cleaned up +5. Clamp 0–100.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_n2_runtime.md`. Findings with app, severity,
confidence, `file:line`, and the profiler needed for any runtime claim.
Per-severity count. Clearly tag memory findings as proven vs potential.
