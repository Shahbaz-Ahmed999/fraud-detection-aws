@echo off
REM ==========================================
REM Fraud Detection AWS - Windows Setup Script
REM ==========================================

echo.
echo ========================================
echo  Fraud Detection AWS - Setup Script
echo ========================================
echo.

REM Check Python installation
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.9+ from python.org
    pause
    exit /b 1
)
python --version
echo [OK] Python found!
echo.

REM Check pip installation
echo [2/6] Checking pip installation...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip not found. Please reinstall Python with pip.
    pause
    exit /b 1
)
pip --version
echo [OK] pip found!
echo.

REM Create virtual environment
echo [3/6] Creating virtual environment...
if exist venv (
    echo [INFO] Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    echo [OK] Virtual environment created!
)
echo.

REM Activate virtual environment
echo [4/6] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)
echo [OK] Virtual environment activated!
echo.

REM Upgrade pip
echo [5/6] Upgrading pip...
python -m pip install --upgrade pip
echo [OK] pip upgraded!
echo.

REM Install dependencies
echo [6/6] Installing Python packages...
echo [INFO] This may take 5-10 minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install some packages.
    echo [INFO] You can install manually with: pip install -r requirements.txt
    pause
    exit /b 1
)
echo [OK] All packages installed successfully!
echo.

REM Success message
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Keep this terminal open (virtual environment is activated)
echo   2. Download dataset from Kaggle
echo   3. Run: jupyter notebook
echo.
echo To activate environment later, run:
echo   venv\Scripts\activate.bat
echo.
echo To deactivate environment, run:
echo   deactivate
echo.
pause
