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

SWITCHES: tuple[SwitchEntityDescription, ...] = (
    # Battery Charger
    SwitchEntityDescription(
        name="battery_charger",
        key="battery_charger",
        translation_key="battery_charger",
        icon="mdi:battery-charging",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up LVUPS sensors from config entry."""

    # Add all switches
    async_add_entities([LVUPSBatteryCharger(hass, SWITCHES[0], config_entry)])


class LVUPSBatteryCharger(SwitchEntity):
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
        self._lvups = hass.data[DOMAIN][config_entry.entry_id]
        self.entity_description = description

        # Set attributes (inherited from SensorEntity)
        self._attr_unique_id = f"{self._lvups.id}_{description.key}"
        self._attr_device_info = self._lvups.device_info

    # This property is important to let HA know if this entity is online or not.
    # If an entity is offline (return False), the UI will refelect this.
    @property
    def available(self) -> bool:
        """Return True if value is not None."""
        if self.is_on is None:
            return False
        return True

    # This property lets HA know the value of the sensor
    @property
    def is_on(self) -> bool | None:
        """Return the state of the sensor."""
        return getattr(self._lvups, "battery_ischarging")

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self._lvups.battery_charge(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self._lvups.battery_charge(False)

    async def async_added_to_hass(self) -> None:
        """Run when this Entity has been added to HA."""
        # Sensors should also register callbacks to HA when their state changes
        self._lvups.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self) -> None:
        """Entity being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        self._lvups.remove_callback(self.async_write_ha_state)
