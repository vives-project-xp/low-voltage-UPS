"""Platform for button integration."""

from __future__ import annotations

import logging

from homeassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# A list of all buttons (add more if you need them)
BUTTONS: tuple[ButtonEntityDescription, ...] = (
    # Restart the device
    ButtonEntityDescription(
        name="restart",
        key="restart",
        translation_key="restart",
        device_class=ButtonDeviceClass.RESTART,
        entity_category=EntityCategory.CONFIG,
    ),
)


# This is the main function that is called by HA to set up the platform.
async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up LVUPS sensors from config entry."""

    # Create all buttons and add them to HA.
    for description in BUTTONS:
        async_add_entities([LVUPSButton(hass, description, config_entry)])


# This is the class that represents a button.
class LVUPSButton(ButtonEntity):
    """Representation of a LVUPS Button that is updated via MQTT."""

    _attr_has_entity_name = (
        True  # We want to use the friendly name from the entity registry
    )
    should_poll = False  # We get updates via MQTT subscription so no need for polling the device for updates

    def __init__(
        self,
        hass: HomeAssistant,
        description: ButtonEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        self._lvups = hass.data[DOMAIN][config_entry.entry_id]
        self.entity_description = description

        # Set attributes (inherited from SensorEntity)
        self._attr_unique_id = f"{self._lvups.id}_{description.key}"
        self._attr_device_info = self._lvups.device_info

    def press(self) -> None:
        """Handle the press of the button."""
        setattr(self._lvups, self.entity_description.key, True)

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
