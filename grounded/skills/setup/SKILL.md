---
name: setup
description: Configure or refresh Grounded shared development rules after installing the plugin. Use when the user requests Grounded setup or selects plugin onboarding.
disable-model-invocation: true
---

# Grounded setup

Connect the bundled shared policy to the current host's user instructions. This affects future workspaces for that host; existing user instructions outside the managed block are preserved and changed files are backed up.

Resolve the plugin root from this skill's own location: two directories above `skills/setup/`. Do not resolve it from the user's project or hardcode a cache version. Verify `setup/manage.py` and `rules/development.md` exist there. If this skill was copied without the plugin assets, explain that the complete Grounded plugin is needed and stop.

Read `rules/development.md` from that plugin root once. Determine the active host from the runtime: `codex` or `claude`. Configure only that host unless the user explicitly requests both. If the host is unclear, ask which one. Explain the target instruction file and that the operation connects shared rules; it does not install OpenSpec, Superpowers, Ponytail or duplicate the plugin's review skills.

Run from the downloaded plugin, using its resolved absolute path:

```sh
python3 "<plugin-root>/setup/manage.py" configure --host <codex-or-claude> --dry-run
python3 "<plugin-root>/setup/manage.py" configure --host <codex-or-claude>
```

macOS or Linux and Python 3.11+ are required. Use the host's execution permissions. An explicit setup request authorizes this configuration; do not ask again unless the runtime requires approval. On malformed blocks, symbolic links or unsupported host paths, report the error and preserve the user's files rather than replacing them manually.

Report the plugin version, actual result and backup location. Setup records `grounded-version` inside the managed block. Start a new conversation to load the host instructions; in the current conversation use the policy already read. Rerun this setup after plugin updates to refresh the managed policy and version. Do not run the standalone `install` command alongside the native plugin.
