# Workflow and skill calls

**English** | [한국어](workflow.ko.md)

Setup installs the [shared development policy](../rules/development.md) into each selected host. That file is the sole authority for skill selection, approvals, and verification. This guide covers tool-specific mechanics, invocation syntax, and Superpowers handoffs; follow the installed policy if guidance here conflicts with it.

## Product requirements (PRD)

For a PRD request, reuse the active OpenSpec change or open one when the requirements need durable agreement. Capture the user problem, evidence or assumptions, measurable success criteria, and MVP scope in the proposal. Record agreed behavior and acceptance scenarios in the linked specs. Ask about unresolved choices that would change behavior or scope.

Use the proposal and linked specs as the PRD deliverable. Keep implementation work in that change's `tasks.md` when implementation is requested. For a PRD-only request, finish after checking that the requirements and success criteria are traceable to the product problem.

## Tools provided by Grounded

- **Current technical docs.** Use the host's Context7 OAuth connection for version-specific lookups. Resolve the library ID and query one topic at a time. If Context7 is unavailable, fetch the exact official remote release/tag/package artifact; unversioned current docs do not verify a pinned version. Follow the [shared policy](../rules/development.md) for reporting unavailable evidence.
- **CLI automation.** Use `cli-hub-meta-skill` to search for an existing CLI when an app workflow lacks a suitable CLI or MCP integration. Use `cli-anything` to build, refine, test, or validate a harness only when an existing option does not fit. Ordinary shell commands stay with the terminal/RTK; MCP server work stays with `mcp-builder`. Discovery is read-only; ask before installing a package or changing app/system state. Neither skill bypasses credentials, access controls, or quotas.
- **Portfolio reference study.** Use `craft-anything` only when the user explicitly requests its early-alpha Study → Build → Check → Ready workflow for an authorized personal website, app, or game portfolio project. Keep third-party references clean-room; do not copy protected assets or content. Run its managed `doctor` command first. If the host adapter is unsupported, use its study evidence and let the active coding agent implement the project.
- **Browser QA.** Use the project's existing browser tests and tools first. When browser verification is needed and the project has no suitable tool, use the managed Microsoft `playwright-cli` and Chromium. Use the managed executable at `~/.local/share/skills-environment/playwright/<installed-version>/playwright-cli` when it is outside PATH. Check the changed user flow in a running browser.
- **Tracker tickets.** Use the managed `to-tickets` skill when the user requests recurring ticket breakdown or publication. Use the existing `tasks.md` as the source for OpenSpec changes and link tickets to their source tasks. Confirm the target tracker and project before publishing, and publish only with explicit authorization.

Choose each ECC documentation skill independently. Use `doc-updater` when an update requires reconciling changes, contracts, or sources. Short updates based on verified facts can be edited directly unless the skill is requested. Invoke `docs-governance` when a separate integrity audit is requested or agreed.

## Skill calls

This table gives invocation spellings for skills already chosen by judgment; it does not choose a route or imply a bundle. Choose from repository evidence about the files, contracts, dependencies, and runtime behavior that will change or be reviewed; do not infer technology from a feature name. Finish that evidence pass before announcing the final skill set, then cover each distinct changed behavior with its domain owner or explicitly note that none adds value. Treat a matching ownership cue as required. Context7 validates API sources but does not replace domain skills. Include the relevant change, file, or request when invoking a selected skill.

| To do this | Codex | Claude Code |
|---|---|---|
| Reconcile changes, contracts, or sources for a docs update | `$doc-updater` | `/doc-updater` |
| Run a separate read-only document audit | `$docs-governance` | `/docs-governance` |
| Review UI or accessibility | `$web-design-guidelines` | `/web-design-guidelines` |
| Create or visually redesign a UI | `$frontend-design` | `/frontend-design` |
| Change React/Next component, hook, rendering, routing, or framework behavior | `$vercel-react-best-practices` | `/vercel-react-best-practices` |
| Design, review, or change compound components or reusable component APIs | `$vercel-composition-patterns` | `/vercel-composition-patterns` |
| Resolve version-specific React/Next API behavior | Context7 official docs | Context7 official docs |
| Verify a flow in the browser | `$playwright-cli` | `/playwright-cli` |
| Prepare or publish approved tracker tickets | `$to-tickets` | `/to-tickets` |
| Build or change an MCP server | `$mcp-builder` | `/mcp-builder` |
| Find an existing CLI for an app workflow | `$cli-hub-meta-skill` | `/cli-hub-meta-skill` |
| Build/refine a CLI harness when no existing option fits | `$cli-anything` | `/cli-anything` |
| Study/recreate an authorized portfolio reference with Craft Anything | `$craft-anything` | `/craft-anything` |
| Investigate a reproducible bug or unexplained failure | `$systematic-debugging` | `/systematic-debugging` |
| Keep an implementation small | `$ponytail` | `/ponytail` |
| Review completion evidence when a separate check is needed | `$verification-before-completion` | `/verification-before-completion` |
| Design with Superpowers | `$brainstorming` | `/brainstorming` |
| Write an implementation plan with Superpowers | `$writing-plans` | `/writing-plans` |
| Execute a Superpowers plan in this session | `$executing-plans` | `/executing-plans` |
| Change a CI/CD pipeline | `$ci-cd-and-automation` | `/ci-cd-and-automation` |
| Plan a progressive rollout or rollback | `$deployment-patterns` | `/deployment-patterns` |

Choose verification by the deliverable: run focused regression/contract tests for code and APIs, exercise browser and keyboard behavior for UI, validate authorization and migrations for data/security work, check the real workflow or deployment when available, compare docs against the source diff, and measure performance against a same-environment baseline. A helper/unit test does not verify its caller's hook, route, or integration lifecycle unless it exercises that boundary. For read-only reviews, cite the relevant source/configuration and state limits. Use `verification-before-completion` for an explicit verification/acceptance audit request, before commits/PRs, or for delegated implementation. For material risk requiring code review, use `requesting-code-review`; do not also load completion verification solely to repeat its requirements/diff pass. An implementation request, ordinary test run, or status update alone does not trigger it. For ordinary checks, reuse valid evidence. Follow the original procedure when the verification skill is selected. Resume context only for a user- or task-identified interrupted task with a recoverable record; fresh requests and validation scenarios are not continuations.

For the native Grounded plugin's scope review, engineering review, or ADR, prefix the skill name with `grounded:`. For example, use `$grounded:plan-review-ceo` in Codex or `/grounded:plan-review-ceo` in Claude. Standalone installs use `plan-review-ceo`, `plan-review-eng`, and `adr` without the prefix. OpenSpec provides its own project-specific entry points. For Context7, ask for the current official documentation in chat.

## Choosing or switching to the full Superpowers workflow

Setup installs the 15 Superpowers v7 skills as standalone skills. Choose individual debugging, TDD, code review, and verification techniques by task under the shared policy. The full design and execution workflow requires explicit selection. The other ten skills are available on request. Setup omits the Superpowers startup hooks. Use platform invocation or ask for an individual skill by name, such as `using-git-worktrees` or `finishing-a-development-branch`.

- **Default.** Follow the [shared development policy](../rules/development.md) for skill selection.
- **Full workflow.** When the user asks to use Superpowers for design and execution, start at the applicable step. Use `brainstorming` and `writing-plans` if design or planning is needed, then choose `executing-plans` or, with explicit authorization, `subagent-driven-development`. One plan is active at a time.
- **Handoff.** A supporting skill can be used while the current plan remains active. If the selected approach stalls, state the evidence and gap, then suggest the smallest next step; don't stack another workflow automatically. If that step would replace the active plan, ask first unless the user already requested the switch. Record the old plan's status, retained requirements and tests, failed approach, open decisions, and new plan location alongside the existing change or plan. Pause the old plan, preserve its history, and keep one active plan. Use the same handoff when switching back to OpenSpec.

Setup installs Ponytail without its startup hooks or audit and review commands.

## Optional stages retain full internal procedures

Selecting fewer stages does not mean reducing the selected skill's review depth:

- `plan-review-ceo`: audit → premise/reuse/dream-state challenge → 2–3 alternatives and approach approval → scope mode → eleven review sections (UX conditional) → requirement/ADR candidates → confirmed verdict and note.
- `plan-review-eng`: standalone or current CEO-reviewed intake → four technical sections including coverage/ambition checks → task dependency/parallel-lane analysis → ADR candidates → confirmed verdict and note.
- `adr`: intent/scope/chain confirmation → context intake → six interview branches → three-persona review → six-criterion completeness and anti-monolith gates → validated record/supersession.

Reviews are interactive unless the user has explicitly delegated the applicable decisions/pacing. Do not fabricate user answers. A review invocation authorizes its review note in `.ai/reviews/` or the established review location, not implementation or another stage. Prior approvals apply only to unchanged reviewed inputs. Notes contain findings, evidence and decisions; they are not duplicate requirement/design/task documents.

CEO and engineering review may inspect the same interface for different reasons. Reuse existing diagrams/evidence and check technical gaps/deltas; do not re-ask settled questions or duplicate findings. Do not skip required substantive checks to hit an arbitrary token budget. No runtime quality equivalence or token savings have yet been measured for this adaptation.

## Host smoke checks

For both Codex and Claude, confirm an explicitly selected Superpowers workflow can open its next skill from the installed list. Check that a routine task does not start opt-in workflows. For Codex fixture runs, use skill paths and hashes recorded in `outcome.json` to check which copy was referenced. Missing path evidence is inconclusive.

After updating and rerunning setup, use a disposable project to confirm the two host-dependent paths:

1. Connect Grounded's Context7 from the host's MCP controls, then request a version-specific documentation lookup. Verify that Context7 resolves the library and returns documentation.
2. Start an OpenSpec change, then explicitly request a switch to Superpowers. Verify that the handoff retains the old plan and evidence and identifies one new active plan. Confirm that a standalone debugging request leaves the active plan in place.

## Limits

Host/user/project instructions can conflict with this policy. Setup detects known user-level names/plugins; doctor also scans conventional project/ancestor skill directories. Neither can prove arbitrary prose, renamed plugins or nonstandard locations conflict-free. Resolve contradictory instructions before proceeding; do not silently override them. No prompt can guarantee model compliance. Verify actual invocation traces and outcomes in each host.
