@echo off
echo ========================================
echo Restarting Ashoka Dashboard (Fresh)
echo ========================================
echo.

echo Step 1: Cleaning cache...
if exist .nicegui rmdir /s /q .nicegui
echo Cache cleared!
echo.

echo Step 2: Starting application...
echo.
echo IMPORTANT: After application starts:
echo 1. Open browser in INCOGNITO/PRIVATE mode
echo 2. Go to http://localhost:8080
echo 3. Login with demo / demo123
echo 4. Timer should be GREEN!
echo.
echo If timer is still not green, press Ctrl+Shift+R to hard refresh
echo.
echo ========================================
echo Starting now...
echo ========================================
echo.

python run_auth_demo.py
