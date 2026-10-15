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

Use Conventional Commits for commit messages; see [`rules/development.md`](rules/development.md).

## Releases

- Create a release tag only from an up-to-date commit on `main`.
- Tags use `skills-v<MAJOR>.<MINOR>.<PATCH>`, for example `skills-v0.1.1`.
- Pushing a `skills-v*` tag runs the release workflow and publishes a GitHub Release. Never move or reuse a published tag.

```sh
git switch main
git pull --ff-only
git tag -a skills-v0.1.1 -m "skills v0.1.1"
git push origin skills-v0.1.1
```

## GitHub protection

The repository is public, so anyone can view and fork it. Writing requires explicitly granted repository access; repository administration, including changing visibility or deleting the repository, is limited to owners and administrators.

An active ruleset targets `refs/heads/main` and blocks force-pushes and branch deletion. It has no bypass actors. Repository owners and administrators can still change or remove the ruleset, so keep repository access limited to trusted collaborators.
