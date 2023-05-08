# Showcase

## List of contents

1. [Installation](#1-installation)
    1. [Requirements](#11-requirements)
    2. [Setup containers](#12-setup-containers)
    3. [Configure Home Assistant](#13-configure-home-assistant)

2. [Usage](#2-usage)

## 1. Installation

### 1.1 Requirements

Before you can run the showcase, you need to install the following dependencies:

- Docker

### 1.2 Setup containers

To setup the containers, follow the steps below:

1. Make sure docker is running.
2. Open a terminal in the `showcase` directory.
3. Run the following command in the terminal:

    ```bash
    docker-compose up
    ```

4. Wait for the containers to start.
5. Now we copy the component to the Home Assistant container, run the following command in the terminal:

    ```bash
    docker cp ../component/ homeassistant:/config/custom_components
    ```

6. Restart the Home Assistant container.

### 1.3 Configure Home Assistant

After the containers are started, got to the Home Assistant web interface using the following [link](http://localhost:8123).  
Now you can configure Home Assistant to your liking, for more info about this, see the [Home Assistant documentation](https://www.home-assistant.io/docs/).  
We also need to add our mqtt broker to Home Assistant, for more info about this, see the [MQTT documentation](https://www.home-assistant.io/integrations/mqtt/).  
The mqtt broker is available at `localhost:1883`.

## 2. Usage

After setting up the environment, you should have a working Home Assistant installation with the low-voltage-UPS component installed.
Now you simply need to add a low-voltage-UPS device to your Home Assistant installation, for more info about this, see the [Home Assistant documentation](https://www.home-assistant.io/docs/configuration/devices/).

For automation examples, please look at the [Home-Use](home-use.md) section.
