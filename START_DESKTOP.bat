@echo off
echo ========================================
echo Chemical Equipment Visualizer - Desktop
echo ========================================
echo.

cd frontend-desktop

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing/Updating dependencies...
pip install -q -r requirements.txt

echo.
echo Starting Desktop Application...
echo.
python src\main.py

pause
