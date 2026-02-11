@echo off
REM GitHub Actions Deployment Setup for AMFI TER Analysis
REM This script initializes git and pushes to GitHub

setlocal enabledelayedexpansion
cls

echo.
echo ======================================================
echo   AMFI TER Analysis - GitHub Actions Deployment
echo ======================================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed or not in PATH
    echo Install from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo.
echo Step 1: Checking repository status...
echo.

REM Check if git is already initialized
if not exist .git (
    echo Git repository not initialized. Initializing...
    git init
    if %errorlevel% neq 0 (
        echo ERROR: Failed to initialize git repository
        pause
        exit /b 1
    )
    echo ✓ Git repository initialized
) else (
    echo ✓ Git repository already initialized
)

echo.
echo Step 2: Configuring git user...
echo.

REM Get current git user
for /f "tokens=*" %%a in ('git config user.name') do set GIT_USER=%%a
for /f "tokens=*" %%a in ('git config user.email') do set GIT_EMAIL=%%a

if "!GIT_USER!"=="" (
    echo Git user name not configured. Enter your GitHub username:
    set /p GIT_USER="GitHub Username: "
    git config user.name "!GIT_USER!"
)

if "!GIT_EMAIL!"=="" (
    echo Git email not configured. Enter your GitHub email:
    set /p GIT_EMAIL="GitHub Email: "
    git config user.email "!GIT_EMAIL!"
)

echo ✓ Git user configured: !GIT_USER! (!GIT_EMAIL!)

echo.
echo Step 3: Adding files to git...
echo.

git add .
if %errorlevel% neq 0 (
    echo ERROR: Failed to add files
    pause
    exit /b 1
)
echo ✓ Files added to git

echo.
echo Step 4: Creating initial commit...
echo.

git commit -m "Initial commit: AMFI TER Analysis with GitHub Actions" -q
if %errorlevel% neq 0 (
    echo WARNING: Commit failed (might be normal if no changes)
)
echo ✓ Commit created

echo.
echo Step 5: Setting main branch...
echo.

git branch -M main
echo ✓ Branch renamed to main

echo.
echo ======================================================
echo   IMPORTANT: Manual Steps Required
echo ======================================================
echo.
echo 1. Create a new repository on GitHub:
echo    - Go to https://github.com/new
echo    - Repository name: amfi-ter-analysis
echo    - Description: AMFI TER Analysis with GitHub Actions
echo    - Choose Public or Private
echo    - Do NOT initialize with README or .gitignore
echo    - Click "Create repository"
echo.
echo 2. After creating GitHub repository, run:
echo    git remote add origin https://github.com/YOUR-USERNAME/amfi-ter-analysis.git
echo    git push -u origin main
echo.
echo 3. Or paste this command:
set /p REPO_URL="Enter your GitHub repository URL (blank to skip): "

if not "!REPO_URL!"=="" (
    echo.
    echo Adding remote and pushing...
    git remote add origin !REPO_URL! 2>nul
    if !errorlevel! equ 128 (
        echo Remote already exists, updating...
        git remote set-url origin !REPO_URL!
    )
    git push -u origin main
    if !errorlevel! equ 0 (
        echo ✓ Successfully pushed to GitHub
        echo.
        echo Visit your repository:
        echo !REPO_URL!
    ) else (
        echo.
        echo ERROR: Push failed. Try manually:
        echo git push -u origin main
    )
)

echo.
echo ======================================================
echo   Post-Deployment Steps
echo ======================================================
echo.
echo 1. Go to your GitHub repository
echo 2. Click "Actions" tab
echo 3. You should see "AMFI TER Daily Analysis" workflow
echo 4. Click "Run workflow" to test
echo 5. Monitor the run and check generated files
echo.
echo The workflow will now run daily at 9:00 AM IST
echo.
echo Documentation:
echo - DEPLOYMENT_GUIDE.md - Comprehensive deployment guide
echo - GITHUB_ACTIONS_GUIDE.md - GitHub Actions specific guide
echo.
echo ======================================================

pause
