---
name: reuse-review
description: Review changes for duplicated implementations and missed reuse of existing components, functions, hooks, services, validators, models, and configuration. Language- and framework-agnostic. Use for reuse audits, DRY reviews, reinvention checks, or reviewing whether new code belongs in an existing shared abstraction.
---

# Reuse Review

Determine whether a change recreates an existing capability and identify the smallest compatible reuse. Search beyond the diff; report evidence, not resemblance. Apply to any language, framework, frontend, backend, scripts, or monorepo.

Audit and recommend by default. Modify code only when implementation is requested. Do not install dependencies, generate catalogs, commit, publish review comments, or change other skills merely to perform an audit. This skill can be a focused review or a lane within a broader review; it does not require another skill or multiple agents.

## Establish scope and context

- Honor the requested files, directory, PR, branch, or repository. For change reviews, inspect added/modified code and relevant callers; search the whole repository for existing equivalents. Existing unchanged duplication is context, not a new finding unless the change worsens it. A full-repository audit may report existing duplication.
- Resolve the comparison base from the request and repository conventions. Verify its freshness when reviewing a branch or PR. Include staged, unstaged, and relevant untracked source when reviewing local work. State the actual scope and any unavailable base; do not silently treat missing diff data as a clean review.
- Read applicable repository instructions, package boundaries, exports, dependency manifests, and design or architecture conventions. Discover actual shared locations instead of assuming a framework or a directory such as `src/components`.

## Investigate reuse

For each meaningful new capability, identify what it does independently of its name. Search names, synonyms, behavior, underlying APIs, signatures, messages, validation rules, repeated structures, imports, documentation, and tests. Use `rg` and repository navigation where available. Text matches are leads, not proof; different names may implement the same behavior.

Search shared packages and public APIs, nearby features, existing callers, and wrappers around dependencies already used by the project. Check components and variants, business services, hooks/composables, parsers, validators, formatters, models, constants, configuration, and infrastructure helpers as relevant. Exclude vendored/generated/build output by default; include ignored or untracked first-party source when relevant. Do not count generated repetition as a hand-maintained duplicate. Do not expand into an internet search for replacement libraries unless requested.

Read each candidate implementation and representative callers/tests before accepting equivalence. Compare:

- Input/output contracts, defaults, errors, edge cases, side effects, and state ownership.
- Domain semantics, authorization, tenant isolation, transactions, and runtime constraints where applicable.
- For UI: behavior, validation, focus, keyboard interaction, accessibility, styling contracts, controlled state, and available variants. Appearance alone does not prove equivalence.
- Import/export visibility, dependency direction, package/runtime compatibility, and ownership. A private helper in an unrelated feature is not automatically a shared public API.

## Choose a justified action

- **REUSE**: an accessible existing implementation satisfies the needed contract; cite the export and integration point.
- **EXTEND / COMPOSE**: an existing implementation covers the core need and a small compatible extension or composition supplies the difference. Explain that difference and the impact on current callers. Do not add a wrapper when an existing option already suffices.
- **CONSOLIDATE**: independently maintained implementations encode the same responsibility, but neither is an appropriate shared owner yet. Cite the occurrences and propose the narrowest sensible common home. Do not create a third implementation while leaving the duplicates behind.
- **KEEP DISTINCT**: differences in semantics, contracts, dependencies, or lifecycle justify separation. Explain the material reason when it helps resolve a plausible duplicate.
- **CREATE**: no suitable reusable implementation was found within the searched scope. State what was searched; absence of a match is not proof that none exists elsewhere.

Prefer established shared implementations to new abstractions when they fit. Do not force sharing based on matching names, a small repeated expression, or hypothetical future users. Do not recommend importing across forbidden boundaries, degrading accessibility or behavior, introducing dependency cycles, or coupling independently evolving domains. Repeated tests, protocol-required shapes, deliberate forks, and generated code may legitimately remain separate.

## Evidence and priority

Every actionable duplication finding must include:

1. The reviewed location and symbol, with verified file and line references.
2. The existing counterpart (or consolidation counterparts), also with verified file and line references.
3. The actual behavioral overlap, material differences, and why reuse is compatible.
4. The practical impact of keeping separate implementations and the smallest concrete remedy.

Do not publish “there is probably a helper somewhere” as a finding. Investigate it or mark it as an unresolved coverage limitation. Deduplicate reports about the same underlying abstraction. Never invent line numbers or snippets.

Rank by demonstrated impact, not by the mere presence of duplication. High priority requires a concrete correctness, security, or substantial maintenance consequence; ordinary compatible reuse opportunities are usually medium or low priority. Keep speculative extraction suggestions separate from verified findings. Do not block a review for harmless repetition or an unsupported suspicion.

## Report

Use the user's or project's review language. Lead with verified findings, ordered by impact. For each, provide priority, a short title, both locations, compatibility evidence, impact, and recommended action. Add a compact decision table only when several reviewed capabilities benefit from comparison:

| Reviewed capability | Existing implementation | Decision | Reason |
|---|---|---|---|

End with scope/coverage limitations and a focused verdict: changes recommended, no actionable reuse findings, or insufficient evidence. “No findings” means no verified problems in the inspected scope, not a guarantee that the repository contains no duplication. When integrated into another review, return these findings in its requested format rather than imposing a second report.

## Design references

Original workflow informed by the evidence requirements of [DRY Reviewer](https://github.com/tufantunc/review-pro/blob/main/core/skills/dry/SKILL.md) and the reuse/compose/create decisions in [Bitovi Component Reuse](https://github.com/bitovi/ai-enablement-prompts/blob/main/plugins/react/skills/component-reuse/SKILL.md). Self-contained: no external skill or framework is required at runtime.
