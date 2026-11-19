# One workflow per job

Setup installs the [shared development policy](../rules/development.md) into each selected host. Use this page as a reference for ownership, skill calls, and workflow handoffs.

| Task | Planning owner | Implementation | Extra review |
|---|---|---|---|
| Typo, local styling | Request | Direct edit; Ponytail scope; inspect result | None |
| Clear local bug | Request | Superpowers debugging, relevant regression test and verification | Only if requested/risky |
| Clear multi-file change | Short scope/acceptance statement in chat | Selected Superpowers techniques + Ponytail | One code review if substantial |
| Material new behavior/design uncertainty | OpenSpec proposal/specs/design/tasks | Implement the existing task list | Scope/engineering review when accepted |
| API/interface contract | Direct design when settled; OpenSpec owns behavior agreement when ambiguous | Addy `api-and-interface-design` for API boundaries, versioning, errors, and compatibility | Contract tests for success/error/auth and compatibility behavior |
| Performance investigation | Establish a measured baseline and target first | Addy `performance-optimization` for a focused investigation | Comparable before/after metric; no claim from code review alone |
| Security-sensitive change | Identify affected trust boundaries and expected allow/deny behavior | Addy `security-and-hardening` for authentication, authorization, tenant isolation, or untrusted inputs such as uploads and webhooks | Verify affected controls with targeted tests; use the existing code review path when applicable |
| Add or improve production telemetry | Identify the production behavior or failure that needs visibility | Addy `observability-and-instrumentation` for logs, metrics, traces, or alerts | Confirm the signal answers the operational question |
| Nontrivial database migration | State engine and data invariants; OpenSpec when rollout or compatibility is uncertain | ECC `database-migrations`; use `mysql-patterns` only for MySQL | Engine-native migration/retry/rollback checks; don't generalize MySQL evidence to other engines |
| Ordinary CI/CD pipeline change | Request or existing task | Addy `ci-cd-and-automation`; validate the affected workflow and checks | ENG only for material release, data, security, or verification risk |
| Progressive delivery or coordinated migration rollout | Request or OpenSpec when contracts are material | Addy owns pipeline mechanics; ECC `deployment-patterns` owns canary/rollout/abort/rollback strategy | ENG when failure handling or rollback contracts carry material risk |

OpenSpec is not mandatory merely because it exists in the repository. Existing behavior specifications must remain accurate. Escalate from a direct fix when investigation reveals cross-system contracts or significant uncertainty.

## Product requirements (PRD)

For a PRD request, reuse the active OpenSpec change or open one when the requirements need durable agreement. Capture the user problem, evidence or assumptions, measurable success criteria, and MVP scope in the proposal. Record agreed behavior and acceptance scenarios in the linked specs. Ask about unresolved choices that would change behavior or scope.

Use the proposal and linked specs as the PRD deliverable. Keep implementation work in that change's `tasks.md` when implementation is requested. For a PRD-only request, finish after checking that the requirements and success criteria are traceable to the product problem.

## Tools provided by Grounded

- **Current technical docs.** Use the Context7 MCP connection bundled with the native Grounded plugin. Resolve the library ID, then query the official match with one topic at a time. Sign in once per host via its MCP connection controls. Use upstream official docs if the connection is unavailable.
- **MCP server development.** Use Anthropic `mcp-builder` when building or changing an MCP server. Use OpenSpec for unresolved tool contracts or permissions, and use the existing security review path for changed trust boundaries.
- **Browser QA.** Use the project's existing browser tests and tools first. When browser verification is needed and the project has no suitable tool, use the managed Microsoft `playwright-cli` and Chromium. Check the changed user flow in a running browser.
- **UI review.** Follow the project's UI standards. For a requested UX or accessibility review, use Grounded `web-design-guidelines` with the Vercel rules installed by setup. Confirm affected keyboard and focus behavior in the browser when relevant.
- **Documentation updates.** Invoke ECC `doc-updater` to keep existing READMEs, guides, API docs, or requested codemaps consistent with current code. Verify relevant links, paths, commands, and examples. For requested release notes or changelog updates, verify the changes from the previous release tag to the target release against the Git diff and available PRs. Summarize user-visible changes, breaking changes, and any required upgrade steps.
- **Documentation integrity.** Invoke ECC `docs-governance` for read-only audits of mapped documents, links, ADR indexes, or evidence references. Reuse project document owners and existing OpenSpec and ADR workflows.
- **Tracker tickets.** Use the managed `to-tickets` skill when the user requests recurring ticket breakdown or publication. Use the existing `tasks.md` as the source for OpenSpec changes and link tickets to their source tasks. Confirm the target tracker and project before publishing, and publish only with explicit authorization.

Choose each ECC documentation skill independently. Use `doc-updater` for requested updates and release notes. Invoke `docs-governance` when a separate integrity audit is requested or agreed.

## Skill calls

Choose the skill for the current task and include the change, file, or request in the same message.

| To do this | Codex | Claude Code |
|---|---|---|
| Update docs, a changelog, or release notes | `$doc-updater` | `/doc-updater` |
| Run a separate read-only document audit | `$docs-governance` | `/docs-governance` |
| Review UI or accessibility | `$web-design-guidelines` | `/web-design-guidelines` |
| Verify a flow in the browser | `$playwright-cli` | `/playwright-cli` |
| Prepare or publish approved tracker tickets | `$to-tickets` | `/to-tickets` |
| Build or change an MCP server | `$mcp-builder` | `/mcp-builder` |
| Investigate a bug or unexpected test failure | `$systematic-debugging` | `/systematic-debugging` |
| Keep an implementation small | `$ponytail` | `/ponytail` |
| Verify completion | `$verification-before-completion` | `/verification-before-completion` |
| Design with Superpowers | `$brainstorming` | `/brainstorming` |
| Write an implementation plan with Superpowers | `$writing-plans` | `/writing-plans` |
| Execute a Superpowers plan in this session | `$executing-plans` | `/executing-plans` |
| Change a CI/CD pipeline | `$ci-cd-and-automation` | `/ci-cd-and-automation` |
| Plan a progressive rollout or rollback | `$deployment-patterns` | `/deployment-patterns` |

For the native Grounded plugin's scope review, engineering review, or ADR, prefix the skill name with `grounded:`. For example, use `$grounded:plan-review-ceo` in Codex or `/grounded:plan-review-ceo` in Claude. Standalone installs use `plan-review-ceo`, `plan-review-eng`, and `adr` without the prefix. OpenSpec provides its own project-specific entry points. For Context7, ask for the current official documentation in chat.

## Choosing or switching to the full Superpowers workflow

Setup installs the 15 Superpowers v7 skills as standalone skills. The five debugging, TDD, code-review, and verification skills retain their usual task-based use. The other ten are available on request. Setup omits the Superpowers startup hooks. Use platform invocation or ask for an individual skill by name, such as `using-git-worktrees` or `finishing-a-development-branch`.

- **Default.** Preserve the routing above. Use Ponytail for a lean implementation, selected Superpowers techniques for implementation checks, and OpenSpec for material agreement and durable requirements. Clear multi-step work can use the scope and acceptance agreed in chat.
- **Full workflow.** When the user asks to use Superpowers for design and execution, start at the applicable step. Use `brainstorming` and `writing-plans` if design or planning is needed, then choose `executing-plans` or, with explicit authorization, `subagent-driven-development`. One plan is active at a time.
- **Handoff.** A supporting skill can be used while the current plan remains active. If the user asks to replace the workflow, record the old plan's status, retained requirements and tests, failed approach, open decisions, and new plan location alongside the existing change or plan. Pause execution of the old plan, preserve its history, and use the new plan. Follow the same handoff for switching back to OpenSpec. Ask one focused question only if plan ownership is ambiguous.

The Ponytail skill is installed without its startup hooks or audit/review commands. Its principles apply during implementation; Superpowers remains the one default code-review procedure. Optional pre-implementation scope/engineering reviews have different outputs and never run automatically in sequence.

## Optional stages retain full internal procedures

Selecting fewer stages does not mean reducing the selected skill's review depth:

- `plan-review-ceo`: audit → premise/reuse/dream-state challenge → 2–3 alternatives and approach approval → scope mode → eleven review sections (UX conditional) → requirement/ADR candidates → confirmed verdict and note.
- `plan-review-eng`: standalone or current CEO-reviewed intake → four technical sections including coverage/ambition checks → task dependency/parallel-lane analysis → ADR candidates → confirmed verdict and note.
- `adr`: intent/scope/chain confirmation → context intake → six interview branches → three-persona review → six-criterion completeness and anti-monolith gates → validated record/supersession.

Reviews are interactive unless the user has explicitly delegated the applicable decisions/pacing. Do not fabricate user answers. A review invocation authorizes its review note in `.ai/reviews/` or the established review location, not implementation or another stage. Prior approvals apply only to unchanged reviewed inputs. Notes contain findings, evidence and decisions; they are not duplicate requirement/design/task documents.

CEO and engineering review may inspect the same interface for different reasons. Reuse existing diagrams/evidence and check technical gaps/deltas; do not re-ask settled questions or duplicate findings. Do not skip required substantive checks to hit an arbitrary token budget. No runtime quality equivalence or token savings have yet been measured for this adaptation.

## Host smoke checks

After updating and rerunning setup, use a disposable project to confirm the two host-dependent paths:

1. Connect Grounded's Context7 from the host's MCP controls, then request a version-specific documentation lookup. Verify that Context7 resolves the library and returns documentation.
2. Start an OpenSpec change, then explicitly request a switch to Superpowers. Verify that the handoff retains the old plan and evidence and identifies one new active plan. Confirm that a standalone debugging request leaves the active plan in place.

## Limits

Host/user/project instructions can conflict with this policy. Setup detects known user-level names/plugins; doctor also scans conventional project/ancestor skill directories. Neither can prove arbitrary prose, renamed plugins or nonstandard locations conflict-free. Resolve contradictory instructions before proceeding; do not silently override them. No prompt can guarantee model compliance. Verify actual invocation traces and outcomes in each host.
