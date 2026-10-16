# skills

Development skills and plugins for Codex and Claude Code.

## Plugins

| Plugin | Skills | Purpose |
|---|---|---|
| [Grounded](grounded/) | `setup`, `adr`, `plan-review-ceo`, `plan-review-eng` | Shared-rule setup and optional architecture decisions, scope reviews, and engineering reviews alongside OpenSpec, Superpowers, and Ponytail. |

## Quick start

Install **Grounded** from its own marketplace. Add the source once on each computer; Codex downloads and manages the plugin, so no manual Git clone is required. This is a custom marketplace, separate from the public OpenAI directory.

For Codex, run these commands in a terminal:

```sh
codex plugin marketplace add reserver7/skills --ref main
codex plugin add grounded@grounded
```

Restart Codex or start a new session, then open `/plugins` to manage Grounded. The marketplace is named `grounded` and the plugin is `grounded@grounded`. This installation was verified with Codex CLI; Claude installation is documented separately in the [Grounded README](grounded/README.md).

| Host | After installation |
|---|---|
| Codex | `$grounded:adr`, `$grounded:plan-review-ceo`, `$grounded:plan-review-eng` |
| Claude Code | `/grounded:adr`, `/grounded:plan-review-ceo`, `/grounded:plan-review-eng` |

After marketplace installation, run `$grounded:setup` in Codex or `/grounded:setup` in Claude Code once per host, then start a new conversation. Setup installs Grounded's pinned OpenSpec, Superpowers, and Ponytail components, connects shared rules across workspaces, and archives overlapping local skills/plugins before disabling them. Unrelated personal skills remain. Rerun setup after plugin updates. See the [Grounded README](grounded/README.md) for prerequisites and backup details.

To update Codex's marketplace and refresh the plugin:

```sh
codex plugin marketplace upgrade grounded
codex plugin add grounded@grounded
```

Run `$grounded:setup` after updating to refresh shared rules. Releases keep their `skills-v<version>` tags and ZIP assets; the default marketplace source follows `main`.

## Repository structure

Grounded's skills, rules, documentation, dependency pins, assets, and setup tools live under [`grounded/`](grounded/). Root marketplace catalogs point to that package. Repository contribution and release practices are in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE). Sources and compatibility changes are documented in [grounded/SOURCES.md](grounded/SOURCES.md).
