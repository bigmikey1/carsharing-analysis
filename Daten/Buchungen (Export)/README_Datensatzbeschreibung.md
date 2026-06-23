# Datensatzbeschreibung – Buchungszahlen (Carsharing-Projekt)

## 1. Zweck der Daten
Die quartalsweise verwalteten Buchungsdaten bilden die **zentrale Datengrundlage** für sämtliche Auswertungen, Kennzahlen (KPIs) und Visualisierungen im Carsharing‑Projekt.  
Sie ermöglichen eine konsistente Analyse der Nutzung, der wirtschaftlichen Entwicklung sowie von Anteilen und Trends über Zeit und Standorte hinweg.

---

## 2. Projekt- und Zeitbezug
- **Projekt**: Carsharing
- **Berichtsstand**: quartalsweise
- **Zeitraum**: fortlaufend seit Projektstart
- **Aktuelle Struktur**:
  - Quartalsdateien (z. B. `Buchungen_01-03_26_raw`)
  - Einheitliches Datenformat über alle Quartale hinweg
- **Zeitformat**: UTC‑8 (Excel‑kompatibel)

---

## 3. Aufbau und Ablage der Datenbanken

### 3.1 Dateibenennung
Jede Quartalsdatei folgt dem Schema:

Buchungen_[Zeitraum]_raw.xlsx

**Beispiele:**
- `Buchungen_01-03_26_raw.xlsx`
- `Buchungen_04-06_26_raw.xlsx`

### 3.2 Struktur
- Alle Quartalsdateien haben:
  - identische Spalten
  - identische Datentypen
  - keine voraggregierten Werte
- Es handelt sich stets um **Rohdaten** auf Buchungsebene.

---

## 4. Bedeutung der Buchungszahlen
Die Buchungszahlen sind die **wichtigste analytische Grundlage** des Projekts.  
Aus ihnen lassen sich unter anderem folgende KPIs ableiten:

- Umsatz (monatlich / quartalsweise)
- Durchschnittliche Fahrten pro Monat
- Fahrten pro Standort
- Umsatz pro Standort
- Umsatz aus Fahrzeit
- Durchschnittliche Fahrtdauer
- Nutzung je Tarif
- Verhältnis Fahrzeit zu Standzeit
- Entwicklung der Nutzung im Zeitverlauf
- Tarif- und Umsatzanteile

---

## 5. Visualisierung & Auswertung
Die Daten eignen sich besonders für:
- **Zeitreihenanalysen** (z. B. Umsatz-, Fahrten- oder Nutzungsentwicklung)
- **Anteilsanalysen** (z. B. Tarifanteile gesamt oder je Standort)
- **Standortvergleiche**

### Umsetzung in Excel
- PivotTable auf Basis der Buchungsdaten erstellen
- Visualisierung direkt anschließen (Diagramme)
- Keine zusätzliche Programmierung notwendig

**Vorteil:**  
Dank des UTC‑8‑Formats können die Daten von Excel **sofort korrekt interpretiert** werden.

---

## 6. Weiterverwendung der Daten
Die Buchungsdaten sind die Basis für:
- Tabelle **`Übersicht_Projekt_Entwicklung`**
- Quartalsweise aggregierte Excel‑Tabellen mit:
  - Anzahl Fahrten
  - Kilometer
  - Stunden
  - Umsatz (brutto)
  - Umsatz nach Abzug von Guthaben

Diese Auswertungen werden **separat gespeichert**, greifen jedoch immer auf die Buchungsdaten zurück.

---

## 7. Zusammenführung der Quartalsdaten zu einer Jahresdatenbank (Power Query)

Da alle Quartalsdateien im gleichen Format vorliegen, können sie einfach zu einer **Jahresdatenbank** kombiniert werden.

### Voraussetzungen
- Einheitliche Spaltenstruktur
- Einheitliche Datentypen
- Alle Dateien im gleichen Ordner
- Keine manuell geänderten Strukturen in einzelnen Quartalen

---

### Schritt-für-Schritt-Anleitung

#### 1. Import über Ordner
1. Excel öffnen
2. **Daten** → **Daten abrufen** → **Aus Datei** → **Aus Ordner**
3. Ordner mit allen `Buchungen_[Zeitraum]_raw`‑Dateien auswählen
4. **Transformieren** klicken

---

#### 2. Dateien kombinieren
1. Im Power Query Editor:
   - **Kombinieren** → **Kombinieren & Transformieren**
2. Eine Quartalsdatei als Beispieldatei auswählen
3. Power Query übernimmt automatisch Struktur und Transformation

---

#### 3. (Optional) Zeitraum ergänzen
Empfohlen für Nachvollziehbarkeit:
- Spalte aus `Quelle.Name` ableiten oder
- manuelle Spalte für Quartal / Jahr ergänzen  
  (z. B. `Q1_2026`)

---

#### 4. Datenprüfung
- Spaltennamen korrekt?
- Datumsformate korrekt (UTC‑8)?
- Zeilenanzahl plausibel?
- Keine Aggregationen durchführen

---

#### 5. Laden der Jahresdatenbank
- **Schließen & Laden**
- Empfohlen:
  - „Nur Verbindung“ oder
  - Laden in separate Jahres‑Arbeitsmappe

Ergebnis ist eine konsolidierte **Jahres‑Rohdatenbank**, aktualisierbar per Klick.

---

## 8. Vorteile des Power‑Query‑Ansatzes
- Keine manuelle Zusammenführung
- Neue Quartale:
  - Datei in den Ordner legen
  - Abfrage aktualisieren
- Einheitliche, reproduzierbare Datenbasis
- Skalierbar für KPIs, PivotTables und Berichte

---

## 9. Best Practices
- Abgeschlossene Quartale nicht nachträglich verändern
- Strukturänderungen zentral im Power Query vornehmen (empfohlen, da eher geringe Datenmenge)
- Jahresdaten nicht per Copy & Paste pflegen
- Dokumentation gemeinsam mit den Daten ablegen/aktualisieren

---

## 10. Ablage & Dokumentation
Diese Datei (`README_Datensatzbeschreibung.md`) dient als:
- technische Dokumentation
- Einstiegshilfe für alle die Carsharing Daten auswerten möchten
- Referenz für Auswertungen und KPI‑Berechnungen
- Kann als Standard für die Dokumentation weiterer Daten und Dataflows für andere Abteilungen genutzt werden




                                                                                                            Michael Dächert, 30.04.26