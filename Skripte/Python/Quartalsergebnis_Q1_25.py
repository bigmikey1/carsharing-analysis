import pandas as pd

DATEI = "Daten\\Buchungen (Export)\\Buchungen 2025\\Buchungen_01-03_25_raw.csv"

from Quartalsergebnis_Q1_26 import GUELTIGE_TARIFE

GUELTIGE_MONATE = ["2025-01", "2025-02", "2025-03"]

def main():
    df = pd.read_csv(DATEI, sep=";", dtype=str)

# ── Bereinigung ─────────────────────────────────────────────
    df["Tarif"] = df["Tarif"].str.strip()
    df["Stationsname"] = df["Stationsname"].str.strip()
    df["Abrechnungsmonat"] = df["Abrechnungsmonat"].str.strip()
    df["Buchungsstatus"] = df["Buchungsstatus"].str.strip()
    df['Fahrtkosten_nach_Guthaben'] = df["Fahrtkosten_nach_Guthaben"].str.strip()

    # ── Filter ──────────────────────────────────────────────────
    df = df[df["Abrechnungsmonat"].isin(GUELTIGE_MONATE)]
    df = df[df["Tarif"].isin(GUELTIGE_TARIFE)]

    # ── Numerische Spalten (deutsches Zahlenformat) ─────────────
    numerische_spalten = ["Fahrtdauer_std", "KM", "Fahrtkosten", "Fahrtkosten_nach_Guthaben"]

    for spalte in numerische_spalten:
        df[spalte] = (
            df[spalte]
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

    # ── Aggregation pro Stationsname ────────────────────────────
    stationen_df = (
        df.groupby("Stationsname", dropna=False)
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
        .sort_values("Anzahl_Fahrten", ascending=False)
    )

    # ── Gesamtsumme Quartal ─────────────────────────────────────
    gesamt_q1_df = pd.DataFrame([{
        "Zeitraum": "Q1 2025",
        "Anzahl_Fahrten": stationen_df["Anzahl_Fahrten"].sum(),
        "Summe_Stunden": stationen_df["Summe_Stunden"].sum(),
        "Summe_KM": stationen_df["Summe_KM"].sum(),
        "Summe_Fahrtkosten": stationen_df["Summe_Fahrtkosten"].sum(),
        "Summe_Fahrtkosten_abzgl_Guthaben": stationen_df["Summe_Fahrtkosten_abzgl_Guthaben"].sum()
    }])

    # ── CSV-Exports ─────────────────────────────────────────────
    stationen_df.to_csv(
        "Auswertung_Stationsnamen_Q1_2025.csv",
        index=False
    )

    gesamt_q1_df.to_csv(
        "Auswertung_Gesamtsumme_Q1_2025.csv",
        index=False
    )
print("Auswertung_Stationsnamen_Q1_2025.csv")
print("Auswertung_Gesamtsumme_Q1_2025.csv")

if __name__ == "__main__":
    main()