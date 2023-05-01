"""Constants for the LVUPS integration."""

# This is the internal name of the integration, it should also match the directory
# name for the integration.
DOMAIN = "lvups"

# Data for each topic
TOPICS_STATE = [
    "uptime",
    "battery_ischarging",
    "battery_percentage",
    "battery_inuse",
    "recieving_power",
]

TOPICS_INFO = [  # Retained messages (only used on device creation)
    "firmware_version",
    "hardware_version",
]
