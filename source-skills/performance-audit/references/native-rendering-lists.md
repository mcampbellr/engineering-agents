# Native · Rendering & Lists (Step N1, scored area, base 100)

> React Native / Expo (and Flutter where source exists). Evaluate re-renders, unstable props/callbacks, context-driven broad renders, and list virtualization. NEVER apply web/DOM rules here. NEVER state FPS/render counts as measured without an RN DevTools/Flipper/Perf-monitor capture.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_perf_discovery.md`.
Run only for apps with `platform=native`. Note Expo SDK version and whether the
New Architecture (Fabric/TurboModules) / Hermes is enabled — do not assume old APIs.
For Flutter, apply the Flutter notes at the end; skip the RN-specific greps.

## Rendering

### 1. Unstable props / inline callbacks into memoized children (MEDIUM–HIGH)
New arrays/objects/closures created inline and passed to `React.memo`/`PureComponent`
children or to `renderItem`, defeating memoization.
```bash
grep -rniE '(renderItem=\{\(|=\{\(\)\s*=>|style=\{\[|style=\{\{)' . --include='*.tsx' --include='*.jsx' -n 2>/dev/null \
  | grep -v node_modules | head -20 || echo "No obvious inline-reference props"
```
Flag only where the child is non-trivial or inside a list row.

### 2. Context causing broad re-renders (MEDIUM)
A single Context holding frequently-changing values (or the whole app state) so
every consumer re-renders on any change; missing selector/split contexts.
Cross-reference `STATE` — global store without selectors is the same failure.

### 3. Expensive render functions / derived work in render (HIGH)
Sorting/filtering/formatting large data inline in a component or in `renderItem`
on every pass; heavy work per list row.

### 4. Unnecessary / derived state (LOW–MEDIUM)
State that mirrors props or is derived from other state (should be computed),
triggering extra render cycles.

## Lists

### 5. ScrollView / `.map()` rendering large collections (CRITICAL–HIGH)
A `ScrollView` (or `View` + `.map`) rendering a large/unbounded collection mounts
every item at once — no virtualization, heavy memory + slow mount.
```bash
grep -rniE '<ScrollView' . --include='*.tsx' --include='*.jsx' -n 2>/dev/null | grep -v node_modules | head
grep -rniE '<(FlatList|SectionList|FlashList)\b' . --include='*.tsx' --include='*.jsx' -n 2>/dev/null | grep -v node_modules | head
```
CRITICAL if the collection is known-large/unbounded; HIGH otherwise.

### 6. FlatList misconfiguration (MEDIUM–HIGH)
- Inline `renderItem`/`keyExtractor` recreated each render.
- Index-as-key `keyExtractor={(_, i) => String(i)}` on a reorderable/dynamic list.
- Complex, un-memoized item component.
- Missing `getItemLayout` for fixed-height rows; nested VirtualizedLists (RN warns).
Flag the specific misconfig with `file:line`.

### 7. FlashList/RecyclerListView opportunity (INFO–LOW, evidence-gated)
Only suggest FlashList/RecyclerListView when there is evidence the workload
justifies it (long list + heavy rows + reported jank). Do NOT auto-recommend
replacing a working FlatList — record as INFO/LOW with the condition to validate.

## SEVERITY GUIDE
- CRITICAL: large/unbounded collection in ScrollView/`.map`; full-list re-render per keystroke.
- HIGH: expensive per-row render, unvirtualized long list, heavy un-memoized items.
- MEDIUM: unstable props into rows, broad context re-renders, FlatList misconfig.
- LOW/INFO: derived-state cleanups, FlashList suggestions.

## CONFIDENCE GUIDE
- HIGH: ScrollView-over-large-collection / inline renderItem directly visible.
- MEDIUM: re-render breadth inferred from context/state shape.
- LOW: "janky" claims — need RN Perf Monitor / DevTools Profiler / Flipper.

## SCORING HINTS
Base 100. Deduct (× confidence): CRITICAL −30, HIGH −20, MEDIUM −10, LOW −4, INFO 0;
LOW-confidence at half. Bonus: virtualized lists with stable `keyExtractor` +
memoized rows +5; selector-based state +5. Clamp 0–100.

## FLUTTER NOTES (if Flutter source present)
Flag: missing `const` constructors on static widgets; `ListView(children:[...])`
with large lists instead of `ListView.builder`; expensive work in `build()`;
`setState` on large subtrees instead of scoped rebuilds; missing `RepaintBoundary`
for costly repaints. Same severity/confidence rules.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_n1_rendering.md`. Findings with app, severity,
confidence, `file:line`, and the profiling tool needed for any runtime claim
(RN DevTools Profiler, Perf Monitor, Flipper, Flutter DevTools). Per-severity count.
