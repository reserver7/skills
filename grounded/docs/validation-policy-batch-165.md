# Development policy validation: batch 165

This batch checks verification choices across a minimal direct fix using Ponytail, a pending-decision OpenSpec with an independent typo fix, and an approved OpenSpec implementation using an explicitly selected Superpowers TDD workflow.

- Starting policy: `3dfed5e5590d9f7f894e621d274b0c63b53cad18d436b5ac439d6331af312236` (**12,517 bytes**).
- Final policy: `3951838be467f958a053dcc6bbe8232d1450bd662559ec1933f191852c10117e` (**12,603 bytes**, below the 14,000-byte setup ceiling).
- Runtime: `gpt-6-luna`, medium reasoning, fresh isolated read-only/write-enabled fixtures as requested. External skills were read from fixture copies matching their prepared hashes; no host `ctx_resume` calls occurred.

| Scenario | Skill route and verification | Assessment |
|---|---|---|
| Existing whitespace bug; user explicitly requested Ponytail | Selected `ponytail` and `systematic-debugging`. Ran the exact existing test before editing (failure for internal whitespace) and after a one-line implementation (pass). Preserved case and signature; only `label.py` changed. No TDD or VBC call. | Appropriate: debugging located the existing defect, Ponytail kept the fix small, and the exact focused test supplied sufficient red/green evidence for this localized change. |
| OpenSpec retention change pending legal and data-owner approval, plus independent README typo | Selected no skill. Read the active OpenSpec gate, changed only the unrelated README typo, left retention code/tests/decision records untouched, and directly requested both authorized approvals. No tests ran for the blocked retention slice. | Appropriate: OpenSpec remained the decision authority; the blocked slice had no unnecessary security/TDD/VBC calls; the independent copy fix was inspected by diff. |
| Approved OpenSpec queue feature with explicit Superpowers TDD request, first run | Selected `test-driven-development` and correctly performed the red/green change, preserved the public return behavior, and updated OpenSpec tasks. It did not read `using-superpowers`, despite the explicit Superpowers opt-in. | Miss: the Grounded policy required opt-in but did not name the Superpowers entry gate. |
| Same approved OpenSpec/Superpowers fixture after the policy update | Selected and read both `using-superpowers` and `test-driven-development`; the focused suite failed for the expected duplicate and passed 2/2 afterward. Preserved order and `None` return; updated supported OpenSpec tasks. Did not add Ponytail or VBC. | The explicit workflow gate and its task-specific procedure now both run; the OpenSpec remains the contract source, and TDD supplies the behavioral verification. |

### Policy change

The policy now says that Superpowers is opt-in, and when selected, `using-superpowers` is the gate before only the matching task-specific procedure/support skills. Default Grounded work does not load that gate. This closes the one runtime miss without making Superpowers or Ponytail a mandatory bundle.

### Cost and limits

The four runtime sessions reported **1,141,910 input tokens** (**1,031,040 cached**), **6,799 output tokens**, and **1,277 reasoning tokens**. These whole-session totals include host and conversation context and cannot be attributed to skills. The Superpowers replay was repeated only after its gateway rule changed. This small cohort does not prove routing for every skill or every task; it directly tests the three requested workflow paths and one affected replay.

### Final checks

The setup suite passed **44/44**, including the new Superpowers-gate policy test. `manage.py check` and `git diff --check` passed; the current policy is 12,603 bytes.
