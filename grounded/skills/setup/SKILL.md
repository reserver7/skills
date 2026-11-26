---
name: setup
description: Configure or refresh Grounded shared development rules after installing the plugin. Use when the user requests Grounded setup or selects plugin onboarding.
disable-model-invocation: true
---

# Grounded setup

Install the managed skill revisions and latest stable OpenSpec package, connect the shared policy to the current host, and move known overlapping local skills/plugins into a recoverable backup. This applies to future workspaces for that host.

Resolve the plugin root from this skill's own location: two directories above `skills/setup/`. Do not resolve it from the user's project or hardcode a cache version. Verify `setup/manage.py` and `rules/development.md` exist there. If this skill was copied without the plugin assets, explain that the complete Grounded plugin is needed and stop.

Read `rules/development.md` from that plugin root once. Determine the active host from the runtime: `codex` or `claude`. Configure only that host unless the user explicitly requests both. If the host is unclear, ask which one. The native plugin already supplies Grounded's ADR and plan review skills; setup installs only OpenSpec and selected implementation skills, including all 15 Superpowers v7 skills and Playwright CLI with managed Chromium, the ticket adapter, `frontend-design`, both Vercel UI/React skill sources, and ECC documentation workflows, avoiding a second copy of Grounded's own skills. Prefer an upstream license file; if it is absent, accept only an explicit license declaration in the official source README and report that basis. Do not synthesize or copy a license text that upstream did not provide. Addy's `ci-cd-and-automation` is the default for ordinary CI/CD; `api-and-interface-design` and `performance-optimization` are conditional on matching tasks. ECC's `database-migrations` is for nontrivial schema migrations, `mysql-patterns` is only for MySQL, and `deployment-patterns` is for complex progressive rollout. Setup backs up only declared managed skill collisions and known conflicting full plugins; unrelated skill folders stay untouched.

Run from the downloaded plugin, using its resolved absolute path:

```sh
python3 "<plugin-root>/setup/manage.py" setup --host <codex-or-claude> --dry-run
python3 "<plugin-root>/setup/manage.py" setup --host <codex-or-claude>
```

Superpowers design and execution workflows are explicit opt-ins. Setup installs the shared development policy for skill selection and omits Superpowers startup hooks.

The native plugin already declares the Context7 OAuth server. After setup, direct the user to the host's MCP connection controls to select Grounded's Context7 server and complete browser sign-in if needed. The host manages the OAuth session. Do not ask for an API key or create a project-level MCP entry.

Use `restore --host <host> --dry-run` to preview and `restore --host <host>` to restore the previous setup snapshot (or the pre-install state). Use `uninstall --host <host> --dry-run` to preview and `uninstall --host <host>` to remove unchanged Grounded-managed skills and policy. Both retain backups and preserve edited files. Grounded dependency versions come from local receipts and caches; restoring removed host marketplace plugins may use the host CLI and configured marketplace.

macOS or Linux, Python 3.11+, Git, Node.js 20.19+, and npm are required. Use the host's execution permissions. An explicit setup request authorizes this configuration; do not ask again unless the runtime requires approval. Setup resolves official stable releases and the latest Vercel UI/React skills, ECC documentation governance, and Anthropic skills revisions, then verifies immutable Git SHAs, license files or explicit upstream README declarations, and npm integrity before host changes. It backs up the host configuration and matching global skill folders, disables overlapping plugins, installs resolved dependencies, and writes the managed policy block. Backups are owner-only and retained. It leaves unrelated skills and project-level files untouched. On malformed blocks, symbolic links or unsupported host paths, report the error and preserve the user's files rather than replacing them manually.

Report the plugin version, resolved dependency versions, plugins disabled, and backup location. Setup records `grounded-version` inside the managed block. Start a new conversation to load the host instructions; in the current conversation use the policy already read. Rerun this setup after plugin updates to refresh the managed policy and dependencies. If recovery reports an incomplete operation, retain its pending record and backup path; address recovery before retrying setup.
