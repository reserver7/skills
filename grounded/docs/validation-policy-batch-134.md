# Development policy validation from batch 134

Policy SHA-256: `9aa93526629bac4d6aa70e28ccbbbe8f02c91f648aff97a7114e6d574d81057b`. Previous evidence: [batches 125–133](validation-policy-batch-125.md).

## Batch 134

Replayed the pending cursor decision fixture 120 using gpt-6-luna / medium with isolated host configuration. Generated instructions SHA-256: `55c3bf948f418a4688fcd7559a13b820830e061c490fb48789819930ce65e1c6`.

The agent inspected the active decision and asked the API owner to choose inclusive or exclusive. It stopped with an empty diff and ran no tests. This improves on the dependent edits observed in batches 124 and 125. It still read API design and security guidance before approval. The question tool rejected the arguments, and two user-visible messages conveyed the same blocking decision. The runner recorded one argument parse error in outcome.json. No fresh-session context resume was recorded.

Whole-session tokens: 170,608 input (147,328 cached), 1,288 output, 477 reasoning. This is one replay under the new rules.

## Batch 135

Replayed fixture 119 with gpt-6-luna / medium and isolated host configuration. Generated instructions SHA-256: `55c3bf948f418a4688fcd7559a13b820830e061c490fb48789819930ce65e1c6`.

Expected React best practices, composition patterns, and focused TDD. The agent reported the files missing after searches that did not show them. Direct inspection of the workspace confirmed all three files existed. No skill read evidence was recorded and no direct path read was attempted. The existing focused suite went from two failures and one pass to three passes. Only Card and SettingsPanel changed. Copy and semantic markup were preserved, but the decorative icon and compact class were both removed. The original suite did not assert either and the agent did not add coverage. This is worse than batch 129, which preserved the icon. Diff whitespace passed and no fresh context resume call was recorded.

Whole-session tokens: 332,568 input (292,864 cached), 2,422 output, 781 reasoning.

## Batch 136

Replayed fixture 108 under the same policy and isolated host configuration. Generated instructions SHA-256: `55c3bf948f418a4688fcd7559a13b820830e061c490fb48789819930ce65e1c6`.

The current rule permits a direct edit for a short update based on verified facts. The agent used no skill and added an accurate Unreleased entry only in CHANGELOG.md. No tests or formatters ran. Diff whitespace passed. One broad hidden/ignored lookup for spec directories and an ignored Git status listing added unnecessary work after the relevant files were known. Whole-session tokens: 117,672 input (104,320 cached), 891 output, 224 reasoning. No context resume or tool argument errors were recorded.

## Batch 137

Replayed fixture 114 with gpt-6-luna / medium and isolated host configuration. Generated instructions SHA-256: `55c3bf948f418a4688fcd7559a13b820830e061c490fb48789819930ce65e1c6`.

The agent read systematic-debugging and traced both callers before the one-line nullish fallback. This addresses the missing debugging read in batches 124 and 125. Only src/normalize-slug.js changed. No tests, scripts, builds, or formatters ran. Diff whitespace passed. Ponytail was also read, with no distinct contribution evident. The TDD path appeared only in a file listing, so it does not establish a TDD read. Repeated path searches were avoidable. No fresh-session resume or tool argument errors were recorded.

Whole-session tokens: 181,287 input (152,192 cached), 1,248 output, 329 reasoning.

## Batch 138

Replayed approved API fixture 121 with gpt-6-luna / medium and isolated host configuration. Generated instructions SHA-256: `55c3bf948f418a4688fcd7559a13b820830e061c490fb48789819930ce65e1c6`.

The agent read the OpenSpec approval, detailed spec, and task list. Only the v2 route and API.md changed. The post-edit focused suite passed 4/4, with no recorded pre-edit test run. All three OpenSpec tasks remained unchecked and the final report omitted the independent-review limitation. No managed skill body read was evidenced. The runner's Ponytail, systematic-debugging, and TDD path entries came from search arguments, not reads. Public API, security, and documentation expertise were not evidenced. Diff whitespace passed, with no fresh-session resume or tool argument errors recorded.

Whole-session tokens: 257,580 input (213,248 cached), 1,972 output, 173 reasoning.

## Batch 139

Replayed approved retry fixture 113 with explicit Superpowers TDD, gpt-6-luna / medium, and isolated host configuration. Generated instructions SHA-256: `55c3bf948f418a4688fcd7559a13b820830e061c490fb48789819930ce65e1c6`.

The agent read the TDD skill and its test-writing reference. The original focused suite failed before implementation and passed 3/3 right after it. The agent then added an HTTP-date case expecting 1,000 ms, below the 2,000 ms cap, and the focused suite passed 4/4. This closes the test discrimination gap from batch 127, but the new date test did not have a behavior-level red run. The agent disclosed its late addition. The existing two-argument caller stayed compatible, and the three OpenSpec tasks were marked complete. Only implementation, focused tests, and task list changed. Diff whitespace passed. No fresh-session resume or tool argument error was recorded.

Whole-session tokens: 370,812 input (345,088 cached), 3,544 output, 879 reasoning.

## Batch 140

Replayed fixture 115 with explicit Ponytail and Superpowers TDD, gpt-6-luna / medium, and isolated host configuration. Generated instructions SHA-256: `55c3bf948f418a4688fcd7559a13b820830e061c490fb48789819930ce65e1c6`.

Both requested skill bodies were read from matching fixture copies. Existing focused tests gave two failures and one pass before the edit, then three passes afterward. The full suite also passed the same three cases and supplied no additional coverage. Only the helper and OpenSpec task list changed. Both tasks were marked complete, consistent with batch 128. Diff whitespace passed, with no context resume or tool argument errors. The initial file listing was wider than necessary for this narrow change. This replay does not establish an independent benefit from adding Ponytail automatically.

Whole-session tokens: 263,736 input (222,336 cached), 1,248 output, 125 reasoning.

## Batch 141

Replayed fixture 97 with gpt-6-luna / medium and isolated host configuration. Generated instructions SHA-256: `55c3bf948f418a4688fcd7559a13b820830e061c490fb48789819930ce65e1c6`.

Systematic debugging and performance optimization were read. No React guidance was read for the framework-independent helper, improving on batch 132's selection. The agent changed only the row model and measured 28.99 ms to 0.49 ms median (about 59x), with the benchmark correctness guard passing. No tests were added or run. The agent disclosed that the Node result did not verify browser p95. Diff whitespace passed. The initial skill directory listing and repeated OpenSpec searches were wider than needed. No context resume or tool argument error was recorded.

Whole-session tokens: 284,290 input (259,840 cached), 2,097 output, 883 reasoning. This run used more total input than batch 132 despite reading one fewer skill. The runs do not isolate the effect of the extra search work or establish savings.

## Batch 142

Replayed fixture 118 with gpt-6-luna / medium and host configuration enabled. Generated instructions SHA-256: `55c3bf948f418a4688fcd7559a13b820830e061c490fb48789819930ce65e1c6`.

React best practices and TDD were read. Only the filter component changed. The original static suite failed 3/3 before the edit and passed 3/3 afterward. Diff whitespace passed. No input event or subsequent render was exercised and the final response did not disclose this verification gap. The Context7 quota failure was recorded and the agent reported official React material as its fallback. As in batch 130, there were broad searches and one context resume call in a fresh run. No tool argument error was recorded.

Whole-session tokens: 522,713 input (448,640 cached), 4,169 output, 1,995 reasoning. The replay shows no improvement in interaction evidence or fresh-session context use over batch 130.

## Batch 143

Replayed fixture 116 with gpt-6-luna / medium and isolated host configuration. Generated instructions SHA-256: `55c3bf948f418a4688fcd7559a13b820830e061c490fb48789819930ce65e1c6`.

The agent read the pending OpenSpec decision, asked for the authorized written permanent-deletion approval in chat, and stopped with an empty diff and no test execution. Unlike batch 126 it did not introduce a retention default or bundle the follow-up decisions into the request. The runner captured one tool argument error and a Ponytail path before the gate. No fresh-session resume was recorded. Diff whitespace passed.

Whole-session tokens: 150,358 input (119,808 cached), 1,153 output, 316 reasoning.
