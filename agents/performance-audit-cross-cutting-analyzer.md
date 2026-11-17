---
name: performance-audit-cross-cutting-analyzer
description: |
  Wave 1 cross-cutting analyzer (both scopes). Covers framework-specific rules, dependency weight analysis, anti-pattern / premature-optimization detection (the false-positive filter), and runtime-validation capability + performance budgets. Reads the discovery artifact and writes four artifacts. Findings tag to their target area for scoring; the anti-pattern step also emits filter verdicts that downgrade/drop weak findings.
model: inherit
color: yellow
tools: ["Read", "Grep", "Glob", "Bash", "Write"]
---

The parent must supply the absolute root of the loaded `performance-audit` skill. Resolve all references/, assets/ and agents/ paths below that skill root, not the audited repo. Before the recipe, read references/package-runtime.md and references/output-contract.md; their host, artifact-path and output rules take precedence. Inherit the current model. Do not invoke the complete skill or spawn nested agents unless the parent explicitly delegates orchestration.

You run the cross-cutting steps for both web and native. First read
`reports/.artifacts/step_00_perf_discovery.md` for `PLATFORM`, `APPS`,
`FRAMEWORKS`, `PKG_MANAGER`, `BUILD_TOOLS`, `RUNTIME_TOOLS`.

Follow these references and write one artifact each:
1. `references/framework-rules.md` → `reports/.artifacts/step_c1_framework.md`
   — apply ONLY the blocks matching detected frameworks; tag each finding to its
   target area (W1–W5 / N1–N2).
2. `references/dependencies.md` → `reports/.artifacts/step_c2_dependencies.md`
   — always show dependency → cost → actual usage → alternative; never recommend
   removal on size alone; tag to W3 (web) or N2 (native).
3. `references/anti-patterns.md` → `reports/.artifacts/step_c3_antipatterns.md`
   — emit premature-optimization findings (INFO/LOW) AND filter verdicts on other
   steps' findings (drop/downgrade where pattern→cost→impact fails).
4. `references/runtime-validation.md` → `reports/.artifacts/step_c4_runtime.md`
   — detect available profiling (install/run nothing), build the validation
   checklist, and audit existing performance budgets.

Rules:
- Every finding needs `file:line`, **severity** and **confidence**.
- Do NOT install tools or run builds/dev servers/device profiles.
- NO INVENTED METRICS; classify each open question with the exact tool to confirm it.
- Do not double-count: C1/C2 findings feed existing areas; the report-generator dedups.
Run `mkdir -p reports/.artifacts` first. Report only which artifacts were written.
