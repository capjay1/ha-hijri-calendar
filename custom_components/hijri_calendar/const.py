"""Constants for the Hijri Calendar integration."""

from __future__ import annotations

from typing import Final

DOMAIN: Final = "hijri_calendar"

CONF_DAY_OFFSET: Final = "day_offset"
DEFAULT_DAY_OFFSET: Final = 0
MIN_DAY_OFFSET: Final = -2
MAX_DAY_OFFSET: Final = 2

RAMADAN_MONTH: Final = 9

# Stable slugs used as enum states; the UI translates them per language.
MONTH_KEYS: Final[tuple[str, ...]] = (
    "muharram",
    "safar",
    "rabi_al_awwal",
    "rabi_al_thani",
    "jumada_al_ula",
    "jumada_al_akhirah",
    "rajab",
    "shaban",
    "ramadan",
    "shawwal",
    "dhu_al_qadah",
    "dhu_al_hijjah",
)
