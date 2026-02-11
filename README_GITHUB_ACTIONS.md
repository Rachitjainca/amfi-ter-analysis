# AMFI TER Analysis - GitHub Actions Deployment

Complete GitHub Actions setup for automated daily AMFI TER (Total Expense Ratio) analysis and reporting.

## 🚀 Quick Start

### Option 1: Batch Script (Windows CMD)
```bash
setup_github_actions.bat
```

### Option 2: PowerShell Script (Windows)
```powershell
.\setup_github_actions.ps1
```

### Option 3: Manual (All platforms)
```bash
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
git add .
git commit -m "Initial commit: AMFI TER Analysis"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/amfi-ter-analysis.git
git push -u origin main
```

---

## 📋 What's Included

### Configuration Files
- **`.github/workflows/ter_analysis.yml`** - GitHub Actions workflow (runs daily at 9:00 AM IST)
- **`.gitignore`** - Git ignore rules

### Python Scripts
- **`ter_github_actions.py`** - Main analysis script (downloads TER files, compares, generates reports)
- **Daily automation** - Automatically handles month transitions and day-to-day comparisons

### Setup Helpers
- **`setup_github_actions.bat`** - Batch script for Windows CMD
- **`setup_github_actions.ps1`** - PowerShell script for Windows (colored output)

### Documentation
- **`DEPLOYMENT_GUIDE.md`** - Comprehensive deployment guide
- **`GITHUB_ACTIONS_GUIDE.md`** - GitHub Actions specific documentation
- **`GITHUB_ACTIONS_CHECKLIST.md`** - Quick reference checklist
- **`README.md`** - This file

---

## ✨ Features

✅ **Automated Daily Execution** - Runs every day at 9:00 AM IST  
✅ **TER File Download** - Automatically downloads latest TER files from AMFI API  
✅ **Day-to-Day Comparison** - Compares current day with previous day  
✅ **Month Change Detection** - Automatically handles month transitions  
✅ **CSV Report Generation** - Generates Regular Plan, Direct Plan, and Comparison reports  
✅ **Auto-Commit Results** - Results automatically pushed to your GitHub repository  
✅ **State Tracking** - Maintains state in JSON file for reliable execution  
✅ **Comprehensive Logging** - All operations logged for debugging  
✅ **Cloud-Based** - No local machine required to keep running  
✅ **Free Tier Compatible** - Works with GitHub's free tier (2,000 minutes/month)  

---

## 📊 Generated Outputs

Daily CSV files in `output/` folder:

| File | Contains |
|------|----------|
| `Regular_Plan_TER_Changes_YYYY-MM-DD.csv` | Regular plan TER changes |
| `Direct_Plan_TER_Changes_YYYY-MM-DD.csv` | Direct plan TER changes |
| `Regular_vs_Direct_TER_Changes_YYYY-MM-DD.csv` | Comparison of changes |

All files automatically committed to your GitHub repository!

---

## 🔧 How It Works

```
9:00 AM IST (Every Day)
        ↓
GitHub Actions Triggers
        ↓
Download Latest TER File
        ↓
Compare with Previous Day
        ↓
Generate CSV Reports
        ↓
Auto-Commit & Push Results
        ↓
✓ Complete
```

---

## 📁 Repository Structure (After Setup)

```
your-repo/
├── .github/
│   └── workflows/
│       └── ter_analysis.yml              ← GitHub Actions workflow
├── downloads/                             ← Downloaded TER files
├── output/                                ← Generated CSV reports
├── logs/                                  ← Execution logs
├── history/                               ← Historical data
├── ter_state.json                         ← State tracking
├── ter_github_actions.py                  ← Main script
├── .gitignore                             ← Git ignore rules
├── setup_github_actions.bat               ← Setup helper (Windows)
├── setup_github_actions.ps1               ← Setup helper (PowerShell)
└── README.md                              ← This file
```

---

## ⏰ Schedule

- **Frequency**: Daily
- **Time**: 9:00 AM IST (UTC+5:30)
- **Cron**: `30 3 * * *` (3:30 UTC)
- **Manual Trigger**: Supported (workflow_dispatch)

---

## 🔐 Security & Requirements

✅ **No API Keys** - AMFI API is public, no authentication needed  
✅ **No Secrets** - All operations use public data  
✅ **GitHub Token** - Automatically available for git operations  
✅ **Permissions** - Repository needs "Read and write permissions" for auto-commits  

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| **DEPLOYMENT_GUIDE.md** | Complete setup guide with architecture details |
| **GITHUB_ACTIONS_GUIDE.md** | In-depth GitHub Actions configuration |
| **GITHUB_ACTIONS_CHECKLIST.md** | Quick reference checklist |
| **README.md** | This file - overview |

**Start with**: `GITHUB_ACTIONS_CHECKLIST.md` for quick setup  
**Deep dive**: `DEPLOYMENT_GUIDE.md` for complete details  

---

## 🚀 Deployment Steps (5 Minutes)

### 1. Create GitHub Repository
1. Go to https://github.com/new
2. Name: `amfi-ter-analysis`
3. Choose Public/Private
4. Click "Create"

### 2. Initialize & Push
Run one of:
- `setup_github_actions.bat` (Windows CMD)
- `setup_github_actions.ps1` (Windows PowerShell)
- Manual commands (see Quick Start)

### 3. Configure Repository
1. Go to Settings → Actions → General
2. Enable "Allow all actions"
3. Set "Read and write permissions"

### 4. Test Workflow
1. Go to "Actions" tab
2. Click "AMFI TER Daily Analysis"
3. Click "Run workflow"
4. Wait for completion

### 5. Verify Results
1. Check `output/` folder
2. See generated CSV files
3. Check workflow logs

---

## ✅ Verification Checklist

After deployment:
- [ ] Repository appears in GitHub
- [ ] `.github/workflows/ter_analysis.yml` exists
- [ ] "AMFI TER Daily Analysis" shows in Actions tab
- [ ] Manual workflow run completes successfully
- [ ] CSV files appear in `output/` folder
- [ ] `ter_state.json` shows today's date
- [ ] Auto-commits appear in history
- [ ] Next day: Automatic run succeeds

---

## 🛠️ Customization

### Change Execution Time
Edit `.github/workflows/ter_analysis.yml`:
```yaml
- cron: '30 3 * * *'  # Change to desired time
```

Examples:
- `0 3 * * *` = 8:30 AM IST
- `30 3 * * *` = 9:00 AM IST (current)
- `0 12 * * *` = 5:30 PM IST

### Change Python Version
```yaml
python-version: '3.10'  # Change to 3.8, 3.9, 3.11, etc.
```

---

## 📞 Support

### Common Issues

**Workflow not appearing?**
- Refresh GitHub page
- Wait 15 minutes for GitHub to recognize workflow
- Ensure `.github/workflows/` directory exists

**Workflow fails?**
- Click failed run
- Check logs for error messages
- Verify AMFI API is accessible

**No files generated?**
- Check workflow logs
- Verify TER data actually changed
- Manually trigger to test

For more help, see **DEPLOYMENT_GUIDE.md**

---

## 📊 GitHub Actions Limits (Free Plan)

✅ Runs per day: Unlimited  
✅ Monthly minutes: 2,000 minutes  
✅ Concurrent jobs: 20  
✅ File size limit: 1 GB  

Our workflow: ~2 minutes per day = **365 minutes/year** (easily within limits)

---

## 🎯 What Happens Each Day

1. **9:00 AM IST** - Workflow automatically triggers
2. **Setup** - Python environment and dependencies
3. **Download** - Latest TER file from AMFI API
4. **Compare** - Current day vs previous day
5. **Analyze** - Calculate TER changes
6. **Generate** - CSV reports for Regular/Direct plans
7. **Save** - Files saved to `output/` folder
8. **Commit** - Results auto-committed to GitHub
9. **Complete** - Logs available in Actions tab

---

## 🔄 Month Transition Handling

When month changes:
1. New TER file automatically downloaded
2. Set as baseline for new month
3. Skip analysis for transition day
4. Next day: Normal comparison begins

This ensures accurate month-to-month tracking.

---

## 📊 Example Output

### Regular_Plan_TER_Changes_2026-02-11.csv
```
NSDL Scheme Code,Scheme Name,Old TER (%),New TER (%),TER Reduction (%)
NSL000003,Scheme A,1.25,1.20,0.05
NSL000004,Scheme B,0.85,0.79,0.06
NSL000005,Scheme C,2.10,2.05,0.05
```

### Logs (ter_analysis.log)
```
2026-02-11 09:00:15 - INFO - Starting AMFI TER Analysis
2026-02-11 09:00:18 - INFO - Downloaded TER file
2026-02-11 09:00:22 - INFO - Regular Plan: 45 changes found
2026-02-11 09:00:23 - INFO - Analysis completed successfully
```

---

## 🌐 Data Source

- **API**: https://www.amfiindia.com/api/populate-te-rdata-revised
- **Provider**: AMFI (Association of Mutual Funds in India)
- **Format**: Excel files with 15 columns
- **Updated**: Daily
- **Cost**: Free, public data

---

## 📝 Next Steps

1. **Immediate**: Run setup script → push to GitHub
2. **First 24 hours**: Monitor first automatic run
3. **One week**: Verify data quality and recurrence
4. **Optional**: Set up GitHub notifications
5. **Optional**: Extend analysis with additional metrics

---

## 🔗 Quick Links

- GitHub: https://github.com
- AMFI: https://www.amfiindia.com/
- GitHub Actions Docs: https://docs.github.com/actions
- Python Pandas: https://pandas.pydata.org/

---

## 📄 License

This project uses public data from AMFI India. No license restrictions.

---

## 🎓 Learning Resources

Within this repo:
- **DEPLOYMENT_GUIDE.md** - System architecture and detailed steps
- **GITHUB_ACTIONS_GUIDE.md** - GitHub Actions specific knowledge
- **GITHUB_ACTIONS_CHECKLIST.md** - Quick reference card
- **ter_github_actions.py** - Well-commented Python code

---

## ✨ Ready to Deploy?

```bash
# Option 1: Windows Batch
setup_github_actions.bat

# Option 2: Windows PowerShell
.\setup_github_actions.ps1

# Option 3: Manual
git init
git add .
git commit -m "AMFI TER Analysis"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

Then follow on-screen instructions!

---

**Last Updated**: February 2026  
**Status**: ✅ Production Ready  
**Tested**: Daily automation with GitHub Actions  

