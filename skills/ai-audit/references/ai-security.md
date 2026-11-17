# AI Security — OWASP LLM Top 10 (Area 7, weight 12%, base 100)

> Map AI-specific security controls to the OWASP Top 10 for LLM Applications (2025): prompt injection, sensitive info disclosure, output handling, excessive agency, unbounded consumption.

---

PROJECT DETECTION (execute first): Read `reports/.artifacts/step_00_ai_detection.md`
for `CALL_SITES`, `FRAMEWORKS`, `SYSTEM_TYPE`. Reuse hardcoded-key findings from
`step_01_ai_integration.md` (do not re-scan keys; reference them).

## Checks

### 1. Prompt injection mitigation — LLM01 (HIGH)
Untrusted input (user text, retrieved docs, web/email/tool output) concatenated
into prompts without isolation or guardrails. Look for external content flowing
straight into `system`/prompt. Credit mitigations: input guardrails, delimiter/
role isolation, allowlists, injection classifiers (e.g. Rebuff, LLM-Guard,
provider moderation).
```bash
grep -rniE '(llm.?guard|rebuff|guardrail|prompt.?shield|jailbreak|injection|moderation|sanitize.?prompt)' \
  . -n 2>/dev/null | grep -v 'node_modules\|test' | head || echo "No prompt-injection mitigation detected (flag HIGH)"
```

### 2. Sensitive info disclosure / PII — LLM02 (HIGH)
User PII sent to the model with no redaction/scrubbing, and no output filtering.
Credit PII redaction in/out (Presidio, regex scrubbers, DLP).
```bash
grep -rniE '(presidio|pii|redact|anonymi|scrub|dlp|mask.?(email|ssn|card))' \
  . -n 2>/dev/null | grep -v 'node_modules\|test' | head || echo "No PII redaction detected (flag HIGH)"
```

### 3. Improper output handling — LLM05 (HIGH)
Model output used in a dangerous sink without validation: `eval`/`exec`, shell,
SQL, HTML render (XSS), file paths. Flag direct use of completions in sinks.
```bash
grep -rniE '(eval\(|exec\(|child_process|subprocess|os\.system|dangerouslySetInnerHTML|execute\(.?(query|sql))' \
  . -n 2>/dev/null | grep -v 'node_modules\|test' | head -20 || echo "No obvious dangerous output sinks"
```

### 4. Excessive agency — LLM06/08 (HIGH)
Tools/agents with unconstrained power (delete, pay, send, deploy) and no human
approval. Cross-reference Area 4 tool least-privilege / HITL.

### 5. Content moderation / guardrails on I/O (MEDIUM)
Moderation or safety filter on inputs and/or outputs (provider moderation
endpoint, safety settings, guardrail layer).

### 6. Unbounded consumption / DoS — LLM10 (MEDIUM)
No per-user rate limiting on the AI endpoint (cross-reference Area 3 rate guard).

## SEVERITY (tag each finding with its OWASP LLM id)
- HIGH: LLM01 no injection defense; LLM02 no PII handling; LLM05 output to dangerous sink; LLM06/08 excessive agency.
- MEDIUM: LLM04/10 no moderation; no rate limiting.

## SCORING HINTS
Base 100. Deduct: no injection mitigation −25; no PII redaction −20; unvalidated
output to sink −20; excessive agency −20; no moderation −10; no rate limiting −10.
Bonus: guardrail/moderation layer +5; PII filter +5.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_07_ai_security.md`. Findings by severity, each
tagged with the OWASP LLM id and `file:line`. Per-severity count.
