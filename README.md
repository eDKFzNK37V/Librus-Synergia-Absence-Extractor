**Librus Synergia Absence Extractor**

This project automates the extraction of non-justified absences (NU) from the Librus Synergia portal using Playwright and Python. It logs in to the portal, navigates to the attendance page, parses absence data, and saves the results to a file. Optionally, it generates a ready-to-send mail body for absence justification.

_There exists the [web version of the app](https://librus-absence-extractor-12a301a054df.herokuapp.com/), but I advice you to use the self run version of it on your PC in virtual envrioment. Which can be found in [here](https://github.com/eDKFzNK37V/Librus-Synergia-Absence-Extractor/tree/dekstop-version)._
**Features**

- Automated login to Librus Synergia via Playwright

- Extraction of NU (non-justified absences) per date

- Saves results to a tab-separated file

- Generates a compact mail body for absence justification:
```
Dzień dobry,
Proszę o usprawiedliwienie moich nieobecności z dnia:
Absences in form of (DD.MM)  roku pańskiego (Current year).

Z wyrazami szacunku
--signer
```
- CLI interface with customizable output and signature

**Requirements**

- Python 3.8+- Python 3.8+

**Instalation guide**
Clone the repository:
```
git clone https://github.com/eDKFzNK37V/Librus-Synergia-Absence-Extractor.git
```
Create and run a virtual enviorament inside a cloned repository directory:
```
python -m venv .venv
.venv\Scripts\Activate
```
Instal dependencies (in activated VE):
```
pip install -r requirements.txt
```
Run the script with use of arguments described bellow:
```
python absence-extractor.py --user YOUR_LOGIN --password YOUR_PASSWORD --signer "Your Name and Surname" 

```  

**Arguments:**

- `--user` _(required)_: Your Librus login

- `--password` _(required)_: Your Librus password 

- `--out`: Output file for NU days (default: `nu_days.txt`) 

- `--skip-mail`: Mail

- `--mail-out`: Output file for mail body (default: `usprawiedliwienie.txt`) 
  
- `--headful`: Show browser window (for debugging)

- `--signer` _(required if --skip-mail is not present)_: Name to use in mail signature (required) 

**Output**

- `nu_days.txt`: Tab-separated list of dates and NU counts (only if NU > 0)

- `usprawiedliwienie.txt`: Polish mail body for absence justification```sh

**Notes**
- This script uses Playwright to automate browser actions. The first run may require browser installation.
- For best results, use a dedicated virtual environment.
- The script is intended for educational/personal use. Do not share your credentials.

**License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
