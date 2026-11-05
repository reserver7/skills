# Development policy

Follow explicit user instructions and the current project's constraints. Choose the lightest complete workflow; classify from the request and relevant code, without loading a routing skill or calling Jev.

## One owner per job

- Clear local bug: use systematic-debugging, reproduce it, add/run a focused regression, make the smallest fix, verify. No SDD without material requirements/design uncertainty.
- Typo/style fix: edit and verify only; skip SDD, broad tests, reviews and Jev.
- Clear work spanning several parts: state scope and acceptance checks in chat, then implement. No separate plan file.
- New behavior with material uncertainty, cross-system contracts, authorization, or persistent-data changes: use OpenSpec when requirements/design need agreement. File count is not the criterion. An OpenSpec directory alone never requires SDD.
- Reuse an active change if the request belongs to it. Keep existing specs accurate when behavior changes. Escalate the workflow if investigation reveals material uncertainty; explain why.
- If plausible interpretations change user-visible behavior, data or APIs, ask one blocker and wait; never assume a default. Sandbox/tool limits do not decide it. Use OpenSpec for durable agreement. Jev compares options only when requested/enabled; it cannot replace the user's decision.
- For unresolved requirements/design/contracts in review or implementation, name OpenSpec and the active change (or say a new one is needed), ask only blockers, and stop. Do not approve/implement through the gap or create a parallel plan. Resume from agreed artifacts.
- OpenSpec owns SDD requirements, design, tasks, validation and archive; `tasks.md` is the only plan. Follow its installed workflow; don't duplicate PRD/design/planning docs.

## Implementation

- Apply Ponytail to coding: reuse existing code, make the smallest complete change, preserve validation/error handling, avoid speculative abstractions. Load `ponytail` once when useful; never also activate its lifecycle hook/plugin or duplicate its full prompt here.
- For bugs use `systematic-debugging`; use `test-driven-development` for nontrivial changes when authorized. For side-effect/dedup changes, test retries and preserve behavior; ask when the contract trades lost retryable work against duplicate effects. For expiring idempotency state, check reclamation and atomic concurrent check-and-record. Honor test limits, report unrun checks and never claim they pass; prose edits need no TDD.
- For interface/data refactors, map caller assumptions and observable behavior first; preserve it or get approval to change. Test authorship and execution are separate permissions. When allowed, write characterization/regression tests for decision-critical contracts and failing tests first for other nontrivial changes. If testing is prohibited/deferred, state the constraint, unverified checks and risk.
- Use `verification-before-completion` before asserting success. Report actual evidence and checks not run. Use `receiving-code-review` when acting on review feedback.
- Implement from chat or the OpenSpec task. Do not use Superpowers planning/brainstorming/execution or subagent-development. Use worktrees only when the task needs isolation.
- Use `requesting-code-review` for substantial/risky work or when asked; skip trivial edits. Don't duplicate Ponytail or pre-implementation review; re-review only changed findings or behavior.

## Interactive questions

- Ask one decision at a time using the active host's schema. If unavailable or rejected, ask once in chat and wait; never repeat it or infer consent.

## Optional reviews and decisions

- `plan-review-ceo`: unresolved product premise, scope or meaningful alternatives before implementation. When invoked, run its full scope challenge and eleven-section review; do not substitute a quick checklist.
- `plan-review-eng`: important architecture, failure handling, security/data contracts, performance or test strategy before implementation. Run its full four-section review, coverage and execution-dependency analysis. Reuse settled CEO facts/decisions and examine technical detail/deltas; do not repeat the same interview or review completed code.
- Suggest optional reviews with a concrete reason; execute when requested/accepted. Never automatically chain scope review, engineering review, ADR and Jev. A direct request for a named review authorizes that review only.
- `adr`: record durable/cross-cutting or hard-to-reverse technical choices through its interview, three-perspective review and completeness gate. Keep feature-local choices in OpenSpec design or the existing project document. Link evidence instead of copying it.
- Jev is optional decision support, only when requested or explicitly enabled for this task. Use the available evaluate tool with focused facts, choices and criteria. No tool means disclose unavailability. Do not send secrets, repeat unchanged evaluations, treat probabilities as proof, or substitute evaluation for tests/approval. Configuration and credentials live outside Git.

## Context and completion

Read only the selected skill and relevant files. Use targeted searches for callers, contracts and applicable prior decisions; do not bulk-load all skills, specs or ADRs. Expand context when evidence requires it. Keep review output to actionable findings and unresolved decisions. Never trade required correctness/security checks for a token target.

The installed skills are a curated subset. Do not install/activate full overlapping plugins alongside them. User instructions outrank this policy; do not silently bypass contradictory project rules.

## Commit messages

When creating a commit, use Conventional Commits: `type(optional-scope): imperative summary`. Choose a specific type such as `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`, `ci`, `perf`, or `revert`; mark breaking changes with `!`.

For releases, follow the target repository's documented version/tag scheme. Synchronize canonical and host-specific manifests before tagging; reject a tag/version mismatch. Build from the tagged source. Publishing a GitHub Release does not by itself publish a provider marketplace update. For Grounded itself, use its bundled `setup/release.py` and repository release instructions.
