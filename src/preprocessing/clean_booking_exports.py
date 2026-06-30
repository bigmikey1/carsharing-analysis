import pandas as pd
from pathlib import Path

# Spalten entfernen
DROP_COLUMNS = [
    "MS-Id",
    "Mobilitätsservice",
    "C-Id",
    "Klasse",
    "Rechnungsnummer"
]

# Ordner mit Buchungsexporten
INPUT_FOLDER = Path(r"M:\Projekte\21 - Carsharing Landkreis\100 - Reports und Projektbegleitung\Carsharing - Analysis\data\input\bookings"
)

from shutil import move

raw_folder = INPUT_FOLDER / "raw"
raw_folder.mkdir(exist_ok=True)

for file in INPUT_FOLDER.glob("*_raw.csv"):

    target = raw_folder / file.name

    if not target.exists():
        move(str(file), str(target)
        )

# Alle Raw-Dateien finden
csv_files = INPUT_FOLDER.rglob("*_raw.csv")

for file in csv_files:

    print(f"Verarbeite: {file.name}")

    df = pd.read_csv(file, sep=";")
 
    # Einheitliche Spaltennamen herstellen
    
    
    COLUMN_MAPPING = {
        "Buchungsdauer (Std.)": "Buchungsdauer_std",
        "Fahrtdauer (Std.)": "Fahrtdauer_std",
        "Zeitkosten (nach Guthaben)": "Zeitkosten_nach_Guthaben",
        "KM-Kosten (nach Guthaben)": "KM_Kosten_nach_Guthaben",
        "Fahrtkosten (nach Guthaben)": "Fahrtkosten_nach_Guthaben"
    }

    df = df.rename(
        columns={
            old: new
            for old, new in COLUMN_MAPPING.items()
            if old in df.columns
        }
    )


    # Nur vorhandene Spalten löschen
    existing_columns = [
        col
        for col in DROP_COLUMNS
        if col in df.columns
    ]

    
    df = df.drop(
    columns=DROP_COLUMNS,
    errors="ignore"
    )
    
    # Zielordner für anonymisierte Dateien
    output_folder = file.parent.parent / "ano"

    # Ordner automatisch anlegen
    output_folder.mkdir(parents=True, exist_ok=True)

    # Neuer Dateiname
    output_file = output_folder / file.name.replace(
        "_raw.csv",
        "_ano.csv"
    )

    df.to_csv(
        output_file,
        index=False,
        sep=";"
    )

    print(f"Gespeichert: {output_file.name}")

print("\n✅ Alle Buchungsdateien verarbeitet.")