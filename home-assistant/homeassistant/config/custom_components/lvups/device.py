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


class LVUPS:
    """LVUPS (device for HA)."""

    def __init__(self, hass: HomeAssistant, name: str, topic: str) -> None:
        """Init LVUPS."""
        self._hass = hass
        self.name = name
        self._id = name.lower()
        self._topic = topic
        self._callbacks = set[Callable[[], None]]()

        # Make event to check if retained announce message is received (on startup)
        self._received_info = asyncio.Event()

        # Creating local variables for the MQTT topics
        # State topics
        self._uptime = None
        self._battery_ischarging = None
        self._battery_percentage = None
        self._battery_inuse = None
        self._recieving_power = None
        # Command topics
        self._battery_charge = None
        # Info topics
        self._firmware_version = None
        self._hardware_version = None

    @property
    def id(self) -> str:
        """Return ID for LVUPS."""
        return self._id

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._id)},
            name=self.name,
            sw_version=self._firmware_version,
            hw_version=self._hardware_version,
            model="LVUPS",
            manufacturer="Vives",
        )

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback, called when LVUPS sensor changes state."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    async def subscribe(self) -> None:
        """Handle subscription to MQTT topics and callbacks when messages are received."""

        def call_callback_for_attribute(attribute):
            """Call the callback for the given attribute."""
            # Define the entity we're looking for
            entity = f"sensor.{self.name}_{attribute}"

            # Filter the callbacks to find the one that corresponds to the entity
            matching_callbacks = [
                callback
                for callback in self._callbacks
                if callback.__self__.entity_id == entity
            ]

            # If there is a matching callback, get the first one in the list (there should only be one)
            if matching_callbacks:
                selected_callback = matching_callbacks[0]
                # Now we have the callback, call it
                selected_callback()

        @ha_callback
        def message_received(message):
            """Handle new MQTT messages."""
            # Check if the message is empty
            if message.payload == "":
                _LOGGER.error("Received empty message on topic %s", message.topic)
                return
            # If not empty try to parse the message as JSON
            try:
                payload = json.loads(message.payload)
            except ValueError:
                _LOGGER.error("Received invalid JSON: %s", message.payload)
                return

            # check if message topic is STATE, if so update the attributes
            if message.topic == self._topic + "/" + "STATE":
                attributes = TOPICS_STATE
                for attribute in attributes:
                    if attribute in payload and payload[attribute] != getattr(
                        self, "_" + attribute
                    ):
                        setattr(self, "_" + attribute, payload[attribute])
                        call_callback_for_attribute(attribute)
                        _LOGGER.debug("Updated %s to %s", attribute, payload[attribute])
                for callback in self._callbacks:
                    callback()

            # check if message topic is INFO, if so update the attributes (only if it's the first info message)
            if (
                message.retain
                and message.topic == self._topic + "/" + "INFO"
                and not self._received_info.is_set()
            ):
                attributes = TOPICS_INFO
                for attribute in attributes:
                    setattr(self, "_" + attribute, payload[attribute])
                    _LOGGER.debug("Updated %s to %s", attribute, payload[attribute])

                self._received_info.set()
                _LOGGER.debug("Received first announce message")

        # Subscribe to all topics and call the message_received function when a message is received
        topics = ["STATE", "INFO"]
        for topic in topics:
            await mqtt.async_subscribe(
                self._hass, self._topic + "/" + topic, message_received
            )
            _LOGGER.debug("Subscribed to topic %s", self._topic + "/" + topic)
        # wait for the retained info message to be received or timeout after 5 seconds
        try:
            await asyncio.wait_for(self._received_info.wait(), timeout=5)
            _LOGGER.debug("Successfully handled first message")
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout while waiting for first message")
            return

    # Define the properties for the attributes (these will be used by the sensors)
    @property
    def uptime(self) -> int | None:
        """Returns the Uptime of the device."""
        return self._uptime

    @property
    def battery_ischarging(self) -> bool | None:
        """Returns the Charging status of the battery."""
        return self._battery_ischarging

    @property
    def battery_percentage(self) -> float | None:
        """Returns the Battery percentage."""
        return self._battery_percentage

    @property
    def battery_inuse(self) -> bool | None:
        """Returns the if the battery is in use."""
        return self._battery_inuse

    @property
    def recieving_power(self) -> bool | None:
        """Returns the if the device is receiving power from the grid."""
        return self._recieving_power

    async def battery_charge(self, value: bool) -> None:
        """Set the battery charge."""
        await mqtt.async_publish(
            self._hass,
            self._topic + "/COMMAND",
            json.dumps({"battery_charge": value}),
        )
