---
name: security-audit
description: "Audit sensitive files, secrets, dependency vulnerabilities, supply-chain integrity and CI/CD security. Use for repository security scanning; application authorization belongs to web-security-audit."
disable-model-invocation: true
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - Bash(python3 */scripts/validate_report.py *)
  - Bash(command -v:*)
  - Bash(git rev-parse:*)
  - Bash(git ls-files:*)
  - Bash(git check-ignore:*)
  - Bash(git worktree list:*)
  - Bash(git -C:*)
  - Bash(gitleaks version:*)
  - Bash(gitleaks detect:*)
  - Bash(gitleaks dir:*)
  - Bash(gitleaks git:*)
  - Bash(trivy --version:*)
  - Bash(trivy fs:*)
  - Bash(govulncheck:*)
  - Bash(go list -m:*)
  - Bash(npm audit:*)
  - Bash(npm outdated:*)
  - Bash(pnpm audit:*)
  - Bash(pnpm outdated:*)
  - Bash(yarn audit:*)
  - Bash(yarn outdated:*)
  - Bash(cargo audit:*)
  - Bash(cargo outdated:*)
  - Bash(pip-audit:*)
  - Bash(pip list --outdated:*)
  - Bash(dotnet list:*)
  - Bash(flutter pub outdated:*)
  - Bash(dart pub outdated:*)
  - Bash(fvm flutter pub outdated:*)
  - Bash(pod outdated:*)
  - Bash(gemini --version:*)
  - Bash(gemini auth status:*)
  - Bash(gemini extensions list:*)
  - Bash(gemini prompt:*)
  - mcp__agent-memory__memory_manifest
  - mcp__agent-memory__memory_list
  - mcp__agent-memory__memory_get
disallowed-tools:
  - Agent
  - Workflow
  - Edit
---

# Auditoría técnica de seguridad

Primero lee [compatibilidad y alcance](references/package-runtime.md) y [formato de salida](references/output-contract.md). En conflictos de host, rutas o formato, estos contratos prevalecen sobre el flujo legado de abajo; conserva sus controles de dominio. Consulta [el catálogo](references/skill-routing.md) para proponer otro especialista sólo si encaja.

## Security Audit

Scored, evidence-based defensive security review of the current repository.

### Hard constraints

Violating any of these invalidates the run.

1. **Read-only outside `reports/`.** The only writes permitted are
   `reports/security_audit.md`, `reports/security_audit.json`, and
   `reports/.history/last_scores.json`. Never create, move, or delete any
   other path.
2. **Never install, update, or configure anything.** No
   `gemini extensions install`, no `go install`, no `brew install`, no
   `npm i -g`, no plugin or extension bootstrap. If a scanner is absent,
   record the skip plus the install command *as a recommendation in the
   report* and move on.
3. **Never run a destructive command.** No `rm`, no `mv`, no `git clean`,
   no `git checkout`, no `truncate`, no redirection into a repo file.
4. **Never `cd`.** Pass paths as arguments (`git -C <dir> ls-files`,
   `npm --prefix <dir> audit`). A failed `cd` silently short-circuits the
   rest of a `&&` chain, and `cd` triggers permission prompts.
5. **Never `exit`.** This runs inside a session, not a standalone script.
   To skip a step, record the skip and continue.
6. **Prefer native tools over Bash.** `Glob`, `Grep`, and `Read` are
   read-only, need no approval, and cover the whole static audit. Use
   `Bash` *only* for the external scanners in Phase C and the two git
   fact-checks in Phase B. Never reimplement `Glob`/`Grep` with
   `find`/`grep` via Bash.
7. **Never invent a finding, a count, a version, or a score.** If
   evidence is missing, write `Not verified` and state what would prove
   it. Every finding needs a real `path:line`.
8. **No governance or ops recommendations.** Do not recommend
   `CODEOWNERS`, `SECURITY.md`, runbooks, deployment procedures, or
   monitoring. Technical security only. This paragraph is an instruction
   to you — it must never appear in the report.

### Degradation contract

No step is mandatory. Any step may be unavailable (tool missing,
permission denied, command error, not a git repo). When that happens:

- Record `SKIPPED: <step> — <observed reason>` in the run notes.
- Carry the skip into the report's affected section and into §13.
- Keep going. **Never abort the audit**, and never make a section's score
  depend on a tool you could not run (see *Unscoreable inputs* in
  `references/scoring.md`).

Report a denial as a denial. Do not retry a denied command with a
reworded variant to get around the refusal.

### Scope resolution

**The skill is invoked from wherever the user happens to be. Never tell
the user to re-run it from somewhere else.** Resolve the scope yourself:

1. `git rev-parse --show-toplevel`. Succeeds ⇒ that is the scope root.
   Audit it. This covers every worktree, so a run from inside any
   worktree needs no question.
2. It fails (the cwd is not a git repo) ⇒ look for a bare+worktree
   layout: `Glob` for `*/.bare` and `*/*/.git` (e.g. `code/.bare`,
   `code/main/.git`). Each directory holding a `.git` entry is a worktree.
   - One worktree found ⇒ audit it and say which one you picked.
   - Several ⇒ **ask with `AskUserQuestion`**. It accepts at most four
     options, and these layouts routinely hold dozens of worktrees, so do
     not try to list them all. `Glob` returns matches newest-first by
     modification time: offer the first three, each labelled with its
     directory name, and say in the question how many exist in total. The
     user reaches any other one through the free-text "Other" field.
     Never guess, and never audit the non-git parent as if it were the
     repo.
   - For the chosen worktree `<wt>`, run every git fact-check against it
     with `git -C <wt> …` (`rev-parse`, `ls-files`, `check-ignore`), and
     point the Phase C scanners at `<wt>`.
3. No git anywhere ⇒ audit the invocation directory as a plain tree, and
   note in §13 that the git-dependent checks (tracked-file verification,
   ignore verification, history scan) were unavailable.

Always exclude from every scan: `node_modules`, `vendor`, `dist`, `build`,
`target`, `.dart_tool`, `.venv`, `__pycache__`, `obj`, `bin`, `.git`,
`reports`.

---

### Phase A — Stack detection (native tools only)

Use one `Glob` call per manifest family; no Bash.

| Manifest | Type | Source globs |
| --- | --- | --- |
| `pubspec.yaml` | `flutter` | `**/*.dart` |
| `package.json` with `@nestjs/core` | `nestjs` | `**/*.ts` |
| `package.json` without it | `nodejs` | `**/*.{ts,js,tsx,jsx}` |
| `go.mod` | `go` | `**/*.go` |
| `Cargo.toml` | `rust` | `**/*.rs` |
| `pyproject.toml`, `requirements.txt` | `python` | `**/*.py` |
| `build.gradle`, `build.gradle.kts` | `gradle` | `**/*.{kt,java}` |
| `pom.xml` | `maven` | `**/*.java` |
| `Package.swift` | `swift` | `**/*.swift` |
| `Podfile` | `cocoapods` | `**/*.{swift,m}` |
| `*.sln`, `*.csproj` | `dotnet` | `**/*.cs` |
| none of the above | `generic` | common source extensions |

Record every match as `type@relative/path`. **Audit all detected stacks**
(a monorepo gets each one covered). When two manifests share a directory,
the table's top-down order wins for that directory.

If `generic`, say so plainly and scope later phases to the broad patterns.

### Phase B — Static audit (native tools, plus two git fact-checks)

#### B1. Sensitive file exposure → §Sensitive File Protection

`Glob` for: `**/.env*`, `**/*.{pem,key,cert,crt,p12,pfx,keystore,jks}`,
`**/service-account*.json`, `**/*-credentials.json`, `**/*-key.json`,
`**/secrets/**`, `**/credentials/**`, plus per stack:

- flutter: `**/google-services.json`, `**/firebase_app_id_file.json`,
  `**/key.properties`, `android/.gitignore`, `ios/.gitignore`
- nodejs/nestjs: `**/ormconfig.json`, `**/docker-compose*.y*ml`
- dotnet: `**/appsettings*.json`, `**/*.pubxml`
- python: `**/settings.py`
- rust: `**/.cargo/credentials*`

**A file existing on disk is not a finding.** For each hit, establish
exposure with evidence before reporting it:

1. `git ls-files -- <paths…>` in one batched call. Listed ⇒ **tracked ⇒
   HIGH finding**. Absent from output ⇒ not tracked.
2. `git check-ignore -v -- <paths…>` in one batched call. A match ⇒
   ignored (safe) and names the `.gitignore:line` that covers it — quote
   that as evidence.
3. Only report as a risk a file that is **tracked**, or **neither tracked
   nor ignored**. A local file that is ignored and untracked is **SAFE** —
   say so explicitly rather than omitting it.
4. Not a git repo ⇒ both checks are unavailable. Report the files as
   `Not verified (no git)` and do not deduct for tracking.

Then `Glob` every `.gitignore` and `Read` them (batch the reads) to check
coverage per stack: common (`node_modules`, `.env*`, `*.log`, `coverage`,
`.DS_Store`), flutter (`build/`, `.dart_tool/`, `*.keystore`,
`key.properties`), node (`node_modules`, `dist`, `.env*`), go (`*.exe`),
rust (`target/`), python (`__pycache__`, `*.pyc`, `.venv/`), dotnet
(`bin/`, `obj/`, `*.user`). Note `.env.example` / `.env.sample` presence
and confirm by reading it that it holds placeholders, not live values.

#### B2. Hardcoded secrets → §Secret Detection

`Grep` with `output_mode: "content"` and `-n` so every finding carries a
real line number. Scope each pattern to the detected stack's globs.

High-signal patterns (HIGH when the match is a literal value, not an env
read):

- Provider-prefixed keys: `AKIA[0-9A-Z]{16}`, `sk_live_`, `sk_test_`,
  `ghp_`, `github_pat_`, `xox[baprs]-`, `AIza[0-9A-Za-z_-]{35}`,
  `-----BEGIN [A-Z ]*PRIVATE KEY-----`
- Assigned literals:
  `(?i)(secret|password|passwd|api[_-]?key|token|private[_-]?key)\s*[:=]\s*["'][^"'$\{]{8,}["']`
- Credentialed URIs:
  `(postgres|postgresql|mysql|mongodb|redis|amqp)://[^:\s"']+:[^@\s"']+@`
- Bearer literals: `Bearer\s+["']?[A-Za-z0-9._-]{20,}`

MEDIUM: cloud/payment credential identifiers without a literal value
(`aws_secret`, `gcp_credentials`, `azure_secret`, `service_account`),
and secret material in `SharedPreferences` / `UserDefaults` / plists.

LOW: informational — e.g. direct `process.env.X` reads in a NestJS
project that otherwise uses `ConfigService`.

**Triage every match before reporting it.** Discard, and say how many you
discarded, when the match is:

- in a test, mock, fixture, example, sample, or snapshot path;
- an env/config *read* (`process.env.X`, `os.Getenv`, `System.getenv`,
  `Platform.environment`), which is correct practice, not a leak;
- a placeholder (`xxx`, `changeme`, `<your-key>`, `example`, `...`,
  all-zero, or a repeated single character);
- a type, interface, constant *name*, or comment with no value;
- inside a lock file or generated artifact.

Also `Glob` for `.gitleaks.toml`, `.pre-commit-config.yaml`,
`.husky/**` and `Read` them to record whether secret-scanning hooks exist.

#### B3. Supply chain → §Supply Chain Integrity

`Glob` + `Read` the lock files: `package-lock.json`, `yarn.lock`,
`pnpm-lock.yaml`, `pubspec.lock`, `go.sum`, `Cargo.lock`, `poetry.lock`,
`Podfile.lock`, `packages.lock.json`. Record presence, and whether entries
carry integrity hashes (`integrity`/`sha512`/`sha256`/`h1:`).

`Grep` the manifests for non-registry sources: `git+`, `git:`,
`"file:`, `path:`, `"link:`, `replace ` directives in `go.mod`, and
`[patch.` in `Cargo.toml`. Each is a supply-chain finding with evidence.

#### B4. Security automation → §Security Automation & CI/CD

`Glob` + `Read`: `.github/dependabot.y*ml`, `renovate.json`,
`.github/renovate.json`, `.snyk`, `.pre-commit-config.yaml`,
`.github/workflows/**`, `.gitlab-ci.yml`.

`Grep` the CI workflows for scanner invocations (`npm audit`, `snyk`,
`trivy`, `grype`, `gitleaks`, `govulncheck`, `cargo audit`, `pip-audit`,
`safety`, `dependency-check`, `codeql`) and for PR triggers
(`pull_request`). Record each as evidence with `path:line`.

#### B5. OWASP pattern scan → §Consolidated Findings (LOW/MEDIUM only)

`Grep` per stack. These feed §8 and the remediation matrix but **never
change a section score**.

- SQL injection: string concatenation or interpolation reaching a query —
  `fmt.Sprintf` into `Query`/`Exec` (go), `.query(` with `+` or a template
  literal (js/ts), `execute(` with `%` or `.format(` (python),
  `SqlCommand`/`ExecuteNonQuery` with `+` (dotnet), `Statement` +
  `executeQuery` with `+` (java/kotlin).
- XSS: `innerHTML =`, `document.write(`, `dangerouslySetInnerHTML`
  (js/ts), `innerHtml =` (dart).
- Path traversal: a request-derived value reaching `path.join` /
  `filepath.Join` / `Path.Combine` / `open(` / `readFile`.
- Code injection: `eval(`, `new Function(`, `Runtime.getRuntime().exec`,
  `subprocess` with `shell=True`, `child_process.exec` with interpolation.

Apply the same triage rules as B2: a pattern in a test or with a constant
argument is not a finding.

### Phase C — External scanners (optional, Bash, each independently skippable)

Probe once with `command -v <tool>`. If absent, or if the probe or the run
is denied or errors, record `NOT_AVAILABLE` plus the install hint and
continue. Never install. Never let one scanner's absence block another.

| Tool | Read-only invocation | Feeds |
| --- | --- | --- |
| `gitleaks` | `gitleaks dir . --no-banner --redacted` (working tree); `gitleaks git . --no-banner --redacted` (history) — fall back to `gitleaks detect --source . --no-git` / `--source .` on older builds | §Secret Detection; history count |
| `trivy` | `trivy fs . --scanners vuln,secret,misconfig -f table` | §Dependency Security; +15 automation |
| `govulncheck` | `govulncheck ./...` | §Dependency Security CVEs |
| `go list` | `go list -m -u all` | outdated modules |
| `npm`/`pnpm`/`yarn` | `<pm> audit --json`; `<pm> outdated` (pick the pm from the lock file present) | CVEs; outdated |
| `cargo` | `cargo audit`; `cargo outdated` | CVEs; outdated |
| `pip-audit` | `pip-audit`; `pip list --outdated` | CVEs; outdated |
| `dotnet` | `dotnet list <sln\|csproj> package --vulnerable --include-transitive`; `--outdated`; `--deprecated` | CVEs; outdated; deprecated |
| flutter/dart | `flutter pub outdated` (or `dart pub outdated`, or `fvm flutter pub outdated`) | outdated; discontinued |
| `pod` | `pod outdated` | outdated |

Keep scanner output bounded — capture severity counts and the top findings
with package name and version, not the full dump.

**Gemini (§10), strictly optional.** `command -v gemini`; if present,
`gemini --version` and `gemini auth status`, then `gemini extensions list`.
Run `gemini prompt "/security:analyze"` **only if** the CLI is present,
authenticated, and the security extension is *already* installed. Do not
install the extension. Do not clean up after the CLI — if it drops files
in the repo, report their paths in §13 and leave them for the user. If any
precondition fails, §10 reads `Skipped — <observed reason>` and that is a
complete, valid outcome.

### Phase D — Score and report

Read `references/scoring.md` now and follow it exactly. It is the single
source of truth for the rubrics, the weights, the 13-section contract, the
unscoreable-input rule, and the Markdown formatting rules.

Order of operations, non-negotiable:

1. Compute all 5 section scores from Phase A–C evidence, each clamped to
   0–100.
2. Compute the overall weighted score and derive every label and the
   posture.
3. *Then* write the report. Content written before the scores exist is
   invalid.
4. `Write` `reports/security_audit.md`. `Write` creates parent
   directories — do not run `mkdir`.
5. `Write` `reports/security_audit.json`, then
   `reports/.history/last_scores.json`.
6. Self-check against the validation checklist in `references/scoring.md`
   and fix any failure in place before reporting completion.

If `reports/.history/last_scores.json` already exists, `Read` it first and
include the delta in §2.

### Closing message to the user

Keep it short: the overall score and posture, the report path, the HIGH
findings as a list, and every skipped step with its observed reason. Do not
restate the report.
