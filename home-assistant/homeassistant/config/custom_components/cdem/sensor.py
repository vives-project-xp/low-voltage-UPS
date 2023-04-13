"""Platform for sensor integration."""
# This file shows the setup for the sensors associated with the cdem.
# They are setup in the same way with the call to the async_setup_entry function
# via HA from the module __init__. Each sensor has a device_class, this tells HA how
# to display it in the UI (for know types).

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
    SensorEntity,
)
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfVolume,
)
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util import slugify

from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)

@dataclass
class CDEMSensorEntityDescription(SensorEntityDescription):
    """Sensor entity description for CDEM."""

    state: Callable | None = None

# Define the sensors that are available
SENSORS: tuple[CDEMSensorEntityDescription, ...] = (
# Meter data
    # Cumulated electricity consumption (high tariff)
    CDEMSensorEntityDescription(
        key="consumption_high_tarif",
        translation_key="consumption_high_tarif",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Cumulated electricity consumption (low tariff)
    CDEMSensorEntityDescription(
        key="consumption_low_tarif",
        translation_key="consumption_low_tarif",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Cumulated electricity production (high tariff)
    CDEMSensorEntityDescription(
        key="production_high_tarif",
        translation_key="production_high_tarif",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Cumulated electricity production (low tariff)
    CDEMSensorEntityDescription(
        key="production_low_tarif",
        translation_key="production_low_tarif",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    # Instantaneous consumption over all phases
    CDEMSensorEntityDescription(
        key="total_power_consumption",
        translation_key="total_power_consumption",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous production over all phases
    CDEMSensorEntityDescription(
        key="total_power_production",
        translation_key="total_power_production",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous voltage L1
    CDEMSensorEntityDescription(
        key="actual_voltage_l1",
        translation_key="actual_voltage_l1",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous voltage L2
    CDEMSensorEntityDescription(
        key="actual_voltage_l2",
        translation_key="actual_voltage_l2",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous voltage L3
    CDEMSensorEntityDescription(
        key="actual_voltage_l3",
        translation_key="actual_voltage_l3",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous current L1
    CDEMSensorEntityDescription(
        key="actual_current_l1",
        translation_key="actual_current_l1",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous current L2
    CDEMSensorEntityDescription(
        key="actual_current_l2",
        translation_key="actual_current_l2",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous current L3
    CDEMSensorEntityDescription(
        key="actual_current_l3",
        translation_key="actual_current_l3",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous active power production L1
    CDEMSensorEntityDescription(
        key="l1_power_production",
        translation_key="l1_power_production",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous active power production L2
    CDEMSensorEntityDescription(
        key="l2_power_production",
        translation_key="l2_power_production",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous active power production L3
    CDEMSensorEntityDescription(
        key="l3_power_production",
        translation_key="l3_power_production",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    # Instantaneous active power consumption L1
    CDEMSensorEntityDescription(
        key="l1_power_consumption",
        translation_key="l1_power_consumption",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous active power consumption L2
    CDEMSensorEntityDescription(
        key="l2_power_consumption",
        translation_key="l2_power_consumption",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous active power consumption L3
    CDEMSensorEntityDescription(
        key="l3_power_consumption",
        translation_key="l3_power_consumption",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Tariff indicator (1=high, 2=low)
    CDEMSensorEntityDescription(
        key="actual_tarif",
        translation_key="actual_tarif",
        device_class=SensorDeviceClass.ENUM,
        options=["Low", "High", "Unknown"],
        icon="mdi:theme-light-dark",
    ),
    # Total gas consumption
   CDEMSensorEntityDescription(
        key="gas_meter_m3",
        translation_key="gas_meter_m3",
        icon="mdi:fire",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
# CDEM Stats
    # Decoded p1 telegrams (by CDEM)
    CDEMSensorEntityDescription(
        key="decoded",
        translation_key="decoded",
#        entity_registry_enabled_default=False,

    ),
    # Timeouts
    CDEMSensorEntityDescription(
        key="timeouts",
        translation_key="timeouts",
#        entity_registry_enabled_default=False,

    ),
    # Published
    CDEMSensorEntityDescription(
        key="published",
        translation_key="published",
#        entity_registry_enabled_default=False,

    ),
    # crc errors
    CDEMSensorEntityDescription(
        key="crcerrors",
        translation_key="crcerrors",
#        entity_registry_enabled_default=False,

    ),
    # Uptime
    CDEMSensorEntityDescription(
        key="uptime",
        translation_key="uptime",
#        entity_registry_enabled_default=False,
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CDEM sensors from config entry."""
    cdem = hass.data[DOMAIN][config_entry.entry_id]

    new_devices = []
    for description in SENSORS:
        new_devices.append(CDEMSensor(cdem, description, config_entry))

    if new_devices:
        async_add_entities(new_devices)


class CDEMSensor(SensorEntity):
    """Representation of a CDEM that is updated via MQTT."""

    should_poll = False # We get updates via MQTT subscription so no need for polling the device for updates
    entity_description: CDEMSensorEntityDescription

    def __init__(
        self,
        cdem,
        description: CDEMSensorEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        self._cdem = cdem
        self.entity_description = description

        slug = slugify(description.key.replace("/", "_"))
        self.entity_id = f"sensor.{self._cdem.name}_{slug}"
        self._attr_unique_id = f"{self._cdem.cdem_id}_{slug}"
        self._attr_name = f"{slug}"

    # This property lets HA know that this sensor belongs to a specific device
    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._cdem.cdem_id)},
            # If desired, the name for the device could be different to the entity
            "name": self._cdem.name,
            "sw_version": self._cdem.firmware_version,
            "hw_version": self._cdem.hardware_version,
            "model": self._cdem.model,
            "manufacturer": self._cdem.manufacturer,
        }

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
        return getattr(self._cdem, self.entity_description.key)


    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        # Sensors should also register callbacks to HA when their state changes
        self._cdem.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        self._cdem.remove_callback(self.async_write_ha_state)
