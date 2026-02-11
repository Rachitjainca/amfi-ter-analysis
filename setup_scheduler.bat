@echo off
REM Script to set up Windows Task Scheduler for daily TER analysis
REM Run this as Administrator to create the scheduled task

echo ========================================================================
echo Setting up Windows Task Scheduler for Daily AMFI TER Analysis
echo ========================================================================
echo.

REM Get the current directory
setlocal enabledelayedexpansion
for /f "delims=" %%A in ('cd') do set "CURRENT_DIR=%%A"
echo Current Directory: %CURRENT_DIR%
echo.

REM Create task
echo Creating scheduled task...
echo.

REM Delete existing task if it exists
taskkill /f /im python.exe /fi "WINDOWTITLE eq AMFI*" 2>nul
schtasks /delete "AMFI-TER-Daily-Analysis" /f 2>nul

REM Create new task - runs daily at 9:00 AM
schtasks /create /tn "AMFI-TER-Daily-Analysis" ^
    /tr "cmd /c \"cd /d %CURRENT_DIR% && C:\Users\rachit.jain\Desktop\AMFI\.venv\Scripts\python.exe ter_daily_automation.py >> logs\ter_automation.log 2>&1\"" ^
    /sc daily ^
    /st 09:00:00 ^
    /ru %USERNAME% ^
    /rp REQUEST

echo.
echo Task created successfully!
echo.
echo ========================================================================
echo Task Details:
echo ========================================================================
echo Task Name: AMFI-TER-Daily-Analysis
echo Schedule: Daily at 09:00 AM
echo Script: ter_daily_automation.py
echo Working Directory: %CURRENT_DIR%
echo Log File: %CURRENT_DIR%\logs\ter_automation.log
echo ========================================================================
echo.
echo To verify the task was created, run:
echo   schtasks /query /tn "AMFI-TER-Daily-Analysis" /v
echo.
echo To run the task manually, run:
echo   schtasks /run /tn "AMFI-TER-Daily-Analysis"
echo.
echo To disable the task, run:
echo   schtasks /change /tn "AMFI-TER-Daily-Analysis" /disable
echo.
echo To delete the task, run:
echo   schtasks /delete /tn "AMFI-TER-Daily-Analysis" /f
echo.
pause
