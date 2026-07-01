# Carsharing -  Data Analysis

Analyse-, Forecasting- und Reporting-Pipeline für das kommunale Carsharing-Netzwerk im Landkreis Regensburg.

---

## Projektziel

Dieses Projekt dient der automatisierten Verarbeitung von Carsharing-Buchungsdaten zur Erstellung von:

- Quartalsauswertungen
- Standortanalysen
- Zeitreihen
- Forecasts je Standort
- Gesamtprojekt-Forecasts
- Visualisierungen für Reportingzwecke

---

## Projektstruktur

```text
data/
├── input/
│   └── bookings/
│       ├── raw/
│       └── ano/
│
├── processed/
│   └── timeseries_monthly_per_location.csv
│   └── result_location_QX_XXXX.csv
│   └── result_total_QX_XXXX.csv
│
└── forecasts/
    ├── forecast_per_location.csv
    └── forecast_total.csv

reports/
└── figures/
    ├── per_location/
    └── total/

src/
├── preprocessing/
├── forecasting/
└── reporting/


## Workflow

### 1. Rohdaten anonymisieren

```text
clean_booking_exports.py
```

Entfernt personenbezogene Felder aus den Buchungsexporten:

- MS-Id
- Mobilitätsservice
- C-Id
- Klasse
- Rechnungsnummer

Zusätzlich werden uneinheitliche Spaltennamen standardisiert.

Output:

```text
*_ano.csv
```

---

### 2. Quartalsberichte erzeugen

```text
quarterly_report.py
```

Erzeugt:

```text
result_location_QX_JAHR.csv
result_total_QX_JAHR.csv
```

Steuerung über:

```python
JAHR = 2026
QUARTAL = 2
```

---

### 3. Zeitreihe erstellen

```text
create_monthly_timeseries.py
```

Aggregiert Buchungen monatlich je Standort.

Output:

```text
timeseries_monthly_per_location.csv
```

Kennzahlen:

- Anzahl Fahrten
- Stunden
- Kilometer
- Nutzungsentgelt (brutto)
- Nutzungsentgelt (netto)

---

### 4. Standort-Forecasts berechnen

```text
station_forecast.py
```

Output:

```text
forecast_per_location.csv
```

Prognostizierte Kennzahlen:

- Anzahl Fahrten
- Stunden
- Kilometer
- Nutzungsentgelt (brutto)
- Nutzungsentgelt (netto)

---

### Verwendete Modelle

#### Nutzungsentgelt (brutto)

Exponential Smoothing

Ziel:

- stärkere Gewichtung aktueller Entwicklungen
- robuste Prognosen bei kurzer Historie

#### Nutzungsentgelt (netto)

Deterministisches Modell:

```text
Netto = Brutto × (1 - Guthabenquote)
```

Die Guthabenquote wird als gleitender Durchschnitt der letzten vier Monate modelliert.

#### Fahrten, Stunden und Kilometer

Lineare Regression (OLS)

```text
y = a + b·t
```

---

### Qualitätskennzahlen

Für jede Prognose werden folgende R²-Werte berechnet:

- Anzahl_Fahrten_R2
- Summe_Stunden_R2
- Summe_KM_R2
- Summe_Fahrtkosten_R2
- Summe_Fahrtkosten_abzgl_Guthaben_R2

---

### 5. Gesamtprojekt aggregieren

```text
project_forecast.py
```

Aggregiert alle Standortprognosen.

Output:

```text
forecast_total.csv
```

---

### 6. Standort-Reports erzeugen

```text
station_report.py
```

Output:

```text
reports/figures/per_location/
```

Visualisiert:

- Ist 2025
- Forecast 2026
- Modellgüte (R²)

für jeden einzelnen Standort.

---

### 7. Gesamtprojekt-Report erzeugen

```text
project_report.py
```

Output:

```text
reports/figures/total/
```

Visualisiert:

- Gesamtprojekt 2025
- Gesamtprojekt Forecast 2026
- aggregierte R²-Werte

---

## Forecast Pipeline

```text
raw booking exports
        │
        ▼
clean_booking_exports.py
        │
        ▼
anonymisierte Exportdateien
        │
        ▼
create_monthly_timeseries.py
        │
        ▼
timeseries_monthly_per_location.csv
        │
        ▼
station_forecast.py
        │
        ▼
forecast_per_location.csv
        │
        ▼
project_forecast.py
        │
        ▼
forecast_total.csv
        │
        ▼
station_report.py
project_report.py
```

---

## Technischer Stack

- Python
- pandas
- NumPy
- statsmodels
- matplotlib
- seaborn

---

## Versionsstand

Version 1.0

Stand: Juni 2026

Erste vollständig reproduzierbare Forecasting- und Reporting-Pipeline für das kommunale Carsharing-Netzwerk.

Ziele: Mehr Modelle trainieren und testen