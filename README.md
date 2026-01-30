

**System Generowania Raportów** to aplikacja analityczna stworzona w języku Python. Narzędzie automatyzuje proces przetwarzania surowych danych sprzedażowych (pliki CSV) i konwertuje je na profesjonalne, sformatowane raporty w formacie PDF.

Aplikacja posiada graficzny interfejs użytkownika (GUI) i działa jako samodzielny program wykonywalny (`.exe`), niewymagający instalacji środowiska Python na komputerze docelowym.

---

## Kluczowe Funkcjonalności

* **Przetwarzanie Danych (ETL):** Import, czyszczenie i agregacja danych z plików CSV przy użyciu biblioteki `Pandas`.
* **Generowanie PDF:** Dynamiczne tworzenie dokumentów zawierających nagłówki, stopki, numerację stron oraz tabele z wynikami analizy (z wykorzystaniem `FPDF`).
* **Interfejs Graficzny (GUI):** Responsywne okno aplikacji zbudowane w `Tkinter`, obsługujące zdarzenia użytkownika i okna dialogowe plików systemowych.
* **Obsługa Kodowania:** Zaimplementowano mechanizmy sanitizacji tekstu (transliteracja polskich znaków), aby zapewnić zgodność ze standardem kodowania `Latin-1` w dokumentach PDF.
* **Standalone Deployment:** Aplikacja skompilowana do pojedynczego pliku wykonywalnego `.exe` (Portable).

---

## Stack Technologiczny

Projekt wykorzystuje standardy przemysłowe w zakresie analizy danych i automatyzacji biurowej:

* **Core:** Python 3.12+
* **Data Analysis:** `pandas` (DataFrames, GroupBy, Aggregations).
* **PDF Engine:** `fpdf` (Programowe rysowanie dokumentów).
* **GUI:** `tkinter` + `ttk` (Natywne widgety Windows).
* **Build Tool:** `PyInstaller` (Kompilacja do kodu maszynowego).

---

## Instalacja i Uruchomienie (Dla Programistów)

Aby uruchomić projekt ze źródeł, wykonaj poniższe kroki:

1.  **Sklonuj repozytorium:**
    ```bash
    git clone https://github.com/wiktoriasikerko05/Projekt-nr-7---Raport-generator.git
    cd raport-generator
    ```

2.  **Zainstaluj wymagane biblioteki:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Uruchom aplikację:**
    ```bash
    python raport_generator.py
    ```

---

## Budowanie pliku .EXE (Deployment)

Aby stworzyć wersję dystrybucyjną dla klienta (plik `.exe`), użyto następującej konfiguracji PyInstallera:

```bash
python -m PyInstaller --onefile --windowed raport_generator.py
