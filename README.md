# skills

[![Latest release](https://img.shields.io/github/v/release/reserver7/skills?filter=skills-v%2A&sort=semver)](https://github.com/reserver7/skills/releases/latest)

Development skills and plugins for Codex and Claude Code.

## Plugins

| Plugin | Skills | Purpose |
|---|---|---|
| [Grounded](grounded/) | `setup`, `adr`, `plan-review-ceo`, `plan-review-eng` | Shared-rule setup and optional architecture decisions, scope reviews, and engineering reviews alongside OpenSpec, Superpowers, and Ponytail. |

## Quick start

Grounded supports Codex marketplace installation. Claude Code currently uses a local clone; Claude marketplace distribution is planned but is not the supported installation path yet.

### Codex

Add the marketplace once per computer and install the plugin:

```sh
codex plugin marketplace add reserver7/skills --ref main
codex plugin add grounded@grounded
```

The marketplace is named `grounded` and the plugin is `grounded@grounded`. Codex installation was verified with Codex CLI. Start a new Codex conversation after installing.

### Claude Code (local clone)

Clone the repository once, then load Grounded from the target project with Claude Code's `--plugin-dir` option:

```sh
git clone https://github.com/reserver7/skills.git ~/grounded-skills
cd /path/to/your/project
claude --plugin-dir ~/grounded-skills/grounded
```

Start Claude from the same command after updating the clone. Run `/grounded:setup` once per host after installation and after plugin updates.

| Host | After installation |
|---|---|
| Codex | `$grounded:adr`, `$grounded:plan-review-ceo`, `$grounded:plan-review-eng` |
| Claude Code | `/grounded:adr`, `/grounded:plan-review-ceo`, `/grounded:plan-review-eng` |

After loading the plugin, run `$grounded:setup` in Codex or `/grounded:setup` in Claude Code once per host, then start a new conversation. Setup resolves the latest stable OpenSpec, Superpowers, and Ponytail releases, connects shared rules across workspaces, and archives overlapping local skills/plugins before disabling them. Unrelated personal skills remain. Rerun setup after plugin updates to refresh the persisted rules and `grounded-version` marker. See the [Grounded README](grounded/README.md) for prerequisites, restore/uninstall commands, and backup details.

Codex checks configured Git marketplaces at startup and refreshes installed plugins when their sources change. Grounded tracks `main`, so changes merged there become available on a subsequent Codex startup; a GitHub Release does not push an update to a running host.

To refresh immediately from a terminal:

```sh
codex plugin marketplace upgrade grounded
```

After each plugin update, rerun `$grounded:setup` to refresh the persisted policy and version marker. `codex plugin add grounded@grounded` is for initial installation, not routine updates. For Claude, update the clone with `git -C ~/grounded-skills pull --ff-only`, then start a new Claude session with `--plugin-dir ~/grounded-skills/grounded` and run `/grounded:setup`. Releases keep their `skills-v<version>` tags and ZIP assets; the Codex marketplace source follows `main`.

## Repository structure

Grounded's skills, rules, documentation, dependency sources, assets, and setup tools live under [`grounded/`](grounded/). Root marketplace catalogs point to that package. See the [changelog](CHANGELOG.md) for release history and [CONTRIBUTING.md](CONTRIBUTING.md) for contribution and release practices.

## License

MIT — see [LICENSE](LICENSE). Sources and compatibility changes are documented in [grounded/SOURCES.md](grounded/SOURCES.md).
