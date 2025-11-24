# GitHub Secrets Setup Guide

This guide walks you through setting up the required secrets for CI/CD workflows.

## Required Secrets

You need to configure three secrets in your GitHub repository:

### 1. CODECOV_TOKEN (Optional but Recommended)

**Purpose**: Uploads test coverage reports to Codecov for tracking code coverage over time.

**How to get it:**
1. Go to https://codecov.io
2. Sign in with your GitHub account
3. Click "Add new repository"
4. Find and add `lucasrodes/whatstk`
5. Go to repository settings in Codecov
6. Copy the "Repository Upload Token"

**Add to GitHub:**
1. Go to https://github.com/lucasrodes/whatstk/settings/secrets/actions
2. Click "New repository secret"
3. Name: `CODECOV_TOKEN`
4. Value: Paste the token from Codecov
5. Click "Add secret"

**Skip if**: You don't want coverage tracking (workflow will continue without it)

---

### 2. PYPI_API_TOKEN (Required for Releases)

**Purpose**: Allows GitHub Actions to publish your package to PyPI when you create a release.

**How to get it:**
1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: `whatstk-github-actions`
4. Scope: Select "Project: whatstk" (more secure than account-wide)
5. Click "Add token"
6. **IMPORTANT**: Copy the token immediately (starts with `pypi-`)
7. Save it securely - you won't see it again!

**Add to GitHub:**
1. Go to https://github.com/lucasrodes/whatstk/settings/secrets/actions
2. Click "New repository secret"
3. Name: `PYPI_API_TOKEN`
4. Value: Paste the token (should start with `pypi-`)
5. Click "Add secret"

**Alternative - Trusted Publishing (More Secure):**

Instead of using an API token, you can set up trusted publishing:

1. Go to https://pypi.org/manage/project/whatstk/settings/publishing/
2. Click "Add a new publisher"
3. Fill in:
   - PyPI Project Name: `whatstk`
   - Owner: `lucasrodes`
   - Repository name: `whatstk`
   - Workflow name: `release.yml`
   - Environment name: (leave empty)
4. Click "Add"

Then update `.github/workflows/release.yml` and remove the `password` line:
```yaml
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  # Remove the 'with: password:' section entirely
```

Trusted publishing is more secure as it doesn't require storing tokens.

---

### 3. READTHEDOCS_WEBHOOK_TOKEN (Optional)

**Purpose**: Triggers a documentation rebuild on ReadTheDocs when you create a release.

**How to get it:**
1. Go to https://readthedocs.org/projects/whatstk/
2. Click "Admin" → "Integrations"
3. Find or create a "GitHub incoming webhook"
4. Copy the webhook URL - it should look like:
   ```
   https://readthedocs.org/api/v2/webhook/whatstk/{project-id}/
   ```
5. The token is the last part of the URL (the project ID)

**Add to GitHub:**
1. Go to https://github.com/lucasrodes/whatstk/settings/secrets/actions
2. Click "New repository secret"
3. Name: `READTHEDOCS_WEBHOOK_TOKEN`
4. Value: Paste the token/project ID
5. Click "Add secret"

**Skip if**: You don't need automatic doc rebuilds (ReadTheDocs will still build on push)

---

## Verifying Setup

### After Adding Secrets

1. Go to https://github.com/lucasrodes/whatstk/settings/secrets/actions
2. You should see all three secrets listed (values will be hidden)
3. Secrets are ready to use!

### Testing the Workflows

**Test CI workflow:**
```bash
git add .github/
git commit -m "Add GitHub Actions workflows"
git push
```
Then check: https://github.com/lucasrodes/whatstk/actions

**Test Release workflow:**
1. Create a tag: `git tag v0.7.2-test`
2. Push tag: `git push origin v0.7.2-test`
3. Or create a GitHub release through the web interface

---

## Security Notes

- ✅ Secrets are encrypted and never exposed in logs
- ✅ Secrets are only available to workflows in your repository
- ✅ You can rotate/update secrets anytime in GitHub settings
- ⚠️ Never commit tokens directly to your repository
- ⚠️ Don't share token values in issues or pull requests
- 💡 Trusted publishing (PyPI) is more secure than API tokens

---

## Troubleshooting

**"Secret not found" error:**
- Check secret name matches exactly (case-sensitive)
- Verify secret was added to repository (not organization or user)
- Secrets may take a minute to become available

**PyPI publishing fails:**
- Verify token has correct scope (project-level, not test PyPI)
- Check token hasn't expired
- Ensure package version doesn't already exist on PyPI

**Codecov upload fails:**
- This is non-critical; workflow will continue
- Verify token is from correct repository
- Check Codecov service status

**ReadTheDocs doesn't rebuild:**
- Verify webhook token is correct
- Check ReadTheDocs build logs
- Ensure webhook is enabled in ReadTheDocs settings

---

## Quick Checklist

- [ ] Add CODECOV_TOKEN secret (optional)
- [ ] Add PYPI_API_TOKEN secret (or set up trusted publishing)
- [ ] Add READTHEDOCS_WEBHOOK_TOKEN secret (optional)
- [ ] Test workflows by pushing to a branch
- [ ] Verify secrets work by checking Actions tab
- [ ] Disable Travis CI once GitHub Actions confirmed working
- [ ] Update README badges to show GitHub Actions status
