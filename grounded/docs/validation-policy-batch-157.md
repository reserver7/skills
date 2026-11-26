# Development policy validation: batch 157

This batch starts after batch 156’s code review found that “nontrivial work” did not clearly include high-risk behavior even when the patch was small.

- Final policy SHA-256: `dcc83cb700eac5f8843af5f6ff53a6fdb126aa568ecd91f792b184b5c4276e1f` (**11,856 bytes**; 144 bytes below the 12,000-byte setup limit).
- Rule delta: select `test-driven-development` for focused TDD when new behavior tests guide nontrivial work; define trust-boundary, destructive/persistent-data, concurrency/idempotency, external-side-effect, and rollback changes as nontrivial regardless of line count. A new deny/abort/no-side-effect case must assert the exact result and side effect on the baseline before implementation. Existing tests count only when they assert that exact path. Separate test-writing and test-running permissions still apply.
- Runtime: `gpt-6-luna`, medium reasoning; fresh ephemeral, disposable fixtures; host MCP disabled and disclosed. Both selected skill bodies matched the prepared fixture hashes; no resume or tool-argument errors.

| Work | Observed route and result | Assessment |
|---|---|---|
| Tenant authorization defect replay | Read debugging, security, TDD, and review skills. The newly added non-member denial test was run against baseline and failed with a successful signed-URL result. A first implementation attempt also failed because the helper parameter was not yet wired; after correction, all four focused tests passed and the diff was clean. No independent reviewer was available, and the agent disclosed that. | The revised rule changed behavior as intended: the exact security failure now has red evidence before the fix. The final helper and tests stayed narrowly scoped. |
| Low-risk duration formatter defect | Read `systematic-debugging` only. The pre-existing boundary test failed at 3600 seconds (`60:00` vs `1:00:00`); the minimal hour branch fixed it, and both tests passed. No new test, framework skill, or TDD body was added. | The high-risk TDD threshold did not expand to a small pure helper with an existing exact failing test. This is a useful countercheck against blanket skill use. |

Combined whole-session usage was **707,909 input** (634,752 cached), **4,210 output**, and **1,125 reasoning tokens**. These totals include host/session context; they cannot be assigned to skill reads or interpreted as measured savings.

Static checks: setup suite **36/36 passed** from `grounded/setup`; `git diff --check`, `py_compile`, and runner `--help` passed. One initial test invocation from the repository root failed to import `test_manage`; rerunning from its actual `grounded/setup` directory passed. The policy remains below the configured byte ceiling. No external skill body, production project, release, or Git history was changed.

The finite evidence in batches 155–157 covers React/Supabase, backend authorization and pure logic, CI/progressive rollout, UI audit, and PM ticket drafting. The latest code-focused runs show appropriate selection or a justified stop, with the security TDD gap corrected and counterchecked. They do not establish perfection across all skills, hosts, or projects. JEV returned no assessment in the previous attempts, so this batch records direct runtime evidence only.
