@echo off
REM Combined setup and instructions script for Librus Absence Extractor

REM 1. Create virtual environment if it doesn't exist
IF NOT EXIST ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM 2. Activate virtual environment
call .venv\Scripts\activate.bat

REM 3. Upgrade pip
python -m pip install --upgrade pip

REM 4. Install requirements
pip install -r requirements.txt

REM 5. Install Playwright and browsers
playwright install



REM 6. Run instructions-with-venv.bat in a new Command Prompt
start cmd /k "instructions-with-venv.bat"

echo Setup complete. Instructions window opened.
