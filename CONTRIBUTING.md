# Contributing

## Branches

- `main` is the only long-lived branch and must stay releasable. Do not force-push or delete it.
- A trivial typo or similarly small documentation correction may go directly to `main`.
- Changes to skills, shared rules, setup, the manifest, or release automation use a short-lived branch and pull request. Start from the latest `main` and use `feat/<slug>`, `fix/<slug>`, `docs/<slug>`, `chore/<slug>`, or `ci/<slug>` as appropriate.
- After merging, delete the working branch. Do not keep `develop`, `release`, or feature branches long-term.

Example:

```sh
git switch main
git pull --ff-only
git switch -c feat/skill-install-check
# make and verify the change
git push -u origin feat/skill-install-check
# open a pull request to main
```

Use Conventional Commits for commit messages; see [`grounded/rules/development.md`](grounded/rules/development.md).

## Releases

- Create a release tag only from an up-to-date commit on `main`.
- Tags use `skills-v<MAJOR>.<MINOR>.<PATCH>`, for example `skills-v0.1.1`.
- `grounded/plugin.json` is the canonical plugin version. Run `python3 grounded/setup/release.py bump <version>` on a release-preparation branch to synchronize it with `grounded/.claude-plugin/plugin.json`, then merge the change through a pull request. Use PATCH for compatible fixes, MINOR for new capabilities, and MAJOR for incompatible changes; before 1.0, use MINOR for incompatible changes.
- Tag the merged version commit. CI requires that the tagged commit belongs to `main` and that both manifests exactly match the tag. A mismatched version stops the release; CI does not rewrite the tagged commit.
- Pushing a valid `skills-v*` tag publishes a GitHub Release with `grounded-<version>.zip`. Never move or reuse a published tag.
- GitHub releases do not submit or publish provider marketplace updates. Use the same tagged version/source and ZIP for each provider's update process. After users update the plugin, rerun Grounded setup to refresh its persisted shared rules.

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
