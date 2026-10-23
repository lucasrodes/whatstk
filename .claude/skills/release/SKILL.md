---
name: release
description: Cut and publish a whatstk release to PyPI. Use when the user asks to release, ship, publish, cut a version, or bump the version of whatstk — e.g. "release 0.9.0", "let's ship a patch", "publish to PyPI".
---

# Releasing whatstk

Publishing is irreversible: a version number can never be reused on PyPI, and a bad release reaches
every user via `pip install`. Work through the steps in order and do not skip verification.

## Step 0 — Preconditions

Confirm all of these before touching anything:

```bash
git rev-parse --abbrev-ref HEAD    # must be: develop
git status --porcelain             # must be empty
git log --oneline origin/main..origin/develop   # the work being released
gh run list --branch develop --limit 5          # CI must be green
```

Also confirm with the user:

- Everything intended for this release is already merged into `develop`.
- The version number and bump type (see below).

If `develop` and `main` are identical there is nothing to release — stop and say so.

## Step 1 — Choose the version

whatstk uses semantic versioning. Current version: see `[project] version` in `pyproject.toml`.

| Bump | Target | Use when |
| ---- | ------ | -------- |
| `make bump.patch` | 0.8.1 → 0.8.2 | Bug fixes only, no API change |
| `make bump.minor` | 0.8.1 → 0.9.0 | New features, deprecations, dependency floor changes |
| `make bump.major` | 0.8.1 → 1.0.0 | Breaking API changes |

Dropping a Python version or changing the output DataFrame schema is at minimum a **minor** bump.

> **Never run `bump-my-version` directly.** A bare `bump-my-version bump patch` produces
> `0.8.2.dev0`, not `0.8.2`, because of the optional `pre` part in the serialize config. The make
> targets compute the version explicitly. Append `--pre` to a make target only if you deliberately
> want a `.dev0` pre-release.

## Step 2 — Cut the release branch

```bash
git checkout develop
git pull origin develop
git checkout -b release/X.Y.Z
```

## Step 3 — Bump the version

```bash
make bump.patch     # or bump.minor / bump.major
```

This creates one commit, `Bump version: A.B.C → X.Y.Z`, touching four files:
`pyproject.toml` (both `[project] version` and `[tool.bumpversion] current_version`),
`whatstk/__init__.py`, `docs/conf.py` and the PyPI badge in `README.md`.

Verify all four moved together — a partial bump ships a package whose `__version__` disagrees with
its metadata:

```bash
git show --stat HEAD
grep -rn "X\.Y\.Z" pyproject.toml whatstk/__init__.py docs/conf.py README.md
```

No tag is created at this point (`tag = false` in the bumpversion config). The tag comes from the
GitHub Release in step 6.

## Step 4 — Update the changelog

Add a section at the top of `docs/source/changelog.rst`, matching the existing style — a bulleted
list of **user-visible** changes with bold category prefixes, followed by the collapsible
`git_changelog` block:

```rst
vX.Y.Z
------

- **Bug fixes**: ...
- **Parser**: ...

.. container:: toggle

    **Show all commits**

    .. git_changelog::
        :rev-list: vA.B.C..HEAD
```

Set `:rev-list:` to span from the previous release tag. Derive the entries from
`git log --oneline vA.B.C..HEAD`, but write them for users, not as a commit dump. Commit:

```bash
git add docs/source/changelog.rst
git commit -m "add changelog for vX.Y.Z"
```

## Step 5 — Validate, then merge to main

```bash
make test        # format, lint, typecheck, unit tests
make docs        # must not add new warnings
```

Then open the PR **against `main`**:

```bash
git push -u origin release/X.Y.Z
gh pr create --base main --title "Release X.Y.Z" --body "..."
```

Wait for `ci-full.yml` — all 12 OS/Python combinations — to pass. Do not merge on a red or pending
matrix; `release.yml` runs the same matrix with `fail-fast: true` and will abort the publish anyway.

Merge once green.

## Step 6 — Publish

Creating the GitHub Release is what triggers publication. The tag is created by this step; it must
be `vX.Y.Z` (leading `v`) and must target `main`.

```bash
git checkout main && git pull origin main
gh release create vX.Y.Z --target main --title "vX.Y.Z" --notes "..."
```

This starts `release.yml`: the full test matrix, then `uv build` and a PyPI publish via trusted
publishing (no token involved). Watch it:

```bash
gh run watch "$(gh run list --workflow=release.yml --limit 1 --json databaseId --jq '.[0].databaseId')"
```

**Confirm with the user before running this command** — it is the irreversible step.

## Step 7 — Verify the published release

```bash
# PyPI has the new version (allow a minute for the index to update)
curl -s https://pypi.org/pypi/whatstk/json | python -c "import json,sys; print(json.load(sys.stdin)['info']['version'])"

# A clean install of the published artifact actually works
uv run --isolated --no-project --with "whatstk==X.Y.Z" python -c "import whatstk; print(whatstk.__version__)"
```

Also check that Read the Docs has built the new version at
<https://whatstk.readthedocs.io/en/latest/> — it builds from its own webhook, not from CI, so a
failure here is silent.

## Step 8 — Back-merge into develop

Easy to forget, and skipping it makes `develop` drift behind `main` so the next release re-applies
the bump commit.

```bash
git checkout develop
git pull origin develop
git merge --no-ff main
git push origin develop
git log --oneline origin/main..origin/develop   # expect: empty
```

Finally, delete the release branch and report to the user: version published, PyPI URL, release
notes URL, and whether RTD rebuilt.

## If something goes wrong

- **Matrix fails in `release.yml`:** nothing was published. Fix on a branch off `main`, then delete
  the GitHub Release *and* its tag before retrying — re-publishing requires a fresh release event.
- **Publish failed after a partial upload:** the version is burned on PyPI. Do not attempt to reuse
  it; bump to the next patch version and release again.
- **Bad release already on PyPI:** yank it (`pypi.org` → Manage → Yank) rather than deleting, then
  ship a fixed patch version. Yanking leaves existing pins working while hiding it from new installs.
