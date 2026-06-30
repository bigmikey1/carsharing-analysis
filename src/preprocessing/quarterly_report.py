import pandas as pd
from pathlib import Path

# ---------------------------------------------------
# Konfiguration
# ---------------------------------------------------
# Die Abfrage ist das einzige was jeweils geändert werden muss. z.B. Ende Q3 2026 dann 
# JAHR = 2026
# QUARTAL = 3
# einfach ersetzen, sobald die neue Datei im ano-Ordner liegt.

JAHR = 2025
QUARTAL = 1

GUELTIGE_TARIFE = [
    "Basis-Tarif",
    "Eco-Tarif",
    "Studierenden-Tarif",
    "ÖPNV-Abo-Tarif",
    "Firmen-Tarif Dienstfahrten",
    "Kommunal-Tarif Dienstfahrten"
]

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FOLDER = (
    BASE_DIR
    / "data"
    / "input"
    / "bookings"
    / "ano"
)

OUTPUT_FOLDER = (
    BASE_DIR
    / "data"
    / "processed"
)

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

# ---------------------------------------------------
# Quartalsdatei bestimmen
# ---------------------------------------------------

DATEI_MAPPING = {
    (2025, 1): "Buchungen_01-03_25_ano.csv",
    (2025, 2): "Buchungen_04-06_25_ano.csv",
    (2025, 3): "Buchungen_07-09_25_ano.csv",
    (2025, 4): "Buchungen_10-12_25_ano.csv",
    (2026, 1): "Buchungen_01-03_26_ano.csv",
    (2026, 2): "Buchungen_04-06_26_ano.csv"
}

DATEI = INPUT_FOLDER / DATEI_MAPPING[(JAHR, QUARTAL)]

print("Lade:", DATEI)

# ---------------------------------------------------
# Daten laden
# ---------------------------------------------------

df = pd.read_csv(
    DATEI,
    sep=";",
    dtype=str
)

print(df.columns.tolist())

# ---------------------------------------------------
# Bereinigung
# ---------------------------------------------------

for spalte in [
    "Tarif",
    "Stationsname",
    "Abrechnungsmonat",
    "Buchungsstatus"
]:
    df[spalte] = df[spalte].str.strip()

# ---------------------------------------------------
# Filter
# ---------------------------------------------------

df = df[
    df["Tarif"].isin(GUELTIGE_TARIFE)
]

# ---------------------------------------------------
# Numerische Felder
# ---------------------------------------------------

numerische_spalten = [
    "Fahrtdauer_std",
    "KM",
    "Fahrtkosten",
    "Fahrtkosten_nach_Guthaben"
]

for spalte in numerische_spalten:

    df[spalte] = (
        df[spalte]
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

# ---------------------------------------------------
# Stationsaggregation
# ---------------------------------------------------

stationen_df = (
    df.groupby("Stationsname", dropna=False)
    .agg(
        Anzahl_Fahrten=(
            "Buchungsstatus",
            lambda x: (x == "finished").sum()
        ),
        Summe_Stunden=(
            "Fahrtdauer_std",
            "sum"
        ),
        Summe_KM=(
            "KM",
            "sum"
        ),
        Summe_Fahrtkosten=(
            "Fahrtkosten",
            "sum"
        ),
        Summe_Fahrtkosten_abzgl_Guthaben=(
            "Fahrtkosten_nach_Guthaben",
            "sum"
        )
    )
    .reset_index()
    .sort_values(
        "Anzahl_Fahrten",
        ascending=False
    )
)

# ---------------------------------------------------
# Gesamtsumme
# ---------------------------------------------------

gesamt_df = pd.DataFrame([{
    "Zeitraum": f"Q{QUARTAL} {JAHR}",
    "Anzahl_Fahrten":
        stationen_df["Anzahl_Fahrten"].sum(),

    "Summe_Stunden":
        stationen_df["Summe_Stunden"].sum(),

    "Summe_KM":
        stationen_df["Summe_KM"].sum(),

    "Summe_Fahrtkosten":
        stationen_df["Summe_Fahrtkosten"].sum(),

    "Summe_Fahrtkosten_abzgl_Guthaben":
        stationen_df["Summe_Fahrtkosten_abzgl_Guthaben"].sum()
}])

# ---------------------------------------------------
# Export
# ---------------------------------------------------

station_output = (
    OUTPUT_FOLDER
    / f"result_location_Q{QUARTAL}_{JAHR}.csv"
)

gesamt_output = (
    OUTPUT_FOLDER
    / f"result_total_Q{QUARTAL}_{JAHR}.csv"
)

stationen_df.to_csv(
    station_output,
    index=False
)

gesamt_df.to_csv(
    gesamt_output,
    index=False
)

print("Erstellt:")
print(station_output)
print(gesamt_output)