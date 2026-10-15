# skills

Development skills and plugins for Codex and Claude Code.

## Plugins

| Plugin | Skills | Purpose |
|---|---|---|
| [Grounded](grounded/) | `setup`, `adr`, `plan-review-ceo`, `plan-review-eng` | Shared-rule setup and optional architecture decisions, scope reviews, and engineering reviews alongside OpenSpec, Superpowers, and Ponytail. |

## Quick start

Install **Grounded** from your host's plugin marketplace. No manual Git clone is required for plugin installation. Public directory listings become searchable after provider approval and publication; they are not published yet.

| Host | After installation |
|---|---|
| Codex | `$grounded:adr`, `$grounded:plan-review-ceo`, `$grounded:plan-review-eng` |
| Claude Code | `/grounded:adr`, `/grounded:plan-review-ceo`, `/grounded:plan-review-eng` |

After marketplace installation, run `$grounded:setup` in Codex or `/grounded:setup` in Claude Code once per host, then start a new conversation. Setup connects shared rules to the host's user instructions across workspaces, preserving personal instructions and backing up changes. Rerun setup after plugin updates to refresh the rules. External tools are configured separately; setup does not install duplicate review skills. See the [Grounded README](grounded/README.md).

## Repository structure

Grounded's skills, rules, documentation, dependency pins, assets, and setup tools live under [`grounded/`](grounded/). Root marketplace catalogs point to that package. Repository contribution and release practices are in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE). Sources and compatibility changes are documented in [grounded/SOURCES.md](grounded/SOURCES.md).
