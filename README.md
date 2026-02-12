# AMFI TER Analysis - Package Distribution

## Installation

### PyPI (Recommended)
```bash
pip install amfi-ter-analysis
```

### Development Installation
```bash
git clone https://github.com/Rachitjainca/amfi-ter-analysis.git
cd amfi-ter-analysis
pip install -e ".[dev]"
```

### From Source
```bash
pip install .
```

## Quick Start

### Using as a Python Package
```python
from amfi_ter_analysis import download_ter_file, read_ter_file, find_ter_columns
from amfi_ter_analysis import analyze_ter_changes

# Download TER files
jan_file = download_ter_file(1, 2026)
feb_file = download_ter_file(2, 2026)

# Read and analyze
jan_df = read_ter_file(jan_file)
feb_df = read_ter_file(feb_file)

# Get changes
regular_changes, direct_changes = analyze_ter_changes(jan_df, feb_df)
```

### Using Daily Automation
```python
from amfi_ter_analysis import ter_daily_automation

# Run daily analysis
ter_daily_automation.main()
```

### Command Line Tool
```bash
amfi-ter-analysis
```

## Features

- ✅ Automatic daily TER file downloads
- ✅ TER changes comparison and analysis  
- ✅ Category-based filtering and grouping
- ✅ Google Chat notifications
- ✅ GitHub Actions workflow integration
- ✅ Comprehensive reporting and tracking
- ✅ Daily automation with state management

## Documentation

- [Quick Start Guide](QUICKSTART.md)
- [Automation Guide](AUTOMATION_GUIDE.md)
- [GitHub Actions Setup](GITHUB_ACTIONS_GUIDE.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
- [Google Chat Integration](GOOGLE_CHAT_SETUP.md)

## Requirements

- Python 3.8+
- pandas >= 1.3.0
- openpyxl >= 3.7.0
- requests >= 2.26.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Rachit Jain

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and feature requests, please visit: https://github.com/Rachitjainca/amfi-ter-analysis/issues
