# AMFI TER Analysis - GitHub Actions Setup Checklist

## Pre-Deployment Checklist

- [ ] GitHub account created
- [ ] Git installed on local machine
- [ ] All AMFI TER scripts in local folder:
  - [ ] ter_github_actions.py
  - [ ] .github/workflows/ter_analysis.yml
  - [ ] .gitignore
  - [ ] DEPLOYMENT_GUIDE.md
  - [ ] GITHUB_ACTIONS_GUIDE.md

---

## Deployment Steps (5 minutes)

### 1. Create GitHub Repository
- [ ] Go to https://github.com/new
- [ ] Repository name: `amfi-ter-analysis`
- [ ] Choose **Public** or **Private**
- [ ] Do NOT select "Initialize with README"
- [ ] Click "Create repository"

### 2. Initialize Local Repository
```bash
cd c:\Users\rachit.jain\Desktop\AMFI
git init
git config user.name "Your Name"
git config user.email "youremail@example.com"
git add .
git commit -m "Initial commit: AMFI TER Analysis with GitHub Actions"
git branch -M main
```

Or run the provided script:
```bash
setup_github_actions.bat
```

### 3. Push to GitHub
```bash
git remote add origin https://github.com/YOUR-USERNAME/amfi-ter-analysis.git
git push -u origin main
```

### 4. Configure Repository Settings
- [ ] Go to repository Settings
- [ ] Navigate to: **Actions** → **General**
- [ ] Enable "Allow all actions and reusable workflows"
- [ ] Set "Read and write permissions" for GITHUB_TOKEN
- [ ] Click "Save"

### 5. Verify Workflow
- [ ] Go to "Actions" tab
- [ ] See "AMFI TER Daily Analysis" workflow
- [ ] Click "Run workflow" → "Run workflow" (to test manually)
- [ ] Wait for completion (1-2 minutes)

### 6. Check Results
- [ ] Go to "output" folder
- [ ] See generated CSV files with today's date
- [ ] Check "ter_state.json" has been updated
- [ ] Review workflow logs for any messages

---

## What Gets Deployed

```
Repository Root/
├── .github/
│   └── workflows/
│       └── ter_analysis.yml ..................... GitHub Actions workflow
├── ter_github_actions.py .......................... Main analysis script
├── .gitignore ................................... Git ignore rules
├── DEPLOYMENT_GUIDE.md ........................... Deployment instructions
├── GITHUB_ACTIONS_GUIDE.md ....................... GitHub Actions details
├── setup_github_actions.bat ....................... Setup helper
└── This file .................................... Quick reference
```

---

## Schedule Information

| Setting | Value |
|---------|-------|
| **Frequency** | Every day |
| **Time** | 9:00 AM IST (UTC+5:30) |
| **Cron Expression** | `30 3 * * *` (3:30 UTC) |
| **Trigger** | Automatic schedule + Manual (workflow_dispatch) |

---

## Output Files (Generated Daily)

Location: `output/` folder in repository

| File Name | Content |
|-----------|---------|
| `Regular_Plan_TER_Changes_YYYY-MM-DD.csv` | Regular plan TER changes |
| `Direct_Plan_TER_Changes_YYYY-MM-DD.csv` | Direct plan TER changes |
| `Regular_vs_Direct_TER_Changes_YYYY-MM-DD.csv` | Comparison between plans |

**Auto-committed**: All files automatically committed and pushed to GitHub

---

## State Management

File: `ter_state.json`

```json
{
  "last_processed_date": "2026-02-11",
  "month_year": "2026-02",
  "file_history": {
    "2026-02": {
      "filepath": "downloads/TER_...",
      "date": "2026-02-11"
    }
  }
}
```

This file tracks:
- Last processed date
- Current month/year
- Downloaded file paths
- History for month transitions

---

## Quick Commands Reference

### View Workflow Status
```bash
# Check latest commit
git log --oneline -5

# Pull latest changes
git pull origin main
```

### Manual Workflow Trigger
1. Go to GitHub repository
2. Click "Actions" tab
3. Click "AMFI TER Daily Analysis"
4. Click "Run workflow" button

### View Execution Logs
1. Go to "Actions" tab
2. Click on latest workflow run
3. Click "ter-analysis" job
4. Expand each step to see logs

### Change Execution Time
Edit `.github/workflows/ter_analysis.yml`:
```yaml
cron: '30 3 * * *'  # Change this line
```

Common times (UTC+5:30 IST):
- `0 3 * * *` → 8:30 AM IST
- `30 3 * * *` → 9:00 AM IST ← Current
- `0 12 * * *` → 5:30 PM IST

---

## Storage Information

### In Repository
- All generated CSV reports
- State file (ter_state.json)
- Logs and history
- Your analysis scripts

### Downloaded by Workflow
- TER Excel files (auto-downloaded daily)
- Stored in `downloads/` folder
- Automatically included in repository

### Storage Limit (Free GitHub)
- Unlimited for code repository
- 1 GB file size limit per file
- Action logs kept for 90 days

---

## Troubleshooting Quick Links

### Issue: Workflow not appearing
**Solution**: 
- Refresh GitHub page (Ctrl+R)
- Ensure `.github/workflows/ter_analysis.yml` is on main branch
- Wait up to 15 minutes

### Issue: Workflow fails
**Solution**:
1. Click failed workflow run
2. Click "ter-analysis" job
3. Look for error messages
4. Check AMFI API status if download failed

### Issue: No files generated
**Solution**:
- Check logs in workflow run
- Check if TER data actually changed
- Verify `ter_state.json` exists
- Manually trigger to test

### Issue: Permission denied on push
**Solution**:
- Check repository is valid URL
- Verify SSH key or personal access token are configured
- See GitHub docs on authentication

---

## Monitoring Dashboard

After deployment, monitor from:

1. **GitHub Actions Tab**
   - Live status of all runs
   - Historical run data
   - Execution logs

2. **Files in Repository**
   - Check `output/` folder for CSV files
   - Monitor `ter_state.json` for updates
   - Review logs folder

3. **Commit History**
   - Auto-commits from workflow
   - Shows what changed each run
   - Timestamps of executions

---

## Documentation Files

| File | Purpose |
|------|---------|
| `DEPLOYMENT_GUIDE.md` | Complete deployment guide with architecture |
| `GITHUB_ACTIONS_GUIDE.md` | In-depth GitHub Actions specifics |
| `README.md` | Project overview (create your own) |
| This file | Quick reference checklist |

---

## Post-Deployment Verification

Run this checklist 24 hours after deployment:

- [ ] First automatic run completed (9:00 AM IST)
- [ ] CSV files generated in output folder
- [ ] ter_state.json shows today's date
- [ ] One auto-commit in repository history
- [ ] No errors in workflow logs
- [ ] Can manually trigger workflow successfully
- [ ] Generate files on manual trigger
- [ ] Files show correct data structure

If all checks pass: ✅ **Deployment Successful**

---

## Support Resources

- **GitHub Docs**: https://docs.github.com/en/actions
- **GitHub Community**: https://github.community
- **AMFI API**: https://www.amfiindia.com/
- **Python Pandas**: https://pandas.pydata.org/docs

---

## Common Customizations

### Change Frequency to Every 6 hours
Edit cron in `.github/workflows/ter_analysis.yml`:
```yaml
- cron: '0 */6 * * *'
```

### Change Frequency to Weekly (Sunday 9 AM)
```yaml
- cron: '30 3 ? * SUN'
```

### Disable Automatic Runs (Manual Only)
Comment out schedule:
```yaml
# - cron: '30 3 * * *'
```

---

## Next Steps After Deployment

1. **Monitor First Week**
   - Check daily runs complete successfully
   - Verify data quality in output
   - Monitor logs for any warnings

2. **Set Up Notifications** (Optional)
   - GitHub has native email notifications
   - Or integrate with Slack, Teams, etc.

3. **Archive Old Files** (Optional)
   - Export month-end CSV files
   - Keep in separate backup location

4. **Fine-Tune Analysis** (Optional)
   - Adjust comparison logic if needed
   - Add new metrics
   - Extend to other AMFI data

---

**Ready to Deploy?** → Run `setup_github_actions.bat` or follow manual steps above

