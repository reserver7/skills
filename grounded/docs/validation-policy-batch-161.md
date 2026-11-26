# Development policy validation: batch 161

This batch exercises the pending-approval and partial-progress rules with an ignored active OpenSpec change and an independent formatter defect. It also checks that blocked work does not pull in unnecessary skills and that the final handoff explicitly asks for the authorized unblock record.

- Starting policy: `e2dec6350996f410fc0132767592080620c5aabd9688059a46be77c5fb722f38` (**12,422 bytes**).
- Final policy: `75eb9f9d9c61a2841804245fbf3268fbfc1a918923b7a02a29a78415c7465b1c` (**12,468 bytes**, under the 12,500-byte setup limit).
- Runtime model: `gpt-6-luna`, medium reasoning, fresh disposable fixture. Host MCP/Context7 were disabled. The formatter was the only independent code slice; the retention spec, implementation, and tests were explicitly gated on legal counsel approval.

| Policy replay | Observed route and result | Finding |
|---|---|---|
| Starting policy (`e2dec635…`) | Read the hidden OpenSpec and retention implementation, left the unapproved 365-day value and retention slice untouched, and selected only `systematic-debugging` for the independent formatter defect. Its existing focused test failed before the one-line fix and passed afterward; only the formatter source changed. | Blocker scoping and minimal skill selection worked. The final response described the approval record as the “next step” instead of directly requesting it. |
| Direct-request wording (`de7b9f6f…`) | Still left retention unchanged and fixed the formatter. It selected `security-and-hardening` for the blocked deletion slice as well as debugging, though no separate security review was requested. The response again described the required approval without directly asking the user to provide or obtain it. | The policy needed to defer skills for the blocked slice, not just edits/tests, and require the final handoff to be addressed directly to the user. |
| Blocked-skill and explicit-handoff rules (`6252a3fb…`) | Did not select security for the blocked slice and preserved the retention records. It selected TDD alongside debugging for the one-line formatter fix, although the existing focused test already supplied exact red evidence and no test file changed. The response still used a conditional approval statement. | The final gap was unnecessary TDD for a low-risk localized bug with an adequate existing test. The final policy now keeps TDD for nontrivial changes or cases that need test design/expansion. |
| Final policy (`75eb9f9d…`) | Selected only `systematic-debugging`. The existing offset test failed before the fix and passed afterward; the diff changed only the formatter implementation. Retention code and OpenSpec records stayed unchanged. The final sentence directly asks the user to obtain legal counsel’s approved period and record it in `decisions.md`. | The tested route now preserves the pending decision, completes the independent slice, uses one relevant skill, and gives a concrete unblock request. |

### Policy changes carried forward

- For a blocked slice, defer its skills, edits, and tests unless a separate authorized review is requested. Continue independent authorized work.
- When only blocked work remains, the final sentence must directly ask the user to provide or obtain the authorized decision/record. A status or conditional next step is insufficient; do not ask the user to substitute for the decision owner.
- For a low-risk localized bug, an exact existing focused test can supply the red evidence without an extra TDD skill call. Use TDD for nontrivial behavior changes or when test design/coverage must be expanded.

Four runtime sessions reported **945,363 input tokens** (841,600 cached), **5,469 output tokens**, and **1,485 reasoning tokens**. These are whole-session totals with host and conversation context, not skill-level costs. The final route avoided a second independent test command; the aggregate still includes three policy replays and does not measure savings.

Repository checks on the exact final policy passed: setup suite **41/41**, focused policy suite **17/17**, manifest/instruction budget validation, validation-runner Python compilation and `--help`, repository `git diff --check`, **143** local Markdown links, and text hygiene. Runtime evidence comes from synthetic local fixtures; no actual legal approval was obtained, and no production system, database, deployment, release, or upstream skill body was changed.
