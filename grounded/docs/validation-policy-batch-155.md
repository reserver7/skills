# Development policy validation: batch 155

This five-run cohort tested code-heavy integrated engineering choices against policy `0214d804ce0f49b72d0f399c65180e615ae7e64ad87c64c8089812449d553cd0` (11,304 bytes; 12,000-byte setup limit). Runtime: `gpt-6-luna`, medium reasoning, fresh ephemeral Codex runs, disposable fixtures, host MCP disabled. Each run had zero `ctx_resume` calls and zero tool-argument errors.

| Work | Observed route and result | Finding |
|---|---|---|
| React + Supabase workspace events | Read `security-and-hardening`, `systematic-debugging`, `test-driven-development`, and `vercel-react-best-practices`; omitted the required `supabase` specialist. It treated the expected red test for an absent feature as a debugging issue and proceeded using current docs without exact pinned-package evidence. Two focused tests passed and the fixture diff was clean. | Material execution failure: specialist ownership and exact-version stop gate were not followed. This motivated stricter pre-work cue reconciliation and separating expected-red from existing-bug debugging. |
| Read-only Orders UI accessibility audit | `web-design-guidelines` only; source findings were distinguished from browser/runtime checks. No edits or tests. | Appropriate narrow selection. |
| Approved `/v2/alerts` ticket draft | `to-tickets`, `api-and-interface-design`, and `security-and-hardening`; read-only draft. It added data-source, response allowlist, and pagination test criteria relative to the earlier ticket-only route. | Distinct expertise improved security-heavy acceptance criteria, but whole-session input rose from 107,623 to 180,581 tokens. These totals do not establish that the extra skills caused the increase. Do not generalize into a default bundle. |
| Next.js tenant authorization defect | `systematic-debugging`, `security-and-hardening`, TDD, and `requesting-code-review`; focused tests passed 4/4 and diff was clean. The review was a separate self-review, not independent. | Appropriate for an existing authorization defect and material trust boundary. |
| CI plus progressive production rollout | `ci-cd-and-automation`, `deployment-patterns`, TDD, and `requesting-code-review`; focused tests passed 8/8 and diff was clean. No live deployment. Exact Node documentation was used; the missing build script was disclosed. | The CI and rollout roles were distinct and justified; no debugging or completion-verification duplication. |

Combined whole-session usage was **2,376,538 input** (2,133,760 cached), **19,641 output**, and **7,539 reasoning tokens**. These figures include host/session context and cannot be assigned to Grounded or individual skills. External skill bodies were not modified; fixture edits stayed in temporary copies.

The following rule revision and targeted replays are recorded separately in [batch 156](validation-policy-batch-156.md). No release, commit, or push was made.
