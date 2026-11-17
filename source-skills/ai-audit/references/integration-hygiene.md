# Integration Hygiene & Secrets (Area 1, weight 12%, base 100)

> Verify LLM credentials are never hardcoded or embedded in prompts, that official SDKs are used, models are pinned, config comes from env, and calls have timeouts/retries.

---

PROJECT DETECTION (execute first): Read `reports/.artifacts/step_00_ai_detection.md`
for `PROVIDERS`, `FRAMEWORKS`, `PROJECT_PATHS`, `CALL_SITES`. Scan those paths.

## Checks

### 1. Hardcoded LLM API keys (HIGH)
Provider key prefixes leaking into source (NOT in `.env`/example files):
```bash
grep -rniE '(sk-[A-Za-z0-9_-]{20,}|AIza[A-Za-z0-9_-]{20,}|gsk_[A-Za-z0-9]{20,})' \
  . --include='*.ts' --include='*.js' --include='*.py' --include='*.go' 2>/dev/null \
  | grep -v 'node_modules\|dist\|vendor\|.venv\|test\|spec\|example\|\.env' | head -20 \
  || echo "No hardcoded provider keys"
```
Also flag `api_key="..."` / `apiKey: "..."` literals passed to a client constructor.

### 2. Secret embedded in a prompt string (HIGH)
Credentials interpolated into the prompt itself (leaks to the provider and logs):
```bash
grep -rniE '(system|prompt|content|instructions).{0,40}(sk-|sk-ant-|AIza|api[_-]?key|password|secret|token)' \
  . --include='*.ts' --include='*.py' --include='*.js' 2>/dev/null \
  | grep -v 'node_modules\|test\|spec' | head -20 || echo "No secrets in prompts"
```

### 3. Config source (MEDIUM)
Keys/`base_url` should come from env or a secret manager, not literals. Confirm
client init reads `process.env` / `os.environ` / `os.getenv`.
```bash
grep -rniE '(OpenAI|Anthropic|GoogleGenerativeAI|ChatOpenAI|ChatAnthropic)\(' \
  . --include='*.ts' --include='*.py' -n 2>/dev/null | grep -v 'node_modules\|test' | head -20
```

### 4. Model pinning (LOW)
Flag calls with no explicit model, or floating aliases without a dated/pinned
version where the provider offers one. Prefer models centralized in config.
```bash
grep -rniE 'model\s*[:=]\s*["'\''][a-z0-9.\-]+["'\'']' . --include='*.ts' --include='*.py' -n 2>/dev/null \
  | grep -v 'node_modules\|test' | head -30 || echo "No explicit model args found"
```

### 5. Timeouts & retries (LOW)
LLM clients should set request timeout and bounded retries. Absence = LOW.
Grep for `timeout`, `max_retries`, `maxRetries` near client init.

## SEVERITY
- HIGH: hardcoded key in source; secret embedded in prompt.
- MEDIUM: keys/base_url as literals instead of env; unofficial/raw-HTTP client where an official SDK exists.
- LOW: model not pinned/centralized; no timeout/retry config.

## SCORING HINTS (applied by report-generator)
Base 100. Deduct: hardcoded key −30/key (max −60); secret-in-prompt −20/instance;
literal config −10; unofficial client −10; model not pinned −5; no timeout/retry −3.
Bonus: keys only via env/secret manager +5; models pinned & centralized +5.

## ARTIFACT SAVE (mandatory)
Save to `reports/.artifacts/step_01_ai_integration.md` (run `mkdir -p reports/.artifacts`).
Output: checks run, findings grouped by severity with `file:line` and matched
pattern, and a per-severity count. If clean, state "No integration hygiene issues detected."
