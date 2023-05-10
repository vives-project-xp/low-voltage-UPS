# Home Use

## List of contents

1. [Installation](#1-installation)
    1. [Setup Home Assistant](#11-setup-home-assistant)
    2. [Add the custom component](#12-add-the-custom-component)
        1. [Home Assistant Container](#121-home-assistant-container)
        2. [Home Assistant Operating System](#122-home-assistant-operating-system)
    3. [Add lvups device to Home Assistant](#13-add-lvups-device-to-home-assistant)
2. [Usage](#2-usage)

## 1. Installation

### 1.1 Setup Home Assistant

For installation instructions, see the [home assistant documentation](https://www.home-assistant.io/installation/).

**Note:**
Make sure you also have mqtt running either in a container or as an addon.

### 1.2 Add the custom component

#### 1.2.1 Home Assistant Container

If your running Home Assistant Container, you can add the component to your installation by following these steps:

1. Make sure Home Assistant is not running.
2. Make sure you have cloned this repository to your local machine and are in the home-assistant directory.
3. Run the following command:
    ```docker cp ./component/ <container_name>:/config/custom_components/```.
    (replace `<container_name>` with the name of your Home Assistant Container)
4. Start Home Assistant.

That's it, the component is now added to your Home Assistant installation.

#### 1.2.2 Home Assistant Operating System

If your running Home Assistant Operating System, you can add the component to your installation by following these steps:

1. In your Home Assisant instance, go to Settings > Add-ons.
2. Under the Official add-ons section, you will find the File editor add-on.
3. Click on File editor and click on Install. When the installation is complete, the UI will go to the add-on details page for the file editor.
4. Now start the add-on by clicking on Start.
5. Open the user interface by clicking on Open Web UI.
6. In the File editor, go to the config folder of your Home Assistant installation and create a new folder called `custom_components` (if it doesn't exist already).
7. In this folder just drag and drop the content of the `component` folder from this repository.
8. Restart Home Assistant.

That's it, the component is now added to your Home Assistant installation.

### 1.3 Add lvups device to Home Assistant

Now you can add a lvups device to your Home Assistant installation.
This can be done by going to Setting > Devices & services and clicking on the Add Integration button.

Now search for lvups and click on the lvups integration.
Fill in the required information and click on Submit.

That's it, the lvups device is now added to your Home Assistant installation.

**Note:**
Make sure you have added your mqtt broker to Home Assistant before adding the lvups device else it will not work. For more info about this, see the [MQTT documentation](https://www.home-assistant.io/integrations/mqtt/).

## 2. Usage

Now that we have a working Home Assistant installation with the lvups component installed, we can start using it.

### 2.1 Device info

The lvups device has the following attributes:

controls:

- `Charge battery`: A switch that can be used to tell the device it should charge the battery. (default: `off`)
- `Use battery`: A switch that can be used to tell the device it should use the battery, when recieving grid power. (default: `off`)

sensors:

- `Battery percentage`: A sensor that shows the current battery percentage.
- `Charge time`: A sensor that shows the time left until the battery is fully charged, estimate. (When charging)
- `Discharge time`: A sensor that shows the time left until the battery is fully discharged, estimate. (When discharging)
- `Discharge time max load`: A sensor that shows the time left until the battery is fully discharged, estimate on max load. (Always shown)
- `Charging battery`: A sensor that shows if the battery is currently charging.
- `Using battery`: A sensor that shows if the battery is currently being used.
- `Recieving power`: A sensor that shows if the device is currently recieving power from the grid.

Configuration:

- `Battery size`: The capacity of the battery in mAh. (default: `0`)
- `Max charge`: The maximum percentage the battery can be charged to. (default: `100`)
- `Min charge`: The minimum percentage the battery can be discharged to. (default: `0`)
- `Restart`: A button that can be used to restart the device.

Diagnostic:

- `Uptime`: The time the device has been running, in `hours:minutes:seconds` format.

### 2.2 Automation examples

Here are some automation examples that you can use:

- Get a notification when there is no power going to the device (possible grid power loss):

    ```text
        trigger:
            - UPS recieving power: 'off'
        action:
            - Call notify service with message: 'Grid power loss'
    ```

- Charge bettery when solar power is avaialble: (example made using cdem for getting data from smartmeter)

    ```text
        trigger:
            - cdem power production: '> 0'
        condition:
            - UPS battery percentage: '< 100'
        action:
            - UPS charge battery: 'on'
    ```

- Use battery when grid power uses high tarif: (also using the cdem component)

    ```text
        trigger:
            - cdem tarif: 'high'
        condition:
            - UPS battery percentage: '> 50'
        action:
            - UPS use battery: 'on'
    ```


## 3. Troubleshooting

- When performing a firmware update, you will need to reload the lvups device in Home Assistant to see the new firmware version.
