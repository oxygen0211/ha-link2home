"""Config flow for link2home."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN


async def _async_has_devices(hass: HomeAssistant) -> bool:
    """Return if there are devices that can be discovered."""
    devices = ["dummy"]
    return len(devices) > 0


config_entry_flow.register_discovery_flow(DOMAIN, "link2home", _async_has_devices)
