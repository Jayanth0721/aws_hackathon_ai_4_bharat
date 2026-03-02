@echo off
echo 🛡️  Ashoka Platform - Startup Script
echo ======================================
echo.

REM Check Python
echo Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo ✗ Python not found. Please install Python 3.8+
    pause
    exit /b 1
)
echo ✓ Python detected
echo.

REM Create data directory
echo Creating data directory...
if not exist data mkdir data
echo ✓ Data directory ready
echo.

REM Check .env file
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo ✓ .env file created
) else (
    echo ✓ .env file exists
)
echo.

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ✗ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Run tests
echo Running setup tests...
python test_setup.py
if %errorlevel% neq 0 (
    echo ✗ Setup tests failed
    pause
    exit /b 1
)

echo.
echo ======================================
echo 🚀 Launching dashboard...
echo ======================================
echo.
python run_dashboard.py
