"""Platform for sensor integration."""
# This file shows the setup for the sensors associated with the cdem.
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
from homeassistant.const import (
    EntityCategory,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTime,
    UnitOfVolume,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Define the sensors that are available
SENSORS: tuple[SensorEntityDescription, ...] = (
    # Meter data
    # Cumulated electricity consumption (high tariff)
    SensorEntityDescription(
        name="consumption_high_tarif",
        key="consumption_high_tarif",
        translation_key="consumption_high_tarif",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Cumulated electricity consumption (low tariff)
    SensorEntityDescription(
        name="consumption_low_tarif",
        key="consumption_low_tarif",
        translation_key="consumption_low_tarif",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Cumulated electricity production (high tariff)
    SensorEntityDescription(
        name="production_high_tarif",
        key="production_high_tarif",
        translation_key="production_high_tarif",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Cumulated electricity production (low tariff)
    SensorEntityDescription(
        name="production_low_tarif",
        key="production_low_tarif",
        translation_key="production_low_tarif",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Instantaneous consumption over all phases
    SensorEntityDescription(
        name="total_power_consumption",
        key="total_power_consumption",
        translation_key="total_power_consumption",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous production over all phases
    SensorEntityDescription(
        name="total_power_production",
        key="total_power_production",
        translation_key="total_power_production",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous voltage L1
    SensorEntityDescription(
        name="actual_voltage_l1",
        key="actual_voltage_l1",
        translation_key="actual_voltage_l1",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous voltage L2
    SensorEntityDescription(
        name="actual_voltage_l2",
        key="actual_voltage_l2",
        translation_key="actual_voltage_l2",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous voltage L3
    SensorEntityDescription(
        name="actual_voltage_l3",
        key="actual_voltage_l3",
        translation_key="actual_voltage_l3",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous current L1
    SensorEntityDescription(
        name="actual_current_l1",
        key="actual_current_l1",
        translation_key="actual_current_l1",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous current L2
    SensorEntityDescription(
        name="actual_current_l2",
        key="actual_current_l2",
        translation_key="actual_current_l2",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous current L3
    SensorEntityDescription(
        name="actual_current_l3",
        key="actual_current_l3",
        translation_key="actual_current_l3",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous active power production L1
    SensorEntityDescription(
        name="l1_power_production",
        key="l1_power_production",
        translation_key="l1_power_production",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous active power production L2
    SensorEntityDescription(
        name="l2_power_production",
        key="l2_power_production",
        translation_key="l2_power_production",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous active power production L3
    SensorEntityDescription(
        name="l3_power_production",
        key="l3_power_production",
        translation_key="l3_power_production",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous active power consumption L1
    SensorEntityDescription(
        name="l1_power_consumption",
        key="l1_power_consumption",
        translation_key="l1_power_consumption",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous active power consumption L2
    SensorEntityDescription(
        name="l2_power_consumption",
        key="l2_power_consumption",
        translation_key="l2_power_consumption",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous active power consumption L3
    SensorEntityDescription(
        name="l3_power_consumption",
        key="l3_power_consumption",
        translation_key="l3_power_consumption",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Total gas consumption
    SensorEntityDescription(
        name="gas_meter_m3",
        key="gas_meter_m3",
        translation_key="gas_meter_m3",
        icon="mdi:fire",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # CDEM Stats
    # Decoded p1 telegrams (by CDEM)
    SensorEntityDescription(
        name="decoded",
        key="decoded",
        translation_key="decoded",
        state_class=SensorStateClass.TOTAL,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    # Timeouts
    SensorEntityDescription(
        name="timeouts",
        key="timeouts",
        translation_key="timeouts",
        state_class=SensorStateClass.TOTAL,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    # Published
    SensorEntityDescription(
        name="published",
        key="published",
        translation_key="published",
        state_class=SensorStateClass.TOTAL,
        entity_category=EntityCategory.DIAGNOSTIC,
        #        entity_registry_enabled_default=False,
    ),
    # crc errors
    SensorEntityDescription(
        name="crcerrors",
        key="crcerrors",
        translation_key="crcerrors",
        state_class=SensorStateClass.TOTAL,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    # Uptime
    SensorEntityDescription(
        name="uptime",
        key="uptime",
        translation_key="uptime",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.TOTAL,
        entity_category=EntityCategory.DIAGNOSTIC,
        #        entity_registry_enabled_default=False,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CDEM sensors from config entry."""

    # Add all sensors to a list
    for description in SENSORS:
        async_add_entities([CDEMSensor(hass, description, config_entry)])


class CDEMSensor(SensorEntity):
    """Representation of a CDEM sensor that is updated via MQTT."""

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
        if self.native_value is None:
            return False
        return True

    # This property lets HA know the value of the sensor
    @property
    def native_value(self) -> StateType:
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
