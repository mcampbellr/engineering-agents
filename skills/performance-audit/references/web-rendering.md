# Web · Rendering & Hydration (Step W2, scored area, base 100)

> Evaluate client/server boundaries, hydration cost, unnecessary re-renders, expensive component trees, and list virtualization. Web scope only. Framework-aware (RSC/islands/SSR). Distinguish real re-render cost from harmless renders.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_perf_discovery.md`
for `platform=web`, `FRAMEWORKS`, `RENDERING`, `STATE`. Skip native apps.

## Checks

### 1. Unnecessary client components / excessive hydration (HIGH)
Server-capable UI shipped to the client and hydrated for no interactivity.
- **Next App Router:** `"use client"` at the top of large/static subtrees, or on
  files that only render markup. Flag broad `"use client"` boundaries.
- **Astro:** `client:load`/`client:only` on components that are static or could be
  `client:visible`/`client:idle`; static content accidentally hydrated.
- **Nuxt/SvelteKit:** components forced client-only without need.
```bash
grep -rniE '^\s*[\x27"]use client[\x27"]' . --include='*.tsx' --include='*.jsx' -l 2>/dev/null | grep -v node_modules | head -30
grep -rniE 'client:(load|only|visible|idle|media)' . --include='*.astro' -n 2>/dev/null | head -30
```

### 2. SSR/CSR misuse (MEDIUM–HIGH)
Data-heavy content rendered CSR-only (blank then fetch) where SSR/SSG would ship
content; OR expensive SSR of content that is purely static and could be prerendered.
Cross-reference `RENDERING`.

### 3. Unnecessary re-renders from unstable references (MEDIUM)
New object/array/function literals passed as props each render, context values
recreated inline, or state placed too high causing wide subtree re-renders.
```bash
# Inline object/array/fn props and inline context values (candidates, verify by hand)
grep -rniE '(value=\{\{|=\{\[|=\{\(\)\s*=>|Provider value=\{\{)' . --include='*.tsx' --include='*.jsx' -n 2>/dev/null \
  | grep -v node_modules | head -20 || echo "No obvious inline-reference prop patterns"
```
Flag ONLY where the child is expensive or the subtree is large — a cheap leaf
re-render is not a finding (record as INFO at most).

### 4. Expensive derived computation in render (HIGH)
Sorting/filtering/mapping large collections, heavy formatting, or parsing done
inline in render on every pass without memoization or precomputation.

### 5. Large lists without virtualization (HIGH)
Rendering hundreds/thousands of DOM rows via `.map()` with no windowing
(`react-window`, `@tanstack/virtual`, `vue-virtual-scroller`, CSS
`content-visibility`). Flag long lists rendered whole.
```bash
grep -rniE '\.map\(' . --include='*.tsx' --include='*.jsx' --include='*.vue' -n 2>/dev/null | grep -v node_modules | wc -l
grep -rniE '(react-window|react-virtual|@tanstack/virtual|vue-virtual|virtua|content-visibility)' . -l 2>/dev/null | grep -v node_modules | head
```

### 6. Hydration mismatch / layout-affecting hydration (MEDIUM)
Client/server output that diverges (dates, random, `window` at render) forcing
re-render or layout shift on hydrate. Flag `typeof window`, `Date.now()`,
`Math.random()` used during render of SSR components.

## SEVERITY GUIDE
- CRITICAL: full re-render of a large virtualized-worthy list on every keystroke.
- HIGH: broad unnecessary hydration, expensive in-render computation, unvirtualized large list.
- MEDIUM: unstable refs into expensive children, SSR/CSR misuse, hydration mismatch.
- LOW/INFO: cheap-leaf re-renders, micro-memo suggestions (defer to anti-patterns).

## CONFIDENCE GUIDE
- HIGH: static import boundary / unvirtualized list is directly visible.
- MEDIUM: re-render cost inferred; depends on how often state changes.
- LOW: "this might re-render too often" without evidence the child is expensive → React Profiler needed.

## SCORING HINTS
Base 100. Deduct (× confidence): CRITICAL −30, HIGH −20, MEDIUM −10, LOW −4, INFO 0;
LOW-confidence at half. Bonus: virtualization used for long lists +5; correct
server/static rendering of static content +5. Clamp 0–100.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_w2_rendering.md`. Findings with app, severity,
confidence, `file:line`, and — for any re-render claim — the tool to confirm it
(React DevTools Profiler / `why-did-you-render` / Vue Devtools). Per-severity count.
