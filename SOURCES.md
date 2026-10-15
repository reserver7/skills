# Sources and compatibility changes

## External tools

| Source | Pinned version / commit | Installed content |
|---|---|---|
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | npm 1.12.0 | Official CLI under the managed private npm prefix; per-project skills generated only on explicit init |
| [Superpowers](https://github.com/obra/superpowers) | 7.0.0 / bb92a77741419a4ab5f06e711a283343f1ada0c3 | systematic-debugging, test-driven-development, verification-before-completion, requesting-code-review, receiving-code-review |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | 5.2.0 / 2961b52fc1fe6a5a87c7a959a79512e5c2f3ffe5 | ponytail skill only, no hooks |
| Local review and ADR skills | `skills/plan-review-ceo/`, `skills/plan-review-eng/`, `skills/adr/` | Standalone procedures extracted and adapted from the previous local implementation; no external review plugin installation or download |
| [Jev](https://typesafe.ai/) | Optional service, not bundled/pinned | Connection instructions only; configure current official provider separately |

External skill folders and their upstream root LICENSE files are copied from pinned Git checkouts during setup.
External trees are not vendored into this Git repository's new install path.
OpenSpec pins the top-level npm package; its transitive dependency closure is not fully locked by this repository.

## Deliberate adaptations

- Standalone Superpowers skill references lose the plugin-only `superpowers:` prefix.
- `requesting-code-review` uses [a portable adapter](setup/adapters/requesting-code-review.md), retaining upstream `code-reviewer.md`. It handles uncommitted work, existing OpenSpec/chat requirements, available reviewer tools and an explicit no-independent-review fallback. Trivial edits do not spawn reviewers.
- Full Superpowers bootstrap, brainstorming, writing-plans, execution pipelines and full Ponytail startup hooks are excluded to prevent duplicate control flow.
- Every installed skill has Codex invocation metadata. The three optional local skills are explicit-only in both hosts.
- CEO review retains the premise/existing-code/dream-state challenge, 2–3 alternatives, user-selected approach and scope mode, all eleven review sections (UX conditional), diagrams/rescue maps/test coverage, per-issue interaction, verdict and review note. Detailed section/rubric/template resources are loaded at the relevant phase.
- Engineering review retains standalone/CEO-reviewed intake, late-change detection, all four engineering sections, test ambition and coverage diagram, dependency table/parallel lanes/order/conflict analysis, ADR candidates, verdict and review note. Prior CEO facts/decisions are reused rather than re-interviewed; technical deltas are still checked.
- ADR retains intent/scope confirmation, six interview branches, three adversarial perspectives, the six-criterion gate (five passing; unresolved placeholders block), anti-monolith thresholds, required body sections and append-only supersession. Its gate label is not represented as a probability of correctness. Gaps/consequences must be evidence-backed, never fabricated to fill a quota.
- Environment-specific pitch/config/profile/catalog dependencies are replaced by existing OpenSpec/chat inputs and embedded defaults. Host-specific question APIs use the available host tool or direct chat. Automatic handoffs, extra PRDs/plans, duplicate code reviews and separate memory services are excluded; substantive review checks are not removed for token savings.
- Review notes use a host-neutral `.ai/reviews/` location (or the existing project convention). Notes carry reviewed-input evidence so later review can detect changed scope; they do not become a second plan. OpenSpec owns requirements/tasks and Superpowers/Ponytail own implementation.
- The common policy defines ownership and when SDD is unnecessary; it is not a second orchestrator or a copied implementation manual.

These are compatibility adaptations of preexisting local procedures and selected Superpowers skills. No equivalence in review quality or measured token savings is claimed.
The inherited review/ADR copyright notice is consolidated into the root [LICENSE](LICENSE), which is distributed with the three local skills. External Superpowers and Ponytail skills retain their own upstream license files during installation.
Michael Nygard's Context / Decision / Consequences ADR structure is acknowledged.
