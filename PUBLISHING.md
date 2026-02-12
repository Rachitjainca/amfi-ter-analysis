# AMFI TER Analysis - Publishing Guide

## Publishing to PyPI

This guide explains how to publish the `amfi-ter-analysis` package to PyPI (Python Package Index).

### Prerequisites

1. **PyPI Account**: Create an account at https://pypi.org/
2. **Test PyPI Account** (Optional): https://test.pypi.org/ for testing

### Setup

#### 1. Install Build Tools
```bash
pip install build twine
```

#### 2. Create PyPI Token
- Go to https://pypi.org/manage/account/token/
- Create a new API token
- Save it securely

#### 3. Configure `~/.pypirc` (Optional but Recommended)
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

### Publishing Steps

#### 1. Update Version
Edit `pyproject.toml` and `setup.py`:
```
version = "1.0.1"  # Increment version
```

#### 2. Build Distribution
```bash
python -m build
```

This creates:
- `dist/amfi-ter-analysis-1.0.1.tar.gz` (source distribution)
- `dist/amfi-ter-analysis-1.0.1-py3-none-any.whl` (wheel distribution)

#### 3. Test Upload (Optional)
```bash
twine upload --repository testpypi dist/*
```

Then test installation:
```bash
pip install -i https://test.pypi.org/simple/ amfi-ter-analysis==1.0.1
```

#### 4. Publish to PyPI
```bash
twine upload dist/*
```

You'll be prompted for credentials (use `__token__` as username and your token as password).

#### 5. Verify Publication
Check https://pypi.org/project/amfi-ter-analysis/

### Installation After Publishing
```bash
pip install amfi-ter-analysis
```

### GitHub Release (Optional)

1. Create a tag:
   ```bash
   git tag -a v1.0.1 -m "Version 1.0.1"
   git push origin v1.0.1
   ```

2. Go to GitHub → Releases → Draft a new release
   - Select the tag
   - Add release notes
   - Upload `.tar.gz` and `.whl` files from `dist/`

### Version Numbering (Semantic Versioning)

- **MAJOR**.MINOR.PATCH (e.g., 1.0.1)
- MAJOR: Incompatible API changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible

### Automation with GitHub Actions (Optional)

Create `.github/workflows/publish.yml`:
```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install build tools
        run: pip install build twine
      - name: Build distribution
        run: python -m build
      - name: Publish to PyPI
        run: twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

### Troubleshooting

**"Invalid distribution"**
- Run: `twine check dist/*`
- Fix any issues and rebuild

**"Filename conflict"**
- Version already exists; increment version number

**"Authentication failed"**
- Verify token is correct
- Reset token on PyPI if needed

### Resources

- [PyPI Documentation](https://pypi.org/help/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [setuptools Documentation](https://setuptools.pypa.io/)

### Next Steps

1. ✅ Package structure created
2. ⏳ Manual: Update version in `pyproject.toml` and `setup.py`
3. ⏳ Manual: Create PyPI token
4. ⏳ Manual: Run `python -m build`
5. ⏳ Manual: Run `twine upload dist/*`

## Quick Reference

```bash
# Update version
# Edit pyproject.toml and setup.py

# Build
python -m build

# Test upload (optional)
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Clean build files
rm -rf build dist *.egg-info
```

## Support

For issues with publishing, check:
- https://pypi.org/project/amfi-ter-analysis/
- GitHub Issues: https://github.com/Rachitjainca/amfi-ter-analysis/issues
