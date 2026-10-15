---
name: plan-review-eng
description: Use when explicitly asked for a full engineering plan review covering architecture, quality, tests, performance and execution dependencies.
disable-model-invocation: true
---

# Engineering plan review

Read [shared rules](../../rules/development.md) once unless already in host context. Standalone installs fall back to host rules.

Run the full four-section procedure when invoked. Use the user's language and preserve LICENSE.review-skills. This optional stage is not a code implementation pipeline.

## Phase 0 — Intake and mode

Resolve the OpenSpec change and specs/design/tasks, or the existing request/chat plan if SDD is unnecessary. Read relevant code, callers, interfaces, tests and ADRs. Missing design context requires an explicit pause / proceed-with-limitations / cancel choice. Do not require a second handoff document or configuration tree.

- **ceo-reviewed:** a relevant CEO note is APPROVE, its scope matches the task, and its reviewed-input snapshot is current. Reuse its scope, alternatives, accepted decisions and existing evidence; investigate technical gaps/deltas rather than interviewing the user about settled facts again.
- **standalone:** no applicable approved CEO note. Perform a lightweight premise/scope/existing-code check, but do not require or automatically run CEO review.
- An applicable REVISE/REJECT note is not silently bypassed: show it and ask to address it, return to scope review, or explicitly continue standalone with the override and risks recorded.
- Detect late additions since CEO review: requirements, files/modules, decisions or deferred work. Surface deltas and re-confirm changed scope before relying on prior approval. If hashes/revision evidence are unavailable, disclose uncertainty and recheck relevant inputs.

Search existing/platform solutions before recommending new ones. Confidence below 7/10 is low confidence and needs evidence. Honor user/project constraints; use actual host tools or ask in chat and wait.

## Phase 1 — Four engineering sections

Read [the full section procedures](references/sections.md). Walk all four; small scope does not waive test/failure analysis.

1. **Architecture:** module/dependency delta diagram, boundaries, coupling, API/data contracts, authorization, rollback and migration failure modes.
2. **Code quality:** concrete connected-code evidence, reuse/duplication, errors, contracts, over/under-engineering and maintenance implications. Ponytail's minimum-complete-change principle must not drop required behavior.
3. **Tests:** read [the coverage diagram procedure](templates/test-coverage-diagram.md). Map every new path, branch, input, error/rescue and integration to existing/planned/missing tests. Include missing test names and one-sentence specs. Ask the riskiest-path 2am-Friday, hostile-QA and chaos-test questions. Review pyramid balance, flakiness and load/stress needs. Record explicit implement/defer decisions per missing row.
4. **Performance:** algorithmic cost, I/O/network/query behavior, concurrency, memory/cache and expected load. Supply budget deltas with measured/estimated/unknown basis. Never invent results.

For a consequential finding, show file/requirement evidence, reachable failure, options, recommendation and trade-offs. Ask one issue at a time with the host's question tool or chat; stop for the answer. At each section end record "No issues found", or accepted/deferred findings, and wait for transition unless pacing was explicitly delegated. Do not invent issues solely to fill sections. Reuse CEO evidence by link; examine engineering detail and new risks, not the same review twice.

## Phase 2 — Worktree parallelization analysis

Analyze the existing implementation tasks; do not create a second plan or start worktrees/agents.

- Skip only for one module/no independent workstreams or an explicit user instruction; state the reason.
- Produce a dependency table: existing task ID / module directories touched / dependencies.
- Group independent tasks with no shared modules into parallel lanes; shared modules remain sequential, dependencies come first.
- State topological execution order and merge/contract/schema conflict flags. If apparent parallel lanes share a module, call out the conflict and revise the lanes.
- Record recommendations in the review note; OpenSpec tasks remain the execution authority.

## Phase 3 — ADR candidates

Cross-reference existing ADRs. In ceo-reviewed mode retain prior candidates and add only new load-bearing choices; in standalone mode analyze all choices. List candidate decision, evidence, trade-offs, existing record and why a separate ADR is or is not needed. Do not force ADRs for feature-local details or write them automatically. Requirements changes go back to the existing OpenSpec artifacts.

## Phase 4 — Verdict and handoff

Recommend APPROVE / REVISE / REJECT, then obtain final user confirmation unless final approval was explicitly delegated. APPROVE requires all sections completed, no unresolved blocking issue and no missing decision-critical context. Deferrals need explicit owner/condition/risk and do not count as verified fixes.

Write one note at `.ai/reviews/<slug>-eng.md` or the established project review location. Include a column-zero `Verdict: APPROVE|REVISE|REJECT` line, approval source, input paths/revision/hashes when available, mode/scope/deltas, four section results, coverage diagram/decisions, dependency table/lanes/order/conflicts, ADR candidates and unresolved/deferred items.

Recommend only the next needed step: user-approved ADR authoring if a candidate needs recording, otherwise implementation from the existing OpenSpec/chat tasks using selected Superpowers techniques and Ponytail. Do not invoke those stages, another reviewer or Jev automatically. Resume interrupted reviews from the recorded section after checking changed inputs. Approval is plan approval, not proof that code or tests passed.
