# Changelog — Grounded

This file records release context that cannot be recovered from a list of pull request titles: significant design decisions, compatibility or migration guidance, and measured results. Routine changes are listed in the automatically generated GitHub Release notes and do not need a second entry here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html). The canonical plugin version is declared in [`grounded/plugin.json`](grounded/plugin.json). Git tags use `skills-v<version>`.

## [0.4.0] — 2026-11-05

### Changed

- Setup resolves the latest stable OpenSpec npm dist-tag and latest stable Superpowers/Ponytail GitHub releases, verifies immutable package integrity or commit SHAs, and records the selected versions locally. Restore uses retained receipts and caches without resolving newer releases.
- Added `restore` and `uninstall` manager commands. They preserve edited managed files and retain owner-only backups; incomplete recovery leaves a pending record and reports affected paths.
- Kept CI to the existing validation suite plus `manage.py check`; Actions are pinned to full commit SHAs with weekly Dependabot updates. Release-category PR labels remain manual.

The setup policy now favors current upstream releases while preserving reproducibility through local receipts and immutable artifact identities. Setup resolves candidates before changing host state. Users can restore the previous successful environment or uninstall unchanged Grounded-managed files; edited content is retained, and owner-only backups remain available for manual recovery. Codex marketplace restoration may contact the configured marketplace because the CLI does not provide an offline version-selecting restore operation.

Routine repository maintenance and release automation changes are covered by the generated GitHub Release notes. Keep entries here for durable decision context, compatibility or migration guidance, or measured evidence that a PR title cannot convey.

## [0.3.0] — 2026-10-16

This release added the one-step Grounded environment setup and moved the Codex installation to the repository's custom marketplace.

### Added

- A setup entry point that installs pinned shared skills, applies managed host rules, and keeps recoverable backups.
- Codex marketplace installation instructions and a published plugin package.

## [0.2.0] — 2026-10-15

This release prepared Grounded for native Codex and Claude plugin installation, consolidating the skills and shared-rule setup in one repository.

### Added

- Native plugin directory packages for Codex and Claude Code.
- Shared-rule setup and the initial branch and release process.

## [0.1.0] — 2026-10-15

Initial public repository release.
