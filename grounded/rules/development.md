# Development policy

Follow explicit user instructions and the current project's constraints. Choose the lightest complete workflow; classify from the request and relevant code, without loading a routing skill or calling Jev.

## One owner per job

- Clear, local fixes: inspect, change, verify. No SDD paperwork.
- Clear work spanning several parts: state scope and acceptance checks in chat, then implement. No separate plan file.
- New behavior with material uncertainty, cross-system contracts, authorization, or persistent-data changes: use OpenSpec when requirements/design need agreement. File count is not the criterion. An OpenSpec directory alone never requires SDD.
- Reuse an active change if the request belongs to it. Keep existing specs accurate when behavior changes. Escalate the workflow if investigation reveals material uncertainty; explain why.
- If a request leaves a decision-critical behavior unspecified and plausible choices would produce different user-visible results, data changes, or API contracts, pause before implementation and ask only the questions needed to choose. Do not silently pick a default. Use OpenSpec if those requirements/design decisions need a durable agreement. Jev may help compare concrete options only when requested or explicitly enabled; it does not replace clarification or approval.
- For SDD, OpenSpec owns requirements, design, tasks, validation and archive. Its `tasks.md` is the only work plan. Use the installed OpenSpec workflow and its actual instructions; do not create a second PRD, design or Superpowers plan.

## Implementation

- Apply Ponytail to coding: reuse existing code, make the smallest complete change, preserve validation/error handling, avoid speculative abstractions. Load `ponytail` once when useful; never also activate its lifecycle hook/plugin or duplicate its full prompt here.
- For bugs/unexpected behavior, use `systematic-debugging`; for nontrivial behavior changes use `test-driven-development` when tests are authorized. Honor user/project test constraints; do not claim unrun checks passed. Trivial prose/style changes do not need TDD.
- For refactors and changes to existing interfaces or data behavior, identify the existing observable contracts first (including caller assumptions and returned-object behavior), then preserve them or record an explicitly approved change. Treat permission to author tests separately from permission to run them. When test authoring is allowed, write characterization/regression tests for decision-critical contracts before implementation; for other nontrivial behavior changes, write the failing test first. Run tests only when execution is allowed. If authoring is prohibited, or execution is prohibited/deferred, record the constraint, what remains unverified and the resulting risk.
- Use `verification-before-completion` before asserting success. Report actual evidence and checks not run. Use `receiving-code-review` when acting on review feedback.
- Implement from the current request/chat plan or OpenSpec task. Do not invoke Superpowers brainstorming, writing-plans, executing-plans or subagent-driven-development. Worktree isolation is needed only when the workspace/task requires it, not for every edit.
- `requesting-code-review` is the sole default code-review procedure, for substantial/risky changes or when requested. Review a trivial edit directly. Do not add a second generic Ponytail or pre-implementation review. Re-review only changed findings or affected behavior.

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
