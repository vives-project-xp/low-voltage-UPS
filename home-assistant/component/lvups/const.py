"""Constants for the LVUPS integration."""

# This is the internal name of the integration, it should also match the directory
# name for the integration.
DOMAIN = "lvups"

# Data for the STATE topic
TOPICS_STATE = [
    "Battery_percentage",
    "Charge_time",
    "Charging_battery",
    "Discharge_time",
    "Discharge_time_ml",
    "Receiving_power",
    "Uptime",
    "Using_battery",
]

# Data for the INFO topic
TOPICS_INFO = [  # Retained messages (only used/read on device creation)
    "Firmware_version",
    "Hardware_version",
]
