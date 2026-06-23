import pandas as pd
from pathlib import Path

#Konfiguration 
DATEN_ORDNER = Path("Daten") / "Buchungen (Export)"

# Alle CSV-Dateien rekursiv einsammeln
csv_dateien = list(DATEN_ORDNER.rglob("*.csv"))

print(f"Gefundene CSV-Dateien: {len(csv_dateien)}")
for pfad in csv_dateien:
    print(pfad)

GUELTIGE_TARIFE = [
    "Basis-Tarif",
    "Eco-Tarif",
    "Studierenden-Tarif",
    "ÖPNV-Abo-Tarif",
    "Firmen-Tarif Dienstfahrten",
    "Kommunal-Tarif Dienstfahrten"]

# CSV einlesen

dfs = []

for csv_datei in csv_dateien:
    df = pd.read_csv(csv_datei, sep=";", dtype=str)
    df["Quelle_Datei"] = csv_datei.name      # optional, sehr hilfreich!
    df["Quelle_Ordner"] = csv_datei.parent.name # optional, sehr hilfreich!
    dfs.append(df)

roh_df = pd.concat(dfs, ignore_index=True)

print("Alle Buchungsdaten geladen")
print(roh_df.shape)

# ── Bereinigung ────────────────────────────────────────────────
roh_df["Tarif"] = roh_df["Tarif"].str.strip()
roh_df["Stationsname"] = roh_df["Stationsname"].str.strip()
roh_df["Abrechnungsmonat"] = roh_df["Abrechnungsmonat"].str.strip()
roh_df["Buchungsstatus"] = roh_df["Buchungsstatus"].str.strip()

# ── Filter ─────────────────────────────────────────────────────
roh_df = roh_df[roh_df["Tarif"].isin(GUELTIGE_TARIFE)]

# ── Zeitspalten ableiten ───────────────────────────────────────
roh_df["Jahr"] = roh_df["Abrechnungsmonat"].str.slice(0, 4).astype(int)
roh_df["Monat"] = roh_df["Abrechnungsmonat"].str.slice(5, 7).astype(int)
roh_df["JahrMonat"] = roh_df["Abrechnungsmonat"]

# ── Numerische Spalten korrekt konvertieren ────────────────────
numerische_spalten = ["Fahrtdauer_std", "KM", "Fahrtkosten", "Fahrtkosten_nach_Guthaben"]

for spalte in numerische_spalten:
    roh_df[spalte] = (
        roh_df[spalte]
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

# ── Monatsaggregation pro Station ──────────────────────────────
monats_df = (
    roh_df
    .groupby(["Stationsname", "Jahr", "Monat", "JahrMonat"])
    .agg(
        Anzahl_Fahrten=(
            "Buchungsstatus",
            lambda x: (x == "finished").sum()
        ),
        Summe_Stunden=("Fahrtdauer_std", "sum"),
        Summe_KM=("KM", "sum"),
        Summe_Fahrtkosten=("Fahrtkosten", "sum"),
        Summe_Fahrtkosten_abzgl_Guthaben=("Fahrtkosten_nach_Guthaben", "sum")
    )
    .reset_index()
)

# ── Zeitindex t erzeugen (über alle Monate hinweg fortlaufend) ─
monats_df = monats_df.sort_values(["Jahr", "Monat"])
monats_df["t"] = range(1, len(monats_df) + 1)

# Ergebnis als CSV exportieren
monats_df.to_csv(
    "Zeitreihe_Monat_Standort.csv",
    index=False
)

print("Zeitreihe_Monat_Standort.csv wurde erfolgreich erstellt.")
print(monats_df.head())

# Die Ergebnisdatei "Zeitreihe_Monat_Standort.csv" enthält nun die monatlichen Aggregationen pro 
# Station und dient als Grundlage für die Zeitreihenanalyse. Jede Zeile repräsentiert eine Station in einem bestimmten Monat,
#  mit den entsprechenden Fahrtdaten und einem fortlaufenden Zeitindex "t".