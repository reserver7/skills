---
name: setup
description: Configure or refresh Grounded shared development rules after installing the plugin. Use when the user requests Grounded setup or selects plugin onboarding.
disable-model-invocation: true
---

# Grounded setup

Install Grounded's pinned shared implementation skills and OpenSpec package, connect the shared policy to the current host, and move known overlapping local skills/plugins into a recoverable backup. This applies to future workspaces for that host.

Resolve the plugin root from this skill's own location: two directories above `skills/setup/`. Do not resolve it from the user's project or hardcode a cache version. Verify `setup/manage.py` and `rules/development.md` exist there. If this skill was copied without the plugin assets, explain that the complete Grounded plugin is needed and stop.

Read `rules/development.md` from that plugin root once. Determine the active host from the runtime: `codex` or `claude`. Configure only that host unless the user explicitly requests both. If the host is unclear, ask which one. The native plugin already supplies Grounded's ADR and review skills; setup installs only the pinned OpenSpec package and selected Superpowers/Ponytail skills, avoiding a second copy of Grounded's own skills.

Run from the downloaded plugin, using its resolved absolute path:

```sh
python3 "<plugin-root>/setup/manage.py" setup --host <codex-or-claude> --dry-run
python3 "<plugin-root>/setup/manage.py" setup --host <codex-or-claude>
```

macOS or Linux, Python 3.11+, Git, Node.js 20.19+, and npm are required. Use the host's execution permissions. An explicit setup request authorizes this configuration; do not ask again unless the runtime requires approval. Setup backs up the host configuration and matching global skill folders, disables overlapping plugins, installs the pinned dependencies, and writes the managed policy block. It leaves unrelated skills and project-level files untouched. On malformed blocks, symbolic links or unsupported host paths, report the error and preserve the user's files rather than replacing them manually.

Report the plugin version, installed dependencies, plugins disabled, and backup location. Setup records `grounded-version` inside the managed block. Start a new conversation to load the host instructions; in the current conversation use the policy already read. Rerun this setup after plugin updates to refresh the managed policy and dependencies.
