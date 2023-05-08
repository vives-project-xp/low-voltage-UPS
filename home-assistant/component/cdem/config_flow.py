"""Config flow for Hello World integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.mqtt import valid_subscribe_topic
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Data schema for the user input
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("name"): str,
        vol.Required("topic"): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    # Validate name
    # Check if name is unique
    try:
        for device in hass.data[DOMAIN]:
            if hass.data[DOMAIN][device].name == data["name"].lower():
                raise NameAlreadyExists
    except KeyError:
        pass  # No device exists for this domain, so we can continue

    # Check if name is too short
    if len(data["name"]) < 3:
        raise NameTooShort

    # Check if name is too long
    if len(data["name"]) > 32:
        raise NameTooLong

    # Validate topic
    # Check if topic is valid
    if data["topic"].endswith("/#"):
        data["topic"] = data["topic"][:-2]

    topic_valid = False
    try:
        valid_subscribe_topic(f"{data['topic']}/#")
    except vol.Invalid:
        topic_valid = False
    else:
        topic_valid = True

    if not topic_valid:
        raise InvalidTopic

    # Return info that will be used store the config entry.
    return {"title": data["name"], "data": data}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for CDEM."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except NameAlreadyExists:
                errors["base"] = "name_already_exists"
            except NameTooShort:
                errors["base"] = "name_too_short"
            except NameTooLong:
                errors["base"] = "name_too_long"
            except InvalidTopic:
                errors["base"] = "invalid_topic"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=info["data"])

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class NameAlreadyExists(HomeAssistantError):
    """Error to indicate the name already exists."""


class NameTooShort(HomeAssistantError):
    """Error to indicate the name is too short."""


class NameTooLong(HomeAssistantError):
    """Error to indicate the name is too long."""


class InvalidTopic(HomeAssistantError):
    """Error to indicate the given topic is invalid."""
