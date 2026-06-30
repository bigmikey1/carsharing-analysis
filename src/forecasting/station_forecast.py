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

BASE_DIR = Path(__file__).resolve().parent

CSV_PATH = (
    BASE_DIR
    / ".."
    / ".."
    / "Daten"
    / "Regression (Grundlage Prognose)"
    / "Zeitreihe_Monat_Standort.csv"
).resolve()

OUTPUT_PATH = (
    BASE_DIR
    / ".."
    / ".."
    / "Daten"
    / "Regression (Grundlage Prognose)"
    / "Prognose_2026_Stationsbezogen.csv"
).resolve()

print("CSV Pfad:", CSV_PATH)
print("Existiert:", CSV_PATH.exists())


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

    ergebnisse.append(result_row)

    # R² für Fahrtkosten über OLS zusätzlich berechnen (nur zur Bewertung, weil ExponentialSmoothing kein R² liefert)
    model_brutto_r2 = sm.OLS(
        y_brutto,
        X
    ).fit()

    result_row["Summe_Fahrtkosten_R2"] = round(
        model_brutto_r2.rsquared,
        3
    )

# ─────────────────────────────────────────────────────────────
# Export
# ─────────────────────────────────────────────────────────────

prognose_df = pd.DataFrame(ergebnisse)

prognose_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("Prognose je Station exportiert")
print(OUTPUT_PATH)

# ─────────────────────────────────────────────────────────────
# Einstellungen für Plots
# ─────────────────────────────────────────────────────────────

plt.rcParams["font.family"] = "Arial"

sns.set_style("whitegrid")

zeit_df = df.copy()

# ─────────────────────────────────────────────────────────────
# Einzelplots
# ─────────────────────────────────────────────────────────────

for station in prognose_df["Stationsname"]:

    row = prognose_df[
        prognose_df["Stationsname"] == station
    ]

    df_station = zeit_df[
        zeit_df["Stationsname"] == station
    ]


    ist_2025 = {
        "Fahrten":
            df_station[df_station["Jahr"] == 2025]["Anzahl_Fahrten"].sum(),

        "Stunden":
            df_station[df_station["Jahr"] == 2025]["Summe_Stunden"].sum(),

        "KM":
            df_station[df_station["Jahr"] == 2025]["Summe_KM"].sum(),

        "Nutzungsentgelt (brutto)":
            df_station[df_station["Jahr"] == 2025]["Summe_Fahrtkosten"].sum(),

        "Nutzungsentgelt (netto, nach Guthaben)":
            df_station[df_station["Jahr"] == 2025]["Summe_Fahrtkosten_abzgl_Guthaben"].sum()
    }

    prognose_2026 = {
        "Fahrten":
            row["Anzahl_Fahrten_2026"].values[0],

        "Stunden":
            row["Summe_Stunden_2026"].values[0],

        "KM":
            row["Summe_KM_2026"].values[0],

        "Nutzungsentgelt (brutto)":
            row["Summe_Fahrtkosten_2026"].values[0],

        "Nutzungsentgelt (netto, nach Guthaben)":
            row["Summe_Fahrtkosten_abzgl_Guthaben_2026"].values[0]
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

        if col in row.columns:
            val = row[col].values[0]

            if pd.isna(val):
                val_str = "-"
            else:
                val_str = str(val).replace(".", ",")

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
        f"{station} – Ist 2025 vs Prognose 2026"
    )
    # Achsenbeschriftungen
    plt.ylabel("")
    plt.xlabel("")

    plt.tight_layout()
    # Speichern
    plt.savefig(
        f"{station}_vgl_prognose26.png"
    )
    # Anzeigen
    plt.show()

    plt.close()