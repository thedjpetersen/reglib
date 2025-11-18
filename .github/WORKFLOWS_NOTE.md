# GitHub Actions Workflows

The workflow files are ready but cannot be pushed via API due to GitHub security restrictions.

## To Add Workflows:

1. **Via GitHub UI:**
   - Go to your repository on GitHub
   - Click "Add file" → "Create new file"
   - Name it `.github/workflows/ci.yml`
   - Copy contents from the local `.github/workflows/ci.yml` file
   - Repeat for `docs.yml` and `release.yml`

2. **Or via git with local credentials:**
   ```bash
   git add .github/workflows/
   git commit -m "Add GitHub Actions workflows"
   git push
   ```

## Workflow Files Available:

- **ci.yml**: Continuous Integration
  - Tests on Python 3.8-3.12
  - Linting with ruff
  - Type checking with mypy
  - Security scanning with bandit
  - Code coverage reporting

- **docs.yml**: Documentation Building
  - Builds Sphinx documentation
  - Uploads artifacts

- **release.yml**: Release Automation
  - Publishes to PyPI on tags
  - Creates GitHub releases

All workflow files are in `.github/workflows/` directory.
