# AI Usage Detection

> Detect whether and how a project uses AI/LLMs and agent frameworks. Framework-agnostic with runtime project-type detection. This is the MANDATORY first step; if no AI usage is found the audit stops here.

---

Goal: Produce the detection artifact that all downstream steps depend on. Record
providers, frameworks, system type, call sites, and project paths. If no AI usage
is detected, report cleanly and stop the audit.

## PROJECT ROOT & PATHS (execute first)

- Identify manifests to know the stack(s): `package.json`, `requirements.txt`,
  `pyproject.toml`, `Pipfile`, `go.mod`, `pom.xml`, `build.gradle`, `Gemfile`,
  `composer.json`, `*.csproj`.
- For monorepos, record `stack@path` pairs (e.g. `python@services/api`,
  `node@apps/web`). Scan each path.

## PROVIDER / SDK DETECTION (dependencies)

Grep manifests and lockfiles for AI SDKs. Absence of a dependency does not rule
out raw HTTP usage (see Call-Site Detection).

```bash
# JS/TS
grep -rniE '"(openai|@anthropic-ai/sdk|@google/(generative-ai|genai)|@langchain/[a-z-]+|langchain|langgraph|@langchain/langgraph|llamaindex|^ai$|"ai"|cohere-ai|@mistralai/[a-z-]+|groq-sdk|@aws-sdk/client-bedrock-runtime|openrouter|ollama|together-ai|replicate)"' \
  package.json 2>/dev/null || echo "No JS AI SDKs in package.json"

# Python
grep -rniE '(^openai|^anthropic|google-generativeai|google-genai|^langchain|langgraph|llama-index|llama_index|litellm|dspy|dspy-ai|instructor|guidance|crewai|pyautogen|autogen|semantic-kernel|cohere|mistralai|groq|boto3.*bedrock|ollama|transformers|vllm)' \
  requirements.txt pyproject.toml Pipfile 2>/dev/null || echo "No Python AI SDKs"

# Go
grep -rniE '(sashabaranov/go-openai|anthropics/anthropic-sdk-go|google/generative-ai-go|tmc/langchaingo|cohere-ai/cohere-go)' \
  go.mod 2>/dev/null || echo "No Go AI SDKs"
```

Map matches to `PROVIDERS` and `FRAMEWORKS`:
- Providers: `openai`, `anthropic`, `google/gemini`, `cohere`, `mistral`,
  `groq`, `bedrock`, `azure-openai`, `openrouter`, `ollama`, `together`, `replicate`.
- Frameworks: `langchain`, `langgraph`, `llama-index`, `vercel-ai-sdk` (the `ai`
  package), `crewai`, `autogen`, `dspy`, `semantic-kernel`, `litellm`,
  `instructor`, or `raw-sdk`/`none`.

## API-KEY / ENV DETECTION

```bash
grep -rniE '(OPENAI_API_KEY|ANTHROPIC_API_KEY|GEMINI_API_KEY|GOOGLE_API_KEY|GOOGLE_GENAI_API_KEY|GROQ_API_KEY|MISTRAL_API_KEY|COHERE_API_KEY|AZURE_OPENAI_[A-Z_]+|OPENROUTER_API_KEY|TOGETHER_API_KEY|REPLICATE_API_TOKEN|HUGGINGFACE(HUB)?_API_TOKEN)' \
  . --include='*.env*' --include='*.ts' --include='*.js' --include='*.py' --include='*.go' \
  -l 2>/dev/null | grep -v 'node_modules\|dist\|vendor\|.venv' | head -30 || echo "No AI env keys found"
```

## CALL-SITE DETECTION (catches raw HTTP too)

```bash
grep -rniE '(chat\.completions\.create|\.responses\.create|messages\.create|generate_content|GenerativeModel|\.invoke\(|\.stream\(|StateGraph|add_node|create_react_agent|ChatOpenAI|ChatAnthropic|ChatGoogleGenerativeAI|generateText|streamText|api\.anthropic\.com|api\.openai\.com|generativelanguage\.googleapis\.com)' \
  . --include='*.ts' --include='*.tsx' --include='*.js' --include='*.py' --include='*.go' \
  -n 2>/dev/null | grep -v 'node_modules\|dist\|vendor\|.venv\|test\|spec' | head -60 \
  || echo "No LLM call sites found"
```

Record every hit as a `file:line` entry in `CALL_SITES`.

## SYSTEM TYPE CLASSIFICATION

Infer `SYSTEM_TYPE` from frameworks and call patterns (governs which dimensions
matter downstream — see `references/evaluation.md`):
- **RAG** — vector store / retriever / embeddings present (`pinecone`, `chroma`,
  `weaviate`, `pgvector`, `faiss`, `.as_retriever`, `embeddings`)
- **Multi-Agent** — `langgraph`, `crewai`, `autogen`, multiple agents / supervisor
- **Autonomous** — tool-calling loop, `create_react_agent`, agent executor with tools
- **Conversational** — chat history / message threads, chatbot UI routes
- **Extraction** — structured output / JSON schema / `instructor` / function calling for parsing
- **Content** — generation of marketing/text/media
- **Code** — code generation / review
- **Single-call** — one-shot completion with no orchestration
A project may be more than one; record all that apply, primary first.

## DECISION

- If `PROVIDERS`, `FRAMEWORKS`, `CALL_SITES`, and env keys are ALL empty:
  set `AI_DETECTED=false`. Write the artifact, then STOP the audit and report:
  "No AI/LLM usage detected — ai-audit does not apply to this project."
- Otherwise set `AI_DETECTED=true` and continue.

## ARTIFACT SAVE (mandatory)

Save to `reports/.artifacts/step_00_ai_detection.md`. Run first: `mkdir -p reports/.artifacts`

Output format (downstream steps parse these keys):
```
AI_DETECTED=[true|false]
PROVIDERS=[comma list]
FRAMEWORKS=[comma list]
SYSTEM_TYPE=[comma list, primary first]
PROJECT_PATHS=[stack@path|...]
CALL_SITES:
- file:line — snippet
...
ENV_KEYS_FOUND=[comma list]
```
Followed by a short prose summary of how the project uses AI.
