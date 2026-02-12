# Contributing to AMFI TER Analysis

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Report issues professionally

## Getting Started

### Fork and Clone
```bash
git clone https://github.com/YOUR-USERNAME/amfi-ter-analysis.git
cd amfi-ter-analysis
```

### Setup Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### Run Tests
```bash
pytest tests/
pytest --cov=amfi_ter_analysis  # With coverage
```

### Code Style
```bash
# Format code
black amfi_ter_analysis/

# Check style
flake8 amfi_ter_analysis/

# Type checking
mypy amfi_ter_analysis/
```

## Making Changes

### Branch Naming
- Feature: `feature/description`
- Bug fix: `bugfix/description`
- Documentation: `docs/description`

Example:
```bash
git checkout -b feature/add-caching
```

### Commit Messages
- Clear and descriptive
- Present tense ("Add feature" not "Added feature")
- Reference issues: "Fix #123"

### Pull Request Process

1. **Create PR** with:
   - Clear title and description
   - Reference to related issues
   - List of changes (what and why)

2. **PR Checks**:
   - All tests must pass
   - Code style must be consistent
   - No new warnings

3. **Review**:
   - Address feedback constructively
   - Keep PRs focused and manageable

4. **Merge**:
   - Squash commits if appropriate
   - Delete branch after merge

## Reporting Issues

### Bug Reports
Include:
- Python version
- OS and environment
- Minimal reproducible example
- Error messages and traceback

### Feature Requests
Include:
- Use case and motivation
- Expected behavior
- Alternative approaches considered

## Documentation

- Update docstrings for code changes
- Keep README.md current
- Add examples for new features
- Update changelog/version notes

## Package Structure

```
amfi_ter_analysis/
├── __init__.py           # Package exports
├── ter_analysis.py       # Core analysis functions
├── ter_daily_automation.py   # Daily automation
└── ter_github_actions.py     # GitHub Actions integration
```

## Testing Guidelines

```python
# Example test structure
def test_download_ter_file():
    """Test TER file download functionality"""
    result = download_ter_file(2, 2026)
    assert result is not None
    assert os.path.exists(result)

def test_read_ter_file():
    """Test Excel file reading"""
    df = read_ter_file("test_data.xlsx")
    assert df is not None
    assert len(df) > 0
```

## Version Bumping

1. Update `pyproject.toml`
2. Update `setup.py`
3. Update `CHANGELOG.md`
4. Commit: "Bump version to X.Y.Z"
5. Tag: `git tag vX.Y.Z`
6. Push: `git push origin main --tags`

## Release Process

1. Ensure all tests pass: `pytest`
2. Run linters: `flake8`, `black --check`, `mypy`
3. Build: `python -m build`
4. Check distribution: `twine check dist/*`
5. Upload: `twine upload dist/*`

## Questions?

- Open an issue
- Discussions: GitHub Discussions
- Email: rachit.jain@example.com

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Git Workflow](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)

---

Happy contributing! 🎉
