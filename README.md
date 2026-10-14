# Hijri Calendar (Umm al-Qura) for Home Assistant

Exposes today's Hijri date and a Ramadan flag, converted with the official
Umm al-Qura tables. Fully offline — no API, no account, no network access.

## Entities

| Entity | Example state | Notes |
| --- | --- | --- |
| `sensor.hijri_calendar_date` | `01/05/1448` | Attributes: `iso`, `day`, `month`, `year`, `month_name_en`, `month_name_ar`, `weekday_en`, `weekday_ar`, `month_length`, `year_length`, `gregorian` |
| `sensor.hijri_calendar_day` | `1` | Day of the Hijri month, 1–30 |
| `sensor.hijri_calendar_month` | `jumada_al_ula` | Enum, translated in the UI (English and Arabic) |
| `sensor.hijri_calendar_year` | `1448` | |
| `binary_sensor.hijri_calendar_ramadan` | `off` | Attributes: `starts_on`, `ends_on`, `days_until`, `day_of_ramadan`, `days_remaining` |

## Installation

### HACS (custom repository)

1. HACS → three-dot menu → **Custom repositories**
2. Add `https://github.com/capjay1/ha-hijri-calendar`, category **Integration**
3. Install, restart Home Assistant
4. Settings → Devices & Services → **Add Integration** → *Hijri Calendar*

### Manual

Copy `custom_components/hijri_calendar/` into your `config/custom_components/`
directory and restart.

## Options

**Day offset** (−2 … +2). The Hijri day begins at sunset, while this integration
follows the local civil day. Set `+1` if you want the date to match the evening
reckoning, or to follow a local sighting announcement that differs from the
Umm al-Qura tables.

## Range

The Umm al-Qura tables cover **1343–1500 AH (1924-08-01 – 2077-11-16 CE)**.
Outside that window the entities go unavailable rather than guessing.

## Example automation

```yaml
automation:
  - alias: Ramadan lighting scene
    triggers:
      - trigger: state
        entity_id: binary_sensor.hijri_calendar_ramadan
        to: "on"
    actions:
      - action: scene.turn_on
        target:
          entity_id: scene.ramadan_evening
```

## Credit

Conversion by [hijridate](https://pypi.org/project/hijridate/).
