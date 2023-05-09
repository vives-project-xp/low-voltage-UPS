"""The LVUPS device."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
import json
import logging

from homeassistant.components import mqtt
from homeassistant.core import HomeAssistant, callback as ha_callback
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, TOPICS_INFO, TOPICS_STATE

# In a real implementation, this would be in an external library that's on PyPI.
# The PyPI package needs to be included in the `requirements` section of manifest.json
# See https://developers.home-assistant.io/docs/creating_integration_manifest
# for more information.

_LOGGER = logging.getLogger(__name__)


# The LVUPS device class
class LVUPS:
    """LVUPS (device for HA)."""

    def __init__(self, hass: HomeAssistant, name: str, topic: str) -> None:
        """Init LVUPS."""
        self._hass = hass
        self.name = name
        self._id = name.lower()
        self._topic = topic
        self._callbacks = dict[
            str, Callable[[], None]
        ]()  # List of callbacks for platforms (attribute, callback)
        self._subscriptions = dict[
            str, Callable[[], None]
        ]()  # List of subscriptions (topic, callback)

        # Make event to check if retained announce message is received (on creation/loading of device)
        self._received_info = asyncio.Event()

        # Creating local variables for the MQTT topics
        # State topics
        self._battery_percentage = None
        self._charge_time = None
        self._charging_battery = None
        self._discharge_time = None
        self._discharge_time_ml = None
        self._receiving_power = None
        self._uptime = None
        self._using_battery = None
        # Command topics
        self._battery_size = 0  # None
        self._charge_battery = False
        self._max_battery_charge = 100.0  # None
        self._min_battery_charge = 0.0  # None
        self._restart = False
        self._use_battery = False
        # Info topics
        self._firmware_version = None
        self._hardware_version = None

    # Device properties
    @property
    def id(self) -> str:
        """Returns the ID of the LVUPS."""
        return self._id

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about the LVUPS."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._id)},
            name=self.name,
            sw_version=self._firmware_version,
            hw_version=self._hardware_version,
            model="LVUPS",
            manufacturer="Vives",
        )

    # Properties for the topics (to be used by the platforms)
    ## State topics
    @property
    def battery_percentage(self) -> int | None:
        """Returns the battery percentage."""
        return self._battery_percentage

    @property
    def charge_time(self) -> int | None:
        """Returns the time to fully charge the battery (when charging)."""
        return self._charge_time

    @property
    def charging_battery(self) -> bool | None:
        """Returns if the battery is charging."""
        return self._charging_battery

    @property
    def discharge_time(self) -> int | None:
        """Returns the time to fully discharge the battery (when discharging)."""
        return self._discharge_time

    @property
    def discharge_time_ml(self) -> int | None:
        """Returns the time to fully discharge the battery on max load (always)."""
        return self._discharge_time_ml

    @property
    def receiving_power(self) -> bool | None:
        """Returns if the device is receiving power from the grid."""
        return self._receiving_power

    @property
    def uptime(self) -> int | None:
        """Returns the Uptime of the device."""
        return self._uptime

    @property
    def using_battery(self) -> bool | None:
        """Returns if the device is using the battery."""
        return self._using_battery

    ## Command topics
    @property
    def battery_size(self) -> int | None:
        """Returns the size of the battery."""
        return self._battery_size

    @battery_size.setter
    def battery_size(self, value: int) -> None:
        """Set the size of the battery."""
        self._battery_size = value
        self._hass.add_job(
            mqtt.async_publish(
                self._hass,
                self._topic + "/COMMAND",
                json.dumps({"Battery_size": self._battery_size}),
            )
        )

    @property
    def charge_battery(self) -> bool | None:
        """Returns if the battery should be charging."""
        return self._charge_battery

    @charge_battery.setter
    def charge_battery(self, value: bool) -> None:
        """Set if the battery should be charging."""
        self._charge_battery = value
        self._hass.add_job(
            mqtt.async_publish(
                self._hass,
                self._topic + "/COMMAND",
                json.dumps({"Charge_battery": self._charge_battery}),
            )
        )

    @property
    def max_battery_charge(self) -> float | None:
        """Returns the maximum battery charge (when chraging)."""
        return self._max_battery_charge

    @max_battery_charge.setter
    def max_battery_charge(self, value: float) -> None:
        """Set the maximum battery charge (when chraging)."""
        self._max_battery_charge = value
        self._hass.add_job(
            mqtt.async_publish(
                self._hass,
                self._topic + "/COMMAND",
                json.dumps({"Max_battery_charge": self._max_battery_charge}),
            )
        )

    @property
    def min_battery_charge(self) -> float | None:
        """Returns the minimum battery charge (when discharging)."""
        return self._min_battery_charge

    @min_battery_charge.setter
    def min_battery_charge(self, value: float) -> None:
        """Set the minimum battery charge (when discharging)."""
        self._min_battery_charge = value
        self._hass.add_job(
            mqtt.async_publish(
                self._hass,
                self._topic + "/COMMAND",
                json.dumps({"Min_battery_charge": self._min_battery_charge}),
            )
        )

    @property
    def restart(self) -> bool | None:
        """Returns if the device should restart."""
        return self._restart

    @restart.setter
    def restart(self, value: bool) -> None:
        """Set if the device should restart."""
        self._restart = value
        self._hass.add_job(
            mqtt.async_publish(
                self._hass,
                self._topic + "/COMMAND",
                json.dumps({"Restart": self._restart}),
            )
        )
        self._restart = False  # reset after publishing (because it's a button)

    @property
    def use_battery(self) -> bool | None:
        """Returns if the battery should be used."""
        return self._use_battery

    @use_battery.setter
    def use_battery(self, value: bool) -> None:
        """Set if the battery should be used."""
        self._use_battery = value
        self._hass.add_job(
            mqtt.async_publish(
                self._hass,
                self._topic + "/COMMAND",
                json.dumps({"Use_battery": self._use_battery}),
            )
        )

    # Methods
    async def subscribe(self) -> None:
        """Handle subscription to MQTT topics and callbacks when messages are received."""

        def call_callback_for_attribute(attribute):
            """Call the callback for the given attribute."""
            # Check if the attribute is in the callback dictionary
            if attribute not in self._callbacks.keys():
                return

            # If it is, get the callback
            callback = self._callbacks[attribute]

            # Call the callback
            callback()

        def validate_mqqt_message(message):
            """Validate the mqqt message (not empty and valid JSON)."""
            # Check if the message is empty
            if message.payload == "":
                _LOGGER.error("Received empty message on topic %s", message.topic)
                return False

            # Check is the message is valid JSON
            try:
                json.loads(message.payload)
            except ValueError:
                _LOGGER.error("Received invalid JSON: %s", message.payload)
                return False

            return True

        @ha_callback
        def message_received(message):
            """Handle new MQTT messages."""
            # Check if the message is valid and valid JSON
            if not validate_mqqt_message(message):
                return

            # Convert the payload to json
            payload = json.loads(message.payload)

            # Check if message topic is STATE, if so update the attributes
            if message.topic == self._topic + "/" + "STATE":
                attributes = TOPICS_STATE
                for attribute in attributes:
                    if (
                        attribute not in payload
                        and getattr(self, "_" + attribute.lower()) is not None
                    ):
                        setattr(self, "_" + attribute.lower(), None)
                        call_callback_for_attribute(attribute.lower())
                        _LOGGER.debug("Updated %s to %s", attribute, None)

                    if attribute in payload and payload[attribute] != getattr(
                        self, "_" + attribute.lower()
                    ):
                        setattr(self, "_" + attribute.lower(), payload[attribute])
                        call_callback_for_attribute(attribute.lower())
                        _LOGGER.debug("Updated %s to %s", attribute, payload[attribute])

                    if (
                        attribute not in payload
                        and getattr(self, "_" + attribute.lower()) is not None
                    ):
                        setattr(self, "_" + attribute.lower(), None)

            # Check if message topic is INFO, if so update the attributes (only if it's the first info message)
            if (
                message.retain
                and message.topic == self._topic + "/" + "INFO"
                and not self._received_info.is_set()
            ):
                attributes = TOPICS_INFO
                for attribute in attributes:
                    if attribute in payload:
                        setattr(self, "_" + attribute.lower(), payload[attribute])
                        _LOGGER.debug("Updated %s to %s", attribute, payload[attribute])

                self._received_info.set()
                _LOGGER.debug("Received first announce message")

        # Subscribe to all topics and call the message_received function when a message is received
        topics = ["STATE", "INFO"]
        for topic in topics:
            subscription = await mqtt.async_subscribe(
                self._hass, self._topic + "/" + topic, message_received
            )
            _LOGGER.debug("Subscribed to topic %s", self._topic + "/" + topic)
            self._subscriptions[topic] = subscription

        # Wait for the retained info message to be received or timeout after 5 seconds
        try:
            await asyncio.wait_for(self._received_info.wait(), timeout=5)
            _LOGGER.debug("Successfully handled first message")
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout while waiting for first message")
            return

    async def unsubscribe(self) -> None:
        """Unsubscribe from all MQTT topics."""
        for topic, subscription in self._subscriptions.items():
            subscription()
            _LOGGER.debug("Unsubscribed from topic %s", topic)

    def register_callback(self, callback: dict[str, Callable[[], None]]) -> None:
        """Register callback, called when LVUPS sensors change state."""
        self._callbacks.update(callback)

    def remove_callback(self, callback: dict[str, Callable[[], None]]) -> None:
        """Remove previously registered callback."""
        for key in callback:
            if key in self._callbacks:
                self._callbacks.pop(key)
