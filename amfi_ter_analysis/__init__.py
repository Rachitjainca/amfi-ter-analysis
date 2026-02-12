"""
AMFI TER Analysis Package

A comprehensive tool for analyzing Total Expense Ratio (TER) data from AMFI (Association of Mutual Funds in India).
Includes daily automation, GitHub Actions integration, and detailed TER comparison reports.

Features:
- Automatic daily TER file downloads
- TER changes comparison and analysis
- Category-based filtering and grouping
- Google Chat notifications
- GitHub Actions workflow integration
- Comprehensive reporting and tracking

Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Rachit Jain"
__author_email__ = "rachit.jain@example.com"
__license__ = "MIT"

from .ter_analysis import (
    download_ter_file,
    read_ter_file,
    find_ter_columns,
    compare_ter_data,
    analyze_ter_changes
)

from .ter_daily_automation import (
    get_current_month_year,
    load_state,
    save_state
)

from .ter_github_actions import (
    analyze_and_report
)

__all__ = [
    'download_ter_file',
    'read_ter_file',
    'find_ter_columns',
    'compare_ter_data',
    'analyze_ter_changes',
    'get_current_month_year',
    'load_state',
    'save_state',
    'analyze_and_report'
]
