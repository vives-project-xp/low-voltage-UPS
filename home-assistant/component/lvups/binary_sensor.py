"""Platform for binary sensor integration."""

from __future__ import annotations

import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# A list of all binary sensors (add more if you need them)
BINARY_SENSORS: tuple[BinarySensorEntityDescription, ...] = (
    # Indicating that the battery is being charged (charging)
    BinarySensorEntityDescription(
        name="charging_battery",
        key="charging_battery",
        translation_key="charging_battery",
    ),
    # Indicating that the battery is in use (discharging)
    BinarySensorEntityDescription(
        name="using_battery",
        key="using_battery",
        translation_key="using_battery",
    ),
    # Indicating if mains power is being received
    BinarySensorEntityDescription(
        name="receiving_power",
        key="receiving_power",
        translation_key="receiving_power",
    ),
)

# A list of the icons used for each binary sensor (add more if you need them)
ICONS = {
    "charging_battery": {
        True: "mdi:battery-charging",
        False: "mdi:battery",
    },
    "using_battery": {
        True: "mdi:battery-arrow-down",
        False: "mdi:battery",
    },
    "receiving_power": {
        True: "mdi:power-plug",
        False: "mdi:power-plug-off",
    },
}


# This is the main function that is called by HA to set up the platform.
async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up LVUPS binary sensors from config entry."""

    # Create all the binary sensors and add them to HA.
    for description in BINARY_SENSORS:
        async_add_entities([LVUPSBinarySensor(hass, description, config_entry)])


# This is the class that represents a binary sensor.
class LVUPSBinarySensor(BinarySensorEntity):
    """Representation of a LVUPS BinarySensor that is updated via MQTT."""

    _attr_has_entity_name = (
        True  # We want to use the friendly name from the entity registry
    )
    should_poll = False  # We get updates via MQTT subscription so no need for polling the device for updates

    def __init__(
        self,
        hass: HomeAssistant,
        description: BinarySensorEntityDescription,
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

    # This property lets HA know what icon to use in the frontend.
    @property
    def icon(self) -> str | None:
        """Return the icon to use in the frontend, if any."""
        if self.is_on is None:
            return ICONS[self.entity_description.key][False]
        return ICONS[self.entity_description.key][self.is_on]

    # This property lets HA know the value of the sensor
    @property
    def is_on(self) -> bool | None:
        """Return the state of the sensor."""
        return getattr(self._lvups, self.entity_description.key)

    async def async_added_to_hass(self) -> None:
        """Run when this Entity has been added to HA."""
        # Binary sensors should also register callbacks to HA when their state changes
        self._lvups.register_callback(
            {self.entity_description.key: self.async_write_ha_state}
        )

    async def async_will_remove_from_hass(self) -> None:
        """Run when this Entity is being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        self._lvups.remove_callback(
            {self.entity_description.key: self.async_write_ha_state}
        )
