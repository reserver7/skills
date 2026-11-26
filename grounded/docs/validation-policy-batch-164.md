# Development policy validation: batch 164

This batch addresses evidence that `verification-before-completion` could be routed for nearly every explicit validation request. Batch 153 had already recorded redundant completion-verification calls alongside code review and CI/rollout guidance. The old phrase “explicit verification/acceptance audit request” did not distinguish an acceptance audit from running requested tests or validating skill routing.

- Starting development policy: `60e1b0323ee508f74afa41a414f197d7b1a73733f2c41b043018c6970cc4dd35` (**12,441 bytes**).
- Final development policy: `3dfed5e5590d9f7f894e621d274b0c63b53cad18d436b5ac439d6331af312236` (**12,517 bytes**, within the 14,000-byte setup ceiling).
- Setup policy ceiling remains **14,000 bytes**; final policy headroom is **1,483 bytes**.
- Runtime model: `gpt-6-luna`, medium reasoning, disposable read-only fixture; host MCP disabled.

| Evidence | Result | Assessment |
|---|---|---|
| Policy regression test, red | The revised test first failed because the active policy did not contain the narrower acceptance-audit trigger or the explicit routing-validation exclusion. | Confirmed the test detects the wording gap. |
| Policy regression test, green | The test passed after narrowing the trigger and stating that focused checks, scenario tests, and skill-routing validation use relevant project/domain checks without automatically invoking this skill. | The rule now distinguishes a requested work check from a requirement-by-requirement acceptance audit. |
| Runtime focused-test request | The agent read the fixture instructions and ran `python3.13 -m unittest test_basic.py -v` (1/1 passed). It selected **no skill**, made no changes, and did not call `verification-before-completion`. | Confirms ordinary read-only test requests do not trigger a generic final skill. Runtime route was observed on the final policy; the previous policy was not replayed against this exact prompt. |

The policy retains `verification-before-completion` for a requested requirement-by-requirement acceptance audit, before commits/PRs, and delegated implementation. It also retains the rule against adding it solely to duplicate a material code review. No positive-trigger runtime replay was needed because those triggers were not changed.

The runtime session reported **73,386 input tokens** (58,240 cached), **284 output tokens**, and **0 reasoning tokens**. These are whole-session figures, not the cost of an individual skill. No external skill body or application code was changed.

### Final checks

The focused routing-policy test passed after its expected red result. The Grounded setup suite passed **43/43**, the manifest/policy check passed, **153** local Markdown links were valid, and `git diff --check` passed. The current policy is 12,517 bytes with SHA-256 `3dfed5e5590d9f7f894e621d274b0c63b53cad18d436b5ac439d6331af312236`.

### Limits

This single runtime case covers an ordinary read-only focused test request. It does not prove routing across every task, host, skill, or model; explicit acceptance audits, commits/PRs, and delegated implementation were not replayed in this batch.
