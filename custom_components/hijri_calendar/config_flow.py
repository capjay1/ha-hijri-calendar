"""Config and options flow for the Hijri Calendar integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import (
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.helpers import selector

from .const import (
    CONF_DAY_OFFSET,
    DEFAULT_DAY_OFFSET,
    DOMAIN,
    MAX_DAY_OFFSET,
    MIN_DAY_OFFSET,
)
from .coordinator import HijriConfigEntry

OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_DAY_OFFSET, default=DEFAULT_DAY_OFFSET): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=MIN_DAY_OFFSET,
                max=MAX_DAY_OFFSET,
                step=1,
                mode=selector.NumberSelectorMode.BOX,
            )
        )
    }
)


class HijriConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the initial setup. There is nothing to ask, so one click is enough."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm the single instance."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=vol.Schema({}))

        return self.async_create_entry(title="Hijri Calendar", data={})

    @staticmethod
    def async_get_options_flow(entry: HijriConfigEntry) -> HijriOptionsFlow:
        """Return the options flow."""
        return HijriOptionsFlow()


class HijriOptionsFlow(OptionsFlow):
    """Let the user nudge the date by a day."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(
                data={CONF_DAY_OFFSET: int(user_input[CONF_DAY_OFFSET])}
            )

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA, self.config_entry.options
            ),
        )
