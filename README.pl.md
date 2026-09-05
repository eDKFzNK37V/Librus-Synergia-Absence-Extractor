**Librus Synergia Absence Extractor**

[English](README.md) | Polish

Ten projekt automatyzuje proces pozyskiwania danych dotyczących nieuzasadnionych nieobecności (NU) z portalu Librus Synergia przy użyciu biblioteki Playwright i języka Python. Loguje się do portalu, przechodzi do strony obecności, analizuje dane dotyczące nieobecności i zapisuje wyniki do pliku. Opcjonalnie generuje gotową do wysłania treść wiadomości e-mail służącą do uzasadnienia nieobecności.


Można pominąć proces instalacji, korzystając z dedykowanych plików `.bat`:

`First time use.bat`

`Repetetive use after installation.bat`


**Funkcje**

- Zautomatyzowane logowanie do Librus Synergia za pomocą biblioteki Playwright

- Pobieranie danych dotyczących nieusprawiedliwionych nieobecności (NU) według daty

- Zapisywanie wyników do pliku rozdzielanego tabulatorami

- Generuje zwięzłą treść wiadomości e-mail z uzasadnieniem nieobecności:
```
Dzień dobry,
Proszę o usprawiedliwienie moich nieobecności z dnia:
Nieobecności w formacie (DD.MM)  roku pańskiego (bieżący rok).

Z wyrazami szacunku
--podpisujący
```
- Interfejs CLI z możliwością dostosowania treści wyjściowej i podpisu

**Wymagania**

- Python 3.8+

- git 2.51.0+ (do polecenia klonowania repozytorium; jeśli nie masz git, użyj przycisku do pobrania)

**Instrukcja instalacji**
Sklonuj repozytorium:
```
git clone https://github.com/eDKFzNK37V/Librus-Synergia-Absence-Extractor.git

```

lub pobierz plik ręcznie [tutaj](https://github.com/eDKFzNK37V/Librus-Synergia-Absence-Extractor/archive/refs/heads/dekstop-version.zip), rozpakuj go, a następnie przejdź do katalogu rozpakowanego folderu w wierszu poleceń.

Utwórz i uruchom środowisko wirtualne w katalogu sklonowanego repozytorium:
```
python -m venv .venv
.venv\Scripts\Activate
```
Zainstaluj zależności (w aktywowanym środowisku wirtualnym):
```
pip install -r requirements.txt
```
Uruchom skrypt, używając argumentów opisanych poniżej:
```
python absence-extractor.py --user TWOJA_NAZWA_UŻYTKOWNIKA --password TWOJE_HASŁO --signer „Twoje imię i nazwisko” 

```  

**Argumenty:**

- `--user` _(wymagane)_: Twoja nazwa użytkownika w Librus

- `--password` _(wymagane)_: Twoje hasło w Librus 

- `--out`: Plik wyjściowy zawierający liczbę dni nieobecności (domyślnie: `nu_days.txt`) 

- `--skip-mail`: Wiadomość e-mail

- `--mail-out`: Plik wyjściowy zawierający treść wiadomości e-mail (domyślnie: `usprawiedliwienie.txt`) 
  
- `--headful`: Wyświetl okno przeglądarki (do debugowania)

- `--signer` _(wymagane, jeśli nie podano opcji --skip-mail)_: Nazwa do użycia w podpisie wiadomości e-mail (wymagane) 

**Wynik**

- `nu_days.txt`: Lista dat i liczb dni NU rozdzielonych tabulatorami (tylko jeśli NU > 0)

- `usprawiedliwienie.txt`: Treść wiadomości e-mail w języku polskim zawierająca uzasadnienie nieobecności```sh

**Uwagi**
- Ten skrypt wykorzystuje bibliotekę Playwright do automatyzacji działań przeglądarki. Pierwsze uruchomienie może wymagać instalacji przeglądarki.
- Aby uzyskać najlepsze wyniki, należy korzystać z dedykowanego środowiska wirtualnego.
- Skrypt jest przeznaczony do użytku edukacyjnego/osobistego. Nie udostępniaj swoich danych logowania.

**Licencja**
Ten projekt jest objęty licencją MIT. Szczegółowe informacje znajdują się w pliku [LICENSE](LICENSE).


Przetłumaczono z DeepL.com (wersja darmowa)
