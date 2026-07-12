# Software Inventory Scanner

Program skanuje zainstalowane aplikacje Windows i zapisuje raporty w formatach TXT, CSV oraz JSON.

Jesli chcesz tylko szybko uruchomic projekt po sklonowaniu, otworz:

```text
START.md
```

## Krok 1 - wersja CLI

Cel pierwszego kroku:

- oddzielic skanowanie od zapisu raportow,
- dodac obsluge bledow,
- dodac logowanie,
- dodac eksport do kilku formatow,
- przygotowac kod tak, aby pozniej mozna bylo dodac GUI.

## Struktura projektu

```text
.
+-- app.py
+-- inventory
|   +-- __init__.py
|   +-- console_ui.py
|   +-- filters.py
|   +-- logger_setup.py
|   +-- reports.py
|   +-- scanner.py
|   +-- summary.py
|   +-- system_info.py
+-- README.md
+-- requirements.txt
```

## Co robi kazdy plik

`app.py`

- uruchamia program,
- odczytuje argumenty z konsoli,
- wywoluje skanowanie,
- zapisuje raporty,
- pokazuje uzytkownikowi wynik pracy.

`inventory/console_ui.py`

- odpowiada za czytelny wyglad konsoli,
- pokazuje panele,
- pokazuje tabele,
- pokazuje zapisane pliki.

`inventory/scanner.py`

- uruchamia kontrolowana komende PowerShell,
- skanuje rejestr Windows,
- pobiera dane z HKLM, HKCU oraz WOW6432Node,
- zamienia wynik PowerShella z JSON na dane Pythona,
- usuwa duplikaty,
- zapisuje bledy do logow.

`inventory/filters.py`

- filtruje programy po nazwie,
- filtruje programy po producencie,
- pozwala pokazac tylko programy bez wersji,
- przygotowuje informacje o aktywnych filtrach.

`inventory/reports.py`

- zapisuje raport TXT,
- zapisuje raport CSV,
- zapisuje raport JSON,
- tworzy folder dla kazdego uruchomienia,
- dodaje date i godzine do nazwy folderu oraz pliku.

`inventory/logger_setup.py`

- tworzy folder `logs`,
- zapisuje bledy do `logs/app.log`.

`inventory/summary.py`

- liczy liczbe programow,
- liczy liczbe producentow,
- liczy programy bez wersji,
- liczy programy bez producenta,
- przygotowuje liste najczestszych producentow.

`inventory/system_info.py`

- sprawdza, czy program dziala jako administrator,
- pobiera podstawowe informacje o systemie Windows.

## Kolejnosc wykonania - krok po kroku

### 1. Tworzymy strukture projektu

Czynnosc:

- tworzymy plik `app.py`,
- tworzymy folder `inventory`,
- dodajemy pliki `scanner.py`, `reports.py`, `logger_setup.py`.

Dlaczego:

- nie trzymamy calego programu w jednym pliku,
- pozniej GUI bedzie moglo uzyc tych samych modulow.

### 2. Tworzymy bezpieczniejsze skanowanie

Czynnosc:

- PowerShell uruchamiamy przez liste argumentow, nie przez skladanie tekstu od uzytkownika,
- dodajemy `-NoProfile`, aby profil PowerShella uzytkownika nie zmienial wyniku,
- dodajemy timeout,
- sprawdzamy kod zakonczenia procesu,
- zapisujemy bledy do logow.

Dlaczego:

- program jest stabilniejszy,
- latwiej znalezc blad,
- unikamy przypadkowego wykonywania danych wpisanych przez uzytkownika.

### 3. Pobieramy dane jako JSON

Czynnosc:

- PowerShell zwraca dane przez `ConvertTo-Json`,
- Python odczytuje wynik przez `json.loads`.

Dlaczego:

- JSON jest latwiejszy i bezpieczniejszy do parsowania niz tekstowa tabela PowerShella.

### 4. Normalizujemy dane

Czynnosc:

- puste wartosci zamieniamy na pusty tekst,
- usuwamy spacje z poczatku i konca,
- usuwamy duplikaty po nazwie, wersji i producencie.

Dlaczego:

- raport jest czytelniejszy,
- aplikacje z rejestru 32-bit i 64-bit nie powinny powtarzac sie bez potrzeby.

### 5. Zapisujemy raporty

Czynnosc:

- zapisujemy TXT dla czlowieka,
- CSV dla Excela,
- JSON dla dalszej automatyzacji.
- kazde uruchomienie zapisujemy w osobnym folderze z data i godzina.

Dlaczego:

- kazdy format ma inne zastosowanie,
- pozniej GUI bedzie moglo dac wybor formatu.

### 6. Testujemy program

Czynnosc:

```powershell
python -m py_compile app.py inventory\scanner.py inventory\reports.py inventory\logger_setup.py
python app.py --output work\test_reports --format all --timeout 60
```

Oczekiwany wynik:

- brak bledow skladni,
- w folderze raportow powstaje podfolder z data i godzina,
- w podfolderze powstaja pliki TXT, CSV i JSON.

### 7. Dopiero pozniej budujemy EXE

Czynnosc:

- po potwierdzeniu, ze wersja CLI dziala, instalujemy PyInstaller,
- budujemy pierwszy plik `.exe`.

Dlaczego:

- latwiej naprawiac bledy w Pythonie niz w spakowanym EXE.

## Krok 2 - podsumowanie i kontrola uprawnien

Cel drugiego kroku:

- pokazac w konsoli, czy program dziala jako administrator,
- dodac ostrzezenie, gdy program nie ma uprawnien administratora,
- dodac podsumowanie raportu,
- zapisac podsumowanie do TXT i JSON.

### 1. Sprawdzamy uprawnienia administratora

Czynnosc:

- dodajemy plik `inventory/system_info.py`,
- uzywamy Windows API przez `ctypes.windll.shell32.IsUserAnAdmin()`,
- wynik pokazujemy w konsoli.

Dlaczego:

- czesc informacji z rejestru moze byc niedostepna bez wyzszych uprawnien,
- uzytkownik od razu wie, czy raport moze byc niepelny.

### 2. Tworzymy podsumowanie

Czynnosc:

- dodajemy plik `inventory/summary.py`,
- liczymy liczbe programow,
- liczymy unikalnych producentow,
- liczymy programy bez wersji,
- liczymy programy bez producenta,
- wyznaczamy najczestszych producentow.

Dlaczego:

- raport nie jest tylko lista programow,
- od razu widac jakosc danych i ogolny obraz systemu.

### 3. Dodajemy podsumowanie do raportow

Czynnosc:

- w raporcie TXT dodajemy sekcje `SUMMARY`,
- w raporcie JSON zapisujemy obiekt z `summary` i `programs`,
- CSV zostaje plaska tabela, aby dobrze otwieral sie w Excelu.

Dlaczego:

- TXT jest wygodny do czytania,
- JSON jest dobry dla automatyzacji,
- CSV powinien zostac prosty i tabelaryczny.

### 4. Testujemy krok 2

Czynnosc:

```powershell
python -m py_compile app.py inventory\scanner.py inventory\reports.py inventory\logger_setup.py inventory\summary.py inventory\system_info.py
python app.py --format all
```

Oczekiwany wynik:

- program pokazuje, czy dziala jako administrator,
- konsola pokazuje liczbe producentow i brakujace dane,
- raport TXT zawiera sekcje `SUMMARY`,
- raport JSON zawiera pola `summary` oraz `programs`.

## Krok 3 - filtry CLI

Cel trzeciego kroku:

- dodac wyszukiwanie po nazwie programu,
- dodac filtrowanie po producencie,
- dodac opcje pokazania tylko programow bez wersji,
- zapisac informacje o filtrach w TXT i JSON.

### 1. Dodajemy modul filtrowania

Czynnosc:

- tworzymy plik `inventory/filters.py`,
- dodajemy funkcje `apply_filters`,
- dodajemy funkcje `build_filter_info`.

Dlaczego:

- logika filtrowania jest oddzielona od `app.py`,
- GUI bedzie moglo pozniej uzyc tych samych funkcji.

### 2. Dodajemy argumenty CLI

Czynnosc:

- dodajemy `--search`,
- dodajemy `--publisher`,
- dodajemy `--missing-version-only`.

Przyklady:

```powershell
python app.py --search python
python app.py --publisher Microsoft
python app.py --missing-version-only
python app.py --search visual --publisher Microsoft
```

### 3. Liczymy podsumowanie po filtrach

Czynnosc:

- najpierw skanujemy wszystkie programy,
- potem stosujemy filtry,
- dopiero na koncu liczymy podsumowanie i zapisujemy raport.

Dlaczego:

- raport pokazuje wynik dokladnie dla tego, co wybral uzytkownik,
- jednoczesnie zapisujemy liczbe programow przed filtrowaniem.

### 4. Testujemy krok 3

Czynnosc:

```powershell
python -m py_compile app.py inventory\scanner.py inventory\reports.py inventory\logger_setup.py inventory\summary.py inventory\system_info.py inventory\filters.py
python app.py --search python
python app.py --publisher Microsoft --format txt
python app.py --missing-version-only --format json
```

Oczekiwany wynik:

- program pokazuje aktywne filtry w konsoli,
- raport TXT zawiera sekcje `FILTERS`,
- raport JSON zawiera informacje o filtrach w `summary.filters`.

## Krok 4 - czytelny terminal

Cel czwartego kroku:

- poprawic wyglad wyniku w konsoli,
- dodac panele i tabele,
- oddzielic wyglad terminala od logiki programu,
- przygotowac wygodniejsza obsluge przed budowa GUI.

### 1. Dodajemy biblioteke Rich

Czynnosc:

- instalujemy biblioteke `rich`,
- dodajemy ja do `requirements.txt`.

Komenda:

```powershell
python -m pip install rich
```

Dlaczego:

- `rich` pozwala tworzyc czytelne tabele i panele w terminalu,
- program wyglada lepiej bez budowania pelnego GUI.

### 2. Tworzymy modul widoku konsoli

Czynnosc:

- tworzymy plik `inventory/console_ui.py`,
- przenosimy wyswietlanie komunikatow poza `app.py`,
- dodajemy funkcje do pokazywania naglowka, systemu, filtrow, podsumowania i zapisanych plikow.

Dlaczego:

- `app.py` pozostaje czytelny,
- pozniejsza zamiana CLI na GUI bedzie latwiejsza.

### 3. Testujemy widok

Czynnosc:

```powershell
python -m py_compile app.py inventory\console_ui.py inventory\filters.py inventory\scanner.py inventory\reports.py inventory\logger_setup.py inventory\summary.py inventory\system_info.py
python app.py --publisher Microsoft --format txt
```

Oczekiwany wynik:

- konsola pokazuje panel systemu,
- podsumowanie jest w tabeli,
- aktywne filtry sa w tabeli,
- zapisane raporty sa pokazane w osobnej tabeli.

## Uruchomienie

Jesli uruchamiasz projekt pierwszy raz, zainstaluj zaleznosci:

```powershell
python -m pip install -r requirements.txt
```

```powershell
python app.py
```

## Przyklady

Zapis wszystkich formatow do domyslnego folderu `reports`:

```powershell
python app.py
```

Przykladowe drzewo zapisu:

```text
reports
+-- 2026-07-05_08-20-00
|   +-- software_inventory_2026-07-05_08-20-00.txt
|   +-- software_inventory_2026-07-05_08-20-00.csv
|   +-- software_inventory_2026-07-05_08-20-00.json
```

Zapis tylko CSV:

```powershell
python app.py --format csv
```

Zapis do wybranego folderu:

```powershell
python app.py --output C:\Temp\inventory --format all
```

Ustawienie dluzszego limitu skanowania:

```powershell
python app.py --timeout 60
```

Filtrowanie po nazwie:

```powershell
python app.py --search python
```

Filtrowanie po producencie:

```powershell
python app.py --publisher Microsoft
```

Pokazanie tylko programow bez wersji:

```powershell
python app.py --missing-version-only
```

## Budowa pliku EXE

Najpierw instalacja PyInstaller:

```powershell
pip install pyinstaller
```

Budowa pliku EXE:

```powershell
pyinstaller --onefile --name SoftwareInventoryScanner app.py
```

Gotowy plik bedzie w folderze:

```text
dist\SoftwareInventoryScanner.exe
```
