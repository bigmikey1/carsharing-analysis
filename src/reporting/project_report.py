import pandas as pd
import numpy as np
import statsmodels.api as sm
from pathlib import Path
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
    / "forecast_total.csv"
)

OUTPUT_FOLDER = (
    BASE_DIR
    / "reports"
    / "figures"
    / "total"
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
# Gesamtprojekt aggregieren
# ─────────────────────────────────────────────────────────────

df_agg = (
    zeit_df
    .groupby("Jahr")
    .agg(
        Anzahl_Fahrten=("Anzahl_Fahrten", "sum"),
        Summe_Stunden=("Summe_Stunden", "sum"),
        Summe_KM=("Summe_KM", "sum"),
        Summe_Fahrtkosten=("Summe_Fahrtkosten", "sum"),
        Summe_Fahrtkosten_abzgl_Guthaben=(
            "Summe_Fahrtkosten_abzgl_Guthaben",
            "sum"
        )
    )
    .reset_index()
)

row = prognose_df.iloc[0]

ist_2025 = {
    "Fahrten":
        df_agg.loc[
            df_agg["Jahr"] == BASE_YEAR,
            "Anzahl_Fahrten"
        ].iloc[0],

    "Stunden":
        df_agg.loc[
            df_agg["Jahr"] == BASE_YEAR,
            "Summe_Stunden"
        ].iloc[0],

    "KM":
        df_agg.loc[
            df_agg["Jahr"] == BASE_YEAR,
            "Summe_KM"
        ].iloc[0],

    "Nutzungsentgelt (brutto)":
        df_agg.loc[
            df_agg["Jahr"] == BASE_YEAR,
            "Summe_Fahrtkosten"
        ].iloc[0],

    "Nutzungsentgelt (netto, nach Guthaben)":
        df_agg.loc[
            df_agg["Jahr"] == BASE_YEAR,
            "Summe_Fahrtkosten_abzgl_Guthaben"
        ].iloc[0]
}

prognose_2026 = {
    "Fahrten":
        row["Anzahl_Fahrten_2026"],

    "Stunden":
        row["Summe_Stunden_2026"],

    "KM":
        row["Summe_KM_2026"],

    "Nutzungsentgelt (brutto)":
        row["Summe_Fahrtkosten_2026"],

    "Nutzungsentgelt (netto, nach Guthaben)":
        row["Summe_Fahrtkosten_abzgl_Guthaben_2026"]
}

plot_df = pd.DataFrame({
        "Kennzahl": list(ist_2025.keys()),
        "Ist 2025": list(ist_2025.values()),
        "Prognose 2026": list(prognose_2026.values())
    })

plot_df_long = plot_df.melt(
        id_vars="Kennzahl",
        var_name="Typ",
        value_name="Wert"
    )

plot_df_long["Kennzahl_wrap"] = (
        plot_df_long["Kennzahl"]
        .apply(wrap_label)
    )

plt.figure(figsize=(11, 7))

ax = sns.barplot(
        data=plot_df_long,
        x="Kennzahl_wrap",
        y="Wert",
        hue="Typ",
        palette={
            "Ist 2025": "#4C72B0",
            "Prognose 2026": "#DD8452"
        }
    )

    # Werte auf Balken annotieren
for i, p in enumerate(ax.patches):

        value = p.get_height()

        if value < 0.005:
            continue

        kpi = plot_df_long.iloc[
            i % len(plot_df_long)
        ]["Kennzahl"]

        is_currency = (
            "Nutzungsentgelt" in kpi
        )

        label = format_de(
            value,
            is_currency
        )

        ax.annotate(
            label,
            (
                p.get_x() + p.get_width() / 2.,
                value
            ),
            ha='center',
            va='bottom',
            fontsize=8
        )

    # ── R² für alle Kennzahlen anzeigen ───────────────────────

r2_text = ""

r2_mapping = {
    "Fahrten": "Anzahl_Fahrten_R2",
    "Stunden": "Summe_Stunden_R2",
    "KM": "Summe_KM_R2",
    "Nutzungsentgelt (brutto)": "Summe_Fahrtkosten_R2",
    "Nutzungsentgelt (netto, nach Guthaben)": "Summe_Fahrtkosten_abzgl_Guthaben_R2"
    }

for kpi, col in r2_mapping.items():

    if col in row.index:
        val = row[col]

        if pd.isna(val):
            val_str = "-"
        else:
            val_str = f"{val:.3f}".replace(".", ",")

        r2_text += f"R² {kpi}: {val_str}\n"

    # Plotten
plt.text(
    0,
    plot_df_long["Wert"].max() * 0.95,
    r2_text,
    fontsize=8,
    va='top'
    )
    # Titel
plt.title(
    f"Gesamtprojekt – Ist {BASE_YEAR} vs Forecast {REPORT_YEAR}"
    )

    # Achsenbeschriftungen
plt.ylabel("")
plt.xlabel("")
plt.tight_layout()
    
    # Speichern
plt.savefig(
    OUTPUT_FOLDER
    / f"Gesamtprojekt_vgl_forecast{str(REPORT_YEAR)[-2:]}.png",
    dpi=300,
    bbox_inches="tight"
    )

plt.close()