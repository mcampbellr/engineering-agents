# Observability & Usage Metrics (Area 5, weight 13%, base 0)

> Verify tracing, token/cost/latency logging, trace/session IDs, and alerting actually wrap real AI calls. Base 0 — credit only what is implemented.

---

PROJECT DETECTION (execute first): Read `reports/.artifacts/step_00_ai_detection.md`
for `FRAMEWORKS` and `CALL_SITES`.

**Adversarial rule:** credit a control only if it wraps actual AI calls in the
request path. A logging import that is never called, or metrics that nothing
reads, does not count.

## Checks (additive)

### 1. Tracing / observability tool (+30)
```bash
grep -rniE '(langsmith|LANGCHAIN_TRACING|langfuse|arize|phoenix|braintrust|openinference|opentelemetry|otel|helicone|portkey)' \
  . -n 2>/dev/null | grep -v 'node_modules\|test' | head -20 || echo "No tracing/observability tool detected"
```
Confirm it is initialized and wraps calls (env `LANGCHAIN_TRACING_V2`, `@observe`
decorators, OTel span instrumentation, callback handlers).

### 2. Token usage logging (+20)
Per-call token counts captured from `usage` / `usage_metadata` and logged/stored.
```bash
grep -rniE '(usage|prompt_tokens|completion_tokens|total_tokens|input_tokens|output_tokens|usageMetadata)' \
  . -n 2>/dev/null | grep -v 'node_modules\|test' | head -20 || echo "No token usage capture detected"
```

### 3. Cost tracking / accounting (+15)
Token counts converted to cost, or a cost field logged/aggregated per call/user.

### 4. Latency metrics (+10)
Request duration measured around LLM calls and recorded.

### 5. Trace / session IDs (+10)
Correlation IDs (`trace_id`, `session_id`, `run_id`, `conversation_id`) propagated
through calls for debugging multi-step flows.

### 6. Alerting on cost / error / drift (+15)
Alerts/thresholds on token/cost budget, error rates, latency, or eval-score drops.

Cap total at 100.

## SEVERITY (for the findings list)
- HIGH: production AI system with zero tracing and no usage capture.
- MEDIUM: partial (e.g. logs tokens but no tracing, or tracing but no alerting).
- LOW: missing latency metrics or correlation IDs only.

## SCORING HINTS
Base 0; add per implemented control above; cap 100. Report the additive breakdown.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_05_ai_observability.md`. List each control as
present/absent with `file:line` evidence, the additive subtotal, and note the
tracing/eval tooling detected for Project Detection Results.
