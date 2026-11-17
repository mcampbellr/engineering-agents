# Scoring and report contract

Single source of truth for scores, structure, and formatting. Where any
other file disagrees with this one, this one wins.

## Weights

| Section | Weight | Evidence source |
| --- | --- | --- |
| Sensitive File Protection | 0.25 | B1 |
| Secret Detection | 0.30 | B2 + gitleaks |
| Dependency Security | 0.20 | Phase C audits + outdated/deprecated |
| Supply Chain Integrity | 0.10 | B3 |
| Security Automation & CI/CD | 0.15 | B4 + trivy |

`overall = round(file*0.25 + secret*0.30 + dep*0.20 + supply*0.10 + auto*0.15)`

## Labels and posture

| Score | Label | Posture |
| --- | --- | --- |
| 85–100 | Strong | Secure |
| 70–84 | Fair | Needs Attention |
| 50–69 | Weak | At Risk |
| 0–49 | Critical | Critical |

The overall score in §1 and §2 must be identical, and each §1 score must
match its detail section exactly.

## Rubrics

Clamp every section to 0–100 after applying its modifiers.

**Sensitive File Protection** — base 100:
- `.env` tracked in git (confirmed via `git ls-files`): −30 each
- Private key or cert tracked: −25 each
- Cloud credential file tracked: −25 each
- No `.env` pattern in any `.gitignore` (confirmed absent): −15
- Missing stack-specific patterns: −10 per category
- `.env.example` present with placeholder values only: +5
- Per-platform `.gitignore` files present (e.g. `android/`, `ios/`): +5

**Secret Detection** — base 100:
- HIGH finding (literal secret or API key in source): −20 each, floor −60
- MEDIUM finding (cloud or payment credential identifier): −10 each, floor −40
- LOW finding: −3 each, floor −15
- Secrets found in git history by gitleaks: −15
- Pre-commit secret-scanning hook configured: +5
- `.gitleaks.toml` present: +5

**Dependency Security** — base 100:
- Critical CVE: −25 · High: −15 · Medium: −5 · Low: −2
- More than 5 outdated deps: −10; more than 10: −20 (not cumulative — take the larger)
- Deprecated or discontinued package: −10 each, floor −30
- Lock file missing: −20
- All deps at latest: +5
- Lock file carries integrity hashes: +5

**Supply Chain Integrity** — base 100:
- Git-sourced dependency: −10 each
- Path or link dependency: −5 each
- Dependency from an unknown registry: −20 each
- No lock file: −25
- Lock file without integrity hashes: −15
- Every dependency from an official registry: +10
- Checksums verified present across the lock file: +5

**Security Automation & CI/CD** — base **0**, additive:
- Dependabot configured: +20 — or Renovate: +15 (take the larger, not both)
- Snyk configured: +15
- CI runs a vulnerability scanner: +20
- CI triggers on pull requests: +10
- Pre-commit security hook: +10
- Lock file validated in CI (`npm ci`, `--frozen-lockfile`): +10
- Additional scanner available and run (trivy, grype): +15

## Unscoreable inputs

**A tool you could not run is never a deduction.** The absence of
gitleaks, trivy, govulncheck or Gemini is an audit-coverage limitation,
not a security defect.

- A *missing optional scanner* → do not deduct. Score the section from the
  static evidence you do have, state `Coverage: partial — <tool>
  unavailable` under its Score Breakdown, and add installing it as a
  recommendation.
- A section with **no usable evidence at all** (e.g. Dependency Security
  with no manifest, no lock file, and every audit tool unavailable) →
  mark it `Score: N/A (not scoreable) — <reason>`, drop its weight from
  the formula, and renormalize the remaining weights so they sum to 1.0.
  Show the renormalized formula in §1.
- Never write a fabricated 0 to fill a gap, and never omit a section.

## The 13 sections

1. Security Scoring Breakdown — the 5 section scores with their weights,
   then the formula with real numbers substituted, then Overall Score,
   then Security Posture. First thing the reader sees.
2. Executive Summary — Overall Score, top findings, priority
   recommendations. If prior history exists: `Previous: N/100, Change: ±M
   (improving|declining|unchanged)`.
3–7. The five scored sections, **ordered by score ascending** (weakest
   first). Ties break in this order: Secret Detection, Sensitive File
   Protection, Dependency Security, Supply Chain Integrity, Security
   Automation & CI/CD. Sections marked `N/A` sort last.
8. Consolidated Findings by Severity — HIGH, then MEDIUM, then LOW.
9. Remediation Priority Matrix — finding, severity, effort, impact.
10. Gemini AI Analysis — results, or `Skipped — <observed reason>`.
11. Project Detection Results — every `type@path` found, and the globs scanned.
12. Appendix: Evidence Index — every `path:line` cited in the report.
13. Scan Metadata — date, scope root, tools available vs. unavailable,
    every skipped step with its reason, and total files scanned.

Each scored section (3–7) carries all seven of:

- **Description** — one line on what it evaluates
- **Score** — `NN/100 (Label)`
- **Score Breakdown** — `Base: 100`, then one line per modifier with its
  signed value, then `Final: NN/100 (Label)`
- **Key Findings** — bullets, each tagged `[HIGH]` / `[MEDIUM]` / `[LOW]`
- **Evidence** — concrete `path:line` references
- **Risks** — what goes wrong if unaddressed
- **Recommendations** — numbered, prioritized, technical

Dependency Security additionally carries **Dependency Age Analysis**:
outdated count, deprecated count, and the top offenders with current and
latest versions.

## Formatting

Real GitHub-flavored Markdown. The file is `.md` and is read as rendered
Markdown — earlier versions of this skill contained contradictory
"no markdown" rules; they are void.

- Title: `# Security Audit Report`, nothing before it
- Sections: `## N. Section Name`
- Bullets `- `, numbered lists `1. `, paths in backticks
- Bold for emphasis; tables where they aid reading
- Severity always as `[HIGH]:` / `[MEDIUM]:` / `[LOW]:`
- Scores always as `NN/100 (Label)`
- ASCII punctuation; no smart quotes or fancy dashes
- One blank line between sections, never three
- Ends with §13, then the metadata block below

## JSON outputs

`reports/security_audit.json`:

```json
{
  "overallScore": 0,
  "posture": "Secure|Needs Attention|At Risk|Critical",
  "scores": {
    "sensitiveFile": 0,
    "secretDetection": 0,
    "dependencySecurity": 0,
    "supplyChainIntegrity": 0,
    "securityAutomation": 0
  },
  "findings": { "high": 0, "medium": 0, "low": 0 },
  "skipped": ["gitleaks: not installed"],
  "timestamp": "ISO8601",
  "projectTypes": ["go@."]
}
```

A section scored `N/A` serializes as `null`, not `0`.

`reports/.history/last_scores.json` takes the same `scores`, `findings`,
`projectTypes` and `timestamp`, plus `"overall": <int>`.

## Validation checklist

Before reporting completion, verify and fix in place:

- [ ] All 13 sections present, in order, §1 first and §13 last
- [ ] §1 has 5 scored lines with weights, the substituted formula, Overall, Posture
- [ ] §2 states the Overall Score
- [ ] §3–7 each have Score, Score Breakdown with `Base:` and `Final:`, and all seven subsections
- [ ] §3–7 ordered by score ascending, `N/A` last
- [ ] Every §1 score matches its detail section
- [ ] Every label matches its score range
- [ ] Every finding has a severity tag and a real `path:line`
- [ ] No fabricated count, version, CVE, or score
- [ ] Every skipped tool appears in §13 with its observed reason
- [ ] No instruction text from this file or `SKILL.md` leaked into the report
- [ ] No CODEOWNERS, SECURITY.md, runbook, or monitoring recommendation
- [ ] Both JSON files written and well-formed

## Metadata block

End the report with exactly:

```
---
Generated by: security-audit (local skill)
Skill: security-audit
Date: YYYY-MM-DD
---
```
