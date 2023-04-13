"""Platform for sensor integration."""
# This file shows the setup for the sensors associated with the cover.
# They are setup in the same way with the call to the async_setup_entry function
# via HA from the module __init__. Each sensor has a device_class, this tells HA how
# to display it in the UI (for know types). The unit_of_measurement property tells HA
# what the unit is, so it can display the correct range. For predefined types (such as
# battery), the unit_of_measurement should match what's expected.
import random

from homeassistant.const import (
    PERCENTAGE,
)
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.helpers.entity import Entity, DeviceInfo
from homeassistant.core import HomeAssistant

from .const import DOMAIN


# See cover.py for more details.
# Note how both entities for each roller sensor (battry and illuminance) are added at
# the same time to the same list. This way only a single async_add_devices call is
# required.
async def async_setup_entry(
    hass: HomeAssistant,
    config_entry,
    async_add_entities
):
    """Add sensors for passed config_entry in HA."""
    cdem = hass.data[DOMAIN][config_entry.entry_id]

    new_devices = []
    new_devices.append(BatterySensor(cdem))
    new_devices.append(IlluminanceSensor(cdem))

    if new_devices:
        async_add_entities(new_devices)


# This base class shows the common properties and methods for a sensor as used in this
# example. See each sensor for further details about properties and methods that
# have been overridden.
class SensorBase(Entity):
    """Base representation of a Hello World Sensor."""

    should_poll = False

    def __init__(self, cdem) -> None:
        """Initialize the sensor."""
        self._cdem = cdem

    # To link this entity to the cover device, this property must return an
    # identifiers value matching that used in the cover, but no other information such
    # as name. If name is returned, this entity will then also become a device in the
    # HA UI.
    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._cdem.cdem_id)},
            # If desired, the name for the device could be different to the entity
            "name": self.name,
            "sw_version": self._cdem.firmware_version,
            "model": self._cdem.model,
            "manufacturer": self._cdem.manufacturer,
        }

    # This property is important to let HA know if this entity is online or not.
    # If an entity is offline (return False), the UI will refelect this.
    @property
    def available(self) -> bool:
        """Return True if cdem is available."""
        return self._cdem.online

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        # Sensors should also register callbacks to HA when their state changes
        self._cdem.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        self._cdem.remove_callback(self.async_write_ha_state)

class BatterySensor(SensorBase):
    """Representation of a Sensor."""

    # The class of this device. Note the value should come from the homeassistant.const
    # module. More information on the available devices classes can be seen here:
    # https://developers.home-assistant.io/docs/core/entity/sensor
    device_class = SensorDeviceClass.BATTERY

    # The unit of measurement for this entity. As it's a SensorDeviceClass.BATTERY, this
    # should be PERCENTAGE. A number of units are supported by HA, for some
    # examples, see:
    # https://developers.home-assistant.io/docs/core/entity/sensor#available-device-classes
    _attr_unit_of_measurement = PERCENTAGE

    def __init__(self, cdem) -> None:
        """Initialize the sensor."""
        super().__init__(cdem)

        # As per the sensor, this must be a unique value within this domain. This is done
        # by using the device ID, and appending "_battery"
        self._attr_unique_id = f"{self._cdem.cdem_id}_battery"

        # The name of the entity
        self._attr_name = f"{self._cdem.name} Battery"

        self._state = random.randint(0, 100)

    # The value of this sensor. As this is a SensorDeviceClass.BATTERY, this value must be
    # the battery level as a percentage (between 0 and 100)
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._cdem.battery_level


# This is another sensor, but more simple compared to the battery above. See the
# comments above for how each field works.
class IlluminanceSensor(SensorBase):
    """Representation of a Sensor."""

    device_class = SensorDeviceClass.ILLUMINANCE
    _attr_unit_of_measurement = "lx"

    def __init__(self, cdem) -> None:
        """Initialize the sensor."""
        super().__init__(cdem)
        # As per the sensor, this must be a unique value within this domain. This is done
        # by using the device ID, and appending "_battery"
        self._attr_unique_id = f"{self._cdem.cdem_id}_illuminance"

        # The name of the entity
        self._attr_name = f"{self._cdem.name} Illuminance"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._cdem.illuminance
