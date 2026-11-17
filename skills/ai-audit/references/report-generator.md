# AI Audit Report Generator

> Synthesize all AI-audit artifacts into a comprehensive report with quantitative scoring, severity classification, cost profile, and legal advisory. MUST follow the exact 16-section structure from assets/report-template.md. Every section is MANDATORY — do not merge, skip, or rename. Scored detail sections (3–10) MUST be dynamically ordered by score ascending.

---

Goal: Generate the final AI Audit report by integrating all analysis artifacts
using the standardized structure from `assets/report-template.md`.

## MANDATORY REPORT STRUCTURE (16 sections)
1. AI Audit Scoring Breakdown (8 scored lines + Overall + Posture)
2. Executive Summary (Overall Score + top findings + priority recommendations)
3–10. Scored Detail Sections (DYNAMIC ORDER — score ascending, lowest first):
   Integration Hygiene & Secrets · Prompt Engineering & Efficiency · Token Cost
   Control & Caching · Agent Architecture & Scalability · Observability & Usage
   Metrics · Evaluation & Quality · AI Security (OWASP LLM) · Legal & Compliance
11. Consolidated Findings by Severity (HIGH, MEDIUM, LOW — tag OWASP LLM ids)
12. AI Usage & Cost Profile
13. Legal & Compliance Advisory (non-scored)
14. Remediation Priority Matrix
15. Project Detection Results
16. Appendix: Evidence Index & Scan Metadata

## DYNAMIC ORDERING
After computing all 8 area scores, sort sections 3–10 by score ascending (lowest
= Section 3). Tiebreaker order for equal scores: Observability, Evaluation,
AI Security, Token Cost & Caching, Prompt Engineering, Integration Hygiene,
Agent Architecture, Legal & Compliance.

## ARTIFACT INTEGRATION
Read and cross-reference:
- `reports/.artifacts/step_00_ai_detection.md` — AI_DETECTED, PROVIDERS, FRAMEWORKS, SYSTEM_TYPE, CALL_SITES (Sections 12, 15)
- `step_01_ai_integration.md` — Area 1 (Integration Hygiene & Secrets)
- `step_02_ai_prompt.md` — Area 2 (Prompt Engineering & Efficiency) + token hotspots
- `step_03_ai_caching.md` — Area 3 (Token Cost & Caching) + caching coverage
- `step_04_ai_architecture.md` — Area 4 (Agent Architecture)
- `step_05_ai_observability.md` — Area 5 (Observability)
- `step_06_ai_evaluation.md` — Area 6 (Evaluation) + dimension coverage
- `step_07_ai_security.md` — Area 7 (AI Security, OWASP LLM ids)
- `step_08_ai_legal.md` — Area 8 (Legal scored) + Advisory Annex (Section 13)

If `AI_DETECTED=false` in step_00, do NOT produce a scored report — output only:
"No AI/LLM usage detected — ai-audit does not apply to this project."

## SCORING SYSTEM

8 scored areas with weights (sum = 1.00):
- Integration Hygiene & Secrets — 0.12 — base 100
- Prompt Engineering & Efficiency — 0.15 — base 100
- Token Cost Control & Caching — 0.15 — base 100
- Agent Architecture & Scalability — 0.12 — base 100
- Observability & Usage Metrics — 0.13 — base 0 (additive)
- Evaluation & Quality — 0.12 — base 0 (additive)
- AI Security (OWASP LLM) — 0.12 — base 100
- Legal & Compliance — 0.09 — base 100

Score labels and AI-Readiness posture mapping:
- 85–100 = Strong = "Production-Ready"
- 70–84 = Fair = "Needs Attention"
- 50–69 = Weak = "At Risk"
- 0–49 = Critical = "Critical"

Apply the deduction/addition rubrics documented in each area reference file
("SCORING HINTS"). Base-100 areas subtract per severity; base-0 areas (5, 6) add
per implemented control. Clamp every area score to 0–100.

OVERALL SCORE FORMULA:
```
overall = round(
  integration*0.12 + prompt*0.15 + caching*0.15 + architecture*0.12 +
  observability*0.13 + evaluation*0.12 + security*0.12 + legal*0.09
)
```
The Overall Score in Section 1 and Section 2 MUST match.

## MANDATORY COMPUTATION ORDER (before writing any prose)
- Step A — Extract findings + counts from every step artifact.
- Step B — Compute each of the 8 area scores via its rubric; clamp 0–100.
- Step C — Compute Overall Score via the formula.
- Step D — Determine labels (Strong/Fair/Weak/Critical) for each score and Overall.
- Step E — Verify all 9 scores (8 areas + overall) exist before writing content.
A report without computed scores is INVALID.

REJECTION CRITERIA: if an artifact is missing and a base-100 area score cannot be
computed, assign that area 0 and note "Score: 0/100 (Critical) — Insufficient data
from [artifact]". For base-0 areas (Observability, Evaluation) a missing artifact
means 0 by definition. Never omit a scored area.

SCORE COMPARISON: if `reports/.history/last_ai_scores.json` exists, read previous
`overall` + `timestamp`; add to Section 2: "Previous: [N]/100, Change: [+/-M]
([improving|declining|unchanged])".

## SECTION FORMAT

Scored sections (3–10) MUST include:
- **Description** — what this area evaluates
- **Score** — `[Score]/100 ([Label])`
- **Score Breakdown** — Base → each deduction/addition with value → Final. Example:
  ```
  Base: 100
  - No prompt caching w/ large static prefixes (MEDIUM): -20
  - No rate/budget guard (MEDIUM): -15
  + Response cache present: +5
  Final: 70/100 (Fair)
  ```
- **What's Right ✅** — good practices observed, with `file:line`
- **What's Wrong ❌** — findings with `[HIGH|MEDIUM|LOW]` (+ OWASP LLM id for Area 7) and `file:line`
- **Risks** — consequences if unaddressed
- **Recommendations** — numbered, prioritized

Special sections:
- **Section 1** — 8 lines "[Area]: [Score]/100 ([Label])" + "Overall Score: …" + "AI-Readiness Posture: …"
- **Section 11** — 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW, each finding with `file:line`, source area, and OWASP LLM id where applicable
- **Section 12 (AI Usage & Cost Profile)** — providers/models detected; token hotspots (largest/most-frequent prompts); caching coverage estimate; calls missing `max_tokens`; runaway-loop risks
- **Section 13 (Legal & Compliance Advisory)** — paste the advisory annex from step_08 verbatim, leading with the "not legal advice" disclaimer
- **Section 14** — Remediation Priority Matrix: Priority | Finding | Effort | Impact
- **Section 15** — Project Detection Results: providers, frameworks, system type, call-site count, tracing/eval tooling detected
- **Section 16** — Evidence Index (artifact references) + Scan Metadata table

## FORMATTING
Use Markdown: `#` headings, `**bold**`, tables, `` `backtick` `` for paths/`file:line`.
Severity as `[HIGH]`/`[MEDIUM]`/`[LOW]`. Scores as `[Score]/100 ([Label])`. Report
starts with the H1 title and nothing before it. Do NOT leak generator/rubric
instructions into the output.

## JSON EXPORT (mandatory)
After the Markdown report, write `reports/ai_audit.json` (run `mkdir -p reports`):
```json
{
  "overallScore": 0,
  "posture": "Production-Ready|Needs Attention|At Risk|Critical",
  "scores": {
    "integrationHygiene": 0, "promptEfficiency": 0, "tokenCaching": 0,
    "agentArchitecture": 0, "observability": 0, "evaluation": 0,
    "aiSecurity": 0, "legalCompliance": 0
  },
  "findings": { "high": 0, "medium": 0, "low": 0 },
  "providers": [], "frameworks": [], "systemType": [],
  "timestamp": "[ISO8601]"
}
```

## SCORE HISTORY (mandatory, after MD + JSON)
Write `reports/.history/last_ai_scores.json` (run `mkdir -p reports/.history`) with
`overall`, `timestamp`, `scores` (8 areas), `findings`, `providers`, `frameworks`, `systemType`.
