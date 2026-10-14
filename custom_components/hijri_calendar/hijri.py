"""Pure Umm al-Qura calendar maths.

Deliberately free of any Home Assistant imports so it can be unit tested
standalone, and so the conversion logic stays easy to reason about.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from hijridate import Gregorian, Hijri

from .const import MONTH_KEYS, RAMADAN_MONTH

# Bounds of the Umm al-Qura tables shipped with hijridate.
MIN_HIJRI_YEAR = 1343
MAX_HIJRI_YEAR = 1500


class HijriOutOfRange(ValueError):
    """Raised when a date falls outside the Umm al-Qura tables."""


@dataclass(frozen=True, slots=True)
class HijriData:
    """Everything the entities need for one calendar day."""

    gregorian: date
    year: int
    month: int
    day: int
    month_key: str
    month_name_en: str
    month_name_ar: str
    day_name_en: str
    day_name_ar: str
    formatted: str
    iso: str
    month_length: int
    year_length: int
    is_ramadan: bool
    ramadan_start: date
    ramadan_end: date
    days_until_ramadan: int
    day_of_ramadan: int | None
    days_left_in_ramadan: int | None


def _ramadan_bounds(hijri_year: int) -> tuple[date, date]:
    """Return the Gregorian first and last day of Ramadan in a Hijri year."""
    first = Hijri(hijri_year, RAMADAN_MONTH, 1)
    last_day = first.month_length()
    start = first.to_gregorian()
    end = Hijri(hijri_year, RAMADAN_MONTH, last_day).to_gregorian()
    return (
        date(start.year, start.month, start.day),
        date(end.year, end.month, end.day),
    )


def build_hijri_data(today: date) -> HijriData:
    """Convert a Gregorian date into the full set of Hijri facts."""
    try:
        hijri = Gregorian(today.year, today.month, today.day).to_hijri()
    except (OverflowError, ValueError) as err:
        raise HijriOutOfRange(f"{today} is outside the Umm al-Qura tables") from err

    year, month, day = hijri.datetuple()
    is_ramadan = month == RAMADAN_MONTH

    # Which Ramadan are we measuring against? The current one if we are in it
    # or still ahead of it this Hijri year, otherwise next year's.
    target_year = year if month <= RAMADAN_MONTH else year + 1
    if target_year > MAX_HIJRI_YEAR:
        raise HijriOutOfRange(f"Ramadan {target_year} is outside the Umm al-Qura tables")

    ramadan_start, ramadan_end = _ramadan_bounds(target_year)

    day_of_ramadan = day if is_ramadan else None
    # Inclusive of today, so the final day of Ramadan reads 1, not 0.
    days_left_in_ramadan = (ramadan_end - today).days + 1 if is_ramadan else None
    days_until_ramadan = max((ramadan_start - today).days, 0)

    return HijriData(
        gregorian=today,
        year=year,
        month=month,
        day=day,
        month_key=MONTH_KEYS[month - 1],
        month_name_en=hijri.month_name("en"),
        month_name_ar=hijri.month_name("ar"),
        day_name_en=hijri.day_name("en"),
        day_name_ar=hijri.day_name("ar"),
        formatted=f"{day:02d}/{month:02d}/{year}",
        iso=f"{year}-{month:02d}-{day:02d}",
        month_length=hijri.month_length(),
        year_length=hijri.year_length(),
        is_ramadan=is_ramadan,
        ramadan_start=ramadan_start,
        ramadan_end=ramadan_end,
        days_until_ramadan=days_until_ramadan,
        day_of_ramadan=day_of_ramadan,
        days_left_in_ramadan=days_left_in_ramadan,
    )
