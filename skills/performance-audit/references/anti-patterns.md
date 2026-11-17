# Cross · Anti-Patterns & Premature Optimization (Step C3)

> A dual-purpose guard. (a) It emits its OWN findings for optimizations that cost complexity without measurable benefit. (b) It is the false-positive filter every other step must pass its findings through: no finding survives unless `pattern → cost → impact` is plausible for the ACTUAL workload. This is what keeps the audit honest and prevents "could be faster" noise.

---

SCOPE GUARD (execute first): Read `reports/.artifacts/step_00_perf_discovery.md`.
Also read the other step artifacts as they complete, to sanity-check their findings.

## PRINCIPLE

A pattern is NOT a problem merely because a faster alternative exists. A finding is
only valid when all four hold:
1. **pattern** — the construct is actually present (evidence `file:line`),
2. **cost** — it does measurable/plausible work (large N, hot path, frequent call),
3. **impact** — that work affects a user-perceived metric or resource, and
4. **recommendation** — a concrete, lower-cost alternative exists.
If any link is missing → downgrade to INFO or drop it.

## Anti-patterns to actively flag (as findings, usually INFO–LOW)

### 1. Unnecessary / incorrect memoization
`useMemo`/`useCallback`/`React.memo` (or Vue `computed`, Angular memo) wrapping
trivial values, or with deps that change every render (no-op). Cost: extra
allocations + code complexity, zero benefit. → INFO/LOW. Escalate to MEDIUM only if
it masks a correctness bug.

### 2. Over-splitting / excessive lazy loading
Dozens of tiny dynamic `import()`s creating request overhead worse than one chunk;
lazy-loading tiny always-visible components. → INFO/LOW.

### 3. Over-engineered / duplicated caching layers
Multiple caches for the same data (query cache + manual cache + context), or a
cache where the data is cheap to recompute. Risk: staleness bugs + memory. → LOW.

### 4. Over-engineered state management
Heavy global store / middleware stack for trivial local state; premature
normalization. → INFO.

### 5. Micro-optimizations with negligible impact
Hand-rolled loops replacing readable code, premature `for` over `map` on tiny
arrays, string-concat tricks, etc. → INFO. Note that readability lost > perf gained.

### 6. Complexity added without a measurement
A comment/PR claims a perf win but no benchmark/profile backs it; the code is now
harder to maintain. → INFO, recommend measuring or reverting.

## FALSE-POSITIVE FILTER (apply to every other step's findings)

When consolidating, re-check each candidate finding from W*/N*/C1/C2:
- Is the collection/loop actually large or the path actually hot? If it's a
  10-item static list, a "missing virtualization/memo" finding → drop or INFO.
- Is the component actually expensive, or a cheap leaf? Cheap leaf re-render → drop.
- Is the dependency actually imported and on the client path? Stale/dev-only → not a runtime finding.
- Does the fix add more complexity/risk than the impact justifies? → INFO with the tradeoff stated.

## SEVERITY / CONFIDENCE
Own findings are almost always INFO or LOW (they are the *opposite* of urgent).
Never mark a premature-optimization observation as HIGH/CRITICAL. Confidence
reflects how sure you are it's genuinely a no-benefit cost.

## OUTPUT (mandatory)
Save to `reports/.artifacts/step_c3_antipatterns.md`, with two parts:
1. **Own findings** — anti-pattern observations (INFO/LOW), each with `file:line`,
   the missing link if it's borderline, and the simpler alternative.
2. **Filter verdicts** — a list of other-step findings you recommend downgrading or
   dropping, with the reason (which of the 4 links fails). The report-generator
   applies these before finalizing severities.
