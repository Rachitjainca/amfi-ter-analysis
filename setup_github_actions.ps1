# GitHub Actions Setup Script for PowerShell
# AMFI TER Analysis - GitHub Actions Deployment

Write-Host ""
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  AMFI TER Analysis - GitHub Actions Deployment" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Git is installed: $gitVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ ERROR: Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Install from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 1: Checking repository status..." -ForegroundColor Cyan
Write-Host ""

# Check if git is already initialized
if (!(Test-Path ".git")) {
    Write-Host "Initializing git repository..."
    git init
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Git repository initialized" -ForegroundColor Green
    } else {
        Write-Host "✗ ERROR: Failed to initialize git repository" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "✓ Git repository already initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 2: Configuring git user..." -ForegroundColor Cyan
Write-Host ""

# Get current git user
$gitUser = git config user.name
$gitEmail = git config user.email

if ([string]::IsNullOrEmpty($gitUser)) {
    $gitUser = Read-Host "Enter your GitHub username"
    git config user.name $gitUser
}

if ([string]::IsNullOrEmpty($gitEmail)) {
    $gitEmail = Read-Host "Enter your GitHub email"
    git config user.email $gitEmail
}

Write-Host "✓ Git user configured: $gitUser ($gitEmail)" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Adding files to git..." -ForegroundColor Cyan
Write-Host ""

git add .
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Files added to git" -ForegroundColor Green
} else {
    Write-Host "✗ ERROR: Failed to add files" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 4: Creating initial commit..." -ForegroundColor Cyan
Write-Host ""

git commit -m "Initial commit: AMFI TER Analysis with GitHub Actions" -q
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Commit created" -ForegroundColor Green
} else {
    Write-Host "⚠ Warning: Commit skipped (might be normal if no changes)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 5: Setting main branch..." -ForegroundColor Cyan
Write-Host ""

git branch -M main
Write-Host "✓ Branch renamed to main" -ForegroundColor Green

Write-Host ""
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  IMPORTANT: Manual Steps Required" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Create a new repository on GitHub:" -ForegroundColor Yellow
Write-Host "   - Go to https://github.com/new" -ForegroundColor Cyan
Write-Host "   - Repository name: amfi-ter-analysis" -ForegroundColor Cyan
Write-Host "   - Description: AMFI TER Analysis with GitHub Actions" -ForegroundColor Cyan
Write-Host "   - Choose Public or Private" -ForegroundColor Cyan
Write-Host "   - Do NOT initialize with README or .gitignore" -ForegroundColor Cyan
Write-Host "   - Click 'Create repository'" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. After creating GitHub repository, run:" -ForegroundColor Yellow
Write-Host "   git remote add origin https://github.com/YOUR-USERNAME/amfi-ter-analysis.git" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""

# Ask for repository URL
$repoUrl = Read-Host "Enter your GitHub repository URL (or press Enter to skip)"

if (![string]::IsNullOrEmpty($repoUrl)) {
    Write-Host ""
    Write-Host "Adding remote and pushing..." -ForegroundColor Cyan
    
    # Try to add remote
    git remote add origin $repoUrl 2>$null
    if ($LASTEXITCODE -eq 128) {
        # Remote already exists
        Write-Host "Remote already exists, updating..." -ForegroundColor Yellow
        git remote set-url origin $repoUrl
    }
    
    # Push to remote
    git push -u origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ Successfully pushed to GitHub" -ForegroundColor Green
        Write-Host ""
        Write-Host "Visit your repository:" -ForegroundColor Cyan
        Write-Host $repoUrl -ForegroundColor Yellow
    } else {
        Write-Host ""
        Write-Host "✗ ERROR: Push failed. Try manually:" -ForegroundColor Red
        Write-Host "git push -u origin main" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  Post-Deployment Steps" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to your GitHub repository" -ForegroundColor Yellow
Write-Host "2. Click 'Actions' tab" -ForegroundColor Yellow
Write-Host "3. You should see 'AMFI TER Daily Analysis' workflow" -ForegroundColor Yellow
Write-Host "4. Click 'Run workflow' to test" -ForegroundColor Yellow
Write-Host "5. Monitor the run and check generated files" -ForegroundColor Yellow
Write-Host ""
Write-Host "The workflow will now run daily at 9:00 AM IST" -ForegroundColor Green
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "- DEPLOYMENT_GUIDE.md ............ Comprehensive deployment guide" -ForegroundColor Cyan
Write-Host "- GITHUB_ACTIONS_GUIDE.md ....... GitHub Actions specific guide" -ForegroundColor Cyan
Write-Host "- GITHUB_ACTIONS_CHECKLIST.md ... Quick reference checklist" -ForegroundColor Cyan
Write-Host ""
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
