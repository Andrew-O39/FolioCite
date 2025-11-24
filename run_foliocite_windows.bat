@echo off
setlocal

echo ======================================
echo   FolioCite - Local Setup and Launch
echo ======================================
echo.

REM --- Always work in the folder of this script ---
cd /d "%~dp0"

REM --- Detect Python (try py, then python) ---
where py >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    set PY_CMD=py
) ELSE (
    set PY_CMD=python
)

echo Using Python command: %PY_CMD%
echo.

REM --- Create virtual environment if it doesn't exist ---
IF NOT EXIST .venv (
    echo Creating virtual environment in ".venv" ...
    %PY_CMD% -m venv .venv
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo Failed to create virtual environment. Make sure Python is installed.
        echo You can download it from https://www.python.org/
        pause
        exit /b 1
    )
) ELSE (
    echo Virtual environment ".venv" already exists. Skipping creation.
)

REM --- Activate virtual environment ---
call .venv\Scripts\activate

REM --- Install dependencies (no pip upgrade to avoid confusing message) ---
echo.
echo Installing dependencies from requirements.txt ...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo There was an error installing dependencies.
    echo Please check that "requirements.txt" is in the same folder as this file.
    pause
    exit /b 1
)

echo.
echo ======================================
echo   Starting FolioCite
echo   Open your browser at:
echo     http://127.0.0.1:8000
echo   Close this window to stop the app.
echo ======================================
echo.

REM --- Open browser ---
start "" http://127.0.0.1:8000

REM --- Run Uvicorn (app lives in FolioCiteApp/main.py) ---
%PY_CMD% -m uvicorn FolioCiteApp.main:app --host 127.0.0.1 --port 8000

echo.
echo Uvicorn has stopped. Press any key to close this window.
pause
endlocal