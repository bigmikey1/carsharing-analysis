Guthabenmodell

Ziel: Die Netto-Nutzungsentgelte sollen nicht unabhängig prognostiziert werden, da sie fachlich direkt mit den Brutto-Nutzungsentgelten zusammenhängen.

Hintergrund: Netto = Brutto - eingelöstes Guthaben

Die logische Modellierung über: Nettoquote = Netto / Brutto führte teilweise zu unrealistischen Ergebnissen, da kleine Änderungen der Quote über das Gesamtjahr zu starken Abweichungen eskalierten.

Neue Logik:

1. Historisches Guthaben bestimmen:
        Guthaben = Brutto - Netto

2. Historische Guthabenquote berechnen:
        Guthabenquote = Guthaben / Brutto

3. Statt eine Regression auf die Quote anzuwenden,
        wird ein rollierender Durchschnitt der letzten Monate genutzt.

Vorteil:
- deutlich stabiler
- weniger Overfitting
- realistischer Businessbezug
 Netto bleibt proportional zu Brutto

4. Netto-Prognose berechnen:
        Netto = Brutto × (1 - Guthabenquote)

5. Zusätzlicher Sicherheits-Constraint:
        Netto darf niemals größer als Brutto sein.

Dadurch bleibt:
Die historische Differenz zwischen Brutto und Netto weitgehend erhalten
- der Forecast fachlich belastbar
- die Prognose robuster gegen Ausreißer