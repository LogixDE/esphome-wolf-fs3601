# 3 – Firmware (ESPHome)

Datei: [`firmware/therme-fernversteller.yaml`](../firmware/therme-fernversteller.yaml), Firmware 1.4, getestet mit ESPHome 2026.11. Die Werte für `api_encryption_key`, `wifi_ssid` und `wifi_password` kommen aus deiner `secrets.yaml`, siehe [`firmware/secrets.example.yaml`](../firmware/secrets.example.yaml).

## Betriebsarten

| Betriebsart | Bedeutung |
|---|---|
| **Automatik** | Stufenlose **Heizkurve 0–100 %**. 0 % = 12 964 Ω (tiefster Wert der alten FB), 100 % = 16 297 Ω (höchster). Home Assistant regelt diesen Wert nach. |
| Therme intern | K8 geschlossen, K1–K2 gebrückt, wie ohne Fernbedienung. Auch der Rückfall bei HA-Ausfall. |
| Tag / Nacht | Handbetrieb mit der Skala der alten FB: „Sollwert (Handbetrieb)“ −3 … +3, „Nachtregler (Handbetrieb)“ 2 … 9. Die Firmware rechnet über das gemessene Kennfeld in Ohm um. |
| Aus | Stellung 0 der alten FB, 3 872 Ω |
| Test (Widerstand) | direkte Ohm-Vorgabe zum Messen und Kalibrieren |

## Entitäten

| Entität | Kategorie |
|---|---|
| Betriebsart, Heizkurve | Steuerung |
| Sollwert (Handbetrieb), Nachtregler (Handbetrieb) | Konfiguration |
| Test-Widerstand, Widerstand Ziel, Widerstand K1-K2, Rückfall aktiv, Sollwert begrenzt | Diagnose |
| Betriebszeit, ESPHome-Version, IP-Adresse, Online, WLAN-Signal | Diagnose |

Die blaue LED des Super Mini (GPIO8) dient als Status-LED. Sie blinkt, solange WLAN oder API fehlen.

## So entsteht der Widerstand

1. Aus Betriebsart und Einstellungen berechnet die Firmware einen **Zielwiderstand**.
2. Sie probiert alle 64 Kombinationen der sechs Bit-Relais durch und nimmt die, deren Summe `r0 + Σ rbit[i]` dem Ziel am nächsten kommt.
3. Ist ein Relais an, überbrückt es seinen Widerstand.

```cpp
const float r0 = 12883.0f;   // alle Bit-Relais geschlossen (Mittel beider Polungen)
const float rbit[6] = {68.0f, 120.0f, 215.0f, 458.0f, 884.0f, 1727.0f};
```

Diese Werte sind **auf der eigenen Platine gemessen**. Wer nachbaut, misst sie neu, siehe [2 – Hardware](2_hardware.md#messen-auf-der-platine-beide-polungen).

## Sicherheit

- **Ohne Firmware oder ohne Strom:** Alle Relais-LEDs sind aus. Dann ist K8 geschlossen, und der Kessel regelt intern.
- **Ohne Home Assistant > 30 min:** automatisch „Therme intern“, Sensor **Rückfall aktiv** = an. Kommt HA zurück, gilt wieder die vorherige Betriebsart.
- `reboot_timeout: 0s` bei API und WLAN, damit der ESP bei einem HA-Ausfall nicht dauernd neu startet.
