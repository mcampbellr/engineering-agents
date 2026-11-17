# Token Cost Control & Caching (Area 3, weight 15%, base 100)

> Verify caching (prompt + response), rate/budget guards, cheaper-model routing, and runaway-loop protection — the controls that prevent token/cost leaks.

---

PROJECT DETECTION (execute first): Read `reports/.artifacts/step_00_ai_detection.md`
for `PROVIDERS`, `FRAMEWORKS`, `CALL_SITES`. Cross-reference prompt hotspots from
`step_02_ai_prompt.md`.

## Checks

### 1. Prompt caching (MEDIUM if large static prefixes exist and none used)
Detect provider-native caching:
- Anthropic: `cache_control` / `{"type": "ephemeral"}` on system or tool blocks.
- OpenAI: automatic prefix caching (>1024 tokens) — credit if prompts are prefix-stable
  and ordered static→dynamic; flag if dynamic content is prepended, defeating cache.
- Gemini: `caching`/`CachedContent`/`cached_content` (context caching).
```bash
grep -rniE '(cache_control|ephemeral|CachedContent|cached_content|createCachedContent|prompt.?cach)' \
  . --include='*.ts' --include='*.py' -n 2>/dev/null | grep -v 'node_modules\|test' | head -20 \
  || echo "No prompt caching detected"
```
If large/repeated static system prompts exist (from Area 2) and no caching → flag MEDIUM.

### 2. Response cache (LOW–MEDIUM)
Exact-match or semantic cache for repeated queries (Redis/LRU/`GPTCache`/
`langchain` cache / semantic cache). Absence with high-repeat workloads → flag.
```bash
grep -rniE '(set_llm_cache|InMemoryCache|RedisCache|GPTCache|semantic.?cache|responseCache)' \
  . -n 2>/dev/null | grep -v 'node_modules\|test' | head || echo "No response cache detected"
```

### 3. Rate limiting / budget guard (MEDIUM)
Per-user/per-session token or request caps, spend ceilings, or budget alerts.
Absence means one runaway prompt can burn spend uncontrolled.
```bash
grep -rniE '(rate.?limit|ratelimit|token.?budget|max.?spend|budget|usage.?limit|throttle)' \
  . -n 2>/dev/null | grep -v 'node_modules\|test' | head || echo "No rate/budget guard detected"
```

### 4. Model tiering (LOW)
Cheap/small models for routing, classification, summarization; large models only
where needed. Flag a single expensive model used for every subtask.

### 5. Runaway-loop / backoff protection (HIGH for unbounded loop, else MEDIUM)
Agent/retry loops must have iteration caps and exponential backoff. Flag `while
True`/`for` loops calling the LLM with no bound, or retries with no backoff.
Cross-reference recursion limits in Area 4.

## SEVERITY
- HIGH: unbounded LLM loop with no iteration cap.
- MEDIUM: no prompt caching despite large static prefixes; no rate/budget guard; retries without backoff.
- LOW: no response cache; single expensive model for trivial subtasks; no token/cost accounting.

## SCORING HINTS
Base 100. Deduct: no caching w/ large prefixes −20; no rate/budget guard −15;
retries w/o backoff −10; unbounded loop −20; single model for subtasks −5; no token accounting −5.
Bonus: prompt caching implemented +10; response/semantic cache +5; cheaper-model tiering +5.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_03_ai_caching.md`. Report which caching/guard
controls are present vs absent, with `file:line`, plus an estimate of caching
coverage (share of large static prompts that are cached) for the Cost Profile.
