"""Sensor platform for the Hijri Calendar integration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import MONTH_KEYS
from .coordinator import HijriConfigEntry, HijriCoordinator
from .entity import HijriEntity
from .hijri import HijriData

PARALLEL_UPDATES = 0


@dataclass(frozen=True, kw_only=True)
class HijriSensorEntityDescription(SensorEntityDescription):
    """Describes a Hijri sensor."""

    value_fn: Callable[[HijriData], StateType]
    attr_fn: Callable[[HijriData], dict[str, Any]] | None = None


SENSORS: tuple[HijriSensorEntityDescription, ...] = (
    HijriSensorEntityDescription(
        key="date",
        translation_key="hijri_date",
        value_fn=lambda data: data.formatted,
        attr_fn=lambda data: {
            "iso": data.iso,
            "day": data.day,
            "month": data.month,
            "year": data.year,
            "month_name_en": data.month_name_en,
            "month_name_ar": data.month_name_ar,
            "weekday_en": data.day_name_en,
            "weekday_ar": data.day_name_ar,
            "month_length": data.month_length,
            "year_length": data.year_length,
            "gregorian": data.gregorian.isoformat(),
        },
    ),
    HijriSensorEntityDescription(
        key="day",
        translation_key="hijri_day",
        value_fn=lambda data: data.day,
    ),
    HijriSensorEntityDescription(
        key="month",
        translation_key="hijri_month",
        device_class=SensorDeviceClass.ENUM,
        options=list(MONTH_KEYS),
        value_fn=lambda data: data.month_key,
        attr_fn=lambda data: {"month_number": data.month},
    ),
    HijriSensorEntityDescription(
        key="year",
        translation_key="hijri_year",
        value_fn=lambda data: data.year,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HijriConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Hijri sensors."""
    coordinator = entry.runtime_data
    async_add_entities(
        HijriSensor(coordinator, description) for description in SENSORS
    )


class HijriSensor(HijriEntity, SensorEntity):
    """A single value derived from today's Hijri date."""

    entity_description: HijriSensorEntityDescription

    def __init__(
        self,
        coordinator: HijriCoordinator,
        description: HijriSensorEntityDescription,
    ) -> None:
        """Initialise the sensor."""
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> StateType:
        """Return the sensor value."""
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return the extra attributes, if this sensor has any."""
        if (attr_fn := self.entity_description.attr_fn) is None:
            return None
        return attr_fn(self.coordinator.data)
