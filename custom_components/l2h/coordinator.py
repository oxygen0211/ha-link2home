"""Coordinator entity for Link2Home."""
import logging

from pyl2h.udp import UDPServer

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import callback
from homeassistant.helpers import device_registry
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN, MANUFACTURER

_LOGGER = logging.getLogger(__name__)
l2h_server = UDPServer()

class L2HUpdateCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass, entity_callback):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="Link2Home",
        )
        self.hass.states.async_set("l2h.test", "Initialized")
        self.entity_callback = entity_callback
        _LOGGER.info("Current config: %s", self.data)
        _LOGGER.info("Coordinator initialized")

    @callback
    def status_callback(self, status):
        """Status update callback for Link2Home devices."""
        mac = status["mac"].hex("_")
        entity_id = device_registry.format_mac(mac)
        state_id = f"switch.{entity_id}"
        # state_id = "switch.l2hsocket"
        _LOGGER.info("Device %s status update: %s", state_id, status)

        if 1 not in status["channels"]:
            return

        state = status["channels"][1]
        attributes = {
            "mac": mac,
            "ip": status["ip"],
            "channels": status["channels"],
        }
        data = self.data if self.data else {}
        if state_id not in data:
            self.entity_callback(state_id)

        data[state_id] = {**attributes, "state": state}
        self.async_set_updated_data(data)

    def listen(self):
        """Start listening for UDP broadcastes status Updates with Lin2Home generic protocol."""
        _LOGGER.info("Starting UDP Listener")
        l2h_server.listen(self.status_callback)

    def set_state(self, idx, new_state):
        """Set status (on/off) of a given Entity."""
        device = self.data[idx]
        l2h_server.setStatus(device["ip"], 1, new_state)


class L2HEntity(CoordinatorEntity, SwitchEntity):
    """An entity using CoordinatorEntity.

    The CoordinatorEntity class provides:
      should_poll
      async_update
      async_added_to_hass
      available

    """

    def __init__(self, coordinator, idx):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{idx}"
        self.idx = idx
        self.logger = logging.getLogger("L2HEntity")
        self.entity_id = idx

    @property
    def device_info(self) -> DeviceInfo:
        """Allow Home Assistant to create a Device entry for us."""
        return DeviceInfo(
            identifiers={((DOMAIN), self.idx)},
            name=self.name,
            manufacturer=MANUFACTURER,
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_is_on = self.coordinator.data[self.idx]["state"]
        self.schedule_update_ha_state()

    async def async_turn_on(self, **kwargs):
        """Turn the light on.

        Example method how to request data updates.
        """
        # Do the turning on.
        # ...

        # Update the data
        self.coordinator.set_state(self.idx, True)

    async def async_turn_off(self, **kwargs):
        """Turn the light on.

        Example method how to request data updates.
        """
        # Do the turning on.
        # ...

        # Update the data
        self.coordinator.set_state(self.idx, False)
