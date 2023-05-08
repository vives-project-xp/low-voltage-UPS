"""Platform for number integration."""

from __future__ import annotations

import logging

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# A list of all numbers (add more if you need them)
NUMBERS: tuple[NumberEntityDescription, ...] = (
    # Battery size
    NumberEntityDescription(
        name="battery_size",
        key="battery_size",
        translation_key="battery_size",
        device_class=NumberDeviceClass.ENERGY_STORAGE,
        native_max_value=1_000_000,
        native_min_value=0,
        native_step=1,
        native_unit_of_measurement="mAh",
        entity_category=EntityCategory.CONFIG,
    ),
    # Maximum battery charge
    NumberEntityDescription(
        name="max_battery_charge",
        key="max_battery_charge",
        translation_key="max_battery_charge",
        device_class=NumberDeviceClass.BATTERY,
        native_max_value=100.0,
        native_min_value=0.0,
        native_step=0.1,
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.CONFIG,
    ),
    # Minimum battery charge
    NumberEntityDescription(
        name="min_battery_charge",
        key="min_battery_charge",
        translation_key="min_battery_charge",
        device_class=NumberDeviceClass.BATTERY,
        native_max_value=100.0,
        native_min_value=0.0,
        native_step=0.1,
        native_unit_of_measurement=PERCENTAGE,
        entity_category=EntityCategory.CONFIG,
    ),
)


# This is the main function that is called by HA to set up the platform.
async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up LVUPS sensors from config entry."""

    # Create all numbers and add them to HA.
    for description in NUMBERS:
        async_add_entities([LVUPSNumber(hass, description, config_entry)])


# This is the class that represents a number.
class LVUPSNumber(NumberEntity):
    """Representation of a LVUPS that is updated via MQTT."""

    _attr_has_entity_name = (
        True  # We want to use the friendly name from the entity registry
    )
    should_poll = False  # We get updates via MQTT subscription so no need for polling the device for updates

    def __init__(
        self,
        hass: HomeAssistant,
        description: NumberEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        self._lvups = hass.data[DOMAIN][config_entry.entry_id]
        self.entity_description = description

        # Set attributes (inherited from SensorEntity)
        self._attr_unique_id = f"{self._lvups.id}_{description.key}"
        self._attr_device_info = self._lvups.device_info

    def set_native_value(self, value: float) -> None:
        """Update the current value."""
        setattr(self._lvups, self.entity_description.key, value)

    async def async_added_to_hass(self) -> None:
        """Run when this Entity has been added to HA."""
        # Sensors should also register callbacks to HA when their state changes
        self._lvups.register_callback(
            {self.entity_description.key: self.async_write_ha_state}
        )

    async def async_will_remove_from_hass(self) -> None:
        """Entity being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        self._lvups.remove_callback(
            {self.entity_description.key: self.async_write_ha_state}
        )
