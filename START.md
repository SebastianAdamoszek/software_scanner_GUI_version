# Szybki Start

Ta instrukcja jest dla osoby, ktora dopiero sklonowala projekt i chce szybko uruchomic program w VS Code.

## 1. Otworz projekt w VS Code

Otworz folder projektu, czyli folder, w ktorym widzisz pliki:

```text
app.py
requirements.txt
setup.bat
run.bat
inventory/
```

## 2. Otworz terminal

W VS Code wybierz:

```text
Terminal -> New Terminal
```

## 3. Zainstaluj biblioteki

W terminalu wpisz:

```powershell
.\setup.bat
```

Ten krok instaluje biblioteki z pliku `requirements.txt`.

## 4. Uruchom skaner

W terminalu wpisz:

```powershell
.\run.bat
```

Program przeskanuje zainstalowane aplikacje i zapisze raporty.

## 5. Gdzie sa raporty

Raporty znajdziesz w folderze:

```text
reports/
```

Kazde uruchomienie tworzy osobny folder z data i godzina, na przyklad:

```text
reports/
+-- 2026-07-05_08-50-33/
|   +-- software_inventory_2026-07-05_08-50-33.txt
|   +-- software_inventory_2026-07-05_08-50-33.csv
|   +-- software_inventory_2026-07-05_08-50-33.json
```

## Przydatne komendy

Uruchomienie bez plikow `.bat`:

```powershell
python app.py
```

Tylko raport CSV:

```powershell
python app.py --format csv
```

Filtrowanie po producencie:

```powershell
python app.py --publisher Microsoft
```

Pokazanie tylko programow bez wersji:

```powershell
python app.py --missing-version-only
```
