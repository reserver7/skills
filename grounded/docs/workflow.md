# One workflow per job

**English** | [한국어](workflow.ko.md)

Setup installs the [shared development policy](../rules/development.md) into each selected host. Use this page as a reference for ownership, skill calls, and workflow handoffs.

There is no fixed skill count: combine skills when their roles complement each other across distinct phases or aspects of a task; avoid overlapping calls. Before acting, briefly list each planned skill and its role/reason (or say no dedicated skill applies). This is an FYI, not an approval request; continue without waiting. If investigation changes the route, announce the added skill and reason before using it.

## Selecting and combining skills

Before acting, match the requested deliverables and material risks to the shared policy. Load each required specialist once and add another skill only for work or checks it owns. Use the table below as a reference. Revisit the selection if scope or risk changes.

If a required skill is missing from the active host, check the Grounded-managed catalog for that skill and report the limitation. Continue with a bounded fallback if it satisfies the request. Ask or stop when a required procedure cannot be completed. Use Grounded Setup to repair missing managed skills.

For a trust-boundary change, check access decisions even when a database or MCP specialist owns implementation. For new telemetry, use the observability skill. Debugging applies when there is an actual fault to diagnose. For an authorized bug regression, a test runner error does not demonstrate the intended failure. Confirm the behavior fails before the fix when execution is available, then rerun the focused check. Planned or written tests and executed tests should be reported separately.

Before claiming completion, check once that each requested deliverable and material risk has suitable evidence. Reuse valid results and rerun only affected checks. For compatible API extensions, use the interface-design guidance to check the existing contract. For substantive documentation or release notes, use doc-updater. Use docs-governance for separately requested audits.

Choose the approach when outcomes are equivalent. Ask once and wait if an unresolved choice materially changes behavior, data, API contracts, operational risk, or rollback cost. Use Jev only when enabled and authorized to compare concrete options.

A step is required if the user or applicable project rules require it or it is needed to demonstrate completion. Add a suggested follow-on step only if it serves a distinct role. If a required step is blocked, name the unmet criterion and stop. Report applied changes separately from outcomes you could not confirm.

When evaluating workflow cost, compare similar tasks for skill calls, repeated reads and checks, and missed required checks. Include token counts when available.

Use systematic debugging for bugs. Add Addy `security-and-hardening` when a fix changes who or what can access a resource, or under which conditions. Ponytail is optional for a direct bug fix. Add general code review only for a distinct concern and reuse relevant evidence. If Superpowers already directs the edit, continue with that procedure.

| Task | Planning owner | Implementation | Extra review |
|---|---|---|---|
| Typo, local styling | Request | Direct minimal edit; invoke Ponytail only if its guidance helps; inspect result | None |
| Clear local bug | Request | Debug and reproduce per shared policy. Check test writing and execution permissions separately. TDD requires both. Reuse permitted evidence and report skipped checks. For direct edits, Ponytail is optional for a direct edit. | Only if requested/risky |
| Clear multi-file change | Short scope/acceptance statement in chat | Use the fitting Superpowers procedure or Ponytail for a lean direct edit; don't layer Ponytail onto Superpowers by default | One code review if substantial |
| Material new behavior/design uncertainty | OpenSpec proposal/specs/design/tasks | Implement the existing task list | Scope/engineering review when accepted |
| API/interface contract | Direct design when settled; OpenSpec owns behavior agreement when ambiguous | Addy `api-and-interface-design` for API boundaries, versioning, errors, and compatibility | Contract tests for success/error/auth and compatibility behavior |
| Performance investigation | Establish a measured baseline and target first | Addy `performance-optimization` for a focused investigation | Comparable before/after metric; no claim from code review alone |
| Security-sensitive change | Identify affected trust boundaries and expected allow/deny behavior | Addy `security-and-hardening` for authentication, authorization, tenant isolation, or untrusted inputs such as uploads and webhooks | Verify affected controls. Add general code review only for distinct broader concerns; separate scope and merge duplicate findings |
| Add or improve production telemetry | Identify the production behavior or failure that needs visibility | Addy `observability-and-instrumentation` for logs, metrics, traces, or alerts | Confirm the signal answers the operational question |
| Nontrivial database migration | State engine and data invariants; OpenSpec when rollout or compatibility is uncertain | ECC `database-migrations`; use `mysql-patterns` only for MySQL | Engine-native migration/retry/rollback checks; don't generalize MySQL evidence to other engines |
| Ordinary CI/CD pipeline change | Request or existing task | Addy `ci-cd-and-automation`; validate the affected workflow and checks | ENG only for material release, data, security, or verification risk |
| Progressive delivery or coordinated migration rollout | Request or OpenSpec when contracts are material | Addy owns pipeline mechanics; ECC `deployment-patterns` owns canary/rollout/abort/rollback strategy | ENG when failure handling or rollback contracts carry material risk |

OpenSpec is not mandatory merely because it exists in the repository. Existing behavior specifications must remain accurate. Escalate from a direct fix when investigation reveals cross-system contracts or significant uncertainty.

## Product requirements (PRD)

For a PRD request, reuse the active OpenSpec change or open one when the requirements need durable agreement. Capture the user problem, evidence or assumptions, measurable success criteria, and MVP scope in the proposal. Record agreed behavior and acceptance scenarios in the linked specs. Ask about unresolved choices that would change behavior or scope.

Use the proposal and linked specs as the PRD deliverable. Keep implementation work in that change's `tasks.md` when implementation is requested. For a PRD-only request, finish after checking that the requirements and success criteria are traceable to the product problem.

## Tools provided by Grounded

- **Current technical docs.** Before version-sensitive implementation, review, or recommendations, use Context7. Pinned SDK/package/API/CLI/cloud versions and CI action tags such as `actions/setup-python@v5` count. Resolve the library ID, then query the official match for that version and topic, one topic at a time. Sign in once per host via its MCP connection controls. If the exact pin is unindexed, inspect its official release/tag source or package artifact; nearest-version docs do not prove exact behavior. If that source is unavailable, disclose the gap and don't claim verification.
- **MCP server development.** Use Anthropic `mcp-builder` when building or changing an MCP server. Use OpenSpec for unresolved tool contracts or permissions, and use the existing security review path for changed trust boundaries.
- **CLI automation.** Use `cli-hub-meta-skill` to search for an existing CLI when an app workflow lacks a suitable CLI or MCP integration. Use `cli-anything` to build, refine, test, or validate a harness only when an existing option does not fit. Ordinary shell commands stay with the terminal/RTK; MCP server work stays with `mcp-builder`. Discovery is read-only; ask before installing a package or changing app/system state. Neither skill bypasses credentials, access controls, or quotas.
- **Portfolio reference study.** Use `craft-anything` only when the user explicitly requests its early-alpha Study → Build → Check → Ready workflow for an authorized personal website, app, or game portfolio project. Keep third-party references clean-room; do not copy protected assets or content. Run its managed `doctor` command first. If the host adapter is unsupported, use its study evidence and let the active coding agent implement the project.
- **UI creation and review.** Use `frontend-design` when creating or visually redesigning a UI. Use `web-design-guidelines` for a separate UI/accessibility review, and confirm affected keyboard and focus behavior in the browser when relevant. Use `vercel-react-best-practices` for React/Next implementation; load `vercel-composition-patterns` only for compound components, boolean-prop complexity, or reusable component APIs. Query Context7 for version-specific API behavior. Use Addy `api-and-interface-design` only when a public component contract changes, and `performance-optimization` for measured investigations after setting a baseline and target.
- **Browser QA.** Use the project's existing browser tests and tools first. When browser verification is needed and the project has no suitable tool, use the managed Microsoft `playwright-cli` and Chromium. Check the changed user flow in a running browser.
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
| Create or visually redesign a UI | `$frontend-design` | `/frontend-design` |
| Implement or refactor React/Next code | `$vercel-react-best-practices` | `/vercel-react-best-practices` |
| Change compound components or reusable component APIs | `$vercel-composition-patterns` | `/vercel-composition-patterns` |
| Resolve version-specific React/Next API behavior | Context7 official docs | Context7 official docs |
| Verify a flow in the browser | `$playwright-cli` | `/playwright-cli` |
| Prepare or publish approved tracker tickets | `$to-tickets` | `/to-tickets` |
| Build or change an MCP server | `$mcp-builder` | `/mcp-builder` |
| Find an existing CLI for an app workflow | `$cli-hub-meta-skill` | `/cli-hub-meta-skill` |
| Build/refine a CLI harness when no existing option fits | `$cli-anything` | `/cli-anything` |
| Study/recreate an authorized portfolio reference with Craft Anything | `$craft-anything` | `/craft-anything` |
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

- **Default.** Preserve the routing above. Use a Superpowers procedure when its task-specific guidance fits; use Ponytail for a lean direct edit when useful. Do not pair them by default. Use OpenSpec for material agreement and durable requirements. Clear multi-step work can use the scope and acceptance agreed in chat.
- **Full workflow.** When the user asks to use Superpowers for design and execution, start at the applicable step. Use `brainstorming` and `writing-plans` if design or planning is needed, then choose `executing-plans` or, with explicit authorization, `subagent-driven-development`. One plan is active at a time.
- **Handoff.** A supporting skill can be used while the current plan remains active. If the selected approach stalls, state the evidence and gap, then suggest the smallest next step; don't stack another workflow automatically. If that step would replace the active plan, ask first unless the user already requested the switch. Record the old plan's status, retained requirements and tests, failed approach, open decisions, and new plan location alongside the existing change or plan. Pause the old plan, preserve its history, and keep one active plan. Use the same handoff when switching back to OpenSpec.

The Ponytail skill is installed without its startup hooks or audit/review commands. Its lean-change principles can guide implementation generally, but invoke Ponytail only when its skill guidance adds value. When a selected Superpowers procedure directs the code edit, use that procedure without adding Ponytail. Superpowers remains the one default code-review procedure. Optional pre-implementation scope/engineering reviews have different outputs and never run automatically in sequence.

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
