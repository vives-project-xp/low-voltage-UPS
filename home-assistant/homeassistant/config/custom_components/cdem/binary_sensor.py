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

BINARY_SENSORS: tuple[BinarySensorEntityDescription, ...] = (
    # Tariff indicator (1=high, 2=low)
    BinarySensorEntityDescription(
        name="actual_tarif",
        key="actual_tarif",
        translation_key="actual_tarif",
        icon="mdi:theme-light-dark",
    ),
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CDEM sensors from config entry."""

    # Add all binary sensors to a list
    for description in BINARY_SENSORS:
        async_add_entities([CDEMBinarySensor(hass, description, config_entry)])


class CDEMBinarySensor(BinarySensorEntity):
    """Representation of a CDEM binary sensor that is updated via MQTT."""

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
        self._cdem = hass.data[DOMAIN][config_entry.entry_id]
        self.entity_description = description

        # Set attributes (inherited from SensorEntity)
        self._attr_unique_id = f"{self._cdem.cdem_id}_{description.key}"
        self._attr_device_info = self._cdem.device_info

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
        return getattr(self._cdem, str(self.entity_description.key))

    async def async_added_to_hass(self) -> None:
        """Run when this Entity has been added to HA."""
        # Sensors should also register callbacks to HA when their state changes
        self._cdem.register_callback(
            {self.entity_description.key: self.async_write_ha_state}
        )

    async def async_will_remove_from_hass(self) -> None:
        """Entity being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        self._cdem.remove_callback(
            {self.entity_description.key: self.async_write_ha_state}
        )
