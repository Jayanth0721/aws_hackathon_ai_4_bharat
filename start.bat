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

REM Check FFmpeg
echo Checking FFmpeg...
where ffmpeg >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ FFmpeg detected
) else (
    echo ⚠️  FFmpeg not found!
    echo.
    echo FFmpeg is required for audio/video processing.
    echo.
    echo Quick Install Options:
    echo   1. Using winget (Recommended):
    echo      winget install --id=Gyan.FFmpeg -e
    echo.
    echo   2. Using Chocolatey:
    echo      choco install ffmpeg
    echo.
    echo   3. Manual: See INSTALL_FFMPEG_WINDOWS.md
    echo.
    echo Would you like to install FFmpeg now using winget? (Y/N)
    set /p install_ffmpeg=
    
    if /i "%install_ffmpeg%"=="Y" (
        echo Installing FFmpeg using winget...
        winget install --id=Gyan.FFmpeg -e
        if %errorlevel% equ 0 (
            echo ✓ FFmpeg installed successfully
            echo ⚠️  Please restart this script in a NEW terminal window
            pause
            exit /b 0
        ) else (
            echo ✗ FFmpeg installation failed
            echo Please install manually. See INSTALL_FFMPEG_WINDOWS.md
            pause
            exit /b 1
        )
    ) else (
        echo Continuing without FFmpeg...
        echo Audio/video processing will not work until FFmpeg is installed.
        echo.
    )
)
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
    echo ⚠️  Please edit .env and add your GOOGLE_API_KEY
) else (
    echo ✓ .env file exists
)
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ✗ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Python dependencies installed
echo.

REM Run tests (if exists)
if exist test_setup.py (
    echo Running setup tests...
    python test_setup.py
    if %errorlevel% neq 0 (
        echo ✗ Setup tests failed
        pause
        exit /b 1
    )
    echo.
)

echo ======================================
echo 🚀 Launching dashboard...
echo ======================================
echo.
python run_dashboard.py
pause
)

echo.
echo ======================================
echo 🚀 Launching dashboard...
echo ======================================
echo.
python run_dashboard.py
