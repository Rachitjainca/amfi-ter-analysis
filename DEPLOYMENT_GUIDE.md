# AMFI TER Analysis - GitHub Actions Deployment

## Quick Start Guide

### 1. Create GitHub Repository
```bash
# If not already created
echo "# AMFI TER Analysis" >> README.md
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/amfi-ter-analysis.git
git push -u origin main
```

### 2. Repository Settings
1. Go to **Settings** → **Actions** → **General**
2. Enable **Allow all actions and reusable workflows**
3. Select **Read and write permissions** for GITHUB_TOKEN
4. Click **Save**

### 3. Verify Configuration
1. Go to **Actions** tab
2. You should see **"AMFI TER Daily Analysis"** workflow
3. Workflow runs every day at **9:00 AM IST (3:30 UTC)**

---

## Features

✅ **Automatic Daily Execution** - Runs every day at 9:00 AM IST  
✅ **Month Change Detection** - Automatically handles month transitions  
✅ **Day-to-Day Comparison** - Compares current day with previous day  
✅ **CSV Report Generation** - Outputs for Regular, Direct, and comparison analyses  
✅ **Auto-Commit Results** - Results are pushed back to repository  
✅ **Comprehensive Logging** - All operations logged for debugging  
✅ **No Secrets Required** - No API keys or credentials needed  

---

## What Gets Generated

### Daily Output Files
Located in `output/` directory (date format: YYYY-MM-DD):

| File | Content |
|------|---------|
| `Regular_Plan_TER_Changes_YYYY-MM-DD.csv` | Regular plan TER changes |
| `Direct_Plan_TER_Changes_YYYY-MM-DD.csv` | Direct plan TER changes |
| `Regular_vs_Direct_TER_Changes_YYYY-MM-DD.csv` | Comparison of changes |

### State Management
- `ter_state.json` - Tracks last processed date, current month, file history
- `downloads/` - Contains downloaded TER Excel files
- `logs/ter_analysis.log` - Execution logs

---

## How It Works

### Daily Execution Flow

```
9:00 AM IST
    ↓
GitHub Actions Triggers
    ↓
Download latest TER file from AMFI API
    ↓
Check if month changed
    ├─ YES: Set new month baseline, wait for next day
    └─ NO: Continue to comparison
    ↓
Compare current day with previous day
    ├─ Regular Plan: Calculate TER differences
    ├─ Direct Plan: Calculate TER differences
    └─ Comparison: Find common schemes with changes
    ↓
Generate CSV reports
    ↓
Save state to JSON
    ↓
Auto-commit and push to GitHub
    ↓
✓ Complete
```

### Month Transition Handling
When month changes:
1. New TER file is downloaded and set as baseline
2. State file is updated with new month/year
3. Analysis is skipped for that day (waiting for next day to compare)
4. Next day: Comparison begins with new baseline

---

## File Reference

### .github/workflows/ter_analysis.yml
- GitHub Actions workflow configuration
- Triggers: Daily schedule at 9:00 AM IST or manual workflow_dispatch
- Environment: Ubuntu latest with Python 3.10
- Steps: Download, install dependencies, run analysis, commit results

### ter_github_actions.py
Core analysis script with:
- `load_state()` - Load state from ter_state.json
- `download_ter_file()` - Download from AMFI API
- `read_ter_file()` - Parse Excel files
- `compare_schemes()` - Compare TER changes
- `analyze_daily()` - Main orchestration function

---

## Execution Logs

View logs in the **Actions** tab:
1. Click on a completed or running workflow
2. Click on the `ter-analysis` job
3. View detailed logs for each step

Example log excerpt:
```
2026-02-11 09:00:15 - INFO - Starting AMFI TER Analysis
2026-02-11 09:00:18 - INFO - Downloading TER file for 2026-2...
2026-02-11 09:00:21 - INFO - Read 1547 records
2026-02-11 09:00:22 - INFO - Regular Plan: 45 changes found
2026-02-11 09:00:22 - INFO - Direct Plan: 38 changes found
2026-02-11 09:00:23 - INFO - Regular vs Direct: 25 common schemes
2026-02-11 09:00:24 - INFO - Analysis completed successfully
```

---

## Customization

### Change Execution Time
Edit `.github/workflows/ter_analysis.yml`:
```yaml
schedule:
  - cron: '30 3 * * *'  # Change to desired time
```

Cron reference:
- `0 3 * * *` = 3:00 AM UTC (8:30 AM IST)
- `30 3 * * *` = 3:30 AM UTC (9:00 AM IST) ← **Current**
- `0 12 * * *` = 12:00 PM UTC (5:30 PM IST)

### Change Python Version
Edit version in workflow:
```yaml
python-version: '3.10'  # Change to 3.8, 3.9, 3.11, etc.
```

### Add Notifications
Use GitHub's native features:
1. Enable email notifications in Settings → Notifications
2. Or set up custom GitHub Actions for webhooks/alerts

---

## Troubleshooting

### Workflow Not Running
**Problem**: Workflow doesn't appear in Actions tab  
**Solution**: 
- Ensure `.github/workflows/ter_analysis.yml` is on the `main` branch
- Wait up to 15 minutes for GitHub to recognize the workflow
- Refresh the page

### Workflow Fails
**Problem**: Workflow shows as failed in Actions  
**Solution**:
1. Click the failed run
2. Click `ter-analysis` job
3. Expand each step to see errors
4. Common issues:
   - Network error downloading TER file → Check AMFI API
   - Git push failed → Check repository permissions
   - Python import error → Check dependencies in workflow

### No Changes Committed
**Problem**: Expected CSV files not appearing in repository  
**Solution**:
- This is normal if no TER changes occurred
- Check logs to confirm analysis ran
- Manually trigger workflow to test
- If files generated but not committed, check git actor permissions

### State File Out of Sync
**Problem**: ter_state.json shows old dates  
**Solution**:
- Manually trigger workflow by going to Actions → AMFI TER Daily Analysis → Run workflow
- Or wait for next scheduled run
- The state automatically updates on each run

---

## Verifying Setup

### Step 1: Check Workflow File
```bash
ls -la .github/workflows/ter_analysis.yml
# Should show the file exists
```

### Step 2: Check Script
```bash
ls -la ter_github_actions.py
# Should show the file exists
```

### Step 3: Run Manually
1. Go to GitHub repository
2. Click "Actions" tab
3. Click "AMFI TER Daily Analysis"
4. Click "Run workflow" → "Run workflow"
5. Wait for completion (should take 30 seconds to 2 minutes)

### Step 4: Verify Results
1. After workflow completes, check the repository
2. Look for new files in `output/` directory
3. Check `ter_state.json` has been updated
4. Review workflow logs for any messages

---

## Commits History

Each successful run generates a commit:
```
Auto: AMFI TER Analysis - 2026-02-11 09:00:23
Auto: AMFI TER Analysis - 2026-02-10 09:00:45
Auto: AMFI TER Analysis - 2026-02-09 09:01:12
```

Only commits if changes occurred (prevents empty commits).

---

## Monitoring Progress

### Real-time Monitoring
1. Go to repository "Actions" tab
2. See all workflow runs with status indicators:
   - 🟢 Green = Success
   - 🔴 Red = Failed
   - 🟡 Yellow = In progress

### Historical View
1. Click "AMFI TER Daily Analysis" workflow
2. See all past runs with timestamps
3. Click on any run to see detailed logs

### File Generation
1. Push to repository and refresh
2. Navigate to `output/` folder
3. See CSV files with dates
4. Click on files to view content

---

## Architecture Diagram

```
┌─────────────────────────────────────┐
│      GitHub Actions Scheduler       │
│    (Cron: 30 3 * * * = 9:00 IST)   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│    Setup Python 3.10 Environment    │
│         + Dependencies              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   ter_github_actions.py             │
│   - Download TER file (AMFI API)    │
│   - Load previous state             │
│   - Compare Regular vs Direct TER   │
│   - Generate CSV reports            │
│   - Update state.json               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Commit & Push Results             │
│   - output/*.csv files              │
│   - ter_state.json                  │
│   - logs/ter_analysis.log           │
└──────────────┬──────────────────────┘
               │
               ▼
         ✓ Complete
```

---

## Key Differences from Windows Scheduler Version

| Aspect | Windows | GitHub Actions |
|--------|---------|---|
| Trigger | Windows Task Scheduler | GitHub Actions Cron |
| Storage | Local C:\ drive | GitHub repository + workflow artifacts |
| State | ter_state.json (local) | ter_state.json (in repo, tracked by git) |
| Logs | ter_analysis.log (local) | Viewable in GitHub Actions UI |
| Execution | Runs on your machine | Runs on GitHub's servers |
| Uptime | Requires machine on | Always available |
| Cost | Hardware cost | Free (within GitHub Actions limits) |

---

## GitHub Actions Limits (Free Plan)

- ✅ **Jobs per day**: 20 concurrent
- ✅ **Monthly minutes**: 2,000 minutes included
- ✅ **Execution time**: 35 days of continuous runs
- ✅ **Frequency**: Can run multiple times per day

Our workflow uses ~2 minutes per day = well within limits.

---

## Success Indicators

After deployment, you should see:

1. ✅ Workflow showing in "Actions" tab
2. ✅ First run completes within 2 minutes
3. ✅ Files appear in `output/` folder
4. ✅ `ter_state.json` updated with current date
5. ✅ Commits appearing in repository history
6. ✅ Next day: New CSV files generated automatically

