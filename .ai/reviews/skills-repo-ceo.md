# CEO review — skills repository

## Review inputs

- **Target:** full skills repository, including current tracked and untracked changes.
- **Base:** `8c69722ed95839c2dda36e58d52ba263d87d3758` (`origin/main` at review time).
- **Working tree at initial review:** 14 modified tracked files and 5 untracked files; 242 insertions / 43 deletions in the tracked diff, plus the untracked files. After the user chose to remove automatic PR labels, the label workflow was deleted, leaving 4 untracked implementation files.
- **Reviewed-input hashes:** `git diff HEAD --binary` SHA-256 `271fbf5f683e1ca738ba0ad3feda9feae0e2735feb064b110c6a5cfffb5efede`; initial combined diff and untracked-file snapshot SHA-256 `df396a62f627b1ebcbbd0649a5a9a75cb89688ee28bb87a03c259e1b44b101e2` (5 files, before label-workflow removal). The later scope change is recorded in this review note.
- **Prior artifacts:** no active OpenSpec change, existing CEO note, or applicable ADR was found in the repository.
- **Review limits:** review only. No implementation changes were made other than this review note. For the user's CI-duration question, the current local validation commands were timed on 2026-11-05: 13 unit tests passed in 0.42 s wall time (reported test runtime 0.017 s), and `manage.py check` passed in 0.03 s. No live host installation was exercised.

## Phase 1 — scope challenge

### Premise and existing-code leverage

The repository is a portable skills and setup package for Codex and Claude Code. The main premise holds: users need a repeatable, inspectable way to install project guidance and selected external skills across machines. The existing Grounded plugin, setup manager, source manifest, `installed.json`, doctor command, backup locations, and validation workflow already provide the right base; no new orchestration layer is justified.

The current source manifest and setup validator pin external Git revisions and the OpenSpec npm version. The selected direction during this review is to resolve the latest stable dependency versions on each setup, record exactly what was resolved, and offer recovery to the previous installed version. The working implementation still pins the versions, so the chosen direction is not yet reflected by the current code or docs.

### Dream state

On a new machine, a user installs Grounded from its host distribution, runs setup, sees the exact upstream versions and integrity identifiers selected, and can restore the previous managed installation or remove Grounded-managed files without losing user-edited files. Updates are sourced only from trusted official upstream manifests. The repo stays small and its CI remains fast.

### Alternatives considered

| Approach | Benefits | Costs / risks | Decision |
|---|---|---|---|
| A. Keep fixed pins | Reproducible installs and simple validation | Stale skills until manifest edits/release; does not satisfy latest-on-setup preference | Rejected by user |
| B. Resolve latest stable during setup and write a local receipt | Fresh setup; per-machine differences are explicit; recoverable when paired with restore | Network and upstream availability affect setup; resolution and rollback add state/error paths | **Selected and approved** |
| C. Always track a mutable default branch | Simplest upstream selector | Non-reproducible and weak integrity evidence; prerelease/unreviewed code risk | Rejected |

### Locked mode

- **Mode:** REDUCTION.
- **Included:** implement the already-approved latest-stable resolution, local resolved-version receipt, explicit restore/uninstall, trusted-source/stable-version/integrity checks, private permissions for ordinary backups, short README ownership, and full-SHA pinning for GitHub Actions with reviewed automated updates.
- **Excluded:** automatic PR labeling (user chose to remove it to keep CI/CD small), Graphify, new host smoke suites, CI matrices/jobs, new platform integrations, telemetry, automatic backup cleanup, atomic two-manifest bumping, and redesign of the GitHub ruleset.
- **Deferred:** atomic host-manifest bump; GitHub ruleset requiring a PR; automatic backup deletion. These deferrals carry the risks recorded below.

## Phase 2 — review sections

### 1. Architecture and system diagram

```text
Codex marketplace (main) ─┐
                          ├─> Grounded host plugin ─> grounded/setup/manage.py
Claude clone (main) ──────┘                          ├─ resolve official latest stable
                                                     ├─ validate + record version/SHA/integrity
                                                     ├─ conflict scan + private backups
                                                     ├─ install/update managed skills and rules
                                                     ├─ installed receipt + doctor
                                                     └─ restore/uninstall managed state

PR / push to main ─> one validate job (13 unit tests + repository check)
tag ─> release verification/package ─> GitHub Release ZIP
```

The current system separates host delivery from external skills installation and has a single setup manager. That is a good boundary. The selected dynamic resolver and receipt/restore behavior belongs in the existing source-manifest + manager + state/doctor path, not a second manager. Setup currently consumes exact manifest pins; adding “latest” requires a clearly defined resolver contract and a receipt before any host mutation. It must reject missing, prerelease, malformed, or untrusted candidates before touching installed files.

The happy path is documented above. Missing source metadata, an empty release list, or an upstream/API failure must abort before host changes. A valid candidate should produce a durable local receipt before installation. A mid-install failure should restore the old managed state and report any failed recovery with plugin/file and backup path. Existing backups make file recovery possible; previous dependency-version recovery is not currently implemented. No database migration or service scaling surface exists. At 10×/100× repo growth, the likely first pressure is maintenance/readability of long skill instructions and their strict size caps, not runtime load. GitHub and upstream registries are external single points of failure during setup/update.

**Rollback posture:** restore the saved prior managed state using the approved restore command; preserve user-edited files and backup data. Until that command and version receipt exist, the practical recovery is manual backup restoration or reinstalling a previously known source, with no guaranteed dependency pin to select.

### 2. Error and rescue map

| Failure surface | Current behavior/evidence | Required behavior | Status |
|---|---|---|---|
| Upstream latest metadata unavailable or invalid | Current manager validates fixed pins; selected resolver is not implemented | Abort before host mutation; identify source and reason | Open implementation requirement |
| Candidate install fails partway | Manager attempts rollback; outer conflict cleanup reports failures | Return actionable status and affected plugin/file plus backup path | User accepted requirement; not implemented |
| Native plugin disable/remove fails during conflict migration | Inner cleanup uses `check=False` and does not report restore-command failures | Surface incomplete restore and exact recovery path | User accepted correction; not implemented |
| Backup cannot be created/restored | Some outer rollback errors are surfaced; no user-facing restore command exists | Fail visibly; do not claim successful recovery | Restore/uninstall work required |
| Release manifest bump fails between files | Codex manifest may be updated while Claude manifest remains old | CI detects mismatch; atomic write deferred and residual risk accepted | Deferred |

### 3. Security and threat model

| Actor / asset | Threat | Required mitigation | Review status |
|---|---|---|---|
| Compromised/untrusted upstream release; installed skills and rules | Setup installs malicious or unintended prerelease content | Resolve only official manifest upstreams; stable releases only; record exact Git SHA / npm version and integrity before host mutation; abort on invalid metadata | Required by user; not implemented |
| Local user or another process; backups/configuration | Backup contents may include user instructions or plugin configuration readable under permissive umask | Owner-only permissions on ordinary backup dirs/files; do not auto-delete; document location/content/manual cleanup | Accepted; not implemented/documented fully |
| GitHub Actions dependency update | Mutable action tags can move | Pin actions to full commit SHAs; update through reviewed automated PRs | Accepted; not yet applied |

No payment, health, or customer PII flow was found. Local backups can contain personal configuration/instructions and should be treated as sensitive. Do not log tokens or full secret-bearing config in resolver/restore diagnostics.

### 4. Data-flow and interaction edge cases

| Edge case | Expected behavior | Tested now? | Risk if untested |
|---|---|---:|---|
| No release/version metadata | Abort before host changes | No dynamic resolver exists | Partial/incorrect installs if fail-open |
| Prerelease or default-branch candidate | Reject | No | Unreviewed code installation |
| Candidate changes between lookup and fetch | Fetch exact resolved commit/version and verify receipt | No | Installed bytes differ from recorded candidate |
| Two setup invocations overlap | Existing lock serializes setup; second invocation cannot mutate concurrently | Existing implementation inspected, tests not run | Lock failure/retry UX remains unverified |
| Duplicate/retried setup | Idempotent installation; preserve prior receipt/backup correctly | Partial unit coverage only | Backup churn or wrong prior version |
| Failure after some host files change | Restore previous managed state; report partial recovery | No end-to-end setup tests | User left in mixed install state |
| User edits a managed file before restore/uninstall | Preserve edited content; do not silently overwrite/delete | Not implemented | User work loss |
| Backup accumulation | Keep backups; tell user where and how to clean manually | Partial docs | Disk growth; silent auto-clean would risk data loss |
| One manifest bump write succeeds, second fails | CI detects mismatch; local partial update risk accepted | Existing check path inspected | Brief inconsistent checkout |

### 5. Code quality and reuse

The repository already has cohesive modules: `manage.py` for setup/state, `release.py` for version/release work, a single source manifest, and focused tests. Reuse these. Do not introduce a second setup router or generalized plugin framework. The install flow currently has filesystem rollback and an installed-state record, but lacks version-level restore/uninstall. `validate_repo()` enforces exact Git and npm pins, which conflicts with the approved dynamic latest policy and must be revised together with docs/state/doctor—not merely loosened in one validator. `release.py` writes the Codex and Claude manifests sequentially; atomic update was explicitly deferred. README detail is duplicated at the root and under `grounded/`; the root should be quick-start and `grounded/README.md` the canonical detailed guide.

The CEO skill is 5,988 bytes under a 6,000-byte limit (12 bytes headroom); ENG is 5,964 bytes and ADR 5,576. Development rules are 6,317 bytes under a 6,500-byte limit. This is a maintenance constraint, not a reason to drop required behavior; prefer deduplication/progressive disclosure if later additions approach caps.

### 6. Test coverage and ambition

```text
Path / contract                         Existing test evidence     Missing / decision
──────────────────────────────────────  ─────────────────────────  ─────────────────────────────
Configure and release helpers           13 unit tests exist        Not run in this review
Repository/source manifest validation   validate workflow calls    Dynamic latest/stable rules
                                         manage.py check            not yet present
Setup lock and install/rollback          Manager code inspected     No end-to-end host setup test
Native conflict migration                Backup/rollback code       No failure-injection coverage
Restore/uninstall                         No command exists          Entire path to implement
Release workflow                          Package/check steps         Not executed in this review
```

The user explicitly does not want CI/CD or testing to consume excessive time. Keep one validation workflow/job and the current 13 tests; do not add separate jobs, a matrix, network-dependent checks, host smoke, E2E, or automatic PR-label workflow. Any essential checks for the approved installation behavior should be fast, focused unit cases inside the existing suite, and should replace or consolidate redundant checks where possible rather than expand the suite by default. The user selected the existing 13-test baseline in this review, so no additional cases are authorized by this note. This leaves high-impact setup/restore paths without added automated coverage; that risk remains explicit. Measured locally on 2026-11-05: the 13-test command passed in 0.42 s wall time (test runner reported 0.017 s), and `manage.py check` passed in 0.03 s. These are local command times, not GitHub runner durations.

### 7. Performance

There is no request-time service or hot path. Grounded’s shipped skills total about 132 KB; the shared development rules file is about 6.3 KB. Actual model-token cost was not measured. The new latest-version lookup adds network work only to setup/update; its latency is unknown and depends on official upstreams. Do not add caching or parallelism without measured need. Automatic label classification is out of scope.

### 8. Observability and debuggability

Current local setup output, doctor checks, `installed.json` hashes, and repository validation provide a reasonable baseline. No telemetry is needed. The future receipt should identify timestamp, upstream, resolved version, exact Git SHA or npm version, integrity/checksum, and backup/previous version. Restore failures must name the affected plugin/file and backup path. Current setup has no explicit restore/uninstall command, so recovery is not discoverable or reliably repeatable.

### 9. Deployment, rollout, and rollback

The current release workflow verifies the tag is on `main`, runs the same 13 tests and repository check, packages a ZIP, and creates a GitHub Release. Four recent successful GitHub release runs (2026-10-15 to 2026-10-16) took 8–12 seconds end to end; the release job itself ran for 5–9 seconds. After the selected change, the local proposal has two workflows total: one validation workflow and this release workflow; no PR-label workflow. The validation workflow is not yet on the remote default branch, so its GitHub runner duration is unknown. `gh release create` supports combining authored notes with generated release notes per the [official CLI documentation](https://cli.github.com/manual/gh_release_create). Codex marketplace source follows `main`; Claude currently uses a clone and `git pull`; publishing a ZIP/release does not itself update either running host.

Remote ruleset inspection found one active ruleset protecting `main` from deletion and force-push and requiring the `validate` check, but it does not require a pull request. The user chose to keep it as-is and accept that PR workflow is guidance rather than remotely enforced policy. Full-SHA action pinning remains accepted but unimplemented. Preserve user-edited files and backups through rollback/uninstall. Do not auto-delete backups; document their exact paths and manual cleanup.

### 10. Long-term trajectory

The package is small enough for an owner-maintained, portable setup tool. The approved dynamic version policy shifts the tradeoff from reproducibility to freshness; the local receipt and explicit restore are necessary to make that choice diagnosable and reversible. Per-machine differences are accepted. The primary long-term risks are upstream API/release drift, ambiguous meaning of “stable,” missing restore coverage, and skill instruction size caps. Keep the stable-channel definition explicit and treat missing/inconsistent upstream metadata as a hard failure. Automatic backup cleanup, Graphify, new platforms, and broader CI are not justified by current evidence.

### 11. Design / UX

**Skipped: `DESIGN_SCOPE=false`.** No user-facing UI or visual design changes are in scope. CLI output and setup documentation are reviewed under error handling, observability, and rollout instead.

## Phase 3 — follow-up triggers

### OpenSpec requirements/design/tasks to update when implementation begins

No active OpenSpec change exists. Create or extend one before implementing the approved cross-system behavior: latest stable resolution, source trust/integrity rules, local version receipt, recovery/restore/uninstall semantics, protection of edited files, and private backup permissions. OpenSpec should own requirements, design, and tasks; do not create a parallel plan document.

### ADR candidates

No ADR is required by this review. Keep the “latest stable per setup, per-machine variation allowed, local receipt plus explicit restore” decision in the implementation OpenSpec unless it becomes a lasting policy shared across multiple tools/repos. If that broader policy emerges, record one ADR then. Atomic two-manifest writes remain explicitly deferred.

### Review-only observations

- Fast CI is a project constraint: one job, 13 existing tests, no matrix/network/host E2E. Locally, tests took 0.42 s wall and repository check 0.03 s; recent GitHub release runs took 8–12 s end to end. Do not add tests beyond the user's accepted baseline without revisiting that decision.
- Current remote ruleset does not require PRs; this is accepted.
- Backups remain until a user manually cleans them; document location and contents.
- Automatic PR labeling is removed from scope to avoid another workflow; manual labeling remains available.
- Do not claim latest-version resolution, restore/uninstall, or action SHA pinning is implemented until changed and verified.

## Phase 4 — verdict

Verdict: REVISE

- **Approval source:** after the REVISE recommendation, the user directed continuation (“다음은?”); this was treated as authorization to prepare the OpenSpec planning artifacts only. It does not approve implementation or an APPROVE verdict.
- **Reason:** the approved direction is materially different from the current implementation. The current source manifest and manager still pin dependency versions; there is no resolved-version receipt, restore, or uninstall command; the agreed source-security checks, ordinary-backup permissions, action SHA pins, and README consolidation are not complete. These are blocking gaps for declaring the repository ready, though they are an actionable and bounded implementation scope.
- **Deferred risks accepted:** atomic manifest bump, no PR-required ruleset, current 13-test baseline without host smoke/E2E, and manual backup cleanup.
- **Next permitted action:** the single OpenSpec change is prepared. Review its requirements/design/tasks before implementation; no implementation or engineering review is started by this CEO review.
- **Implementation verification:** none; this is a repository review, not a claim that changes work.
