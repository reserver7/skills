# One workflow per job

The automatically installed policy is [rules/development.md](../rules/development.md). This document explains ownership; it is not automatically loaded into development sessions.

| Task | Planning owner | Implementation | Extra review |
|---|---|---|---|
| Typo, local styling | Request | Direct edit; Ponytail scope; inspect result | None |
| Clear local bug | Request | Superpowers debugging, relevant regression test and verification | Only if requested/risky |
| Clear multi-file change | Short scope/acceptance statement in chat | Selected Superpowers techniques + Ponytail | One code review if substantial |
| Material new behavior/design uncertainty | OpenSpec proposal/specs/design/tasks | Implement the existing task list | Scope/engineering review when accepted |

OpenSpec is not mandatory merely because it exists in the repository. Existing behavior specifications must remain accurate. Escalate from a direct fix when investigation reveals cross-system contracts or significant uncertainty.

## Calls

| Purpose | Codex | Claude (standalone skill installation) |
|---|---|---|
| Scope review | `$plan-review-ceo <change or request>` | `/plan-review-ceo <change or request>` |
| Engineering review | `$plan-review-eng <change or plan>` | `/plan-review-eng <change or plan>` |
| ADR | `$adr <decision>` | `/adr <decision>` |
| Debug | `$systematic-debugging` | `/systematic-debugging` |
| Lean implementation | `$ponytail` | `/ponytail` |

Setup installs standalone skills, not namespaced plugins. OpenSpec invocations come from its generated files for the particular host/version.

## Why only a subset of Superpowers?

Full Superpowers auto-bootstrap/brainstorming/writing-plans/execution pipelines can create a second plan and require additional agents or workspaces. This environment installs debugging, TDD, verification, requesting review and receiving review only. Their bodies remain pinned upstream instructions except standalone namespace normalization; requesting review has an explicit portable adapter. There is no automatic task delegation. A future execution integration must demonstrate compatibility with OpenSpec `tasks.md` before inclusion.

The Ponytail skill is installed without its startup hooks or audit/review commands. Its principles apply during implementation; Superpowers remains the one default code-review procedure. Optional pre-implementation scope/engineering reviews have different outputs and never run automatically in sequence.

## Optional stages retain full internal procedures

Selecting fewer stages does not mean reducing the selected skill's review depth:

- `plan-review-ceo`: audit → premise/reuse/dream-state challenge → 2–3 alternatives and approach approval → scope mode → eleven review sections (UX conditional) → requirement/ADR candidates → confirmed verdict and note.
- `plan-review-eng`: standalone or current CEO-reviewed intake → four technical sections including coverage/ambition checks → task dependency/parallel-lane analysis → ADR candidates → confirmed verdict and note.
- `adr`: intent/scope/chain confirmation → context intake → six interview branches → three-persona review → six-criterion completeness and anti-monolith gates → validated record/supersession.

Reviews are interactive unless the user has explicitly delegated the applicable decisions/pacing. Do not fabricate user answers. A review invocation authorizes its review note in `.ai/reviews/` or the established review location, not implementation or another stage. Prior approvals apply only to unchanged reviewed inputs. Notes contain findings, evidence and decisions; they are not duplicate requirement/design/task documents.

CEO and engineering review may inspect the same interface for different reasons. Reuse existing diagrams/evidence and check technical gaps/deltas; do not re-ask settled questions or duplicate findings. Do not skip required substantive checks to hit an arbitrary token budget. No runtime quality equivalence or token savings have yet been measured for this adaptation.

## Limits

Host/user/project instructions can conflict with this policy. Setup detects known user-level names/plugins; doctor also scans conventional project/ancestor skill directories. Neither can prove arbitrary prose, renamed plugins or nonstandard locations conflict-free. Resolve contradictory instructions before proceeding; do not silently override them. No prompt can guarantee model compliance. Verify actual invocation traces and outcomes in each host.
