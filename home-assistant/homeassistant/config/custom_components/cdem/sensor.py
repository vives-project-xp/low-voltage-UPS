"""Support for CDEM through MQTT."""
from __future__ import annotations

from homeassistant.components import mqtt
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import slugify

from .definitions import SENSORS, CDEMSensorEntityDescription
from .const import DOMAIN, TOPIC_PREFIX

async def async_setup_entry(
    _: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CDEM sensors from config entry."""
    async_add_entities(CDEMSensor(description, config_entry) for description in SENSORS)


class CDEMSensor(SensorEntity):
    """Representation of a CDEM that is updated via MQTT."""

    _attr_has_entity_name = True
    entity_description: CDEMSensorEntityDescription

    def __init__(
        self, description: CDEMSensorEntityDescription, config_entry: ConfigEntry
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = description

        slug = slugify(DOMAIN + '_' + description.key.replace("/", "_"))
        self.entity_id = f"sensor.{slug}"
        self._attr_unique_id = f"{config_entry.entry_id}-{slug}"

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            if message.payload == "":
                self._attr_native_value = None
            elif self.entity_description.state is not None:
                # Perform optional additional parsing
                self._attr_native_value = self.entity_description.state(message.payload)
            else:
                self._attr_native_value = message.payload

            self.async_write_ha_state()

        try:
            await mqtt.async_subscribe(
                self.hass, TOPIC_PREFIX + '/' + self.entity_description.key, message_received, 1
            )
        except:
            self._attr_entity_registry_enabled_default = False
