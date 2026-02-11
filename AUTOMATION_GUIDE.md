# AMFI TER Daily Automation Guide

## Overview

This automated system downloads AMFI TER (Total Expense Ratio) files daily and compares changes in Real Base TER for both Regular and Direct plans on a day-to-day basis. When the month changes, it automatically downloads the new month's file.

## Files

### Main Scripts
- **ter_daily_automation.py** - Main automation script that runs daily
- **setup_automation.py** - Setup script to configure Windows Task Scheduler
- **setup_scheduler.bat** - Batch script alternative for task scheduler setup
- **ter_analysis.py** - Original analysis script (for manual one-time analysis)
- **create_comparison.py** - Creates Direct vs Regular comparison

### Output Files (Generated Daily)
- **output/Daily_Regular_Plan_Changes_YYYY-MM-DD.csv** - Daily Regular plan TER changes
- **output/Daily_Direct_Plan_Changes_YYYY-MM-DD.csv** - Daily Direct plan TER changes

### Supporting Files
- **ter_state.json** - Tracks last processed date, month, and previous day data
- **logs/ter_automation.log** - Daily execution logs
- **downloads/TER_MM-YYYY.xlsx** - Downloaded TER files
- **history/TER_Data_MM-YYYY_YYYYMMDD.pkl** - Snapshots for comparison

## Setup Instructions

### Option 1: Using Python Setup Script (Recommended)

1. Open **Command Prompt as Administrator**
2. Navigate to the AMFI directory:
   ```
   cd C:\Users\rachit.jain\Desktop\AMFI
   ```
3. Run the setup script:
   ```
   python setup_automation.py
   ```
4. Follow the prompts - the task will be created automatically

### Option 2: Using Batch Script

1. Open **Command Prompt as Administrator**
2. Navigate to the AMFI directory:
   ```
   cd C:\Users\rachit.jain\Desktop\AMFI
   ```
3. Run the batch script:
   ```
   setup_scheduler.bat
   ```

### Option 3: Manual Task Scheduler Setup

1. Open "Task Scheduler" in Windows
2. Click "Create Task"
3. Configure:
   - **General Tab:**
     - Name: AMFI-TER-Daily-Analysis
     - User: Your Windows username
     - Run with highest privileges: Yes
   
   - **Triggers Tab:**
     - New > Daily
     - Time: 09:00:00 (or preferred time)
     - Enabled: Yes
   
   - **Actions Tab:**
     - Program: C:\Users\rachit.jain\Desktop\AMFI\.venv\Scripts\python.exe
     - Arguments: ter_daily_automation.py
     - Start in: C:\Users\rachit.jain\Desktop\AMFI

## How It Works

### First Run (Month Change)
1. Detects new month
2. Downloads TER file for current month
3. Saves baseline data
4. Waits until next day to start comparisons

### Daily Runs
1. Downloads current month TER file
2. Loads previous day's data
3. Compares TER changes
4. If changes detected:
   - Saves Daily_Regular_Plan_Changes_YYYY-MM-DD.csv
   - Saves Daily_Direct_Plan_Changes_YYYY-MM-DD.csv
5. Saves current data for next day's comparison
6. Updates state file

### Output Format

**Daily Change Files Contain:**
| Column | Description |
|--------|-------------|
| NSDL Scheme Code | Unique scheme identifier |
| Scheme Name | Fund scheme name |
| Previous [Plan] - Base TER (%) | TER on previous day |
| Current [Plan] - Base TER (%) | TER on current day |
| TER Date (Change) | Date of change |
| TER Reduction (%) | Change amount (positive = reduction) |

## Useful Commands

### View Task Status
```
schtasks /query /tn "AMFI-TER-Daily-Analysis" /v
```

### Run Task Immediately
```
schtasks /run /tn "AMFI-TER-Daily-Analysis"
```

### Disable Task (without deleting)
```
schtasks /change /tn "AMFI-TER-Daily-Analysis" /disable
```

### Re-enable Task
```
schtasks /change /tn "AMFI-TER-Daily-Analysis" /enable
```

### Delete Task
```
schtasks /delete /tn "AMFI-TER-Daily-Analysis" /f
```

### View Logs
```
type logs\ter_automation.log
```

### Clear Logs
```
del logs\ter_automation.log
```

## Directory Structure

```
AMFI/
├── ter_daily_automation.py      # Main daily script
├── setup_automation.py          # Setup script
├── setup_scheduler.bat          # Batch setup
├── ter_analysis.py              # Original analysis
├── create_comparison.py         # Comparison generator
├── ter_state.json               # State tracking
│
├── downloads/
│   └── TER_MM-YYYY.xlsx         # Downloaded files
│
├── output/
│   ├── Daily_Regular_*.csv      # Daily regular plan changes
│   ├── Daily_Direct_*.csv       # Daily direct plan changes
│   ├── Regular_Plan_TER_Changes.csv
│   ├── Direct_Plan_TER_Changes.csv
│   └── Direct_vs_Regular_TER_Comparison.csv
│
├── history/
│   └── TER_Data_MM-YYYY_*.pkl   # Daily snapshots
│
└── logs/
    └── ter_automation.log        # Execution logs
```

## Troubleshooting

### Task Not Running
- Check if Task Scheduler is enabled
- Verify Python path is correct in task action
- Run with Administrator privileges
- Check event viewer for errors

### "Module not found" Error
- Ensure all dependencies are installed:
  ```
  pip install requests pandas openpyxl
  ```

### Missing Previous Day Data
- This occurs on first month - task initializes and waits until next day
- Subsequent days will have comparisons

### Download Failures
- Check internet connection
- Verify AMFI website is accessible
- Check logs for error details

## Monthly Transitions

When the month changes:
1. Old month file is kept in downloads/ for reference
2. New month file is automatically downloaded
3. State file is updated
4. Daily comparisons resume from next successful download

## Data Retention

- **Excel Files** (downloads/): Kept indefinitely, not overwritten
- **Pickle Files** (history/): Keep 30-60 days for comparison history
- **Output CSV Files** (output/): Timestamped, all saved for reporting
- **Logs**: Can be manually cleared; recommend keeping for audit trail

## Testing

To test the automation without waiting for 9:00 AM:

```
cd C:\Users\rachit.jain\Desktop\AMFI
python ter_daily_automation.py
```

This will execute immediately and you'll see output in the console.

## Monitoring

### Check Recent Executions
```
Get-ScheduledTaskInfo -TaskName "AMFI-TER-Daily-Analysis"
```

### View Task History (PowerShell)
```
Get-WinEvent -LogName "Microsoft-Windows-TaskScheduler/Operational" | 
Where-Object {$_.Message -like "*AMFI-TER*"} | 
Select-Object -First 10
```

## Support

For issues or modifications needed:
1. Check the logs/ folder for error messages
2. Run ter_daily_automation.py manually to debug
3. Verify all files are present in the AMFI directory
4. Ensure internet connectivity during scheduled run time
