@echo off
echo.
echo ====================================
echo   💸 Expense Tracker CLI
echo ====================================
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

echo [INFO] Activating virtual environment...
call venv\Scripts\activate

echo [INFO] Starting Expense Tracker...
echo.

python -m expense_tracker

echo.
echo ====================================
echo   Thanks for using Expense Tracker!
echo ====================================
pause
