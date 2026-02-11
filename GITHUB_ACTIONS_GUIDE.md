# GitHub Actions - AMFI TER Analysis Deployment Guide

## Setup Instructions

### 1. Initialize Git Repository
If you haven't already:
```bash
cd /path/to/AMFI
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/AMFI.git
git push -u origin main
```

### 2. Push to GitHub
```bash
git push origin main
```

### 3. Verify Workflow
- Go to your repository on GitHub
- Click on "Actions" tab
- You should see "AMFI TER Daily Analysis" workflow
- The workflow runs automatically every day at **9:00 AM IST (3:30 UTC)**

### 4. Manual Trigger
You can manually run the workflow:
1. Go to "Actions" tab
2. Click "AMFI TER Daily Analysis"
3. Click "Run workflow" button

---

## How It Works

### Daily Schedule
- **Time**: 9:00 AM IST (UTC+5:30) every day
- **Cron**: `30 3 * * *` (3:30 UTC = 9:00 AM IST)
- **Action**: Downloads latest TER file and compares with previous day

### File Output
Generated CSV files are saved to `output/` directory and automatically committed back to your repository:
- `Regular_Plan_TER_Changes_YYYY-MM-DD.csv` - Regular plan changes
- `Direct_Plan_TER_Changes_YYYY-MM-DD.csv` - Direct plan changes
- `Regular_vs_Direct_TER_Changes_YYYY-MM-DD.csv` - Comparison
- `ter_state.json` - State tracking (auto-updated)

### Logs
All execution logs are saved in `logs/ter_analysis.log`

---

## Directory Structure
```
AMFI/
├── .github/
│   └── workflows/
│       └── ter_analysis.yml          # GitHub Actions workflow
├── downloads/                          # Downloaded TER Excel files
├── output/                             # Generated CSV reports
├── logs/                               # Execution logs
├── history/                            # Historical data
├── ter_github_actions.py              # Main analysis script
├── ter_state.json                     # State file (tracked in git)
├── .gitignore                         # Git ignore rules
└── README.md
```

---

## File Structure in Repository

### GitHub Actions Workflow (.github/workflows/ter_analysis.yml)
- Runs on schedule (9:00 AM IST daily)
- Sets up Python 3.10 environment
- Installs dependencies (pandas, openpyxl, requests)
- Runs analysis script
- Automatically commits and pushes results

### Main Script (ter_github_actions.py)
**Key Features:**
- Downloads latest TER file from AMFI API
- Maintains state in `ter_state.json` (committed to git)
- Compares current day with previous day
- Detects month changes automatically
- Generates CSV reports for Regular and Direct plans
- Logs all operations

**State Management:**
```json
{
  "last_processed_date": "2026-02-11",
  "month_year": "2026-02",
  "file_history": {
    "2026-02": {
      "filepath": "downloads/TER_2026_02_20260211_090000.xlsx",
      "date": "2026-02-11"
    }
  },
  "daily_snapshots": {}
}
```

---

## Example Output

### Terminal Output
```
2026-02-11 09:00:15 - INFO - ============================================================
2026-02-11 09:00:15 - INFO - Starting AMFI TER Analysis
2026-02-11 09:00:15 - INFO - ============================================================
2026-02-11 09:00:15 - INFO - Current date: 2026-02-11
2026-02-11 09:00:15 - INFO - Last processed: 2026-02-10
2026-02-11 09:00:15 - INFO - Current month: 2026-02
2026-02-11 09:00:18 - INFO - Downloading TER file for 2026-2...
2026-02-11 09:00:21 - INFO - Downloaded: downloads/TER_2026_02_20260211_090018.xlsx
2026-02-11 09:00:21 - INFO - Read 1547 records from downloads/TER_2026_02_20260211_090018.xlsx
2026-02-11 09:00:22 - INFO - Comparing Regular Plan TER changes...
2026-02-11 09:00:22 - INFO - Regular Plan: 45 changes found
2026-02-11 09:00:22 - INFO - Saved to output/Regular_Plan_TER_Changes_2026-02-11.csv
2026-02-11 09:00:22 - INFO - Comparing Direct Plan TER changes...
2026-02-11 09:00:22 - INFO - Direct Plan: 38 changes found
2026-02-11 09:00:22 - INFO - Saved to output/Direct_Plan_TER_Changes_2026-02-11.csv
2026-02-11 09:00:23 - INFO - Regular vs Direct: 25 common schemes with changes
2026-02-11 09:00:23 - INFO - Saved to output/Regular_vs_Direct_TER_Changes_2026-02-11.csv
2026-02-11 09:00:24 - INFO - ============================================================
2026-02-11 09:00:24 - INFO - Analysis completed successfully
```

### Commit Message
```
Auto: AMFI TER Analysis - 2026-02-11 09:00:23
```

---

## Environment Variables

No additional environment variables needed. The workflow uses:
- `GITHUB_TOKEN` - Automatically available for Git operations
- Python 3.10 - Set in workflow configuration

---

## Troubleshooting

### Workflow Not Running
1. Check the "Actions" tab in your GitHub repository
2. Verify the workflow file is in `.github/workflows/ter_analysis.yml`
3. Ensure main branch is set as default branch
4. Wait for the scheduled time (9:00 AM IST) or manually trigger

### Workflow Failing
1. Click on the failed workflow run
2. Check "Build" logs for error messages
3. Common issues:
   - Network timeout: Check AMFI API availability
   - Git push failure: Check repository permissions
   - Python/dependency errors: Check workflow setup

### Files Not Committed
- The workflow uses `continue-on-error: true` for git operations
- If no changes, no commit is made (this is normal)
- Check logs to see what was generated

---

## Customization

### Change Execution Time
Edit `.github/workflows/ter_analysis.yml`, find the cron line:
```yaml
- cron: '30 3 * * *'  # Change this
```

Cron format: `minute hour day-of-month month day-of-week`
- `30 3 * * *` = 3:30 AM UTC (9:00 AM IST)
- `0 12 * * *` = 12:00 PM UTC (5:30 PM IST)

### Change Python Version
Edit `python-version: '3.10'` to desired version (3.8, 3.9, 3.11, etc.)

### Add Email Notifications
Contact GitHub Support or use third-party actions for email notifications on success/failure.

---

## Monitoring

### View Run History
1. Go to "Actions" tab in GitHub
2. Click "AMFI TER Daily Analysis"
3. View all past runs with status and logs

### View Generated Files
1. Go to the repository root
2. Browse `output/` folder to see all generated CSV files
3. Check `logs/ter_analysis.log` for execution details
4. Monitor `ter_state.json` for state changes

---

## Security Notes

- ✅ No secrets required
- ✅ No API authentication needed (AMFI API is public)
- ✅ GITHUB_TOKEN is automatically available and scoped
- ✅ All files are committed to your own repository
- ✅ No external credentials stored

---

## Support

If issues arise:
1. Check GitHub Actions logs in the repository
2. Review the workflow file syntax
3. Ensure all directories exist (they're created automatically)
4. Check network connectivity to AMFI API

