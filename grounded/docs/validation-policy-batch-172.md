# Development policy validation: batch 172

This fresh fixture tests an approved, low-complexity public API bug fix where the user explicitly requested Superpowers.

- Policy: `b0cf95bd8e22991fb8fe897ec06a8200edd9037f741bd6c739012c50380ff71c` (**13,562 bytes**).
- Runtime: `gpt-6-luna`, medium reasoning, isolated fixture. Each selected skill body matched its prepared hash.
- Scenario: duplicate `POST /bookmarks` throws a SQLite unique-constraint exception. The approved OpenSpec contract specifies `201` for the first insert, `200` with the existing record for a duplicate, no duplicate row, and propagation of unrelated integrity errors. No schema change, dependency, or unresolved decision.

| Area | Observed route and evidence |
|---|---|
| Skill selection | `using-superpowers` gated the explicit opt-in; `systematic-debugging` traced the existing defect; `test-driven-development` owned the requested test-first sequence; `api-and-interface-design` covered the externally visible response contract. The roles are distinct. No Ponytail, database, or security skill was indicated. `verification-before-completion` was not needed for this focused implementation. |
| Test-first evidence | Before the edit, the duplicate test was reported as **ERROR** because the handler's `sqlite3.IntegrityError` escaped; the distinct-URL test passed. This reproduced the actual defect but did not meet the TDD skill's explicit requirement for a behavioral test failure rather than a test error. |
| Implementation | The handler caught only the duplicate-key conflict, returned the stored row with status 200, and propagated unrelated integrity errors. New-resource status 201 remained intact. The unrelated-error regression test was added; no schema, dependency, or unrelated files changed. |
| Final checks | Focused suite: **3/3 passed**. Full fixture suite: **3/3 passed**. `git diff --check` passed. OpenSpec tasks were marked complete based on the fixture evidence. |

### Assessment and limits

The skill combination was proportional and the result matched the approved contract in the SQLite fixture. The test error is recorded as a TDD procedure deviation, not as a missing skill trigger: the source TDD instructions already distinguish a test assertion failure from an error. Batch 173 adds a Grounded reminder to make that distinction explicit. No production HTTP server, concurrent request, or service database was exercised.

The session reported **639,623 input tokens** (**604,544 cached**), **3,897 output tokens**, and **1,680 reasoning tokens**. These whole-session totals cannot be attributed to individual skills.
