# Development policy validation: batch 173

This batch tests Superpowers opt-in on a private deterministic Python bug fix, with no OpenSpec change, public interface, persistent data, auth, or external service. The same retry-backoff fixture was run before and after targeted rule updates; these are replays, not independent scenarios.

| Run | Policy | Skills read | Result |
|---|---|---|---|
| Initial | `b0cf95bd8e22991fb8fe897ec06a8200edd9037f741bd6c739012c50380ff71c` (13,562 bytes) | `using-superpowers`, `systematic-debugging`, `test-driven-development`, `verification-before-completion` | Assertion red step and implementation checks passed. The completion-verification skill was an unnecessary additional final check: no acceptance audit, commit/PR, or delegated implementation was requested. Test-generated `__pycache__` files remained in the final diff and were omitted from the report. |
| Replay 1 | `edf780123d4b661d66bd574b4acd9227f75fb715df13d1cbb82ece62c85bb8f2` (13,794 bytes) | `using-superpowers`, `systematic-debugging` | TDD was skipped because the low-risk local bug had an exact existing focused test; completion verification was also skipped. The final diff still contained bytecode caches that the report omitted. |
| Final replay | `39a6c2dd8e5ebd7f3986fc07f9f6d6874bc4077b4d780c5b2371a6b50d4a111c` (**13,924 bytes**) | `using-superpowers`, `systematic-debugging`, `test-driven-development` | The prompt explicitly required an assertion-failure red step, so TDD was relevant. It was not duplicated with another workflow. No `verification-before-completion` was loaded. The assertion failures were reproduced before editing; after the fix, focused and full suites each passed **2/2**. The only changed file was `retry_policy.py`; no generated cache remained. |

### Rule updates and assessment

- Made explicit that TDD's red step must be a test assertion failure about missing behavior, not a test error or setup failure; correct the test/harness before implementation.
- Made explicit that test execution or an imminent completion report alone does not trigger `verification-before-completion`; do not call it unless a listed trigger applies.
- Required inspecting the worktree diff after test/tool runs, removing out-of-scope generated artifacts, and reporting all remaining changed files.
- Added focused policy assertions. They failed before the rule updates and passed after. The external skill bodies were not modified.
- Current policy is **13,924 bytes** against Setup's **14,000-byte** limit. Setup's full suite passed **49/49**; `manage.py check` passed.

The final run also encountered an unavailable `python` command and switched to Python 3; a default unittest discovery found no tests, so the agent used `-s tests`, which found and passed the fixture suite. This fallback was reported. The scenario only verifies a local helper and synthetic tests, not runtime integration.

### Runtime cost

Across all four sessions, reported totals were **1,681,812 input tokens** (**1,542,016 cached**), **10,232 output tokens**, and **3,541 reasoning tokens**. These whole-session totals include host and conversation context and cannot be assigned to individual skills. The replays closed two concrete execution gaps; further validation should prefer new coverage over repeating unchanged scenarios.
