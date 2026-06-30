import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────
# Hilfsfunktion für zweizeilige Labels
# ─────────────────────────────────────────────────────────────

def wrap_label(label, max_len=16):

    if len(label) <= max_len:
        return label

    words = label.split()

    line1 = ""
    line2 = ""

    for word in words:
        if len(line1) + len(word) + 1 <= max_len:
            line1 += (" " + word if line1 else word)
        else:
            line2 += (" " + word if line2 else word)

    return line1 + "\n" + line2


# ─────────────────────────────────────────────────────────────
# Deutsche Zahlenformatierung
# ─────────────────────────────────────────────────────────────

def format_de(value, is_currency=False):

    formatted = f"{value:,.2f}"
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")

    if is_currency:
        formatted += " €"

    return formatted


# ─────────────────────────────────────────────────────────────
# Pfade
# ─────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parents[2]

CSV_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "timeseries_monthly_per_location.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "forecasts"
    / "forecast_per_location.csv"
)

# ─────────────────────────────────────────────────────────────
# Daten laden
# ─────────────────────────────────────────────────────────────

df = pd.read_csv(CSV_PATH, sep=",")

df = df.sort_values(
    ["Stationsname", "Jahr", "Monat"]
).reset_index(drop=True)

# Zeitindex je Station
df["t"] = df.groupby("Stationsname").cumcount() + 1

# ─────────────────────────────────────────────────────────────
# Prognose je Station
# ─────────────────────────────────────────────────────────────

ergebnisse = []

for station in df["Stationsname"].unique():

    print(f"\n────────────────────────────────")
    print(f"Station: {station}")

    df_station = df[df["Stationsname"] == station].copy()

    letzter_monat = df_station.iloc[-1]["Monat"]

    fehlende_monate = 12 - letzter_monat

    print("Fehlende Monate:", fehlende_monate)

    result_row = {
        "Stationsname": station
    }

    # ─────────────────────────────────────────────────────────
    # Zeitachse
    # ─────────────────────────────────────────────────────────

    X = df_station[["t"]]

    X = sm.add_constant(X)

    t_future = np.arange(
        df_station["t"].max() + 1,
        df_station["t"].max() + fehlende_monate + 1
    )

    future_monate = list(range(letzter_monat + 1, 13))

    X_future = pd.DataFrame({"t": t_future,})

    X_future = sm.add_constant(X_future)

# ─────────────────────────────────────────────────────────
# Prognose Brutto-Umsatz: exponentielle Glättung
# ─────────────────────────────────────────────────────────

    y_brutto = df_station["Summe_Fahrtkosten"]

    try:

        model_brutto = ExponentialSmoothing(
            y_brutto,
            trend="add",
            seasonal=None
        ).fit()

        brutto_forecast = model_brutto.forecast(fehlende_monate)

    except:

        model_brutto = sm.OLS(
            y_brutto,
            X
        ).fit()

        brutto_forecast = model_brutto.predict(X_future)

    brutto_forecast = np.maximum(brutto_forecast, 0)

    brutto_ist_2026 = df_station[
        df_station["Jahr"] == 2026
            ]["Summe_Fahrtkosten"].sum()

    brutto_gesamt_2026 = (
            brutto_ist_2026 +
            brutto_forecast.sum()
        )

    result_row["Summe_Fahrtkosten_2026"] = round(
        brutto_gesamt_2026,
        2
    )

    result_row["Summe_Fahrtkosten_R2"] = np.nan


    # ─────────────────────────────────────────────────────────
    # Guthabenmodell
    # Netto = Brutto - Guthaben
    # ─────────────────────────────────────────────────────────

    df_station["Guthaben"] = (
        df_station["Summe_Fahrtkosten"]
        - df_station["Summe_Fahrtkosten_abzgl_Guthaben"]
    )

    df_station["Guthabenquote"] = np.where(
        df_station["Summe_Fahrtkosten"] > 0,
        df_station["Guthaben"]
        / df_station["Summe_Fahrtkosten"],
        0
    )

    # Rolling Mean der letzten 4 Monate
    guthabenquote = (
        df_station["Guthabenquote"]
        .tail(4)
        .mean()
    )

    # Sicherheit
    guthabenquote = np.clip(
        guthabenquote,
        0,
        0.5
    )

    # Netto berechnen
    netto_forecast = (
        brutto_forecast *
        (1 - guthabenquote)
    )

    netto_ist_2026 = df_station[
        df_station["Jahr"] == 2026
    ]["Summe_Fahrtkosten_abzgl_Guthaben"].sum()

    netto_gesamt_2026 = (
        netto_ist_2026 +
        netto_forecast.sum()
    )

    # Constraint
    netto_gesamt_2026 = min(
        netto_gesamt_2026,
        brutto_gesamt_2026
    )

    # ─────────────────────────────────────────────────────────
    # R² Netto-Modell
    # ─────────────────────────────────────────────────────────

    netto_real = df_station[
        "Summe_Fahrtkosten_abzgl_Guthaben"
    ]

    netto_pred_hist = (
        df_station["Summe_Fahrtkosten"]
        * (1 - guthabenquote)
    )

    ss_res = np.sum(
        (netto_real - netto_pred_hist) ** 2
    )

    ss_tot = np.sum(
        (netto_real - netto_real.mean()) ** 2
    )

    if ss_tot > 0:
        r2_netto = 1 - (ss_res / ss_tot)
    else:
        r2_netto = np.nan

    result_row[
        "Summe_Fahrtkosten_abzgl_Guthaben_R2"
    ] = round(
        r2_netto,
        3
    )

    result_row[
        "Summe_Fahrtkosten_abzgl_Guthaben_2026"
    ] = round(
        netto_gesamt_2026,
        2
    )

    # ─────────────────────────────────────────────────────────
    # Klassische Kennzahlen - Regression
    # ─────────────────────────────────────────────────────────

    STANDARD_KENNZAHLEN = [
            "Anzahl_Fahrten",
            "Summe_Stunden",
            "Summe_KM"
        ]

    for kennzahl in STANDARD_KENNZAHLEN:

        y = df_station[kennzahl]

        model = sm.OLS(
            y,
            X
        ).fit()

        forecast = model.predict(X_future)

        forecast = np.maximum(forecast, 0)

        ist_2026 = df_station[
            df_station["Jahr"] == 2026
        ][kennzahl].sum()

        gesamt_2026 = (
            ist_2026 +
            forecast.sum()
        )

        result_row[f"{kennzahl}_2026"] = round(
            gesamt_2026,
            2
        )

        result_row[f"{kennzahl}_Trend_monat"] = round(
            model.params["t"],
            3
        )

        result_row[f"{kennzahl}_R2"] = round(
            model.rsquared,
            3
        )


    model_brutto_r2 = sm.OLS(
        y_brutto,
        X
    ).fit()

    result_row["Summe_Fahrtkosten_R2"] = round(
        model_brutto_r2.rsquared,
        3
    )

    ergebnisse.append(result_row)


# ─────────────────────────────────────────────────────────────
# Export
# ─────────────────────────────────────────────────────────────


prognose_df = pd.DataFrame(ergebnisse)

print(prognose_df.shape)

print(
    prognose_df["Stationsname"]
    .value_counts()
)

prognose_df = pd.DataFrame(ergebnisse)

prognose_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("Prognose je Station exportiert")
print(OUTPUT_PATH)