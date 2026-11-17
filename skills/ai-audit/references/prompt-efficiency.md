# Prompt Engineering & Efficiency (Area 2, weight 15%, base 100)

> Evaluate system/user separation, explicit output limits, prompt bloat, prompt versioning, few-shot discipline, and unbounded conversation history.

---

PROJECT DETECTION (execute first): Read `reports/.artifacts/step_00_ai_detection.md`
for `CALL_SITES` and `PROVIDERS`. Inspect each call site.

## Checks

### 1. Explicit output cap `max_tokens` (MEDIUM)
Every production call should bound output length. Flag calls without
`max_tokens` / `maxOutputTokens` / `max_output_tokens`.
```bash
# Anthropic requires max_tokens; OpenAI/Gemini often omit it — flag omissions
grep -rniE '(messages\.create|chat\.completions\.create|generate_content|generateText|streamText)' \
  . --include='*.ts' --include='*.py' -A8 2>/dev/null | grep -v 'node_modules\|test' \
  | grep -iE 'max_tokens|maxtokens|max_output_tokens|maxoutputtokens' | head -20 \
  || echo "No max_tokens set on any call (flag MEDIUM)"
```

### 2. System / user separation (MEDIUM)
Instructions belong in a `system` role, not concatenated into the user message.
Flag a single giant user string carrying role instructions with no `system`.

### 3. Prompt bloat / dead context (LOW–MEDIUM)
Very large inline prompt literals, duplicated boilerplate, or whole files/docs
pasted into every call. Flag inline prompt strings over ~1500 chars and repeated
static blocks (candidates for caching — cross-reference Area 3).

### 4. Prompt versioning / centralization (LOW)
Prompts scattered as inline literals across many files are unversioned. Prefer a
prompt module/registry, template files, or a prompt-management tool.
```bash
grep -rniE '(prompt|system_prompt|SYSTEM_PROMPT|instructions)\s*[:=]' . \
  --include='*.ts' --include='*.py' -l 2>/dev/null | grep -v 'node_modules\|test' | head
```

### 5. Unbounded conversation history (MEDIUM)
Chat/agent loops that append to a messages array with no truncation, windowing,
or summarization grow tokens without limit. Flag message arrays that only `.push`/
`.append` with no trimming or summarize step.

## SEVERITY
- MEDIUM: no `max_tokens`; no system/user separation; unbounded history growth.
- LOW: prompt bloat; unversioned/scattered prompts.

## SCORING HINTS
Base 100. Deduct: no `max_tokens` −10/pattern (max −30); no system/user split −10;
prompt bloat −5/instance (max −20); unversioned prompts −5; unbounded history −10.
Bonus: prompts centralized/versioned +5; few-shot via retrieval not hardcoded bloat +5.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_02_ai_prompt.md`. Findings by severity with
`file:line`; note token-heavy prompt hotspots for the Cost Profile. Per-severity count.
