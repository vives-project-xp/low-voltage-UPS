"""Platform for switch integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# A list of all switches (add more if you need them)
SWITCHES: tuple[SwitchEntityDescription, ...] = (
    # Charge the battery
    SwitchEntityDescription(
        name="charge_battery",
        key="charge_battery",
        translation_key="charge_battery",
    ),
    # Use the battery
    SwitchEntityDescription(
        name="use_battery",
        key="use_battery",
        translation_key="use_battery",
    ),
)


# This is the main function that is called by HA to set up the integration
async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up LVUPS sensors from config entry."""

    # Create all switches and add them to HA.
    for description in SWITCHES:
        async_add_entities([LVUPSSwitch(hass, description, config_entry)])


class LVUPSSwitch(SwitchEntity):
    """Representation of a LVUPS that is updated via MQTT."""

    _attr_has_entity_name = (
        True  # We want to use the friendly name from the entity registry
    )
    should_poll = False  # We get updates via MQTT subscription so no need for polling the device for updates

    def __init__(
        self,
        hass: HomeAssistant,
        description: SwitchEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        self._hass = hass
        self._lvups = hass.data[DOMAIN][config_entry.entry_id]
        self.entity_description = description

        # Set attributes (inherited from SensorEntity)
        self._attr_unique_id = f"{self._lvups.id}_{description.key}"
        self._attr_device_info = self._lvups.device_info

    # This property lets HA know the value of the switch
    @property
    def is_on(self) -> bool | None:
        """Return the state of the sensor."""
        return getattr(self._lvups, self.entity_description.key)

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        setattr(self._lvups, self.entity_description.key, True)
        self._hass.add_job(
            self.async_write_ha_state
        )  # This is needed to update the state of the switch in HA

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        setattr(self._lvups, self.entity_description.key, False)
        self._hass.add_job(
            self.async_write_ha_state
        )  # This is needed to update the state of the switch in HA
