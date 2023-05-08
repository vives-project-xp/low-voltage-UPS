"""Constants for the CDEM integration."""

# This is the internal name of the integration, it should also match the directory
# name for the integration.
DOMAIN = "cdem"

TOPICS = [
    "payload",
    "stats",
    "announce",
]

# Data for each topic
TOPICS_PAYLOAD = [
    "consumption_high_tarif",
    "consumption_low_tarif",
    "production_high_tarif",
    "production_low_tarif",
    "total_power_consumption",
    "total_power_production",
    "actual_voltage_l1",
    "actual_voltage_l2",
    "actual_voltage_l3",
    "actual_current_l1",
    "actual_current_l2",
    "actual_current_l3",
    "l1_power_production",
    "l2_power_production",
    "l3_power_production",
    "l1_power_consumption",
    "l2_power_consumption",
    "l3_power_consumption",
    "actual_tarif",
    "gas_meter_m3",
]

TOPICS_STATS = [
    "decoded",
    "timeouts",
    "published",
    "crcerrors",
    "uptime",
]

TOPICS_ANNOUNCE = [
    "lib-version",
    "pcb-version",
]
