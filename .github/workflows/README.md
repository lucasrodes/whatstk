# GitHub Actions CI/CD

This directory contains GitHub Actions workflows for continuous integration and deployment.

## Workflows

### `test.yml` - Continuous Integration

**Triggers:**
- Push to any branch
- Pull requests to `main` or `develop`

**Jobs:**
- **Matrix Testing**: Tests across multiple Python versions (3.11, 3.12, 3.13, 3.14) and operating systems (Ubuntu, macOS, Windows)
- **Quality Checks**: Runs formatting, linting, and type checking
- **Test Suite**: Executes unit tests with coverage
- **Coverage Upload**: Uploads coverage report to Codecov (Ubuntu + Python 3.13 only)

### `release.yml` - Release & Deployment

**Triggers:**
- GitHub releases (published)
- Tags matching `v*` pattern

**Jobs:**
1. **Test**: Runs full test suite before deployment
2. **Deploy to PyPI**: Builds and publishes package to PyPI using trusted publishing
3. **Trigger Docs**: Triggers ReadTheDocs rebuild via webhook

## Required Secrets

Configure these secrets in your GitHub repository settings:

### For Codecov (optional)
- `CODECOV_TOKEN`: Token from codecov.io for uploading coverage reports

### For PyPI Deployment
- `PYPI_API_TOKEN`: API token from PyPI for package publishing
  - Get from: https://pypi.org/manage/account/token/

### For ReadTheDocs (optional)
- `READTHEDOCS_WEBHOOK_TOKEN`: Webhook token from ReadTheDocs
  - Get from: ReadTheDocs project → Admin → Integrations

## Migration from Travis CI

This setup replaces `.travis.yml` with the following improvements:

- **Faster builds**: GitHub Actions typically faster than Travis CI
- **Better integration**: Native GitHub integration, no external service
- **More flexibility**: Easier to customize and extend
- **Modern tooling**: Uses uv for fast dependency installation
- **Trusted publishing**: Secure PyPI publishing without storing passwords

## Setup Instructions

### 1. Enable GitHub Actions
GitHub Actions are enabled by default. Just push these workflow files.

### 2. Configure PyPI Trusted Publishing (Recommended)

Instead of using API tokens, set up trusted publishing:

1. Go to PyPI project settings
2. Navigate to "Publishing" section
3. Add GitHub as a trusted publisher:
   - Owner: `lucasrodes`
   - Repository: `whatstk`
   - Workflow: `release.yml`
   - Environment: (leave empty)

Then remove the `password` line from `release.yml` and GitHub will authenticate automatically.

### 3. Set up Codecov (if using)

1. Go to https://codecov.io and sign in with GitHub
2. Add the repository
3. Copy the token and add as `CODECOV_TOKEN` secret in GitHub

### 4. Set up ReadTheDocs webhook (if needed)

1. Go to ReadTheDocs project settings
2. Admin → Integrations → Add integration
3. Copy the webhook URL and token
4. Add `READTHEDOCS_WEBHOOK_TOKEN` as GitHub secret

## Local Testing

Test the same checks that run in CI:

```bash
# Run all checks
make check.format  # Format code
make check.lint    # Check linting
make check.type  # Type checking
make unittest   # Run tests

# Or run the full CI suite
make test
```

## Notes

- The `test.yml` workflow continues on linting errors (they don't fail the build)
- Coverage is only uploaded from Ubuntu + Python 3.13 to avoid duplicates
- ReadTheDocs is triggered after successful PyPI deployment on releases
- All workflows use uv for fast dependency resolution and installation
