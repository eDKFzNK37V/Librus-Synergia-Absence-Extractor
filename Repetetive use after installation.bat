@echo off
REM This script activates the virtual environment and shows usage instructions

call .venv\Scripts\activate.bat

echo Welcome to Librus Synergia Absence Extractor!
echo.
echo Usage instructions:
echo.
echo 1. Activate the virtual environment:
echo     call .venv\Scripts\activate.bat
echo.
echo 2. Run the extractor with:
echo     python absence-extractor.py --user YOUR_LOGIN --password YOUR_PASSWORD --signer "Your Name and Surname"
echo.
echo Optional arguments:
echo     --out FILE           Output file for NU days (default: nu_days.txt)
echo     --skip-mail         Skip mail body generation (with that function --signer will not be required)
echo     --mail-out FILE     Output file for mail body (default: usprawiedliwienie.txt)
echo     --headful           Show browser window (for debugging)
echo.
echo Example:
echo     python absence-extractor.py --user jan.kowalski --password tajnehaslo --signer "Jan Kowalski"
echo.
echo For more details, see README.md.
echo.
pause
