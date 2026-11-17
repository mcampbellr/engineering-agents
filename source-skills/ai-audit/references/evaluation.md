# Evaluation & Quality (Area 6, weight 12%, base 0)

> Verify a reference dataset, per-dimension rubrics, CI regression, hallucination/faithfulness checks, and human-in-the-loop review. Base 0 — credit only what is implemented and actually runs.

---

PROJECT DETECTION (execute first): Read `reports/.artifacts/step_00_ai_detection.md`
for `SYSTEM_TYPE` (selects which dimensions matter) and `FRAMEWORKS`.

**Dimensions by system type** (a strategy should cover the relevant ones):
- RAG → context faithfulness, hallucination, answer relevance, retrieval precision, citation
- Multi-Agent → task decomposition, handoff correctness, goal completion, loop detection
- Conversational → tone/safety, instruction following, escalation accuracy
- Extraction → schema compliance, field accuracy, format validity
- Autonomous → safety guardrails, tool-use correctness, cost/token adherence, task completion
- Content → factual accuracy, brand voice, originality
- Code → correctness, safety, test pass rate
- Always → safety (user-facing) and task completion (agentic)

**Adversarial rule:** MISSING until code proves otherwise. Partial coverage of a
critical dimension is MISSING until the gap is quantified. Do not credit AI-SPEC /
docs as implementation. Metric logging ≠ evaluation unless it drives a decision.

## Checks (additive)

### 1. Reference / eval dataset (+25)
```bash
find . \( -name '*.jsonl' -o -name 'eval*.json' -o -name 'evals*.*' -o -name 'testset*' -o -name 'golden*' \) \
  2>/dev/null | grep -v 'node_modules\|.venv' | head || echo "No eval dataset found"
```
Credit only if it targets AI outputs (inputs + expected/rubric), not generic fixtures.

### 2. Rubrics / metrics per dimension (+20)
Defined pass/fail criteria or scored metrics per dimension (code assertions,
LLM-judge rubrics, or metric configs).

### 3. CI regression for prompts/outputs (+20)
```bash
grep -rniE '(promptfoo|deepeval|evaluate\(|ragas|langsmith.*evaluate|braintrust.*eval)' \
  . -n 2>/dev/null | grep -v 'node_modules' | head
find . -name 'promptfoo*.y*ml' 2>/dev/null | head
grep -rniE '(eval|promptfoo|deepeval)' .github/workflows Makefile* 2>/dev/null | head || echo "No eval in CI"
```

### 4. Hallucination / faithfulness checks (+20)
RAG faithfulness / groundedness / factuality checks (RAGAS, custom judges).

### 5. Human-in-the-loop review (+15)
Sampling low-confidence outputs to human review, or a labeling/feedback loop.

Cap total at 100.

## SEVERITY (for the findings list)
- HIGH (BLOCKER): a Critical dimension for the system type has no eval at all.
- MEDIUM (WARNING): partial coverage; evals exist but not automated/CI.
- LOW: nice-to-have dimension missing.

## SCORING HINTS
Base 0; add per implemented item; cap 100. Report the additive breakdown and
which required dimensions (per system type) are COVERED / PARTIAL / MISSING.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_06_ai_evaluation.md`. Include a dimension-coverage
table (dimension · status · evidence `file:line`), the additive subtotal, and eval files found.
