# Development policy validation from batch 144

Policy SHA-256: `96d4e579cb9ca0f126dc53d66635ed1561d409c0169fbf397a60b2e201decc16`. Previous evidence: [batches 134–143](validation-policy-batch-134.md).

## Batch 144

A local smoke check distinguished path mention, read attempt, and visible body in three sample command logs. Replayed fixture 119 with gpt-6-luna / medium and isolated host configuration. Generated instructions SHA-256: `ae50feee0b5547e460a3fa37068600bdcb8121b571cb263b99a91ecbd683e20f`.

Compared with batch 135, the agent opened the managed skill files and preserved the decorative icon. React, composition, TDD, and frontend-design bodies were visible. Frontend-design had no distinct role for this non-redesign. Focused tests passed 3/3, but the compact CSS class was removed and no regression case covered it. Only Card and SettingsPanel changed. Diff whitespace passed. No context resume or argument error was recorded.

Whole-session tokens: 342,550 input (314,752 cached), 2,925 output, 696 reasoning.

## Batch 145

Replayed fixtures 120 and 116 with gpt-6-luna / medium and isolated host configuration. Both used generated instructions SHA-256 `ae50feee0b5547e460a3fa37068600bdcb8121b571cb263b99a91ecbd683e20f`. Both produced empty diffs and ran no tests. No tool argument errors or context resumes were recorded.

| Fixture | Observation | Input (cached), output, reasoning |
|---|---|---|
| Pending cursor boundary | Asked one inclusive/exclusive question and stopped. API design and security skill bodies were visible before approval. | 133,967 (108,928), 1,042, 452 |
| Pending permanent deletion | Stopped without choosing a default. The first request bundled written approval with retention and deletion scope. Security, systematic debugging, and TDD bodies were visible before the approval was resolved. | 182,846 (157,824), 2,185, 1,186 |

## Batch 146

Replayed approved API fixture 121 with the same instructions hash, model, and isolated host configuration. API design, security and TDD bodies were visible. The doc-updater path appeared in a search but its body was not read. The expanded five-test suite failed before the route edit and passed 5/5 afterward. Only the v2 route, focused tests, API documentation, and OpenSpec task list changed. The agent completed the task list, preserved the tracked v1 files, and did not report the independent-review limitation. Diff whitespace passed. No tool argument error or context resume was recorded.

Whole-session tokens: 717,566 input (666,112 cached), 4,572 output, 1,150 reasoning. The latest evidence classifier separated the doc-updater path mention from the three visible skill bodies.

## Batch 147

Replayed Card fixture 119 with gpt-6-luna / medium and isolated host configuration. Instructions SHA-256: `ae50feee0b5547e460a3fa37068600bdcb8121b571cb263b99a91ecbd683e20f`.

React implementation, component composition, and TDD skill bodies were visible. No frontend-design read was recorded, improving on batch 144. Three focused tests passed. The icon remained, but the compact class was again removed and no regression case covered it. Only Card and SettingsPanel changed. Diff whitespace passed. No context resume or argument errors were recorded.

Whole-session tokens: 442,471 input (383,104 cached), 2,230 output, 749 reasoning.

## Batch 148

Replayed product filter fixture 118 with the same instructions hash and model, with host configuration enabled. React implementation and TDD skill bodies were visible. The original static suite failed before implementation and passed 3/3 afterward. Only the filter component changed. No input event and resulting state were tested, and the final report did not disclose this gap. Context7 quota failure was recorded and the agent reported official React sources as fallback. One fresh-session context resume was recorded. Diff whitespace passed.

Whole-session tokens: 452,210 input (422,016 cached), 2,814 output, 870 reasoning.

## Batch 149

Replayed approved catalog retry fixture 113 with explicit Superpowers TDD, gpt-6-luna / medium and isolated host configuration. Instructions SHA-256: `ae50feee0b5547e460a3fa37068600bdcb8121b571cb263b99a91ecbd683e20f`.

TDD and using-superpowers bodies were visible. The original focused tests failed before implementation and passed afterward. The new HTTP-date case expected 1,000 ms against a 2,000 ms cap, but was added after implementation and had no targeted pre-edit failure. The test date string also gives Thursday for a date that falls on Friday, which the runtime accepted. Focused and full runs repeated the same four passing cases. The existing two-argument caller stayed compatible and OpenSpec tasks were marked complete. Diff whitespace passed, with no context resume recorded.

Whole-session tokens: 461,087 input (427,904 cached), 4,053 output, 1,828 reasoning.
