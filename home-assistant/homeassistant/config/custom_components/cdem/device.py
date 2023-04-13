"""The CDEM device"""
from __future__ import annotations

# In a real implementation, this would be in an external library that's on PyPI.
# The PyPI package needs to be included in the `requirements` section of manifest.json
# See https://developers.home-assistant.io/docs/creating_integration_manifest
# for more information.

import asyncio
import logging
import json

from collections.abc import Callable
from homeassistant.core import HomeAssistant, callback
from homeassistant.components import mqtt

from .const import TOPIC_PREFIX, TOPICS, TOPICS_PAYLOAD, TOPICS_STATS #, TOPICS_ANNOUNCE

_LOGGER = logging.getLogger(__name__)

class CDEM:
    """CDEM (device for HA)"""

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        """Init CDEM."""
        self._host = host
        self._hass = hass
        self.name = host
        self._id = host.lower()
        self._callbacks = set()
        self._loop = asyncio.get_event_loop()

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

        # Some static information about this device
        self.manufacturer = "Vives"
        self.model = "CDEM"
        self.firmware_version = "0.1.0"
        self.hardware_version = "0.1.0"

        self._loop.create_task(self.publish_updates())

    @property
    def cdem_id(self) -> str:
        """Return ID for CDEM."""
        return self._id

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback, called when cdem sensor changes state."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    async def publish_updates(self) -> None:
        """Run when this Entity has been added to HA."""

        def call_callback_for_attribute(attribute):
            """Call the callback for the given attribute"""
            # Define the entity we're looking for
            entity = f"sensor.{self.name}_{attribute}"

            # Filter the callbacks to find the one that corresponds to the entity
            matching_callbacks = [callback for callback in self._callbacks if callback.__self__.entity_id == entity]

            # If there is a matching callback, get the first one in the list (there should only be one)
            if matching_callbacks:
                selected_callback = matching_callbacks[0]
                # Now we have the callback, call it
                selected_callback()

        @callback
        def message_received(message):
            """Handle new MQTT messages."""

            # Check if the message is empty
            if message.payload == "":
                _LOGGER.error("Received empty message on topic %s", message.topic)
                return
            else:
                # If on empty try to parse the message as JSON
                try:
                    payload = json.loads(message.payload)
                except ValueError:
                    _LOGGER.error("Received invalid JSON: %s", message.payload)
                    return

            # Loop through the topics and update the values if they are in the payload and have changed
            for topic in TOPICS:
                # Only update the values of the topic that was received
                if message.topic == TOPIC_PREFIX + '/' + topic:
                    # Select the attributes that belong to the topic
                    if topic == "payload":
                        attributes = TOPICS_PAYLOAD
                    elif topic == "stats":
                        attributes = TOPICS_STATS
#                    elif topic == "announce":
#                        attributes = TOPICS_ANNOUNCE

                    # Loop through the attributes and update the values if they are in the payload and have changed
                    for attribute in attributes:
                        if attribute in payload and payload[attribute] != getattr(self, '_' + attribute):
                            setattr(self, '_' + attribute, payload[attribute])
                            _LOGGER.debug("Updated %s to %s", attribute, payload[attribute])
                            call_callback_for_attribute(attribute)

        # Subscribe to all topics and call the message_received function when a message is received
        for topic in TOPICS:
            await mqtt.async_subscribe(self._hass, TOPIC_PREFIX + '/' + topic, message_received)
            _LOGGER.debug("Subscribed to topic %s", TOPIC_PREFIX + '/' + topic)

    # Define the properties for the attributes (these will be used by the sensors)
    @property
    def consumption_high_tarif(self) -> float:
        """Returns the Cumulated electricity consumption (high tariff)"""
        return self._consumption_high_tarif

    @property
    def consumption_low_tarif(self) -> float:
        """Returns the Cumulated electricity consumption (low tariff)"""
        return self._consumption_low_tarif

    @property
    def production_high_tarif(self) -> float:
        """Returns the Cumulated electricity production (high tariff)"""
        return self._production_high_tarif

    @property
    def production_low_tarif(self) -> float:
        """Returns the Cumulated electricity production (low tariff)"""
        return self._production_low_tarif

    @property
    def total_power_consumption(self) -> float:
        """Returns the Instantaneous consumption over all phases"""
        return self._total_power_consumption

    @property
    def total_power_production(self) -> float:
        """Returns the Instantaneous production over all phases"""
        return self._total_power_production

    @property
    def actual_voltage_l1(self) -> float:
        """Returns the Instantaneous voltage L1"""
        return self._actual_voltage_l1

    @property
    def actual_voltage_l2(self) -> float:
        """Returns the Instantaneous voltage L2"""
        return self._actual_voltage_l2

    @property
    def actual_voltage_l3(self) -> float:
        """Returns the Instantaneous voltage L3"""
        return self._actual_voltage_l3

    @property
    def actual_current_l1(self) -> float:
        """Returns the Instantaneous current L1"""
        return self._actual_current_l1

    @property
    def actual_current_l2(self) -> float:
        """Returns the Instantaneous current L2"""
        return self._actual_current_l2

    @property
    def actual_current_l3(self) -> float:
        """Returns the Instantaneous current L3"""
        return self._actual_current_l3

    @property
    def l1_power_production(self) -> float:
        """Returns the Instantaneous active power production L1"""
        return self._l1_power_production

    @property
    def l2_power_production(self) -> float:
        """Returns the Instantaneous active power production L2"""
        return self._l2_power_production

    @property
    def l3_power_production(self) -> float:
        """Returns the Instantaneous active power production L3"""
        return self._l3_power_production

    @property
    def l1_power_consumption(self) -> float:
        """Returns the Instantaneous active power consumption L1"""
        return self._l1_power_consumption

    @property
    def l2_power_consumption(self) -> float:
        """Returns the Instantaneous active power consumption L2"""
        return self._l2_power_consumption

    @property
    def l3_power_consumption(self) -> float:
        """Returns the Instantaneous active power consumption L3"""
        return self._l3_power_consumption

    @property
    def actual_tarif(self) -> str:
        """Returns the Tariff indicator (1=high, 2=low)"""
        if self._actual_tarif == 1:
            return "High"
        if self._actual_tarif == 2:
            return "Low"
        return "Unknown"

    @property
    def gas_meter_m3(self) -> float:
        """Returns the Total gas consumption"""
        return self._gas_meter_m3

    @property
    def decoded(self) -> int:
        """Returns the amount of decoded messages"""
        return self._decoded

    @property
    def timeouts(self) -> int:
        """Returns the amount of timeouts"""
        return self._timeouts

    @property
    def published(self) -> int:
        """Returns the amount of published messages"""
        return self._published

    @property
    def crcerrors(self) -> int:
        """Returns the amount of CRC errors"""
        return self._crcerrors

    @property
    def uptime(self) -> str:
        """Returns the uptime of the CDEM"""
        return self._uptime

#    @property
#    def firmware_version(self) -> str:
#        """Returns the firmware version of the CDEM"""
#        return self._lib_version
#
#    @property
#    def hardware_version(self) -> str:
#        """Returns the hardware version of the CDEM"""
#        return self._pcb_version