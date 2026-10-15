---
name: plan-review-ceo
description: Use when explicitly asked for a CEO-style plan review of premise, alternatives, scope and implementation readiness.
disable-model-invocation: true
---

# CEO plan review

Read [shared rules](../../rules/development.md) once unless already in host context. Standalone installs fall back to host rules.

Run all eleven sections, not a checklist. Use the user's language and LICENSE.review-skills. Never start implementation.

## Integration contract

- Input: named OpenSpec proposal/specs/design/tasks and applicable prior decisions. Without SDD, use the agreed request/chat plan; do not force OpenSpec solely to review.
- OpenSpec owns requirements/design/tasks. A review note records findings and approvals, not another PRD or implementation plan. Use these documents as pitch/handoff inputs.
- Superpowers/Ponytail implement and review code later. Here, inspect code for evidence but do not implement, run a second code review, start worktrees/agents, call Jev or invoke another stage automatically.
- Use the host's actual read/search/question tools. If a question tool is unavailable, ask in chat and wait. Do not fabricate answers or confirmations. Respect explicit delegation already given by the user.

## Phase 0 — Pre-review audit

1. Resolve target, base revision and working-tree changes. Read relevant requirements, design, tasks and ADRs. If required context is missing, offer pause to supply it, proceed with explicit limitations, or cancel. Missing context must remain visible in the verdict.
2. Audit the real system: architecture, interfaces, related implementations, recent changes and existing tests. Search before suggesting new infrastructure.
3. Check available prior review findings and relevant project memory; do not require a memory service or create another ledger.
4. Determine whether UI/design changes are in scope; record DESIGN_SCOPE.
5. If considering expansion, investigate existing/platform capabilities and current external alternatives with available tools. Separate evidence from assumptions; disclose unavailable evidence.

## Phase 1 — Scope challenge

Read [the complete rubric](references/nuclear-scope-rubric.md), then perform 1A–1F in order: premise, existing-code leverage, dream-state mapping, implementation alternatives, mode-specific analysis, temporal interrogation and mode selection. The alternatives substep comes before mode selection.

Present at least 2–3 materially distinct approaches, including the minimal useful option. Compare trade-offs, complexity and risks; recommend one and obtain the user's approach decision before continuing. Do not silently expand, reduce or skip scope. If no approach is acceptable, return to requirements exploration, without invoking a separate skill automatically.

Lock EXPANSION / SELECTIVE / HOLD / REDUCTION with explicit included scope, exclusions, selected approach and deferred items. Each added scope item needs opt-in. Do not invent speed/cost estimates; mark confidence below 7/10 as low confidence and state what evidence is needed.

## Phase 2 — Eleven review sections

Read [all section procedures](references/sections.md). Walk sections in order; do not collapse the full review because the plan is small:

1. Architecture and system diagram.
2. Error/rescue map.
3. Security/threat model.
4. Data-flow edge-case ledger.
5. Code quality and existing-code reuse.
6. Test Coverage Diagram, per-row decisions and test ambition.
7. Performance budget delta, with measured/estimated/unknown basis.
8. Observability/debuggability.
9. Deployment/rollout/rollback.
10. Long-term trajectory.
11. Design/UX, conditionally skipped only when DESIGN_SCOPE is false.

Load the [data-flow template](templates/data-flow-diagram.md) and [error/rescue template](templates/error-rescue-map.md) at their sections. Section 6 requires the coverage shape specified in the section procedure; include new paths, branches, errors, integration points and existing/planned/missing tests.

For each real issue, present evidence, recommended correction, alternatives and consequences; ask one consequential question at a time. Do not batch unrelated approvals. At section end record "No issues found", or accepted fixes/deferred issues, then wait for the user's transition signal unless that pacing was explicitly delegated. An obvious non-discretionary correction may be stated without an artificial choice; do not implement it here.

## Phase 3 — Triggers

Identify (a) changes needed to existing OpenSpec requirements/design/tasks, (b) durable technical choices that may need ADRs, (c) review-only observations. Mark defer/exclusion decisions explicitly. Do not author upstream artifacts or ADRs automatically. Preserve exact requirement links and settled decisions for engineering review.

## Phase 4 — Verdict and note

Recommend APPROVE / REVISE / REJECT from the evidence; APPROVE requires no unresolved blocking issues or missing decision-critical context. Present the final verdict for user confirmation unless final approval was explicitly delegated. User acceptance of a deferral is recorded with its risk; it does not prove the underlying issue fixed.

Write one transient note at `.ai/reviews/<slug>-ceo.md` (or the project's established review location). Reuse this path on resume. Include:
- Target/input paths, base revision, reviewed-input content hashes when available; limitations if snapshot verification is unavailable.
- A column-zero `Verdict: APPROVE|REVISE|REJECT` line, approval source and unresolved/deferred issues.
- Locked scope/approach/mode, alternatives, all section results and required diagrams/maps.
- Requirements-update candidates, ADR candidates and the next permitted action.

Recommend engineering review when useful; do not start it. Do not claim implementation verified. If interrupted, record the last completed section and resume there after checking input changes; never present a partial review as APPROVE.
