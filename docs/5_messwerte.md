# 5 – Messwerte

Alle Widerstände sind mit demselben Multimeter gemessen. So heben sich Messfehler zwischen Original-FB und Ersatzplatine heraus.

## Original FS 3601, Raumeinfluss 0, zwischen Klemme 1 und 2

So misst du selbst: FB vom Kessel abklemmen, Raumeinfluss auf 0, Spitzen mit Krokoklemmen fixieren, nichts anfassen.

### Tag ☼

| Sollwert | −3 | −2 | −1 | Std | +1 | +2 | +3 |
|---|---|---|---|---|---|---|---|
| Ω | 15 442 | 15 544 | 15 762 | 15 937 | 16 097 | 16 230 | 16 297 |

Den Absenkregler zu drehen ändert im Tagbetrieb nichts.

### Nacht ☾

| Nachtregler | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|
| Sollwert −3 | 12 964 | 13 410 | 13 855 | 14 170 | 14 590 | 14 954 | 15 250 | 15 438 |
| Sollwert Std | 14 693 | 14 897 | 15 096 | 15 287 | 15 472 | 15 670 | 15 831 | 15 972 |
| Sollwert +3 | 15 491 | 15 610 | 15 737 | 15 860 | 15 976 | 16 116 | 16 225 | 16 294 |

### Aus (Stellung 0)

3 872 Ω

### Sonstiges

| Größe | Wert |
|---|---|
| Spannung K1–K2 im Betrieb | ≈ 1,8 V AC, K1 = N |
| NTC (Raumfühler) | 7,4 kΩ bei 21 °C |
| K1–K3 in Stellung „Uhr 0/☼“ | 17 kΩ (= K1–K2 + 5,11 k) |

## Ersatzplatine (Mittel beider Polungen)

| Messung | Wert |
|---|---|
| Basis, alle Bits überbrückt | 12 883 Ω |
| alle Bits offen | 16 371 Ω |
| Tag / Sollwert 0 (Ziel 15 937) | 15 969 Ω |
| Therme intern (K8 zu) | ≈ 4 Ω |
| TLP240A Durchgangswiderstand | 0,34 Ω |
| Fotostrom K8 (offen, LED an) | ≈ 80–90 nA → 0,31 mV bei 3,9 k, 1,17 mV bei 12,9 k, 1,30 mV bei 16,4 k |

## Kessel (Wolf NG-2E-17, 1993)

| | Nacht 24./25.11. (Therme intern) | Nacht 25./26.11. (Nacht 6) |
|---|---|---|
| Außentemperatur Ø | +0,2 °C | +0,2 °C |
| Vorlauf Ø | 57,2 °C | 52,1 °C |
| Rücklauf Ø | 54,3 °C | 49,9 °C |
| Brennerlaufzeit 23:18–07:00 | 57,7 min | 51,6 min |
| Brennerstarts | 28 | 27 |

Fühler: Anlegefühler an den Rohren (Kessel, Vorlauf, Rücklauf, Warmwasser, Zirkulation).

## Lehrgeld

- **Widerstände aus dem Sortiment können weit daneben liegen.** Ein „13 k“ hatte etwa 12,6 kΩ, eine Parallelkombination 15 k ∥ 91 k lag ebenfalls deutlich zu tief. Kritische Werte vor dem Einlöten messen.
- **Polungsabhängige Ohm-Werte** bedeuten eine Spannungsquelle im Messkreis. Hier war es der Fotostrom des offenen PhotoMOS. Bei Flussmittelresten wäre es eine galvanische Zelle.
