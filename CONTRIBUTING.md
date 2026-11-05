# Contributing

## Branches

- `main` is the only long-lived branch and must stay releasable. Do not force-push or delete it.
- All changes to `main` go through a pull request so the required `validate` check can pass. Start from the latest `main` and use `feat/<slug>`, `fix/<slug>`, `docs/<slug>`, `chore/<slug>`, or `ci/<slug>` as appropriate.
- After merging, delete the working branch. Do not keep `develop`, `release`, or feature branches long-term.

The `main` ruleset requires the GitHub Actions check named `validate`, blocks force-pushes and deletion, and does not allow bypasses.

Example:

```sh
git switch main
git pull --ff-only
git switch -c feat/skill-install-check
# make and verify the change
git push -u origin feat/skill-install-check
# open a pull request to main
```

Use Conventional Commits for commit messages; see [`grounded/rules/development.md`](grounded/rules/development.md). PR titles and manually applied release-category labels feed the automatically generated GitHub Release notes, which list routine changes. Title prefixes do not assign labels. Update [`CHANGELOG.md`](CHANGELOG.md) only when the release needs durable rationale for a significant decision, compatibility or migration guidance, or measured evidence. Do not copy routine PR summaries into both places. The PR template asks for this context and uses `None` when no curated entry is needed.

## Releases

- Create a release tag only from an up-to-date commit on `main`.
- Tags use `skills-v<MAJOR>.<MINOR>.<PATCH>`, for example `skills-v0.1.1`.
- `grounded/plugin.json` is the canonical plugin version. Run `python3 grounded/setup/release.py bump <version>` on a release-preparation branch to synchronize it with `grounded/.claude-plugin/plugin.json`, and update `extensions.com.openai.publication.release_notes` to start with `Grounded <version>:`. Pull request CI checks the versioned release notes. Use the PR template for reviewer context and follow Conventional Commit title syntax; maintainers apply the release-category label manually. GitHub automatically generates release notes from merged PR titles and categories using `.github/release.yml`; those notes cover routine changes and link to [`CHANGELOG.md`](CHANGELOG.md) only for significant rationale, compatibility or migration guidance, and measured evidence. Update the changelog selectively; do not duplicate ordinary PR summaries. README release badges follow the latest published `skills-v*` tag automatically. Use PATCH for compatible fixes, MINOR for new capabilities, and MAJOR for incompatible changes; before 1.0, use MINOR for incompatible changes.
- Tag the merged version commit. CI requires that the tagged commit belongs to `main` and that both manifests exactly match the tag. A mismatched version stops the release; CI does not rewrite the tagged commit.
- Pushing a valid `skills-v*` tag publishes a GitHub Release with `grounded-<version>.zip`. Never move or reuse a published tag.
- Codex's custom marketplace tracks `main` and refreshes from the Git source when Codex starts; a release tag does not push to running clients. Claude Code currently loads the cloned `grounded/` directory with `claude --plugin-dir`; Claude marketplace distribution is planned separately. After updating either host's plugin source, rerun Grounded setup to refresh the persisted shared rules, resolve current stable dependencies, and update the version marker.

```sh
# On a release-preparation branch; commit and merge this change through a PR
python3 grounded/setup/release.py bump 0.1.1

# After the version change is merged into main
git switch main
git pull --ff-only
git tag -a skills-v0.1.1 -m "Grounded v0.1.1"
git push origin skills-v0.1.1
```

## GitHub protection

The repository is public, so anyone can view and fork it. Writing requires explicitly granted repository access; repository administration, including changing visibility or deleting the repository, is limited to owners and administrators.

An active ruleset targets `refs/heads/main` and blocks force-pushes and branch deletion. It has no bypass actors. Repository owners and administrators can still change or remove the ruleset, so keep repository access limited to trusted collaborators.
