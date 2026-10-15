# Review procedure preservation

The integration selects optional stages; it must not silently replace a selected full review with a short checklist. Detailed resources are loaded at the relevant phase to avoid imposing their cost on unrelated tasks.

| Procedure | Retained checks and outputs | Integration adjustment |
|---|---|---|
| CEO audit | System evidence, retrospective, UI detection, expansion landscape | Existing OpenSpec/chat inputs; no separate pitch/design-handoff requirement |
| CEO scope challenge | Premise, code reuse, dream state, 2–3 alternatives, approach approval, temporal interrogation, four scope modes | No automatic requirements-authoring skill; edits stay in the existing source document |
| CEO eleven sections | Architecture, error/rescue, security, data flow, quality, tests, performance, observability, deployment, long term, conditional UX | Detailed sections and diagrams preserved; user-approved pacing/delegation respected |
| CEO verdict | Confirmed APPROVE/REVISE/REJECT, scope lock, evidence, candidates and note | Host-neutral review path; no automatic engineering review |
| Engineering intake | Standalone/CEO-reviewed, scope check, late changes and blocked prior verdict | Reuse unchanged approved facts; stale notes do not confer approval |
| Engineering four sections | Architecture diagram, quality evidence, complete coverage diagram/test ambition, performance delta | Technical detail/deltas retained; no repeated scope interview or implementation code review |
| Parallelization | Existing task dependency table, module conflicts, lanes and order, explicit skip conditions | Analysis only; no automatic worktree/agent launch or second task list |
| Engineering verdict | ADR candidates, confirmed verdict, complete review note and handoff recommendation | Implementation stays with OpenSpec tasks and selected Superpowers/Ponytail skills |
| ADR intake/interview | New/update/deprecate-only, scope/chain confirmation, six branches | Requirement/evidence references replace pitch coupling; SDD optional |
| ADR adversarial review | New engineer, maintainer, product lead; shared findings escalated and fixed once | Evidence required; never invent a finding merely to fill a quota |
| ADR gate/history | Six criteria, five passing, no unresolved placeholders, anti-monolith tiers, required sections, references and supersession | Embedded defaults instead of external profiles; no claimed correctness percentage |

Deliberately excluded integration machinery: obsolete configuration/locale catalogs, automatic stage chaining, duplicate PRDs/plans, mandatory separate memory service and unavailable host-specific tool names. Those exclusions do not authorize dropping substantive review checks.

The original gate's numerical mechanics are preserved rather than interpreting its historical “90%” label as 90% accuracy. ADR anti-monolith thresholds are L1 (>6 alternatives or >12 consequences), L2 (>8 or >18) and L3 (>12 or >30), with hint, explicit confirmation and refusal respectively.

This is a procedure mapping, not a runtime quality benchmark. See [validation plan](validation.md) for evidence needed before claiming equivalent defect detection or token savings.
