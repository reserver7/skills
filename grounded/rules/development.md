# Development policy

Follow user and project instructions. Use the lightest complete workflow. Skip routing skills and automatic Jev.

## One owner per job

Pick one primary skill per job. Add another only for a distinct deliverable or check.

- Clear local bug: use systematic-debugging, reproduce it, add/run a focused regression, make the smallest fix, verify. No SDD without material requirements/design uncertainty.
- Typo/style fix: edit and verify only; skip SDD, broad tests, reviews and Jev.
- Multi-part clear work: state scope and acceptance in chat; no separate plan file.
- Library/SDK/API/CLI/cloud docs: use Context7. Resolve the ID, then query by version and topic. Keep private data out of queries. If unavailable, use official upstream docs and say so.
- API/interface contract: use Addy `api-and-interface-design` only for API boundary, versioning, error, or compatibility decisions; OpenSpec remains the owner when behavior must be agreed and traced.
- Performance work: establish a baseline and target, then use Addy `performance-optimization` for a focused investigation; claims require before/after measurements.
- Trust-boundary changes: use Addy `security-and-hardening` for targeted defensive review.
- Observability: use Addy `observability-and-instrumentation` when adding or improving logs, metrics, traces, or alerts. For an active incident, use systematic debugging and the project's runbook.
- Database changes: use ECC `database-migrations` for nontrivial schema/data migration planning and `mysql-patterns` only when the target is MySQL. Keep Postgres/Supabase on its existing specialist; use engine-native checks for other databases.
- CI/CD: Addy `ci-cd-and-automation` by default. Add ECC `deployment-patterns` only for canary/blue-green/rolling rollout, automated abort/rollback gates, or coordinated migrations; ENG only for material release/data/security/test risk.
- New behavior with material uncertainty, cross-system contracts, authorization, or persistent-data changes: use OpenSpec when requirements/design need agreement. File count is not the criterion. An OpenSpec directory alone never requires SDD.
- Reuse an active change if the request belongs to it. Keep existing specs accurate when behavior changes. Escalate the workflow if investigation reveals material uncertainty; explain why.
- If plausible interpretations change behavior, data, or APIs, ask one blocker and wait. Never assume a default or let tool limits decide. Use OpenSpec for durable agreement; Jev compares only when requested and never replaces the user's choice.
- For unresolved requirements, design or contracts, name OpenSpec and the active or needed change. Ask the blocker and stop. Resume review or implementation from agreed artifacts without creating a parallel plan.
- For OpenSpec changes, its specs, design, and `tasks.md` own requirements and execution. Follow its validation and archive workflow. Avoid duplicate PRDs or plans.

## Implementation

- Use Ponytail for coding: reuse code, make the smallest complete change, preserve validation/error handling, and avoid speculative abstractions. Load `ponytail` once when useful; skip its hooks/plugin and duplicated prompt.
- Debug with `systematic-debugging`. Use TDD for nontrivial authorized changes; prove the intended failure and reuse an existing test that catches it. Preserve caller behavior and test retries, expiry reclamation, and atomic concurrency for side-effect/dedup changes. Honor test limits; report unrun checks and risks.
- Before interface/data refactors, map caller assumptions and observable behavior; preserve them or get approval. Test authorship and execution are separate permissions. When allowed, add characterization/regression tests for critical contracts. Prose edits need no TDD.
- Before claiming success, use `verification-before-completion`. Reuse passing checks run after the last relevant change if they meet completion criteria. Rerun affected checks after changes. Report evidence and omissions. Use `receiving-code-review` for review feedback.
- Default to chat or OpenSpec. Use Superpowers planning/execution only on request. Record the active plan on handoff. Require explicit subagent approval. Use worktrees only for needed isolation.
- Use `requesting-code-review` for substantial/risky work or on request. Skip trivial edits and duplicate reviews. Re-review changed findings or behavior only.

## Interactive questions

- Ask one decision at a time using the active host's schema. If unavailable or rejected, ask once in chat and wait; never repeat it or infer consent.

## Optional reviews and decisions

- `plan-review-ceo`: for unsettled premise/scope; run its complete scope challenge, alternatives and eleven-section review.
- `plan-review-eng`: for material technical risk; run its complete four-section review, coverage and dependency analysis. Reuse CEO decisions and review only technical deltas.
- Suggest reviews with a concrete reason; execute only when requested/accepted. Never auto-chain CEO, ENG, ADR and Jev. A named request authorizes that review only.
- `adr`: record durable/cross-cutting or hard-to-reverse choices using its full interview, three perspectives and completeness gate. Feature-local choices stay in OpenSpec design. Link evidence; do not copy it.
- Jev is optional and used only when requested/enabled. Send focused facts/options/criteria, never secrets; do not repeat unchanged evaluations or treat scores as proof, tests or approval. Disclose tool unavailability. Keep credentials outside Git.

## Context and completion

Read relevant files, callers, contracts and prior decisions. Keep reviews actionable and preserve required correctness/security checks.

The installed skills are a curated subset. Do not install/activate full overlapping plugins alongside them. User instructions outrank this policy; do not silently bypass contradictory project rules.

## Commit messages

Use Conventional Commits (`feat|fix|docs|refactor|test|chore|build|ci|perf|revert`), imperative summary, and `!` for breaking changes.

For releases, follow the target repository's documented version/tag scheme. Synchronize canonical and host-specific manifests before tagging; reject a tag/version mismatch. Build from the tagged source. Publishing a GitHub Release does not by itself publish a provider marketplace update. For Grounded itself, use its bundled `setup/release.py` and repository release instructions.
