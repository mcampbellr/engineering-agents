# AI Audit Report

---

## 1. AI Audit Scoring Breakdown

| Area | Weight | Score |
|------|--------|-------|
| Integration Hygiene & Secrets | 12% | [Score]/100 ([Label]) |
| Prompt Engineering & Efficiency | 15% | [Score]/100 ([Label]) |
| Token Cost Control & Caching | 15% | [Score]/100 ([Label]) |
| Agent Architecture & Scalability | 12% | [Score]/100 ([Label]) |
| Observability & Usage Metrics | 13% | [Score]/100 ([Label]) |
| Evaluation & Quality | 12% | [Score]/100 ([Label]) |
| AI Security (OWASP LLM) | 12% | [Score]/100 ([Label]) |
| Legal & Compliance | 9% | [Score]/100 ([Label]) |
| **Overall Score** | **100%** | **[Score]/100 ([Label])** |

**AI-Readiness Posture:** [Production-Ready / Needs Attention / At Risk / Critical]

> **Scoring:** Strong (85–100) · Fair (70–84) · Weak (50–69) · Critical (0–49)

---

## 2. Executive Summary

**Description:** AI/LLM usage audit of [Project Name]. Providers: [list]. Frameworks: [list]. System type: [types].

**Overall Score:** [Score]/100 ([Label])
**Previous:** [N]/100, Change: [+/-M] ([improving/declining/unchanged])  _(omit if no history)_

**Top Findings:**
- [Finding 1 with severity]
- [Finding 2 with severity]
- [Finding 3 with severity]

**Priority Recommendations:**
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

---

> **Sections 3–10** are the 8 scored areas, ordered by score ascending (lowest = Section 3).

---

## [N]. [Area Name]

> _(One of: Integration Hygiene & Secrets · Prompt Engineering & Efficiency · Token Cost Control & Caching · Agent Architecture & Scalability · Observability & Usage Metrics · Evaluation & Quality · AI Security (OWASP LLM) · Legal & Compliance)_

**Description:** [What this area evaluates]

**Score:** [Score]/100 ([Label])

**Score Breakdown:**
- Base: [100 or 0]
- [Deduction/addition reason] ([HIGH/MEDIUM/LOW]): [−/+][value]
- **Final:** [Score]/100 ([Label])

### What's Right ✅
- [Good practice observed] — `[file:line]`

### What's Wrong ❌
- **[HIGH/MEDIUM/LOW]** [(LLMxx for security)] — [Finding] — `[file:line]`

### Risks
- [Risk 1]

### Recommendations
1. [Recommendation 1]

---

## 11. Consolidated Findings by Severity

### 🔴 [HIGH] — Immediate Action Required
1. [Finding] — `[file:line]` — Area: [area] [— OWASP LLMxx]
2. [Continue as needed, or "No HIGH severity findings"]

### 🟡 [MEDIUM] — Address Soon
1. [Finding] — `[file:line]` — Area: [area] [— OWASP LLMxx]
2. [Continue as needed, or "No MEDIUM severity findings"]

### 🟢 [LOW] — Best Effort
1. [Finding] — `[file:line]` — Area: [area]
2. [Continue as needed, or "No LOW severity findings"]

---

## 12. AI Usage & Cost Profile

- **Providers / models detected:** [provider@model, …]
- **System type:** [types]
- **Token hotspots:** [largest / most-frequent prompts, `file:line`]
- **Caching coverage:** [share of large static prompts cached; provider mechanism used or "none"]
- **Calls missing `max_tokens`:** [count / list `file:line`]
- **Runaway-loop / backoff risks:** [findings or "none"]

---

## 13. Legal & Compliance Advisory (non-scored)

> **Disclaimer:** Orientation only — not legal advice. Consult qualified counsel. Any EU AI Act risk classification below is indicative, not binding.

| Item | Required? | Detected in repo? | Action |
|------|-----------|-------------------|--------|
| AI interaction disclosure (chat UI) | If user-facing | [Yes/No/N/A] | [action] |
| T&C clause: AI limitations & no-warranty on outputs | Yes | [Yes/No] | [action] |
| Privacy Policy: names AI subprocessor + data flows | Yes | [Yes/No] | [action] |
| AI-generated content labeling | If applicable | [Yes/No/N/A] | [action] |
| PII retention / deletion / opt-out | If PII processed | [Yes/No/N/A] | [action] |
| Provider training opt-out / ZDR | If PII processed | [Yes/No/N/A] | [action] |
| DPIA (GDPR Art. 35) / FRIA (AI Act Art. 27) | If high-risk | [Yes/No/N/A] | [action] |
| Human oversight for consequential decisions | If applicable | [Yes/No/N/A] | [action] |

**EU AI Act — indicative posture:** [prohibited / high-risk / limited-risk / minimal]. [Notes: chatbot transparency Art. 50 from Aug 2026; extraterritorial if outputs affect EU users; penalties up to €35M / 7% turnover.]

**GDPR notes:** [lawful basis, minimization, provider as processor + DPA, cross-border prompt transfer].

---

## 14. Remediation Priority Matrix

| Priority | Finding | Effort | Impact |
|----------|---------|--------|--------|
| 1 | [Finding] | [Low/Medium/High] | [Low/Medium/High] |
| 2 | [Finding] | [Low/Medium/High] | [Low/Medium/High] |

---

## 15. Project Detection Results

- **Providers:** [list]
- **Frameworks:** [list]
- **System type:** [types, primary first]
- **LLM call sites:** [count]
- **Tracing / eval tooling detected:** [list or "none"]
- **Project paths:** [stack@path, …]

---

## 16. Appendix: Evidence Index & Scan Metadata

**Evidence Index (artifacts):**
- `reports/.artifacts/step_00_ai_detection.md`
- `reports/.artifacts/step_01_ai_integration.md` … `step_08_ai_legal.md`

**Scan Metadata:**

| Field | Value |
|-------|-------|
| Scan date | [YYYY-MM-DD] |
| Project path | [Path] |
| Providers / Frameworks | [list] |
| System type | [types] |
| Total findings | [Count] (H:[n] M:[n] L:[n]) |
| Skill | ai-audit |

---
Generated by: [plugin name or "ai-audit"] v[version]
Skill: ai-audit
Date: [YYYY-MM-DD]
---
