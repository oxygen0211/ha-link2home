"""Link2Home switch Platform."""
from __future__ import annotations

import logging
import json

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import L2HEntity, L2HUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up link2home from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    
    @callback
    def entity_callback(idx):
        _LOGGER.info("Adding entity with ID %s", idx)
        async_add_entities([L2HEntity(coordinator, idx)])

    _LOGGER.info("Starting to scan for L2H devices... Change a setting to make them show up")
    coordinator = L2HUpdateCoordinator(hass, entity_callback)
    _LOGGER.info("Current config: %s", json.dumps(hass.data[DOMAIN]))
    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    hass.loop.run_in_executor(None, coordinator.listen)
