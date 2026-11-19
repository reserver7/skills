# Grounded

[![Latest release](https://img.shields.io/github/v/release/reserver7/skills?filter=skills-v%2A&sort=semver)](https://github.com/reserver7/skills/releases/latest)

Grounded is a shared engineering environment for Codex and Claude Code. One setup per host installs the managed skills and development policy. Use the skills that match the task.

- **Plan and implement.** Use OpenSpec for durable requirements, Ponytail for focused implementation, and Superpowers for debugging, TDD, code review, and verification. All 15 Superpowers v7 skills are available. Select its full planning and execution workflow explicitly.
- **Verify and ship.** Use the managed browser for QA, Vercel's rules for UI reviews, and dedicated guidance for API design, databases, security, performance, observability, and delivery.
- **Document and integrate.** Write release notes or update docs with `doc-updater`, run separate audits with `docs-governance`, and prepare tracker issues with `to-tickets`. The native plugin provides Context7 OAuth. Use `mcp-builder` when developing an MCP server.

See the [full skill inventory](grounded/README.md#skills-and-tools) and [Codex and Claude invocation guide](grounded/docs/workflow.md#skill-calls).

## Quick start

Setup requires macOS or Linux, Python 3.11+, Git, Node.js 20.19+, and npm. Install and authenticate your host before setup. See the [installation guide](grounded/README.md#quick-start) for details.

### Codex

Add the marketplace and install Grounded once per computer:

```sh
codex plugin marketplace add reserver7/skills --ref main
codex plugin add grounded@grounded
```

Start a new Codex conversation and run `$grounded:setup`.

### Claude Code

Clone once and launch Claude Code in the project with Grounded enabled:

```sh
git clone https://github.com/reserver7/skills.git ~/grounded-skills
cd /path/to/your/project
claude --plugin-dir ~/grounded-skills/grounded
```

Run `/grounded:setup` in Claude Code.

After setup, start a new conversation to load the shared rules. For technical documentation lookup, connect Grounded's Context7 server in the host's MCP controls and complete browser OAuth when prompted. [Context7 setup](grounded/README.md#context7-documentation-lookup)

## Update and restore

- **Codex:** The marketplace tracks `main`. To refresh immediately, run `codex plugin marketplace upgrade grounded`, start a new conversation, and rerun `$grounded:setup`.
- **Claude Code:** Run `git -C ~/grounded-skills pull --ff-only`, restart with the same `--plugin-dir`, and rerun `/grounded:setup`.

Setup resolves upstream versions again on each run and records the installed versions and commits locally. It backs up known overlapping skills and plugin data before migrating them. See [dependency selection](grounded/SOURCES.md) and [restore and uninstall](grounded/README.md#local-install-and-updates).

## Repository

| Reference | Purpose |
|---|---|
| [Grounded package](grounded/) | Skills, shared rules, installer, and host configuration |
| [Workflow and skill calls](grounded/docs/workflow.md) | Task ownership, invocation, and plan handoffs |
| [Changelog](CHANGELOG.md) | Release history and upgrade guidance |
| [Contributing](CONTRIBUTING.md) | Pull request and release procedure |

The repository is [MIT-licensed](LICENSE). Managed upstream skills retain their [applicable licenses](grounded/SOURCES.md).
