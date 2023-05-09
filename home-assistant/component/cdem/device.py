"""The CDEM device."""
from __future__ import annotations

import asyncio
from collections.abc import Callable
import json
import logging

from homeassistant.components import mqtt
from homeassistant.core import HomeAssistant, callback as ha_callback
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, TOPICS, TOPICS_ANNOUNCE, TOPICS_PAYLOAD, TOPICS_STATS

# In a real implementation, this would be in an external library that's on PyPI.
# The PyPI package needs to be included in the `requirements` section of manifest.json
# See https://developers.home-assistant.io/docs/creating_integration_manifest
# for more information.


_LOGGER = logging.getLogger(__name__)


class CDEM:
    """CDEM (device for HA)."""

    def __init__(self, hass: HomeAssistant, name: str, topic: str) -> None:
        """Init CDEM."""
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

        # Make event to check if retained announce message is received (on startup)
        self._recieved_retained_announce = asyncio.Event()

        # Creating local variables for the MQTT topics
        # Payload topics
        self._consumption_high_tarif = None
        self._consumption_low_tarif = None
        self._production_high_tarif = None
        self._production_low_tarif = None
        self._total_power_consumption = None
        self._total_power_production = None
        self._actual_voltage_l1 = None
        self._actual_voltage_l2 = None
        self._actual_voltage_l3 = None
        self._actual_current_l1 = None
        self._actual_current_l2 = None
        self._actual_current_l3 = None
        self._l1_power_production = None
        self._l2_power_production = None
        self._l3_power_production = None
        self._l1_power_consumption = None
        self._l2_power_consumption = None
        self._l3_power_consumption = None
        self._actual_tarif = None
        self._gas_meter_m3 = None
        # Stats topics
        self._decoded = None
        self._timeouts = None
        self._published = None
        self._crcerrors = None
        self._uptime = None
        # Announce topics
        self._lib_version = None
        self._pcb_version = None

    @property
    def cdem_id(self) -> str:
        """Return ID for CDEM."""
        return self._id

    @property
    def device_info(self) -> DeviceInfo:
        """Information about this entity/device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._id)},
            name=self.name,
            sw_version=self._lib_version,
            hw_version=self._pcb_version,
            model="CDEM",
            manufacturer="Vives",
            suggested_area="Garage",
        )

    def register_callback(self, callback: dict[str, Callable[[], None]]) -> None:
        """Register callback, called when cdem sensor changes state."""
        self._callbacks.update(callback)

    def remove_callback(self, callback: dict[str, Callable[[], None]]) -> None:
        """Remove previously registered callback."""
        for key in callback:
            if key in self._callbacks:
                self._callbacks.pop(key)

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

        @ha_callback
        def message_received(message):
            """Handle new MQTT messages."""
            # Check if the message is empty
            if message.payload == "":
                _LOGGER.error("Received empty message on topic %s", message.topic)
                return
            # If on empty try to parse the message as JSON
            try:
                payload = json.loads(message.payload)
            except ValueError:
                _LOGGER.error("Received invalid JSON: %s", message.payload)
                return

            # Loop through the topics and update the values if they are in the payload and have changed
            for topic in TOPICS:
                # Only update the values of the topic that was received
                if message.topic == self._topic + "/" + topic:
                    # Select the attributes that belong to the topic
                    if topic == "payload":
                        attributes = TOPICS_PAYLOAD
                    elif topic == "stats":
                        attributes = TOPICS_STATS
                    elif topic == "announce":
                        attributes = TOPICS_ANNOUNCE

                    # Loop through the attributes and update the values if they are in the payload and have changed
                    for attribute in attributes:
                        if (
                            attribute not in payload
                            and getattr(self, "_" + attribute.lower()) is not None
                        ):
                            setattr(self, "_" + attribute.lower(), None)
                            call_callback_for_attribute(attribute.lower())
                            _LOGGER.debug("Updated %s to %s", attribute, None)

                        if attribute in payload and payload[attribute] != getattr(
                            self, "_" + attribute
                        ):
                            char_to_replace = list[str](("-", " "))
                            attribute_name = str(attribute)
                            for char in char_to_replace:
                                attribute_name = attribute_name.replace(char, "_")

                            setattr(self, "_" + attribute_name, payload[attribute])
                            _LOGGER.debug(
                                "Updated %s to %s", attribute, payload[attribute]
                            )
                            call_callback_for_attribute(attribute)

            if message.retain and message.topic == self._topic + "/" + "announce":
                self._recieved_retained_announce.set()
                _LOGGER.debug("Received first announce message")

        # Subscribe to all topics and call the message_received function when a message is received
        for topic in TOPICS:
            subscription = await mqtt.async_subscribe(
                self._hass, self._topic + "/" + topic, message_received
            )
            _LOGGER.debug("Subscribed to topic %s", self._topic + "/" + topic)
            self._subscriptions[topic] = subscription

        # wait for the first message to be received or timeout after 5 seconds
        try:
            await asyncio.wait_for(self._recieved_retained_announce.wait(), timeout=5)
            _LOGGER.debug("Successfully handled first message")
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout while waiting for first message")
            return

    async def unsubscribe(self) -> None:
        """Unsubscribe from all MQTT topics."""
        for topic, subscription in self._subscriptions.items():
            subscription()
            _LOGGER.debug("Unsubscribed from topic %s", topic)

    # Define the properties for the attributes (these will be used by the sensors)
    @property
    def consumption_high_tarif(self) -> float | None:
        """Returns the Cumulated electricity consumption (high tariff)."""
        return self._consumption_high_tarif

    @property
    def consumption_low_tarif(self) -> float | None:
        """Returns the Cumulated electricity consumption (low tariff)."""
        return self._consumption_low_tarif

    @property
    def production_high_tarif(self) -> float | None:
        """Returns the Cumulated electricity production (high tariff)."""
        return self._production_high_tarif

    @property
    def production_low_tarif(self) -> float | None:
        """Returns the Cumulated electricity production (low tariff)."""
        return self._production_low_tarif

    @property
    def total_power_consumption(self) -> float | None:
        """Returns the Instantaneous consumption over all phases."""
        return self._total_power_consumption

    @property
    def total_power_production(self) -> float | None:
        """Returns the Instantaneous production over all phases."""
        return self._total_power_production

    @property
    def actual_voltage_l1(self) -> float | None:
        """Returns the Instantaneous voltage L1."""
        return self._actual_voltage_l1

    @property
    def actual_voltage_l2(self) -> float | None:
        """Returns the Instantaneous voltage L2."""
        return self._actual_voltage_l2

    @property
    def actual_voltage_l3(self) -> float | None:
        """Returns the Instantaneous voltage L3."""
        return self._actual_voltage_l3

    @property
    def actual_current_l1(self) -> float | None:
        """Returns the Instantaneous current L1."""
        return self._actual_current_l1

    @property
    def actual_current_l2(self) -> float | None:
        """Returns the Instantaneous current L2."""
        return self._actual_current_l2

    @property
    def actual_current_l3(self) -> float | None:
        """Returns the Instantaneous current L3."""
        return self._actual_current_l3

    @property
    def l1_power_production(self) -> float | None:
        """Returns the Instantaneous active power production L1."""
        return self._l1_power_production

    @property
    def l2_power_production(self) -> float | None:
        """Returns the Instantaneous active power production L2."""
        return self._l2_power_production

    @property
    def l3_power_production(self) -> float | None:
        """Returns the Instantaneous active power production L3."""
        return self._l3_power_production

    @property
    def l1_power_consumption(self) -> float | None:
        """Returns the Instantaneous active power consumption L1."""
        return self._l1_power_consumption

    @property
    def l2_power_consumption(self) -> float | None:
        """Returns the Instantaneous active power consumption L2."""
        return self._l2_power_consumption

    @property
    def l3_power_consumption(self) -> float | None:
        """Returns the Instantaneous active power consumption L3."""
        return self._l3_power_consumption

    @property
    def actual_tarif(self) -> bool | None:
        """Returns the Tariff indicator (1=high, 2=low)."""
        if self._actual_tarif == 1:
            return True

        if self._actual_tarif == 2:
            return False

        return None

    @property
    def gas_meter_m3(self) -> float | None:
        """Returns the Total gas consumption."""
        return self._gas_meter_m3

    @property
    def decoded(self) -> int | None:
        """Returns the amount of decoded messages."""
        return self._decoded

    @property
    def timeouts(self) -> int | None:
        """Returns the amount of timeouts."""
        return self._timeouts

    @property
    def published(self) -> int | None:
        """Returns the amount of published messages."""
        return self._published

    @property
    def crcerrors(self) -> int | None:
        """Returns the amount of CRC errors."""
        return self._crcerrors

    @property
    def uptime(self) -> str | None:
        """Returns the uptime of the CDEM converted to seconds."""
        if self._uptime is None:
            return None

        ## Convert the uptime to seconds
        # First split the string on spaces "3d 0h 11m 18s 354ms" -> ["3d", "0h", "11m", "18s", "354ms"]
        # Than remove the last item from the list ["3d", "0h", "11m", "18s", "354ms"] -> ["3d", "0h", "11m", "18s"] because we don't need the milliseconds
        # Then remove the last character from each item in the list ["3d", "0h", "11m", "18s", "354m"] -> ["3", "0", "11", "18", "354"]
        # Then convert each item in the list to an integer [3, 0, 11, 18, 354]
        # Lastly calculate the total amount of seconds by multiplying the items in the list with the amount of seconds they represent

        days, hours, minutes, seconds = map(
            int, (x[:-1] for x in str(self._uptime).split(" ")[:-1])
        )
        total_seconds = (days * 86_400) + (hours * 3_600) + (minutes * 60) + (seconds)

        return total_seconds
