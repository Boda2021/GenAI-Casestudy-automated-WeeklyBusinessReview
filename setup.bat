@echo off
REM Setup script for Weekly Business Review Automation (Windows)

echo Setting up Weekly Business Review Automation...
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo Error: Python is required
    exit /b 1
)

REM Create virtual environment (optional)
set /p CREATE_VENV="Create virtual environment? (y/n): "
if /i "%CREATE_VENV%"=="y" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Virtual environment activated
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Install Windows-specific packages
echo Installing Windows-specific packages...
pip install pywin32

REM Check for data files
echo.
echo Checking data files...
if not exist "data\ecommerce_data.db" (
    echo Warning: ecommerce_data.db not found in data\ directory
    echo Please copy your database file to data\ecommerce_data.db
)

if not exist "data\WBR_Working_Sheet.xlsx" (
    echo Warning: WBR_Working_Sheet.xlsx not found in data\ directory
    echo Please copy your Excel template to data\WBR_Working_Sheet.xlsx
)

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Ensure data files are in the data\ directory
echo 2. Update email recipient in scripts\generate_email.py
echo 3. Run: python scripts\wbr_automation.py

pause
