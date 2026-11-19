# Sources and compatibility changes

## External tools

| Source | Resolution at setup | Installed content |
|---|---|---|
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | npm `latest` stable dist-tag from `registry.npmjs.org`, verified by package integrity | Official CLI under a versioned private npm prefix; per-project skills generated only on explicit init |
| [Context7](https://github.com/upstash/context7/blob/master/docs/howto/oauth.mdx) | Official remote OAuth MCP endpoint declared in the native plugin manifests | Documentation tools and shared lookup policy; each host handles sign-in and session storage |
| [Superpowers](https://github.com/obra/superpowers) | Latest stable GitHub Release; tag resolved to and fetched by full commit SHA | All 15 Superpowers v7 skill directories, including bundled scripts and references; five task-based techniques and ten opt-in skills |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | Latest stable GitHub Release; tag resolved to and fetched by full commit SHA | ponytail skill only, no hooks |
| [Supabase Agent Skills](https://github.com/supabase/agent-skills) | Latest stable GitHub Release; tag resolved to and fetched by full commit SHA; upstream release includes MIT `LICENSE` | `supabase`, `supabase-postgres-best-practices` |
| [Addy Osmani Agent Skills](https://github.com/addyosmani/agent-skills) | Latest stable GitHub Release; tag resolved to and fetched by full commit SHA; MIT `LICENSE` | `ci-cd-and-automation` for ordinary CI/CD; `performance-optimization` for measured performance work; `api-and-interface-design` for API/interface contract design; `observability-and-instrumentation` for production telemetry; `security-and-hardening` for defensive review of trust-boundary changes |
| [Microsoft Playwright CLI](https://github.com/microsoft/playwright-cli) | Latest stable GitHub release with root Apache-2.0 LICENSE | `playwright-cli`, the matching npm release, and Chromium in Grounded state |
| [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines) | Current default-branch HEAD at setup, recorded by commit SHA; root MIT LICENSE | Upstream `command.md` and license with Grounded's `web-design-guidelines` adapter |
| [Anthropic MCP Builder](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) | Current default-branch HEAD recorded by commit SHA; skill-level Apache-2.0 `LICENSE.txt` | Complete upstream `skills/mcp-builder` folder, including original instructions, references, and scripts |
| [Matt Pocock Skills](https://github.com/mattpocock/skills) | Latest stable GitHub release with root MIT LICENSE | `skills/engineering/to-tickets` with a Grounded adapter for OpenSpec and authorized tracker publication |
| [Everything Claude Code (ECC)](https://github.com/affaan-m/ecc) | Latest stable GitHub Release; tag resolved to and fetched by full commit SHA; MIT `LICENSE` | `deployment-patterns` for complex progressive rollout; `database-migrations` for nontrivial schema migrations; `mysql-patterns` only for MySQL-specific work; `agents/doc-updater.md` as an explicit standalone skill |
| [ECC documentation governance](https://github.com/affaan-m/ECC/tree/main/.agents/skills/docs-governance) | Current default-branch HEAD at setup, recorded by commit SHA; root MIT LICENSE | `docs-governance` with upstream audit scripts and references; uses existing Grounded owners for requirements and ADRs |
| Local review and ADR skills | `skills/plan-review-ceo/`, `skills/plan-review-eng/`, `skills/adr/` | Standalone procedures extracted and adapted from the previous local implementation; no external review plugin installation or download |
| [Jev](https://typesafe.ai/) | Optional service, not bundled/pinned | Connection instructions only; configure current official provider separately |

Setup copies external skill folders, Vercel rules, and their applicable license files from verified Git checkouts. Only dependencies whose applicable license is confirmed at the resolved revision are declared for redistribution through setup; a missing or ambiguous license excludes a skill from this managed package. The resolved versions and immutable identifiers are recorded locally so restore does not resolve newer releases.
External trees are not vendored into this Git repository's new install path.
OpenSpec's installed lockfile is retained in its version cache; caches and backups are local to the machine and are not committed.

## Deliberate adaptations

- Standalone Superpowers skill references lose the plugin-only `superpowers:` prefix.
- `requesting-code-review` uses [a portable adapter](setup/adapters/requesting-code-review.md), retaining upstream `code-reviewer.md`. It handles uncommitted work, existing OpenSpec/chat requirements, available reviewer tools and an explicit no-independent-review fallback. Trivial edits do not spawn reviewers.
- Grounded installs Superpowers planning, execution, and support skills as explicit opt-ins, with a shared plan-handoff note. Superpowers and Ponytail startup hooks remain outside setup.
- Every installed skill has Codex invocation metadata. The three optional local skills are explicit-only in both hosts.
- CEO review retains the premise/existing-code/dream-state challenge, 2–3 alternatives, user-selected approach and scope mode, all eleven review sections (UX conditional), diagrams/rescue maps/test coverage, per-issue interaction, verdict and review note. Detailed section/rubric/template resources are loaded at the relevant phase.
- Engineering review retains standalone/CEO-reviewed intake, late-change detection, all four engineering sections, test ambition and coverage diagram, dependency table/parallel lanes/order/conflict analysis, ADR candidates, verdict and review note. Prior CEO facts/decisions are reused rather than re-interviewed; technical deltas are still checked.
- ADR retains intent/scope confirmation, six interview branches, three adversarial perspectives, the six-criterion gate (five passing; unresolved placeholders block), anti-monolith thresholds, required body sections and append-only supersession. Its gate label is not represented as a probability of correctness. Gaps/consequences must be evidence-backed, never fabricated to fill a quota.
- Environment-specific pitch/config/profile/catalog dependencies are replaced by existing OpenSpec/chat inputs and embedded defaults. Host-specific question APIs use the available host tool or direct chat. Automatic handoffs, extra PRDs/plans, duplicate code reviews and separate memory services are excluded; substantive review checks are not removed for token savings.
- Review notes use a host-neutral `.ai/reviews/` location (or the existing project convention). Notes carry reviewed-input evidence so later review can detect changed scope; they do not become a second plan. OpenSpec owns requirements/tasks and Superpowers/Ponytail own implementation.
- The common policy defines ownership and when SDD is unnecessary; it is not a second orchestrator or a copied implementation manual.

These are compatibility adaptations of preexisting local procedures and selected Superpowers skills. No equivalence in review quality or measured token savings is claimed.
The inherited review/ADR copyright notice is consolidated into the root [LICENSE](../LICENSE) and copied into each local skill as `LICENSE.review-skills`, so direct per-skill downloads remain self-contained. External Superpowers and Ponytail skills retain their own upstream license files during managed installation.
Michael Nygard's Context / Decision / Consequences ADR structure is acknowledged.
