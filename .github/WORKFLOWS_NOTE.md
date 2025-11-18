# GitHub Actions Workflows

⚠️ **Note**: The workflow files are ready in `.github/workflows/` but are **intentionally untracked**
because they cannot be pushed via GitHub API (requires 'workflows' permission).

## Current Status

The following workflow files are ready and tested locally:
- ✅ `.github/workflows/ci.yml` - Continuous Integration
- ✅ `.github/workflows/docs.yml` - Documentation Building
- ✅ `.github/workflows/release.yml` - Release Automation

They are **intentionally left untracked** to avoid git status warnings.

## How to Add Workflows:

### Option 1: Via GitHub UI (Recommended)

1. Go to your repository on GitHub
2. Navigate to `.github/workflows/`
3. Click "Add file" → "Create new file"
4. Copy content from local files:
   - `ci.yml`
   - `docs.yml`
   - `release.yml`
5. Commit directly to your branch

### Option 2: Via Local Git (If You Have Push Access)

```bash
cd /path/to/reglib
git add .github/workflows/
git commit -m "Add GitHub Actions workflows"
git push
```

This will work if you're pushing with your own GitHub credentials (not via API).

### Option 3: Ignore Them

If you don't want to use GitHub Actions, add to `.gitignore`:
```
.github/workflows/
```

## What Each Workflow Does:

### ci.yml - Continuous Integration
- Runs on: Push to main/master/develop and all PRs
- Tests on Python 3.8, 3.9, 3.10, 3.11, 3.12
- Runs: pytest, ruff (lint), mypy (type check), bandit (security)
- Uploads coverage to Codecov
- Validates package build

### docs.yml - Documentation
- Runs on: Push and PRs to main/master
- Builds Sphinx documentation
- Uploads documentation artifacts

### release.yml - Automated Releases
- Runs on: Version tags (v*)
- Builds and publishes to PyPI
- Creates GitHub releases with artifacts
- Handles pre-releases (alpha, beta, rc)

## After Adding Workflows

Once added, all PRs will automatically:
1. Run tests on all Python versions
2. Check code quality (linting, types)
3. Scan for security issues
4. Validate the package builds correctly

This ensures code quality and catches issues before merging!

---

**Status**: Workflows are ready but need manual addition to repository.
