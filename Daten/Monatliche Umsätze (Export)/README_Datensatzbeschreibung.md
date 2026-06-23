# Datensatzbeschreibung – Monatsumsätze nach Tarifelementen (aggregiert)

## 1. Zweck der Daten
Die Datei **`MonatsumsaetzenachTarifelementen_01_25-03_26_raw`** enthält die **monatlich aggregierten Nutzungs‑ und Umsatzkennzahlen** des Carsharing‑Projekts, aufgeschlüsselt nach Tarifelementen.

Sie dient als:
- schnelle Management‑ und Controllingübersicht
- valide Grundlage für Monats‑, Quartals‑ und Jahresvergleiche
- Brücke zwischen Buchungs‑Rohdaten und Management‑KPIs

---

## 2. Projekt- und Zeitbezug
- **Projekt**: Carsharing
- **Zeitraum**: Januar 2025 bis März 2026
- **Zeitliche Auflösung**: monatlich
- **Aggregationsebene**: Gesamtprojekt (keine Einzelbuchungen)

---

## 3. Charakter der Datenbank
- Typ: **aggregierte Auswertungsdaten**
- Nicht auf Buchungsebene
- Datei wird **periodisch neu erzeugt** und kann einfach überschrieben werden. 

Diese Datei ist bereits eine **auswertungsnahe Kennzahlensammlung**.

---

## 4. Enthaltene Spalten und Bedeutung

### Zeitliche Dimension
- **Monat**  
  Berichtsmonat der aggregierten Kennzahlen

---

### Umsatzbezogene Kennzahlen

#### Brutto-Werte
- **Buchung (brutto)**  
  Gesamtumsatz aus Buchungen
- **Zeit (brutto)**  
  Umsatzanteil aus Zeitkomponenten
- **KM (brutto)**  
  Umsatzanteil aus Kilometerleistungen
- **Spätrückgabe (brutto)**  
  Zuschläge aus verspäteter Rückgabe

#### Netto-Werte
- **Fahrten (netto)**  
  Nettoerlöse aus Fahrten
- **Gebühren (netto)**  
  Sonstige Gebühren (z. B. Straf‑ oder Zusatzgebühren)
- **verwendetes Guthaben (netto)**  
  Eingelöste Kunden-Guthaben
- **Monatsgebühr (netto)**  
  Nettoerlöse aus monatlichen Grundgebühren
- **Summe (netto)**  
  Gesamtnettoumsatz des Monats
- **Summe (brutto)**  
  Gesamtbruttoumsatz des Monats

---

### Nutzungskennzahlen
- **Anzahl Buchungen**  
  Gesamtanzahl der Buchungen im Monat
- **Stunden genutzt**  
  Tatsächlich genutzte Fahrzeit
- **Stunden bezahlt**  
  Abgerechnete Fahrzeit
- **KM genutzt**  
  Gefahrene Kilometer
- **KM bezahlt**  
  Abgerechnete Kilometer

---

## 5. Inhaltliche Abgrenzung
Die Datei beantwortet primär:
- Wie hoch sind Umsatz und Nutzung pro Monat?
- Wie hoch ist der "theoretische Verlust" aus der Ausgabe von Guthaben?
- Wie entwickeln sich Nutzung und Erlöse im Zeitverlauf?

---

## 6. Typische KPIs und Analysen
Aus der Datei lassen sich schnell z.B. ableiten:
- Entwicklung der Nutzung (Buchungen, Stunden, Kilometer)
- Verhältnis Nutzung vs. Abrechnung (genutzt vs. bezahlt)
- Durchschnittswerte pro Monat (z. B. Buchungen, Stunden)

Die Datei eignet sich besonders gut für:
- Zeitreihen
- Trendanalysen
- Monats‑ und Quartalsberichte

---

## 7. Visualisierung & Nutzung
- Direkte Nutzung in Excel möglich
- Ideal für:
  - PivotTables
  - Liniendiagramme (Zeitverlauf)
  - Gestapelte Balkendiagramme (Tarifanteile)

Kein zusätzlicher Code notwendig.

---

## 8. Verhältnis zu anderen Datenbanken
Die Datei steht in Beziehung zu:
- Buchungs‑Rohdaten (Detailbasis)
- Kilometerstatistiken
- Quartals‑ und Projektübersichten

Sie bietet eine **verdichtete Sicht** auf dieselben Prozesse und Kennzahlen.

---

## 9. Ablage & Dokumentation
Diese Datei liegt zusammen mit dieser `LESEN_Datensatzbeschreibung.md` im entsprechenden Ordner und dient als:
- Referenz für monatliche Umsatz‑ und Nutzungskennzahlen
- Grundlage für Berichte und Entscheidungsunterlagen
``