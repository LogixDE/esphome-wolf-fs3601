# Helfer für die bedarfsgerechte Heizkurve

Alle Helfer werden in Home Assistant über **Einstellungen → Geräte & Dienste → Helfer → Helfer erstellen** angelegt. Die Raumliste unten passt zu meinem Haus. Bei dir musst du sie an deine Versatile-Thermostat-Entitäten (`climate.heizung_<raum>`) und die Ventilstellungs-Sensoren deiner TRVs (`sensor.<raum>_trv_ventilstellung`) anpassen.

Der **Flur UG** ist bewusst ausgenommen. Sein Heizkörper sitzt neben der Tür zu einem unbeheizten Kellerraum und erreicht sein Soll oft nicht. Ohne Ausnahme würde dieser eine Raum die Kurve für das ganze Haus oben halten.

## Heizung unterversorgte Räume (Template-Sensor)

Anzahl der Räume, die mehr als 0,5 K unter Soll liegen, obwohl ihr Ventil zu mindestens 80 % offen ist. Zustandsklasse: Messung.

```jinja
{# Flur UG bewusst ausgenommen #}
{% set rooms = ['arbeitszimmer','badezimmer','flur_eg','gaste_wc','kuche','phine','schlafzimmer','sonea','wohnzimmer'] %}
{% set ns = namespace(n=0) %}
{% for r in rooms %}
  {% set c = 'climate.heizung_' ~ r %}
  {% set soll = state_attr(c, 'temperature') | float(none) %}
  {% set ist = state_attr(c, 'current_temperature') | float(none) %}
  {% if soll is not none and ist is not none and soll - ist > 0.5
        and states('sensor.' ~ r ~ '_trv_ventilstellung') | float(0) >= 80 %}
    {% set ns.n = ns.n + 1 %}
  {% endif %}
{% endfor %}
{{ ns.n }}
```

## Heizung größtes Raumdefizit (Template-Sensor)

Wie weit der kälteste Raum unter seinem Soll liegt, in K. Ein negativer Wert heißt, alle Räume liegen über Soll. Einheit: K, Zustandsklasse: Messung.

```jinja
{% set rooms = ['arbeitszimmer','badezimmer','flur_eg','gaste_wc','kuche','phine','schlafzimmer','sonea','wohnzimmer'] %}
{% set ns = namespace(d=-99) %}
{% for r in rooms %}
  {% set c = 'climate.heizung_' ~ r %}
  {% set soll = state_attr(c, 'temperature') | float(none) %}
  {% set ist = state_attr(c, 'current_temperature') | float(none) %}
  {% if soll is not none and ist is not none %}{% set ns.d = [ns.d, soll - ist] | max %}{% endif %}
{% endfor %}
{{ ns.d | round(1) }}
```

## Heizung Ventilstellung max (Min/Max-Helfer)

Typ **Maximum** über die Ventilstellungen aller Räume außer Flur UG, auf 0 Nachkommastellen gerundet.

## Heizung Rücklauf Mittel 30 min (Statistik-Helfer)

- Quelle: Rücklauf-Anlegefühler (`sensor.heizung_temperatur_4`)
- Merkmal: **Mittelwert**
- Max. Alter: **30 min**
- Genauigkeit: 1

Dieser Mittelwert dient als Kesselschutz für die NG-2E. Der Kessel taktet, deshalb springt der Momentanwert stark.
