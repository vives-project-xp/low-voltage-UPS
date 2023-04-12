"""Definitions for CDEM data added to MQTT."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfVolume,
)

from homeassistant.util import dt as dt_util

def tariff_transform(value):
    """Transform tariff from number to description."""
    if value == "1.00":
        return "High"
    if value == "2.00":
        return "Low"
    return "Unknown"


def uptime_transform(value):
    """ Transform uptime from '..d ..h ..m ..s ..ms' to timestamp """
    return dt_util.parse_datetime(value)


@dataclass
class CDEMSensorEntityDescription(SensorEntityDescription):
    """Sensor entity description for CDEM."""

    state: Callable | None = None


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
#        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous voltage L3
    CDEMSensorEntityDescription(
        key="actual_voltage_l3",
        translation_key="actual_voltage_l3",
#        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
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
#        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous current L3
    CDEMSensorEntityDescription(
        key="actual_current_l3",
        translation_key="actual_current_l3",
#        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
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
#        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous active power production L3
    CDEMSensorEntityDescription(
        key="l3_power_production",
        translation_key="l3_power_production",
#        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
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
#        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Instantaneous active power consumption L3
    CDEMSensorEntityDescription(
        key="l3_power_consumption",
        translation_key="l3_power_consumption",
#        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
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
        state=tariff_transform,
    ),
    # Total gas consumption
   CDEMSensorEntityDescription(
        key="gas_meter_m3",
        translation_key="gas_meter_m3",
#        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
        icon="mdi:fire",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
# CDEM Stats
    # Decoded p1 telegrams (by CDEM)
    CDEMSensorEntityDescription(
        key="decoded",
        translation_key="decoded",
        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
    ),
    # Timeouts
    CDEMSensorEntityDescription(
        key="timeouts",
        translation_key="timeouts",
        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
    ),
    # Published
    CDEMSensorEntityDescription(
        key="published",
        translation_key="published",
        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
    ),
    # crc errors
    CDEMSensorEntityDescription(
        key="crcerrors",
        translation_key="crcerrors",
        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
    ),
    # Uptime
    CDEMSensorEntityDescription(
        key="uptime",
        translation_key="uptime",
        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
        device_class=SensorDeviceClass.TIMESTAMP,
        state=uptime_transform,
    ),
# Device details
    # IP address
    CDEMSensorEntityDescription(
        key="ip",
        translation_key="ip",
        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
    ),
    # MAC address
    CDEMSensorEntityDescription(
        key="mac",
        translation_key="mac",
        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
    ),
    # Firmware version
    CDEMSensorEntityDescription(
        key="lib-version",
        translation_key="lib-version",
        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
    ),
    # Pcb version
    CDEMSensorEntityDescription(
        key="pcb-version",
        translation_key="pcb-version",
        entity_registry_enabled_default=False,
#        entity_registry_visible_default=False,
    ),
)
