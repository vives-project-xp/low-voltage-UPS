"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations

# In a real implementation, this would be in an external library that's on PyPI.
# The PyPI package needs to be included in the `requirements` section of manifest.json
# See https://developers.home-assistant.io/docs/creating_integration_manifest
# for more information.
# This dummy hub always returns 1 CDEM.
import asyncio
import random

from collections.abc import Callable
from homeassistant.core import HomeAssistant


#class Hub:
#    """Dummy hub for Hello World example."""
#
#    def __init__(self, hass: HomeAssistant, host: str) -> None:
#        """Init dummy hub."""
#        self._host = host
#        self._hass = hass
#        self._name = host
#        self._id = host.lower()
#        self.cdem = CDEM(f"{self._id}_1", f"{self._name} 1", self)
#        self.online = True
#
#    @property
#    def hub_id(self) -> str:
#        """ID for dummy hub."""
#        return self._id
#
#    async def test_connection(self) -> bool:
#        """Test connectivity to the Dummy hub is OK."""
#        await asyncio.sleep(1)
#        return True


class CDEM:
    """CDEM (device for HA)"""

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        """Init CDEM."""
        self._host = host
        self._hass = hass
        self.name = host
        self._id = host.lower()
        self._callbacks = set()
        self._loop = asyncio.get_event_loop()
#        self._target_position = 100
#        self._current_position = 100
        # Reports if the roller is moving up or down.
        # >0 is up, <0 is down. This very much just for demonstration.
#        self.moving = 0

        # Some static information about this device
        self.manufacturer = "Vives"
        self.firmware_version = "0.0.1"
        self.model = "CDEM"

    @property
    def cdem_id(self) -> str:
        """Return ID for CDEM."""
        return self._id

#    @property
#    def position(self):
#        """Return position for roller."""
#        return self._current_position
#
#    async def set_position(self, position: int) -> None:
#        """
#        Set dummy cover to the given position.
#
#        State is announced a random number of seconds later.
#        """
#        self._target_position = position
#
#        # Update the moving status, and broadcast the update
#        self.moving = position - 50
#        await self.publish_updates()
#
#        self._loop.create_task(self.delayed_update())

#    async def delayed_update(self) -> None:
#        """Publish updates, with a random delay to emulate interaction with device."""
#        await asyncio.sleep(random.randint(1, 10))
#        self.moving = 0
#        await self.publish_updates()

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback, called when Roller changes state."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

#    # In a real implementation, this library would call it's call backs when it was
#    # notified of any state changeds for the relevant device.
#    async def publish_updates(self) -> None:
#        """Schedule call all registered callbacks."""
#        self._current_position = self._target_position
#        for callback in self._callbacks:
#            callback()

    @property
    def online(self) -> float:
        """CDEM is online."""
        return True

    @property
    def battery_level(self) -> int:
        """Battery level as a percentage."""
        return random.randint(0, 100)

#    @property
#    def battery_voltage(self) -> float:
#        """Return a random voltage roughly that of a 12v battery."""
#        return round(random.random() * 3 + 10, 2)

    @property
    def illuminance(self) -> int:
        """Return a sample illuminance in lux."""
        return random.randint(0, 500)
