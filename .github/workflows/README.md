# GitHub Actions CI/CD

Workflows for continuous integration and release of `whatstk`.

## Workflows

### `ci-quick.yml` — fast feedback

**Triggers:** every push to any branch (version tags `v*` excluded), and pull requests.

**Runs:** a single job on Ubuntu / Python 3.13 — format, lint, type check, tests with coverage.

The job is skipped for pull requests that are *not* drafts, because a ready-for-review PR is
covered by `ci-full.yml` instead. The intent is one quick signal while you work, and the full
matrix once the PR is ready.

### `ci-full.yml` — full matrix

**Triggers:** pushes to `main` and `develop`; pull requests targeting `main` or `develop`
(including when a draft PR is marked ready for review); manual `workflow_dispatch`.

**Runs:** the same checks across 12 combinations — Ubuntu / macOS / Windows × Python 3.11, 3.12,
3.13, 3.14. Draft PRs are skipped by the `check-ready` job. Coverage is uploaded to Codecov only
from Ubuntu / Python 3.13 to avoid duplicate reports.

### `release.yml` — publish to PyPI

**Trigger:** a GitHub Release being **published**. Creating the tag alone does not start it.

**Jobs:**

1. `test-matrix` — the full 12-way matrix with `fail-fast: true`; any failure aborts the release.
2. `deploy-pypi` — `uv build` then publish via PyPI **trusted publishing**.

See [`../../AGENTS.md`](../../AGENTS.md) for the end-to-end release procedure.

## Steps run by every CI job

Each workflow drives the `Makefile`, so CI and local development stay in sync:

```bash
make .venv              # create the environment (uv sync --all-extras)
make generate-test-data # tests need generated chat fixtures
make check.format       # ruff format --check
make check.lint         # ruff check
make check.type         # pyright
make unittest           # pytest with coverage
```

Locally, `make test` runs the four check targets in one go.

## Configuration

### PyPI — trusted publishing

Publishing uses [trusted publishing](https://docs.pypi.org/trusted-publishers/); there is no API
token to rotate. The trusted publisher on PyPI is configured as:

- Owner: `lucasrodes`
- Repository: `whatstk`
- Workflow: `release.yml`
- Environment: `release`

The `deploy-pypi` job declares `environment: release` and `permissions: id-token: write`; both are
required for the OIDC exchange to work.

### Codecov

`CODECOV_TOKEN` is set as a repository secret. Uploads use `fail_ci_if_error: false`, so a Codecov
outage never fails a build. Thresholds live in [`../../codecov.yml`](../../codecov.yml).

### Read the Docs

Documentation builds are **not** driven from here. Read the Docs builds on its own webhook using
[`../../.readthedocs.yaml`](../../.readthedocs.yaml), which installs via `make install.rtd`.
