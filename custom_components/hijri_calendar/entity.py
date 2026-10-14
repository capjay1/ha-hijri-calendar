"""Base entity for the Hijri Calendar integration."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import HijriCoordinator


class HijriEntity(CoordinatorEntity[HijriCoordinator]):
    """Common device info and naming for every entity we create."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: HijriCoordinator, key: str) -> None:
        """Initialise the entity."""
        super().__init__(coordinator)
        entry_id = coordinator.config_entry.entry_id
        self._attr_unique_id = f"{entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            name="Hijri Calendar",
            manufacturer="Umm al-Qura",
            model="Offline date conversion",
            entry_type=DeviceEntryType.SERVICE,
        )
