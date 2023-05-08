"""The CDEM integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .device import CDEM

# List of platforms to support. There should be a matching .py file for each,
# eg <sensor.py>
PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up CDEM from a config entry."""
    # Stores an instance of the "connecting" class that does the work of speaking with the actual devices.
    cdem = CDEM(hass, entry.data["name"], entry.data["topic"])
    await cdem.subscribe()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = cdem
    # This creates each HA object for each platform your device requires.
    # It's done by calling the `async_setup_entry` function in each platform module.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # This is called when an entry/configured device is to be removed. The class
    # needs to unload itself, and remove callbacks. See the classes for further
    # details

    # Get the instance of the class that was created in the async_setup_entry function.
    cdem = hass.data[DOMAIN][entry.entry_id]

    # Unsubscribe from updates from the device.
    await cdem.unsubscribe()

    # This unloads each platform.
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # Remove the instance of the class from the hass.data dictionary.
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
