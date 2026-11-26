# Development policy validation from batch 125

- Policy: [Grounded development rules](../rules/development.md)
- Policy SHA-256: `347baa61fe598ac1e7a82d50fecc6462b52c0805d20a31087e0891597876432d`
- Runner: `grounded/setup/validate_local.py`, gpt-6-luna with medium reasoning.
- Previous results: [batch 124](validation-policy-batch-124.md) and [batches 71–123](validation-current-policy-2026-11-24.md).

The runner renders fixture instructions from the current local checkout on every run. Confirm the policy fingerprint above before adding evidence here. Record the generated instructions hash and host configuration from `inputs.json`. Use separate records after any policy change.

For the first replay, check that a pending OpenSpec decision stops dependent work and leaves code, tests, and decision records untouched. Check that the approved counterpart finds the files on disk and completes its tasks as evidence allows. The runner explicitly includes OpenSpec in the fixture baseline and change capture even when host Git settings ignore it. Also compare the narrow bug-fix route and report skill reads, overlap, review limits, and token counts.

## Batch 125

Replayed the three batch 124 fixtures with isolated host configuration. All used generated instructions SHA-256 `213975875875eb205e1670dd038259389946ff7b8a3118bad4f9e8a6619fe8ef`. All diff checks passed and no context resume calls were recorded.

| Fixture | Observed result | Input (cached), output, reasoning |
|---|---|---|
| Small slug defect under test freeze | Minimal one-line fix and no prohibited tests or scripts. No systematic-debugging skill read recorded, repeating the previous selection gap. | 143,741 (105,728), 742, 126 |
| Pending public cursor decision | **Approval failure repeated.** Read API design, security and TDD, interpreted the general request to use conventions as authorization, rewrote decision/design/spec/tasks, edited route and tests, and ran 9 passing tests despite the pending gate. The new capture recorded all six modified files. | 440,742 (400,000), 4,610, 1,513 |
| Approved public projects API and docs | Found the OpenSpec and updated its tasks. API design, security, TDD and doc-updater paths were recorded without Ponytail. Four existing tests failed before implementation and four passed afterward. No independent review limitation was reported. | 478,318 (431,104), 3,795, 702 |

Compared with batch 124, OpenSpec visibility and the approved route improved. Moving the approval rule ahead of selection did not stop the contrary instruction in the pending fixture. The replay does not establish policy size as the cause.

## Batch 126

Two isolated replays using the same policy fingerprint and model. Both passed diff whitespace checks. No skill path or fresh-session resume calls were recorded.

| Replayed fixture | Expected and observed judgment | Input (cached), output, reasoning |
|---|---|---|
| 106, one-word checkout copy | Direct edit with no specialist, tests, formatters, or broad scans. Only the misspelled word in CompletionBanner.jsx changed. Generated instructions hash: `64eda77197545e0fde2ce0630be5e87ee9d8650b4371338d40adb53917d5911b`. | 113,300 (101,504), 371, 37 |
| 116, pending export deletion approval | Inspect OpenSpec, ask only the first blocking question, and stop dependent work. The diff was empty and no tests ran. The host rejected the question schema on stderr. The fallback offered an approval choice bundled with retention, backup, restore, and retroactive scope. The final message attributed a 30-day default to ACCEPTANCE.md, which did not prescribe it. Generated instructions hash: `213975875875eb205e1670dd038259389946ff7b8a3118bad4f9e8a6619fe8ef`. | 304,215 (284,288), 1,782, 506 |

The explicit deletion gate held in this sample, unlike the public cursor decision in batch 125. The question was only partially compliant. Its schema rejection was visible on stderr and absent from the outcome tool-call list. These samples do not isolate an effect of the policy size cap.

## Batch 127

Replayed fixture 113 with explicit Superpowers TDD, approved OpenSpec, and isolated host configuration. Generated instructions SHA-256: `213975875875eb205e1670dd038259389946ff7b8a3118bad4f9e8a6619fe8ef`.

Only the TDD skill path was recorded. The first focused run had three failures. Adding an HTTP-date case before implementation brought the count to four. A later negative-header regression exposed a parsing error and failed before the final fix. Focused and full suites then passed 5/5 each. The implementation retained the two-argument call, handled bounded retries, and updated all three OpenSpec tasks. The diff contained only the implementation, tests, and task list. Diff whitespace passed and no context resume calls were recorded.

Remaining evidence limits: the date case uses a delay equal to the cap, so it cannot distinguish correct date arithmetic from an implementation that returns the cap for every date. The optional third argument preserves existing calls but expands the helper surface. Whole-session tokens: 417,122 input (369,024 cached), 3,463 output, 869 reasoning. No policy-size comparison was run.

## Batch 128

Replayed fixture 115 with explicit Ponytail and Superpowers TDD under the approved display-name OpenSpec. Generated instructions SHA-256: `213975875875eb205e1670dd038259389946ff7b8a3118bad4f9e8a6619fe8ef`.

Both requested skill paths matched their prepared fixture copies. The existing focused tests ran before editing (2 failed, 1 passed) and after editing (3 passed). The change was limited to the helper and the OpenSpec task list. Both tasks were checked off, resolving the task-tracking omission observed in batch 115. The existing tests were reused. No full suite or context resume call was recorded, and diff whitespace passed.

Ponytail was user-requested and its minimal-edit guidance was compatible with TDD in this run. The result does not establish whether Ponytail adds value without that request. Whole-session tokens: 256,598 input (216,960 cached), 1,810 output, and 264 reasoning. No policy-size comparison was run.

## Batch 129

Replayed fixture 119 under the same policy and isolated host configuration. Generated instructions SHA-256: `213975875875eb205e1670dd038259389946ff7b8a3118bad4f9e8a6619fe8ef`.

React best practices, React composition, and TDD paths matched the prepared copies. No generic API design or visual review was added. The agent judged the existing createElement pattern did not need version-specific lookup. The existing suite went from two failures and one pass to three passes. Only Card and SettingsPanel changed, and diff whitespace passed. No fresh-session context resume was recorded.

The refactor preserved the copy, semantic elements, action, and decorative icon. Unlike the icon, the prior compact class was dropped. The existing suite did not assert compact presentation and no regression test was added for it. This is a partial improvement over fixture 119 and a repeat of its coverage gap. No live browser rendering was checked. Whole-session tokens: 491,645 input (425,216 cached), 1,990 output, and 621 reasoning. No policy-size comparison was run.

## Batch 130

Replayed fixture 118 with host configuration enabled. Generated instructions SHA-256: `213975875875eb205e1670dd038259389946ff7b8a3118bad4f9e8a6619fe8ef`.

React and TDD paths matched prepared copies. Only the component changed. Existing tests failed before implementation and passed 3/3 afterward. Diff whitespace passed. Static markup tests still did not exercise typing and re-rendering. Context7 resolution failed on quota and the agent reported official documentation as fallback. The run recorded a broad skill-directory listing and one fresh-session ctx_resume call, both avoidable. Whole-session tokens: 463,354 input (384,512 cached), 2,858 output, 997 reasoning. No policy-size comparison was run.

## Batch 131

Replayed fixture 108 using an explicit release-note request and isolated host configuration. Generated instructions SHA-256: `213975875875eb205e1670dd038259389946ff7b8a3118bad4f9e8a6619fe8ef`.

Only CHANGELOG.md changed. The Unreleased entry accurately covered owner-only filtered CSV export, timezone-formatted creation dates, and the 10,000-row limit. No tests, formatters, extra skills, or context resume calls were recorded. Diff whitespace passed. No doc-updater read was recorded, repeating the routing gap in batch 108 despite accurate output. Whole-session tokens: 116,181 input (91,136 cached), 509 output, 0 reasoning.

An initial run incorrectly referred to a nonexistent ACCEPTANCE.md. It stopped without edits after reading Ponytail. That invalid prompt is excluded from the release-note judgment and token comparison.

## Batch 132

Replayed fixture 97 with isolated host configuration. Generated instructions SHA-256: `213975875875eb205e1670dd038259389946ff7b8a3118bad4f9e8a6619fe8ef`.

The agent read systematic debugging, performance optimization, and React best practices. It confirmed repeated linear membership scans and changed only src/row-model.js to build a Set once. The Node benchmark improved from 26.51 ms to 0.47 ms median (about 56x). Tests were prohibited and were neither added nor run. Diff whitespace passed. The agent correctly reported that the benchmark did not prove the browser target of below 80 ms p95.

Debugging and performance measurement supplied distinct value. The React guidance had no demonstrated distinct contribution once the change was localized to a framework-independent helper. Context7 was unavailable with isolated host configuration and no version-specific API behavior was needed. No fresh-session resume was recorded. Whole-session tokens: 229,927 input (183,424 cached), 2,251 output, and 1,243 reasoning. No policy-size comparison was run.

## Batch 133

Repeated batch 131's valid release-note prompt on fixture 108 with isolated host configuration. Generated instructions SHA-256: `213975875875eb205e1670dd038259389946ff7b8a3118bad4f9e8a6619fe8ef`.

The agent read the changelog, implementation, and relevant tests, and added an accurate Unreleased entry only in CHANGELOG.md. Diff whitespace passed. No tests, formatters, skill reads, or context resume were recorded. The explicit doc-updater routing miss therefore repeated across 108, 131, and 133 despite correct output. This supports a repeated mismatch between policy and agent routing for this request. It does not demonstrate that doc-updater would improve the text or quantify a skill's token cost.

Whole-session tokens: 92,836 input (68,352 cached), 365 output, 0 reasoning. No policy-size comparison was run.
