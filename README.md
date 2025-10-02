# Librus Synergia Absence Extractor# Librus Synergia Absence Extractor

This project automates the extraction of non-justified absences (NU) from the Librus Synergia portal using Playwright and Python. It logs in to the portal, navigates to the attendance page, parses absence data, and saves the results to a file. Optionally, it generates a ready-to-send mail body for absence justification.This project automates the extraction of non-justified absences (NU) from the Librus Synergia portal using Playwright and Python. It logs in to the portal, navigates to the attendance page, parses absence data, and saves the results to a file. Optionally, it generates a ready-to-send mail body for absence justification.

## Features## Features

- Automated login to Librus Synergia via Playwright- Automated login to Librus Synergia via Playwright

- Extraction of NU (non-justified absences) per date- Extraction of NU (non-justified absences) per date

- Saves results to a tab-separated file- Saves results to a tab-separated file

- Generates a compact mail body for absence justification- Generates a compact mail body for absence justification

- CLI interface with customizable output and signature- CLI interface with customizable output and signature

## Requirements## Requirements

- Python 3.8+- Python 3.8+

- Playwright for Python- [Playwright for Python](https://playwright.dev/python/)

- BeautifulSoup4- BeautifulSoup4

Install dependencies with:## Installation

````sh1. Clone the repository:

pip install -r requirements.txt   ```sh

python -m playwright install   git clone https://github.com/eDKFzNK37V/Librus-Synergia-Absence-Extractor.git

```   cd Librus-Synergia-Absence-Extractor

````

## Usage2. Create and activate a virtual environment (recommended):

Run the script with your Librus credentials: ```sh

````sh python -m venv .venv

python absence-extractor.py --user YOUR_LOGIN --password YOUR_PASSWORD --signer "Your Name"   .venv\Scripts\activate  # On Windows

```   source .venv/bin/activate  # On Linux/macOS

````

### Arguments3. Install dependencies:

- `--user` (required): Your Librus login ```sh

- `--password` (required): Your Librus password pip install -r requirements.txt

- `--out`: Output file for NU days (default: `nu_days.txt`) # If requirements.txt is missing, install manually:

- `--mail-out`: Output file for mail body (default: `usprawiedliwienie.txt`) pip install playwright beautifulsoup4

- `--signer`: Name to use in mail signature (required) python -m playwright install

- `--headful`: Show browser window (for debugging) ```

## Output## Usage

- `nu_days.txt`: Tab-separated list of dates and NU counts (only NU > 0)Run the script with your Librus credentials:

- `usprawiedliwienie.txt`: Polish mail body for absence justification```sh

python absence-extractor.py --user YOUR_LOGIN --password YOUR_PASSWORD --out nu_days.txt --mail-out usprawiedliwienie.txt --signer "Your Name"

## Example```

````

python absence-extractor.py --user jan.kowalski --password secret123 --signer "Jan Kowalski"### Arguments

```- `--user` (required): Your Librus login

- `--password` (required): Your Librus password

## Notes- `--out`: Output file for NU days (default: `nu_days.txt`)

- This script uses Playwright to automate browser actions. The first run may require browser installation.- `--mail-out`: Output file for mail body (default: `usprawiedliwienie.txt`)

- For best results, use a dedicated virtual environment.- `--signer`: Name to use in mail signature (required)

- The script is intended for educational/personal use. Do not share your credentials.- `--headful`: Show browser window (for debugging)



## License## Output

MIT License- `nu_days.txt`: Tab-separated list of dates and NU counts (only NU > 0)

- `usprawiedliwienie.txt`: Polish mail body for absence justification

## Example
````

python absence-extractor.py --user jan.kowalski --password secret123 --signer "Jan Kowalski"

```

## Notes
- This script uses Playwright to automate browser actions. The first run may require browser installation.
- For best results, use a dedicated virtual environment.
- The script is intended for educational/personal use. Do not share your credentials.

## License
MIT License
```
