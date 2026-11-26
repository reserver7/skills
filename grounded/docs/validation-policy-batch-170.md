# Development policy validation: batch 170

This batch tests a high-risk backend bug-fix route under the unchanged policy from batch 169.

- Policy: `36ca6fd752de65286c99a598b5a41bba57f544e6d5d4f56421a1f4e0b72da406` (**13,423 bytes**).
- Runtime: `gpt-6-luna`, medium reasoning, one fresh isolated fixture. The four selected skill copies matched their prepared hashes.

| Scenario | Observed route | Verification and assessment |
|---|---|---|
| Existing cross-tenant profile-cache leak, direct fix without OpenSpec or Superpowers opt-in | `systematic-debugging`, `security-and-hardening`, `test-driven-development`, and `requesting-code-review`. No Ponytail, OpenSpec, API-design, Superpowers, or completion-verification call. | The owner-then-other-tenant regression reproduced a real leak before the edit. The smallest fix tenant-scoped the cache key while preserving the public signature; the full fixture file passed 3/3 after. The agent separately reviewed the cache-hit path and disclosed that review was not independent. The in-memory test did not verify a real database or concurrent runtime. |

### Assessment

This is a case where combining skills was justified: defect tracing, tenant-boundary security, test-first evidence, and diff review were separate responsibilities. Ponytail's minimal-diff role added no distinct value to the specialist-directed one-line key change; Superpowers was not selected by the user; the API contract did not change. This cohort produced no new routing-policy gap, so the Grounded rules were not changed.

### Runtime cost and limits

The session reported **429,367 input tokens** (**376,704 cached**), **1,897 output tokens**, and **291 reasoning tokens**. These whole-session totals include host and conversation context and cannot be attributed to individual skills. The fixture contained one focused Python test file; it did not represent a live multi-tenant service or production cache.

### Final checks

The focused fixture suite passed **3/3**, and `git diff --check` passed. The policy hash matches batch 169, so its Setup suite result remains applicable. No upstream skill body or repository code was modified.
