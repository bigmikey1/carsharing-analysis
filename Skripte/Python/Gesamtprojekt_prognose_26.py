import pandas as pd
import numpy as np
import statsmodels.api as sm
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def wrap_label(label, max_len=16):
    import textwrap
    return "\n".join(textwrap.wrap(label, max_len))

def format_de(value, is_currency=False):
    formatted = f"{value:,.2f}"
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    if is_currency:
        formatted += " €"
    return formatted


# ─────────────────────────────────────────────────────────────
# Pfade
# ─────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    BASE_DIR / ".." / ".." /
    "Daten" / "Regression (Grundlage Prognose)"
)

ZEITREIHE_PATH = DATA_PATH / "Zeitreihe_Monat_Standort.csv"
PROGNOSE_PATH = DATA_PATH / "Prognose_2026_Stationsbezogen.csv"


# ─────────────────────────────────────────────────────────────
# Daten laden
# ─────────────────────────────────────────────────────────────

df = pd.read_csv(ZEITREIHE_PATH)
prognose_df = pd.read_csv(PROGNOSE_PATH)

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

# ─────────────────────────────────────────────────────────────
# Plot-Daten
# ─────────────────────────────────────────────────────────────

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

plot_df_long["Kennzahl_wrap"] = plot_df_long["Kennzahl"].apply(wrap_label)

# ─────────────────────────────────────────────────────────────
# Plot
# ─────────────────────────────────────────────────────────────

plt.rcParams["font.family"] = "Arial"
sns.set_style("whitegrid")

plt.figure(figsize=(12, 8))

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

# ─────────────────────────────────────────────────────────────
# Werte auf Balken
# ─────────────────────────────────────────────────────────────

for i, p in enumerate(ax.patches):

    value = p.get_height()

    if value < 0.005:
        continue

    kpi = plot_df_long.iloc[i % len(plot_df_long)]["Kennzahl"]

    is_currency = "Nutzungsentgelt" in kpi

    label = format_de(value, is_currency)

    ax.annotate(
        label,
        (p.get_x() + p.get_width() / 2., value),
        ha='center',
        va='bottom',
        fontsize=9
    )

# ─────────────────────────────────────────────────────────────
# R² Text
# ─────────────────────────────────────────────────────────────

r2_text = "\n".join([
    f"R² {k}: {str(v).replace('.', ',')}"
    for k, v in r2_values.items()
])

plt.text(
    0,
    plot_df_long["Wert"].max() * 0.95,
    r2_text,
    fontsize=9,
    va='top'
)

# ─────────────────────────────────────────────────────────────

plt.title("Gesamtprojekt – Ist 2025 vs Prognose 2026")
plt.ylabel("")
plt.xlabel("")

plt.tight_layout()
plt.savefig("Gesamtprojekt_vgl_prognose26.png")
plt.show()