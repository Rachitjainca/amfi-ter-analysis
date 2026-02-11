# QUICK START GUIDE - AMFI TER Daily Automation

## ✅ Setup Complete!

Your automated AMFI TER analysis is ready. Here's what's been set up:

### Files Created:
- **ter_daily_automation.py** - Main daily automation script
- **setup_automation.py** - Windows Task Scheduler setup (Python)
- **setup_scheduler.bat** - Windows Task Scheduler setup (Batch)
- **AUTOMATION_GUIDE.md** - Comprehensive documentation
- **ter_state.json** - Tracks processing state and history

### Directories Created:
- **downloads/** - TER Excel files downloaded from AMFI
- **output/** - Daily comparison reports (CSV files)
- **history/** - Daily data snapshots for comparison
- **logs/** - Execution logs

---

## 🚀 Quick Start (3 Steps)

### Step 1: Configure Windows Task Scheduler
**Option A - Python Setup (Recommended):**
```powershell
cd C:\Users\rachit.jain\Desktop\AMFI
python setup_automation.py
```

**Option B - Batch Setup:**
```cmd
cd C:\Users\rachit.jain\Desktop\AMFI
setup_scheduler.bat
```

### Step 2: Verify Task Creation
```powershell
schtasks /query /tn "AMFI-TER-Daily-Analysis" /v
```

### Step 3: Done!
- Task will run daily at 09:00 AM
- Each day, it will download the latest TER file and compare with previous day
- New month files are auto-downloaded when the month changes

---

## 📊 Output Files

Daily changes will be saved as:
- `output/Daily_Regular_Plan_Changes_YYYY-MM-DD.csv`
- `output/Daily_Direct_Plan_Changes_YYYY-MM-DD.csv`

Format:
```
NSDL Scheme Code | Scheme Name | Previous TER | Current TER | TER Reduction %
```

---

## 🧪 Test Without Waiting

To test immediately (don't wait for 9:00 AM):
```powershell
cd C:\Users\rachit.jain\Desktop\AMFI
python ter_daily_automation.py
```

---

## 📝 Important Notes

1. **First Run:** On the initial run (with a new month), the script will:
   - Download the current month's TER file
   - Save it as baseline
   - Wait until next day for comparisons

2. **Daily Runs:** Every subsequent day, the script will:
   - Download current TER file
   - Compare with previous day data
   - Save changes to output/ folder if any detected

3. **Month Changes:** When month changes:
   - New month file automatically downloaded
   - Previous month data kept for reference
   - Comparison continues with new month data

---

## 🔧 Common Commands

| Command | Purpose |
|---------|---------|
| `schtasks /run /tn "AMFI-TER-Daily-Analysis"` | Run task now |
| `type logs\ter_automation.log` | View execution logs |
| `schtasks /change /tn "AMFI-TER-Daily-Analysis" /disable` | Disable task |
| `schtasks /change /tn "AMFI-TER-Daily-Analysis" /enable` | Re-enable task |
| `schtasks /delete /tn "AMFI-TER-Daily-Analysis" /f` | Delete task |

---

## 📚 Full Documentation

For detailed information, see: **AUTOMATION_GUIDE.md**

---

## ✨ Current Status

✓ Python environment configured  
✓ Daily automation script created  
✓ Task scheduler setup scripts ready  
✓ Directories initialized  
✓ Ready for production use  

**Next:** Run `python setup_automation.py` or `setup_scheduler.bat` to complete Task Scheduler configuration.
