from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm


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

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "forecasts"
    / "forecast_total.csv"
)

OUTPUT_PATH.parent.mkdir(
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

forecast_total = {

    "Anzahl_Fahrten_2026":
        prognose_df["Anzahl_Fahrten_2026"].sum(),

    "Summe_Stunden_2026":
        prognose_df["Summe_Stunden_2026"].sum(),

    "Summe_KM_2026":
        prognose_df["Summe_KM_2026"].sum(),

    "Summe_Fahrtkosten_2026":
        prognose_df["Summe_Fahrtkosten_2026"].sum(),

    "Summe_Fahrtkosten_abzgl_Guthaben_2026":
        prognose_df[
            "Summe_Fahrtkosten_abzgl_Guthaben_2026"
        ].sum()
}

r2_values = {}

mapping = {
    "Anzahl_Fahrten":
        "Anzahl_Fahrten",

    "Summe_Stunden":
        "Summe_Stunden",

    "Summe_KM":
        "Summe_KM",

    "Summe_Fahrtkosten":
        "Summe_Fahrtkosten",

    "Summe_Fahrtkosten_abzgl_Guthaben":
        "Summe_Fahrtkosten_abzgl_Guthaben"
}

df_agg = (
    zeit_df
    .groupby(["Jahr", "Monat"])
    .sum(numeric_only=True)
    .reset_index()
)

df_agg = (
    df_agg
    .sort_values(["Jahr", "Monat"])
    .reset_index(drop=True)
)

df_agg["t"] = range(
    1,
    len(df_agg) + 1
)

for output_name, col in mapping.items():

    X = sm.add_constant(df_agg["t"])

    y = df_agg[col]

    model = sm.OLS(
        y,
        X
    ).fit()

    r2_values[
        f"{output_name}_R2"
    ] = round(
        model.rsquared,
        3
    )

forecast_total.update(
    r2_values
)

forecast_total_df = pd.DataFrame(
    [forecast_total]
)

forecast_total_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    "Gesamtforecast gespeichert:"
)

print(
    OUTPUT_PATH
)