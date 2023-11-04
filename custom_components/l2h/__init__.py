"""The link2home integration."""
from __future__ import annotations

import logging
from .coordinator import L2HUpdateCoordinator, L2HEntity

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.SWITCH]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
) -> bool:
    """Set up link2home from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    _LOGGER.info("L2h platform setup completed")
    return True
