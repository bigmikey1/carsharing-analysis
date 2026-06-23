# Datensatzbeschreibung – Kilometerstatistik (Carsharing-Projekt)

## 1. Zweck der Daten
Die Kilometerstatistik stellt die **monatliche Fahrleistung je Standort** dar und dient als zentrale Übersicht zur Bewertung der Nutzung des Carsharing‑Angebots.

Anhand der Kilometerleistung lassen sich ohne weitere Berechnungen zentrale Fragestellungen beantworten:
- Wie entwickelt sich die Nutzung im Zeitverlauf?
- Wie konstant wird ein Standort genutzt?
- Bei welchen Standorten besteht erkennbarer Handlungsbedarf?

Der Datensatz ist bewusst einfach gehalten und soll eine **schnelle Einordnung auf Standortebene** ermöglichen.

---

## 2. Projekt- und Zeitbezug
- **Projekt**: Carsharing
- **Aktueller Stand**: Ende Quartal 1 / 2026
- **Standorte**:
  - 14 aktive Standorte
  - 15. Standort **Sünching** in Planung (noch nicht enthalten)
- **Zeitliche Auflösung**: monatlich

---

## 3. Aufbau des Datensatzes

### 3.1 Inhalt
Der Datensatz enthält pro Monat und Standort:
- Standortname
- Monat / Jahr
- Gefahrene Kilometer (in km)

Es werden **keine aggregierten KPIs** gespeichert – ausschließlich die Kilometer als Primärkennzahl.

---

### 3.2 Strukturmerkmale
- Einheitliche Struktur über alle Monate
- Keine Zeitverschiebungen oder Umrechnungen notwendig
- Klare Trennung nach Standort und Monat

---

## 4. Datenquelle und Erhebung
- Quelle: operative Fahrdaten (z. B. Fahrzeug- oder Systemauswertungen)
- Erhebung: monatliche Aggregation der gefahrenen Kilometer je Standort
- Einheit: Kilometer [km]

### Hinweise zur Datenqualität
- Rundungsdifferenzen sind möglich
- Fehlende oder auffällige Werte können auf:
  - technische Ausfälle
  - eingeschränkten Betrieb
  - saisonale Effekte  
  zurückzuführen sein

---

## 5. Ableitbare KPIs und Aussagen
Die Kilometerstatistik erlaubt insbesondere folgende Auswertungen:

### 5.1 Nutzung im Zeitverlauf
- Vergleich der monatlichen Kilometer pro Standort
- Erkennen von Wachstums‑ oder Rückgangstrends

### 5.2 Konstanz der Nutzung
- Gleichmäßige Kilometerleistung → stabile Nutzung
- Starke Schwankungen → Hinweis auf strukturelle oder saisonale Effekte

### 5.3 Identifikation von Handlungsbedarf
Ohne zusätzliche Rechnungen erkennbar:
- sehr niedrige Nutzung
- plötzliche Einbrüche
- dauerhaft unterdurchschnittliche Standorte

Die Statistik dient dabei als **Frühindikator**, nicht als Ursachenanalyse.

---

## 6. Nutzung & Interpretation
- Vergleiche erfolgen **relativ zwischen Standorten**
- Geringe Kilometerleistung bedeutet nicht automatisch geringe Nachfrage
- Ergebnisse sollten stets gemeinsam mit:
  - Buchungszahlen
  - Standortbedingungen
  - saisonalen Rahmenbedingungen  
  interpretiert werden

---

## 7. Visualisierung
Die Kilometerdaten eignen sich besonders für:
- Liniendiagramme (Zeitverlauf pro Standort)
- Balkendiagramme (Standortvergleich pro Monat oder Jahr)

Visualisierung kann direkt in Excel erfolgen:
- PivotTable erstellen
- Diagramm hinzufügen

➡️ Keine zusätzliche Aufbereitung oder Programmierung notwendig

---

## 8. Weiterverwendung der Daten
Die Kilometerstatistik ist eine **ergänzende Basis** zu:
- Buchungszahlen
- Stunden‑ und Umsatzdaten
- Übersichts‑ und Entwicklungstabellen des Projekts

Sie wird insbesondere genutzt für:
- Standortbewertungen
- Trendanalysen
- Entscheidungsgrundlagen für Anpassungen im Betrieb

---

## 9. Pflege & Aktualisierung
- Monatliche Ergänzung der Daten
- Abgeschlossene Monate werden nicht nachträglich verändert
- Neue Standorte (z. B. Sünching) werden ab Inbetriebnahme ergänzt

---

## 10. Ablage & Dokumentation
Diese Datei (`LESEN_Datensatzbeschreibung.md`) liegt im gleichen Ordner wie die Kilometerdaten und dient als:
- Dokumentation der Datenbasis
- Einstiegshilfe für neue Nutzer
- Referenz für Analysen und Visualisierungen


                                                                                                        Michael Dächert, 30.03.2026