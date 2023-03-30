# Home Assistant
## About The Project
This project is a smart home automation system that uses Home Assistant as the central hub and Mosquitto as the MQTT broker. 
It is designed to enable the monitoring and control of different home appliances such as energy meters, battery status using MQTT.

## How to install it
Dependencies:
- Docker
- Docker Compose
- **required** [hacs](https://hacs.xyz/docs/configuration/basic/#device-registration) 
- **required** [hacs-integrations](https://github.com/hacs/integration)

To install and run this project, you need to follow the steps below:
1. Clone the repository using the following command:
    ```bash
    git clone <repo_url>
    ```
2. Change the directory to the project folder using the following command:
    ```bash
    cd home-assistant
    ```
3. Start the Home Assistant and MQTT containers using the following command:
    ```bash
    docker-compose up
    ```
## How to run it
1. Start the Home Assistant and MQTT containers using the following command:
    ```bash
    docker-compose up
    ```
2. Open the Home Assistant web interface using the following URL if you are running the containers on your `local machine`:
    ```bash
    http://localhost:8123
    ```  
3. Open the Home Assistant web interface using the following URL if you are running the containers on a `remote machine`:
    ```bash
    http://<remote_machine_ip>:8123
    ```  
## Example usage
After setting up the environment and accessing the Home Assistant interface, users can add and configure various devices and automations to customize their smart home. 
Users can add new devices, such as sensors and switches, by editing the configuration files in the `homeassistant` directory.

to add a new device, users need to add a new entry to the `configuration.yaml` file.

`configuration.yaml`:
```yaml
homeassistant:
default_config:

mqtt: !include mqtt.yaml
group: !include groups.yaml
# automation: !include_dir_list blueprints/
```
to add the low-voltage-UPS, users need to add a new entry to the `mqtt.yaml` file.

`mqtt.yaml`:
```yaml
# the battery
# ---------------------------------------------------------------------
switch:
  # reset battery when on
  - name: "reset battery"
    unique_id: "reset_battery"
    entity_category: "config"
    retain: false
    qos: 0
    command_topic: "homeassistant/battery/reset"
    payload_on:  "1" # reset the battery
    payload_off: "0"   # do nothing

sensor:
  # battery status
  - name: "battery status"
    unique_id: "battery_status"
    device_class: energy
    state_topic: "homeassistant/battery/Status"
    value_template: "{{ value|bool}}"

  # battery in use
  - name: "battery in use"
    unique_id: "battery_in_use"
    device_class: energy
    state_topic: "homeassistant/battery/InUse"
    value_template: "{{ value|bool  }}"

  # battery in use
  - name: "battery is charging"
    unique_id: "battery_is_charging"
    device_class: energy
    state_topic: "homeassistant/battery/IsCharging"
    value_template: "{{ value|bool  }}" 

  # battery charge
  - name: "battery charge"
    unique_id: "battery_charge"
    device_class: energy
    state_topic: "homeassistant/battery/Charge"
    value_template: "{{ value|float /100}}"
    unit_of_measurement: "%"
```
to add the low-voltage-UPS, users need to add a new entry to the `groups.yaml` file.

`groups.yaml`:
```yaml
# the battery
# ---------------------------------------------------------------------
UPS_Battery_energy:
  name: Battery energy
  entities:
    - switch.reset_battery
    - sensor.battery_status
    - sensor.battery_in_use
    - sensor.battery_charge
    - sensor.battery_is_charging
```
## Screenshots
#TODO

## How to set up the dev environment
1. Clone the project repository to your local system.
2. Install Docker and Docker Compose on the host system.
3. Navigate to the project directory.
4. Start the Home Assistant and MQTT containers using the following command:
    ```bash
    docker-compose up
    ```

## License and author info
#TODO 