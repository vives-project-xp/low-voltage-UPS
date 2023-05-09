"""The LVUPS integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .device import LVUPS

# List of platforms to support. There should be a matching .py file for each,
# eg <sensor.py>
PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.NUMBER,
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up LVUPS from a config entry."""
    # Create an instance of the "connecting" class that does the work of speaking with the actual devices.
    lvups = LVUPS(hass, entry.data["name"], entry.data["topic"])

    # Subscribe to updates from the device.
    await lvups.subscribe()

    # Stores the created instance of the class in the hass.data dictionary.
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = lvups

    # This creates each HA object for each platform your device requires.
    # It's done by calling the `async_setup_entry` function in each platform module.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # This is called when an entry/configured device is to be removed. The class
    # needs to unload itself, and remove callbacks. See the classes for further
    # details.

    # Get the instance of the class that was created in the async_setup_entry function.
    lvups = hass.data[DOMAIN][entry.entry_id]

    # Unsubscribe from updates from the device.
    await lvups.unsubscribe()

    # This unloads each platform.
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # Remove the instance of the class from the hass.data dictionary.
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
