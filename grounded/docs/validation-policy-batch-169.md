# Development policy validation: batch 169

This batch checks three remaining boundaries against the current routing policy: explicit Superpowers opt-in while an OpenSpec decision blocks the code slice; sequential owner decisions; and exact-version source fallback when Context7 is unavailable.

- Starting policy: `4cf73757d1f2bddc9b0cee9a56772ae90ff3bf7f2eb19b4d535c16b34995a752` (**13,152 bytes**).
- Final policy: `36ca6fd752de65286c99a598b5a41bba57f544e6d5d4f56421a1f4e0b72da406` (**13,423 bytes**, below the 14,000-byte Setup ceiling).
- Runtime: `gpt-6-luna`, medium reasoning, six sessions. Five corrected/valid sessions are used as behavioral evidence; one initial blocked-change fixture had its `tasks.md` misplaced and is excluded from the conclusions. External skill copies in valid scenarios matched their prepared hashes.

| Scenario | Observed route | Verification and assessment |
|---|---|---|
| Pending retention decision + explicit Superpowers/TDD + independent README typo | No skill was loaded for the blocked retention slice or standalone typo. No retention code, tests, or decision records changed; only the independent README typo was fixed. | Correctly deferred Superpowers, TDD, and all tests until Legal and the data owner record the retention duration and delete/archive choice. The final request names the required owners and record. This confirms blocker scoping with an explicit workflow opt-in. |
| Sequential Product then conditional Legal decisions + explicit Superpowers/TDD | The first two runs loaded no skills or tests and made no edits, but their final handoff also requested the downstream Legal decision. After the policy clarified that the closing request may name only the first owner decision, the replay asked only for the Product owner's scope decision and will reassess Legal approval after the user's response. | The final replay obeyed the sequence and did not treat the engineer's proposed defaults as authorization. The earlier two handoffs exposed a gap in how the rule was applied, even though a general one-question rule already existed. |
| Pinned `actions/checkout@v4.2.2` review with Context7 disabled | Selected `requesting-code-review`, `security-and-hardening`, and `ci-cd-and-automation`. No rollout skill was added because no progressive deployment was in scope. | The session had no Context7 MCP. It used official sources from the exact v4.2.2 tag (`action.yml`, README, and implementation) and found that `persist-credentials: true` violates the approved requirement. It correctly reported no project tests, made no edits, and left runtime Git configuration/post-job cleanup unverified. |

### Rule change

The final policy makes a sequential blocker handoff operational: when decisions are ordered or conditional, ask only the first authorized owner decision; the closing request must name only that decision; reassess downstream approval after the user responds. This is general dependency sequencing, not a retention/export-specific recipe.

No routing change was needed for the explicit Superpowers blocker or exact-source fallback: both followed the current rules. The one malformed fixture attempt is retained in the session cost below but not counted as valid scenario evidence.

### Runtime cost and limits

The six sessions reported **1,085,978 input tokens** (**924,928 cached**), **6,921 output tokens**, and **1,521 reasoning tokens**. These are whole-session totals, including host and conversation context, not skill-attributable costs. The sequential-decision replay under the final policy cost 112,683 input / 91,264 cached / 644 output tokens. The source fallback review did not execute the GitHub workflow and cannot establish actual runner token cleanup or environment protection.

### Final checks

The Grounded Setup suite passed **48/48** under Python 3.13. `manage.py check` and `git diff --check` passed. No upstream skill body was modified.
