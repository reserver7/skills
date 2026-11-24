# Development policy

Follow user/project rules. Use the lightest workflow. Skip route skills and auto Jev.

## Skill selection

Before compound edits/scope changes, check deliverables/risks. Load one skill per distinct need, reuse it, skip catalog scans, name missing skills/fallbacks.

- Clear bug: use the bug-fix procedure below; add no SDD unless requirements/design are materially uncertain.
- Typo/style fix: edit and verify only; skip SDD, broad tests, reviews and Jev.
- Multi-part work: agree scope/acceptance in chat; no plan file.
- Version-sensitive edits/reviews/recommendations: before acting, resolve/query Context7 for pinned version/topic. SDK/API/CLI/cloud pins and CI tags count; keep private data out. If exact pin is unindexed, inspect its official release/tag or package artifact; nearest-version docs don't prove it. If unavailable, disclose the gap; don't claim verified.
- API contracts (incl. compatible extensions): use Addy `api-and-interface-design`. Use OpenSpec for unresolved behavior.
- Docs: use `doc-updater` for substantive updates/release notes, `docs-governance` for requested audits.
- Performance: set baseline/target, then use Addy `performance-optimization`; claims need before/after measurements.
- React/Next framework behavior changes: load Vercel `vercel-react-best-practices` for hooks/effects, rendering, data/routing/caching, or server/client boundaries. Skip typo/copy/docs and non-framework edits. Add `vercel-composition-patterns` for component API changes; Context7 for versioned APIs. `frontend-design` handles visual UI.
- UI/accessibility review-only requests: always load `web-design-guidelines` before assessing; don't load `frontend-design` or edit files unless requested.
- Auth, tenant access, trust boundaries or untrusted-input handling: use Addy `security-and-hardening`.
- Review feedback: use `receiving-code-review` before edits. Use `systematic-debugging` for an existing defect, failing test, or unexplained behavior, not merely a planned behavior change.
- MCP server changes: use `mcp-builder`. Supabase work: use `supabase`.
- Observability changes: use Addy `observability-and-instrumentation`; incidents use debugging and the runbook.
- Database changes: use ECC `database-migrations` for nontrivial schema/data migration planning and `mysql-patterns` only when the target is MySQL. Load the Postgres specialist before Postgres SQL changes.
- CI/CD: Addy `ci-cd-and-automation` by default. Add ECC `deployment-patterns` for canary/blue-green/rolling rollout, automated abort/rollback gates, or coordinated migrations; ENG only for material release/data/security/test risk.
- Use OpenSpec when requirements/design need agreement for materially uncertain behavior, cross-system contracts, authorization, or persistent data; file count is irrelevant. An OpenSpec directory alone does not require SDD.
- For contract, authorization, or persistent data work, inspect relevant active OpenSpec files directly, including ignored files. Reuse the active change and keep specs current.
- Pending approval or unresolved behavior/data/contract/risk/rollback choices: ask once; wait before dependent edits/tests. Legal/regulatory needs authorized approval or formal waiver. Resume from agreed artifacts.
- Read relevant OpenSpec specs, design, and `tasks.md` before changes. Follow its validation/archive workflow without duplicate PRDs or plans.

## Implementation

- Ponytail is optional for direct edits, including bugs; skip it when Superpowers directs the edit. Keep scope minimal and validate.
- Bug fixes: `systematic-debugging` owns reproduction/diagnosis. Check test-writing and execution permission separately. Use TDD for authorized nontrivial changes only if both are allowed. Reuse or add a focused test if allowed; prove the behavior fails before fixing. Preserve caller behavior; cover retries, expiry reclamation and atomic concurrency for side-effect/dedup changes. Report skipped checks.
- Before interface/data refactors, map callers and observable behavior; preserve them or get approval. Test writing and execution have separate permissions; add contract tests only when allowed. Prose needs no TDD.
- Before claiming success, use `verification-before-completion`; check deliverables/risks once, reuse valid evidence, rerun affected checks, and report omissions.
- Prefer chat/OpenSpec; Superpowers is opt-in. If a route stalls, explain the gap and ask before switching. Preserve handoff/one active plan; subagents need approval; use worktrees only when needed.
- Use `requesting-code-review` for substantial/risky work or on request. Alongside Addy, review distinct concerns only and merge duplicate findings. Skip trivial reviews; re-review changed findings only.

## Interactive questions

- Ask one decision at a time using the active host's schema. If unavailable or rejected, ask once in chat and wait; never repeat it or infer consent.

## Optional reviews and decisions

- `plan-review-ceo`: unsettled premise/scope; run its full scope challenge and alternatives.
- `plan-review-eng`: material technical risk; run its full review and dependency analysis. Reuse CEO decisions.
- Suggest reviews with a concrete reason; execute only when requested/accepted. Never auto-chain CEO, ENG, ADR and Jev. A named request authorizes that review only.
- `adr`: record durable/cross-cutting or hard-to-reverse choices using its full interview, three perspectives and completeness gate. Feature-local choices stay in OpenSpec design. Link evidence; do not copy it.
- Jev is optional; use only when enabled/authorized for concrete choices. Send facts/options/criteria, never secrets. Jev advises; user decides. Avoid repeat evaluations; disclose unavailability and keep credentials outside Git.

## Context and completion

Read relevant code/contracts and prior decisions; preserve correctness/security checks.

The installed skills are a curated subset. Do not install/activate full overlapping plugins alongside them. User instructions outrank this policy; do not silently bypass contradictory project rules.

## Commit messages

Use Conventional Commits (`feat|fix|docs|refactor|test|chore|build|ci|perf|revert`), imperative summary, and `!` for breaking changes.

For releases, follow the repository's version/tag scheme. Sync manifests before tagging; reject mismatches and build from the tag. GitHub Release doesn't publish a marketplace update. For Grounded, use `setup/release.py` and its instructions.
