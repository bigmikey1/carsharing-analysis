import pandas as pd
import numpy as np
import statsmodels.api as sm
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt


from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# ─────────────────────────────────────────────────────────────
# Deutsche Zahlenformatierung
# ─────────────────────────────────────────────────────────────

def format_de(value, is_currency=False):

    formatted = f"{value:,.2f}"
    formatted = (
        formatted
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    if is_currency:
        formatted += " €"

    return formatted

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
            line1 += (
                " " + word
                if line1
                else word
            )
        else:
            line2 += (
                " " + word
                if line2
                else word
            )

    return line1 + "\n" + line2

BASE_DIR = Path(__file__).resolve().parents[2]

TIMESERIES_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "timeseries_monthly_per_location.csv"
)

FORECAST_PATH = (
    BASE_DIR
    / "data"
    / "forecasts"
    / "forecast_per_location.csv"
)

OUTPUT_FOLDER = (
    BASE_DIR
    / "reports"
    / "figures"
    / "per_location"
)

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)


print("BASE_DIR:", BASE_DIR)
print("TIMESERIES:", TIMESERIES_PATH.exists())
print("FORECAST:", FORECAST_PATH.exists())


zeit_df = pd.read_csv(TIMESERIES_PATH)

prognose_df = pd.read_csv(FORECAST_PATH)


REPORT_YEAR = 2026
BASE_YEAR = 2025

# ─────────────────────────────────────────────────────────────
# Aggregation Zeitreihe
# ─────────────────────────────────────────────────────────────

df_agg = (
    df.groupby(["Jahr", "Monat"])
    .sum(numeric_only=True)
    .reset_index()
)

# Zeitindex neu
df_agg = df_agg.sort_values(["Jahr", "Monat"]).reset_index(drop=True)
df_agg["t"] = range(1, len(df_agg) + 1)

# ─────────────────────────────────────────────────────────────
# IST 2025 gesamt
# ─────────────────────────────────────────────────────────────

ist_2025 = {
    "Fahrten": df_agg[df_agg["Jahr"] == 2025]["Anzahl_Fahrten"].sum(),
    "Stunden": df_agg[df_agg["Jahr"] == 2025]["Summe_Stunden"].sum(),
    "KM": df_agg[df_agg["Jahr"] == 2025]["Summe_KM"].sum(),
    "Nutzungsentgelt (brutto)": df_agg[df_agg["Jahr"] == 2025]["Summe_Fahrtkosten"].sum(),
    "Nutzungsentgelt (netto, nach Guthaben)": df_agg[df_agg["Jahr"] == 2025]["Summe_Fahrtkosten_abzgl_Guthaben"].sum()
}

# ─────────────────────────────────────────────────────────────
# Prognose 2026 gesamt
# ─────────────────────────────────────────────────────────────

prognose_2026 = {
    "Fahrten": prognose_df["Anzahl_Fahrten_2026"].sum(),
    "Stunden": prognose_df["Summe_Stunden_2026"].sum(),
    "KM": prognose_df["Summe_KM_2026"].sum(),
    "Nutzungsentgelt (brutto)": prognose_df["Summe_Fahrtkosten_2026"].sum(),
    "Nutzungsentgelt (netto, nach Guthaben)": prognose_df["Summe_Fahrtkosten_abzgl_Guthaben_2026"].sum()
}

# ─────────────────────────────────────────────────────────────
# R² Gesamt berechnen
# ─────────────────────────────────────────────────────────────

r2_values = {}

mapping = {
    "Fahrten": "Anzahl_Fahrten",
    "Stunden": "Summe_Stunden",
    "KM": "Summe_KM",
    "Nutzungsentgelt (brutto)": "Summe_Fahrtkosten"
}

for name, col in mapping.items():

    df_hist = df_agg[df_agg["Jahr"] <= 2026]

    X = sm.add_constant(df_hist["t"])
    y = df_hist[col]

    model = sm.OLS(y, X).fit()

    r2_values[name] = round(model.rsquared, 3)