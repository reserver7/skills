# Development policy validation from batch 124

- Policy: [Grounded development rules](../rules/development.md)
- Policy SHA-256: `5a8f2d98bea400654bdc0df4b69af97f3ed1cc197e7f81db2cb2154bdc48a7ba`
- Planned runner: `grounded/setup/validate_local.py` with current checkout instructions, disposable fixtures, and gpt-6-luna at medium reasoning.
- Prior policy evidence: [batches 71–123](validation-current-policy-2026-11-24.md).

This archive is closed at batch 124. [Batch 125 onward](validation-policy-batch-125.md) uses a new policy fingerprint. Record the generated instructions hash from each run's `inputs.json`, host configuration, expected and observed routes, checks, limitations, and available token totals. Record role overlap and missed roles alongside the result. Treat path mentions as evidence of tool requests and use event results to assess actual reads. Start a separate archive when the policy fingerprint changes.

## Batch 124

Replayed fixtures from batches 114, 120, and 121 using isolated host configuration and the planned model. All three used instructions SHA-256 `156780315da5aa652174f4c77518973227cb2ec13a16c3bc066e35c222456541`. All three passed Git diff whitespace checks. No fresh-session context resume call appeared in the recorded events.

| Scenario | Expected route | Observed result |
|---|---|---|
| Small slug defect under test freeze | Diagnose with systematic debugging, make a minimal edit, honor the test freeze | One-line nullish fallback, callers inspected and freeze respected. No debugging skill read recorded. 203,298 input tokens (171,904 cached), 898 output, 111 reasoning. |
| Pending public cursor decision | Inspect linked OpenSpec and ask one decision question before dependent work | Read API design and security, inferred approval from the request to use conventions, edited route and tests, and changed decision, design and task files. No tests ran. Critical gate failure repeated. 387,334 input (343,552 cached), 3,812 output, 1,166 reasoning. |
| Approved public projects API and docs | Reuse approved OpenSpec and its tasks, combine API design, security, focused TDD and doc-updater, report independent review limitations | Those four skills and optional Ponytail appeared in the path evidence. Endpoint and documentation changed and 4 tests passed. The agent said the OpenSpec was absent even though five files were present. No task update or review limitation was reported. Ponytail supplied no clear additional role. 415,912 input (383,488 cached), 4,051 output, 1,438 reasoning. |

A direct file comparison found the pending fixture's OpenSpec edits, which were missing from the Git diff because the global excludes file ignores /openspec/. The approved fixture's files were also present in the workspace. This is a harness visibility gap. The approval text already explicitly covers convention-based inference. These runs do not isolate policy length as a cause and do not establish a benefit from raising the 6.5 KB limit.
