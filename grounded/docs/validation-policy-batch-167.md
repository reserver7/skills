# Development policy validation: batch 167

This batch adds a code-heavy public API combination and a focused replay of a validation gap found in that implementation. The replay tests the updated general rule for structured input formats, without opting into Superpowers.

- Starting policy: `78e2c62c7b4fc25cf4cf683dbbe52e22fb6385a9bee515bf937d91c552aab7d2` (**12,737 bytes**).
- Final policy: `96c9b77c0d7c4895eb8364033145141d6558312e574573d819b65505722d0727` (**12,883 bytes**, below the 14,000-byte setup ceiling).
- Runtime: `gpt-6-luna`, medium reasoning, two fresh isolated fixtures. All selected external skill copies matched their prepared hashes. No `ctx_resume` calls occurred.

| Scenario | Observed skill route | Verification and assessment |
|---|---|---|
| Approved account-scoped cursor API; OpenSpec + explicitly selected Superpowers | `using-superpowers`, `test-driven-development`, `api-and-interface-design`, `security-and-hardening`, and `requesting-code-review`. Each matched fixture copy was read. No Ponytail or completion-verification skill. | Existing focused suite failed before implementation and passed 4/4 after. It checked principal-derived account scope, stable exclusive paging, limit validation, and a malformed cursor with no repository call. The route was appropriate for the new public contract, Superpowers TDD, and trust boundary. Self-review was disclosed as non-independent. HTTP routing and a real repository/backend were absent and correctly reported unverified. |
| Recheck after review found a cursor-validation gap; OpenSpec, no Superpowers | `systematic-debugging`, `test-driven-development`, `security-and-hardening`, and `requesting-code-review`. The public contract did not change, so API design and Superpowers were not repeated. | A new regression for `not-a-time~e1` failed before the fix although the delimiter shape looked valid. The agent added ISO timestamp parsing and an impossible-date regression; the focused suite passed 6/6, including rejection before repository access. It reported that HTTP/repository integration remained unverified and disclosed the separate, non-independent review. |

### Rule change

The first implementation had a malformed-cursor test, but only for a missing delimiter. It accepted a syntactically shaped cursor with an invalid timestamp and queried the repository. The current policy now requires checks for both malformed structure and plausible structure with invalid field values, and rejection before side effects. This generalizes to parsers and structured inputs rather than encoding cursor-specific cases. A policy regression test was added.

The affected behavior was replayed against the updated policy: a shape-valid but semantically invalid cursor failed first, and was then rejected before repository access. The rule now distinguishes procedure selection from evidence quality: a correct skill combination still needs tests that exercise the actual accepted format, malformed values, and side effects. No new trigger forces extra skills; the second run reused only the roles needed for the defect.

### Runtime cost and limits

The two fresh runtime sessions reported **1,501,400 input tokens** (**1,381,760 cached**), **12,217 output tokens**, and **6,111 reasoning tokens**. These are whole-session totals including host and conversation context, not skill-attributable costs. This pair demonstrates one public API implementation and one focused regression replay; it does not establish routing for all API, frontend, CI, or deployment tasks.

### Final checks

The Grounded Setup suite passed **46/46** under Python 3.13. `manage.py check` and `git diff --check` passed. No upstream skill body was modified.
