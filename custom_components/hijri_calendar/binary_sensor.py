"""Binary sensor platform for the Hijri Calendar integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import HijriConfigEntry, HijriCoordinator
from .entity import HijriEntity

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HijriConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Ramadan binary sensor."""
    async_add_entities([RamadanBinarySensor(entry.runtime_data)])


class RamadanBinarySensor(HijriEntity, BinarySensorEntity):
    """On for every day of Ramadan."""

    _attr_translation_key = "ramadan"

    def __init__(self, coordinator: HijriCoordinator) -> None:
        """Initialise the binary sensor."""
        super().__init__(coordinator, "ramadan")

    @property
    def is_on(self) -> bool:
        """Return True while the Hijri month is Ramadan."""
        return self.coordinator.data.is_ramadan

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return context about the current or next Ramadan."""
        data = self.coordinator.data
        return {
            "starts_on": data.ramadan_start.isoformat(),
            "ends_on": data.ramadan_end.isoformat(),
            "days_until": data.days_until_ramadan,
            "day_of_ramadan": data.day_of_ramadan,
            "days_remaining": data.days_left_in_ramadan,
        }
