# Development policy validation from batch 151

Policy SHA-256: `bfcc6c126b57415924468c1345db90b596c8c925f8f1e737456d1fe8942a50d7`. Prior evidence: [initial batch 150](validation-policy-batch-150.md). This revision clarified earliest-decision questions, interaction evidence, and distinct security/review roles.

All three scenario replays used gpt-6-luna / medium and generated instruction SHA-256 `44b6412ad64cf33ac61dcf302a2b4d6e4725357a67e006e15c7b979c7c5a81f7`. Host configuration was enabled only for fixture 118. No unauthorized edits or tests occurred in the blocked deletion case. All diffs passed `git diff --check`.

| Fixture | Replay result | Input (cached), output, reasoning |
|---|---|---|
| 116, pending permanent deletion | No skills, edits, tests, or decision-record changes. The response explained the approval gate but did not directly ask for or request the authorized decision record. This exposed one remaining gap in the stop response. | 121,052 (106,240), 928, 118 |
| 118, React product filter | React and TDD bodies visible; Context7 quota was exhausted and official docs used. Added a description-match test, but all four tests still used server-rendered initial props; no input event was exercised or reported as unverified. One fresh-session `ctx_resume` call recurred. An independent browser check was run separately below. | 490,926 (436,864), 3,378, 1,378 |
| 121, approved user-scoped API | API design, security, TDD, and requesting-code-review bodies visible. Tests failed before implementation and passed 4/4 afterward. The agent performed a separate self-review and explicitly disclosed that no independent review occurred because delegation was prohibited. Route, docs, and OpenSpec tasks were updated. | 831,542 (775,680), 4,701, 1,274 |

## Independent interaction check

To check the filter independently of the agent's SSR tests, the replayed `product-filter.js` was mounted in Playwright Chromium using React/React DOM `19.3.0` from the exact-version CDN. Filling the labeled input with `interior` rendered only “Red mug” and changed the live count to “1 result”; whitespace restored all three items in source order; a nonmatching query rendered “0 results”, the empty state, and no list items. The only browser console error was a missing favicon request from the temporary test harness. This confirms the tested event behavior, while the agent's own test/report still omitted event-level evidence.

Across the three scenario sessions: **1,443,520 input tokens** (1,318,784 cached), **9,007 output**, and **2,770 reasoning**. These are whole-session totals, not per-skill costs. The remaining deletion response was addressed by a final wording clarification in the next policy fingerprint; no additional rule changes were needed for the API review result. The filter implementation passed independent interaction evidence, so the repeated omission is recorded without adding another scenario-specific rule.
