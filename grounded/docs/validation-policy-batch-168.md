# Development policy validation: batch 168

This batch covers read-only React/OpenSpec/Superpowers review and read-only CI plus progressive-deployment review. It also replays two routing/reporting misses found in those scenarios after narrow policy clarifications.

- Starting policy: `96c9b77c0d7c4895eb8364033145141d6558312e574573d819b65505722d0727` (**12,883 bytes**).
- Final policy: `4cf73757d1f2bddc9b0cee9a56772ae90ff3bf7f2eb19b4d535c16b34995a752` (**13,152 bytes**, below the 14,000-byte Setup ceiling).
- Runtime: `gpt-6-luna`, medium reasoning, four fresh isolated sessions. All skill copies read by the final runs matched their prepared hashes. The CI runs used host Context7; no `ctx_resume` calls occurred.

| Scenario | Observed route | Verification and assessment |
|---|---|---|
| Approved React filter review; OpenSpec + Superpowers | The initial run read `using-superpowers`, `requesting-code-review`, and `vercel-react-best-practices`; only the first two appeared in its final skill list. It correctly left accessibility review out of scope. | The existing Node tests passed 2/2 but exercised only the pure helper. Review found the approved trimmed-query behavior missing and correctly left component typing/Clear interactions unverified. A replay after clarifying reporting listed all three skills and their distinct roles. Neither run changed files. The UI interaction tasks remain incomplete. |
| Approved CI canary rollout review; OpenSpec, no Superpowers | Initial route selected `ci-cd-and-automation`, `deployment-patterns`, and `requesting-code-review`, but missed `security-and-hardening` despite reviewing `id-token: write` and production credential scope. A first clarification explicitly named OIDC/CI permissions but still missed the security skill. After clarifying that security review also applies to existing trust boundaries, the replay read and reported all four distinct roles. | Both runs used Context7's exact `/actions/checkout/v4.2.2` docs. The final run confirmed `persist-credentials: false` against the exact official v4.2.2 sources. Review found unsafe 100% promotion before health checks, no real metrics gate or rollback, no test prerequisite, and an unusable provider call. No project tests existed. The OpenSpec tasks remained unchecked; GitHub Actions, protected-environment settings, provider, metrics, and rollback were not integration-tested. No files were changed. |

### Policy changes

The CI route required the security-specialist cue to explicitly cover existing authentication boundaries, including OIDC/workload identity, CI token grants, and production credentials. This is a role cue, not a fixed CI skill bundle: CI mechanics, rollout strategy, security analysis, and review procedure were separate concerns in this fixture.

The React review read the framework specialist but omitted it from the requested final skill list. The policy now requires complete, role-specific skill accounting when the user asks which skills were used, while allowing the report to say a read skill yielded no actionable guidance. The final React replay listed the gate, review procedure, and React specialist separately.

Together with batch 167's structured-input rule, this batch adds no default Superpowers, Ponytail, or completion-verification calls. It tests explicit review paths, avoids tests where none exist or edits are forbidden, and reports runtime boundaries instead of treating source inspection as integration evidence.

### Runtime cost and limits

The four fresh runtime sessions reported **1,196,906 input tokens** (**1,024,640 cached**), **11,350 output tokens**, and **3,484 reasoning tokens**. These are whole-session totals including host and conversation context, not skill-attributable costs. The final CI replay used 488,448 input / 436,864 cached / 4,363 output tokens; the final React replay used 200,188 input / 176,768 cached / 2,179 output tokens. The scenarios are representative checks, not proof that all React or CI/rollout routes are correct.

### Final checks

The Grounded Setup suite passed **48/48** under Python 3.13. `manage.py check` and `git diff --check` passed. No upstream skill body was modified.
