@echo off
REM AMFI TER Analysis - Installation Script (Windows)

setlocal enabledelayedexpansion

echo ==========================================
echo AMFI TER Analysis - Package Installation
echo ==========================================

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo Python version: %python_version%

REM Install from PyPI
echo.
echo Installing amfi-ter-analysis from PyPI...
pip install amfi-ter-analysis

REM Verify installation
echo.
echo Verifying installation...
python -c "from amfi_ter_analysis import download_ter_file, read_ter_file, analyze_ter_changes" 2>nul
if %errorlevel% == 0 (
    echo ✅ Installation successful!
    echo.
    echo Quick start:
    echo   python -c "from amfi_ter_analysis import download_ter_file; download_ter_file(2, 2026)"
) else (
    echo ❌ Installation failed
    exit /b 1
)

echo.
echo ==========================================
echo For usage examples, see:
echo   https://github.com/Rachitjainca/amfi-ter-analysis#readme
echo ==========================================

endlocal
