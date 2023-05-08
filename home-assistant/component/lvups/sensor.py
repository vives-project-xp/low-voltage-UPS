"""Platform for sensor integration."""
# This file shows the setup for the sensors associated with the lvups.
# They are setup in the same way with the call to the async_setup_entry function
# via HA from the module __init__. Each sensor has a device_class, this tells HA how
# to display it in the UI (for know types).

from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# A list of all sensors (add more if you need them)
SENSORS: tuple[SensorEntityDescription, ...] = (
    # Device Uptime
    SensorEntityDescription(
        name="uptime",
        key="uptime",
        translation_key="uptime",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.TOTAL,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    # Indicating the time needed to charge the battery (only available when battery is charging)
    SensorEntityDescription(
        name="charge_time",
        key="charge_time",
        translation_key="charge_time",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        # state_class=SensorStateClass.TOTAL,
    ),
    # Indicating the time needed to discharge the battery (only available when battery is in use)
    SensorEntityDescription(
        name="discharge_time",
        key="discharge_time",
        translation_key="discharge_time",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        # state_class=SensorStateClass.TOTAL,
    ),
    # Indicating the time needed to discharge the battery on max load (always available)
    SensorEntityDescription(
        name="discharge_time_ml",
        key="discharge_time_ml",
        translation_key="discharge_time_ml",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        # state_class=SensorStateClass.TOTAL,
    ),
    # Indicating the battery charge percentage
    SensorEntityDescription(
        name="battery_percentage",
        key="battery_percentage",
        translation_key="battery_percentage",
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
    ),
)


# This is the main function that is called by HA to set up the platform.
async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up LVUPS sensors from config entry."""

    # Create all sensors and add them to HA
    for description in SENSORS:
        async_add_entities([LVUPSSensor(hass, description, config_entry)])


class LVUPSSensor(SensorEntity):
    """Representation of a LVUPS that is updated via MQTT."""

    _attr_has_entity_name = (
        True  # We want to use the friendly name from the entity registry
    )
    should_poll = False  # We get updates via MQTT subscription so no need for polling the device for updates

    def __init__(
        self,
        hass: HomeAssistant,
        description: SensorEntityDescription,
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
        if self.native_value is None:
            return False
        return True

    # This property lets HA know the value of the sensor
    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return getattr(self._lvups, self.entity_description.key)

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
