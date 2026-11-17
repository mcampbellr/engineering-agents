# Agent Architecture & Scalability (Area 4, weight 12%, base 100)

> Evaluate orchestration pattern, state management, recursion/loop limits, modularity for scale, tool least-privilege, and human-in-the-loop for high-risk actions.

---

PROJECT DETECTION (execute first): Read `reports/.artifacts/step_00_ai_detection.md`
for `FRAMEWORKS` and `SYSTEM_TYPE`.

**Applicability:** If `SYSTEM_TYPE=Single-call` and no agent framework is present,
this area is largely N/A — set base 100, deduct only for genuine issues, and note
"single-call app; agentic checks N/A" in the artifact. Full checks apply when an
agent/graph/tool-calling loop is present.

## Checks (agentic systems)

### 1. Recursion / iteration limits (HIGH if missing)
Graphs and agent loops must bound steps. LangGraph: `recursion_limit`.
Frameworks: max iterations / max steps. Absence risks infinite loops + cost blowups.
```bash
grep -rniE '(recursion_limit|max_iterations|maxIterations|max_steps|maxSteps|iteration.?cap)' \
  . -n 2>/dev/null | grep -v 'node_modules\|test' | head || echo "No recursion/iteration limit found (flag HIGH)"
```

### 2. State management (MEDIUM)
Shared state should be explicit and scoped (typed graph state / reducers), not
global mutable variables shared across concurrent runs. Flag module-level mutable
state used inside handlers.

### 3. Orchestration pattern & modularity (MEDIUM)
At scale prefer a clear pattern (supervisor / graph with separated nodes,
specialized tools). Flag monolithic single-function agents mixing routing, tools,
prompts, and business logic in one place.
```bash
grep -rniE '(StateGraph|add_node|add_edge|create_supervisor|Command\(|create_react_agent|Crew\(|AssistantAgent)' \
  . -n 2>/dev/null | grep -v 'node_modules\|test' | head -20
```

### 4. Tool least-privilege (MEDIUM)
Tools exposed to the model should be scoped and safe. Flag tools that run shell,
execute SQL, delete data, or hit the filesystem/network without constraints or
allowlists (also cross-referenced as excessive agency in Area 7 / OWASP LLM06).

### 5. Human-in-the-loop for high-risk actions (MEDIUM)
Consequential/irreversible actions (payments, deletes, external sends) should
require approval / interrupt. Flag autonomous execution of such actions.
```bash
grep -rniE '(interrupt|human.?in.?the.?loop|require.?approval|checkpoint|awaiting.?approval)' \
  . -n 2>/dev/null | grep -v 'node_modules\|test' | head || echo "No human-in-the-loop mechanism found"
```

### 6. Concurrency safety (LOW)
Concurrent runs sharing clients/state should be safe. Flag shared mutable
buffers/histories without isolation per request/session.

## SEVERITY
- HIGH: no recursion/iteration limit in a looping agent/graph.
- MEDIUM: global mutable state; monolithic agent; over-privileged tools; no HITL for high-risk actions.
- LOW: concurrency isolation gaps.

## SCORING HINTS
Base 100. Deduct: no recursion/iteration limit −25; global mutable state −15;
monolithic agent −10; over-privileged tools −10; no HITL for high-risk −10; concurrency gap −5.
Bonus: clear supervisor/graph separation +5; iteration limits set +5.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_04_ai_architecture.md`. State detected pattern
and `SYSTEM_TYPE`, findings by severity with `file:line`, and per-severity count.
If single-call, state N/A explicitly.
