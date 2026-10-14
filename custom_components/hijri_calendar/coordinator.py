"""Coordinator for the Hijri Calendar integration."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_time_change
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import CONF_DAY_OFFSET, DEFAULT_DAY_OFFSET, DOMAIN
from .hijri import HijriData, HijriOutOfRange, build_hijri_data

_LOGGER = logging.getLogger(__name__)

type HijriConfigEntry = ConfigEntry[HijriCoordinator]


class HijriCoordinator(DataUpdateCoordinator[HijriData]):
    """Recompute the Hijri date once per local day.

    There is no I/O here, so there is no polling interval: the conversion is a
    table lookup that only changes when the local calendar day rolls over.
    """

    config_entry: HijriConfigEntry

    def __init__(self, hass: HomeAssistant, entry: HijriConfigEntry) -> None:
        """Initialise the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=None,
        )
        self.day_offset: int = entry.options.get(CONF_DAY_OFFSET, DEFAULT_DAY_OFFSET)

    async def async_setup(self) -> None:
        """Arrange for a refresh shortly after every local midnight."""
        self.config_entry.async_on_unload(
            async_track_time_change(
                self.hass, self._handle_day_rollover, hour=0, minute=0, second=10
            )
        )

    @callback
    def _handle_day_rollover(self, now: datetime) -> None:
        """Kick off a refresh when the local day changes."""
        self.config_entry.async_create_task(
            self.hass, self.async_refresh(), eager_start=True
        )

    async def _async_update_data(self) -> HijriData:
        """Convert the current local date."""
        target = dt_util.now().date() + timedelta(days=self.day_offset)
        try:
            return build_hijri_data(target)
        except HijriOutOfRange as err:
            raise UpdateFailed(str(err)) from err
