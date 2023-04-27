<template>
  <section>
    <PageTitle title="Setup" />
    <div>
      <!-- Alerts -->
      <div class="flex flex-col items-center gap-2 m-2 mx-16">
          <!-- Error alert -->
          <div v-if="error" class="alert alert-error shadow-lg w-fit max-w-full">
            <div>
              <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24" >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{{ error.name }}: {{ error.message }}</span>
            </div>
          </div>
          <!-- Warning alert -->
          <div v-if="!isSupported" class="alert alert-warning shadow-lg w-fit">
            <div>
              <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24" >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <span>
                <p>Warning: Your browser does not support Bluetooth!</p>
              </span>
            </div>
          </div>
          <!-- Success alert -->
          <div v-if="isConnected" class="alert alert-success shadow-lg w-2/4">
            <div>
              <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24" >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Successfully connected to {{ device.name }}</span>
            </div>
          </div>
        </div>
      <div class="mx-16">
        <div class="rounded-2xl tertiary-color-card  w-fit mt-8 m-16 mx-auto">
          <!-- Setup form -->
          <div class="flex flex-col p-4  items-center ">
            <!-- Bluetooth -->
            <h2 class="divider p-2 text-2xl font-bold text-center">Bluetooth</h2>
            <button v-if="!isConnected" id="BtnConnect" class="btn btn-primary w-full" @click="requestDevice()" >
              Connect
            </button>
            <button v-if="isConnected" id="BtnConnect" class="btn btn-primary w-full" @click="DisconnectDevice()" >
              DisConnect
            </button>

            <!-- Name -->
            <div class="flex flex-col gap-4 w-full">
              <h2 class="divider p-2 text-2xl font-bold text-center">Device Name</h2>
              <div class="flex flex-col gap-2">
                <div>
                  <input id="name" type="text" placeholder="New Device name" class="input input-bordered input-md w-full my-1"/>
                  <button class="btn btn-primary w-full" @click="setName()">
                    Send new Device Name
                  </button>
                </div>
              </div>
            </div>
            <!-- Wifi -->
            <div class="flex flex-col gap-4 w-full">
              <h2 class="divider p-2 text-2xl font-bold text-center">Wifi credentials</h2>
              <div class="flex flex-col gap-2">
                <div>
                  <input id="ssid" type="text" placeholder="Network SSID Name" class="input input-bordered input-md w-full my-1"/>
                  <input id="password" type="password" placeholder="Password" class="input input-bordered input-md w-11/12 mb-1"/>
                  <button class="btn btn-info w-1/12 p-2 mb-1" @click="toggleShowPass()">
                    <i v-if="!showPass">
                      <svg class="h-6 w-6 inline-flex " fill="none" xmlns="http://www.w3.org/2000/svg">
                        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                        <g id="SVGRepo_iconCarrier"> 
                          <path d="M12 5C5.63636 5 2 12 2 12C2 12 5.63636 19 12 19C18.3636 19 22 12 22 12C22 12 18.3636 5 12 5Z" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path> 
                          <path d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path> 
                        </g>
                      </svg>
                    </i>
                    <i v-if="showPass">
                      <svg class="h-6 w-6 inline-flex " fill="none" xmlns="http://www.w3.org/2000/svg">
                        <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                        <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                        <g id="SVGRepo_iconCarrier"> 
                          <path d="M20 14.8335C21.3082 13.3317 22 12 22 12C22 12 18.3636 5 12 5C11.6588 5 11.3254 5.02013 11 5.05822C10.6578 5.09828 10.3244 5.15822 10 5.23552M12 9C12.3506 9 12.6872 9.06015 13 9.17071C13.8524 9.47199 14.528 10.1476 14.8293 11C14.9398 11.3128 15 11.6494 15 12M3 3L21 21M12 15C11.6494 15 11.3128 14.9398 11 14.8293C10.1476 14.528 9.47198 13.8524 9.1707 13C9.11386 12.8392 9.07034 12.6721 9.04147 12.5M4.14701 9C3.83877 9.34451 3.56234 9.68241 3.31864 10C2.45286 11.1282 2 12 2 12C2 12 5.63636 19 12 19C12.3412 19 12.6746 18.9799 13 18.9418" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
                        </g>
                      </svg>
                    </i>
                  </button>
                  <button class="btn btn-primary w-full" @click="setWifi()">
                    Send Wifi credentials
                  </button>
                </div>
              </div>
            </div>
            <!-- Mqtt broker -->
            <div class="flex flex-col gap-4 w-full">
              <h2 class="divider p-2 text-2xl font-bold text-center">Mqtt broker</h2>
              <div class="flex flex-col gap-2">
                <div>
                  <input disabled type="text" placeholder="mqtt://" value="mqtt://" class="input input-bordered input-md w-1/4" />
                  <input id="ip" type="text" placeholder="Ip address or hostname" class="input input-bordered input-md w-2/4" />
                  <input id="port" type="text" placeholder="1883" class="input input-bordered input-md w-1/4" />
                </div>
                <button class="btn btn-primary w-full" @click="setMqtt()">
                  send Mqtt ip address
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted } from "vue";

const isSupported = ref(false);
const isConnected = ref(false);
const error = ref();

const device = ref();
const server = ref();
const service = ref();

const ssid_characteristic = ref();
const password_characteristic = ref();
const mqtt_characteristic = ref();
const status_characteristic = ref();
const name_characteristic = ref();

const ipRegex = /^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
const dnsRegex = /^((?!:\/\/)([a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,63})$/;
const showPass = ref(false);

// Check if bluetooth is supported (browser)
const checkSupported = async () => {
  isSupported.value = await navigator.bluetooth.getAvailability();
};

// run the checkSupported function when the page is mounted (created)
onMounted(() => {
  checkSupported();
});

// connect to the device and get the characteristics
const requestDevice = async () => {
  console.log("Requesting device...");
  // Request the device
  device.value = await navigator.bluetooth.requestDevice({
    filters: [{ namePrefix: "UPS" }],
    optionalServices: ["000000ff-0000-1000-8000-00805f9b34fb"],
  });
  // Connect to the device
  server.value = await device.value.gatt.connect();
  // Check if we are connected to the device
  isConnected.value = device.value.gatt.connected;
  if (!isConnected.value) return;
  // Get the service
  service.value = await server.value.getPrimaryService(
    "000000ff-0000-1000-8000-00805f9b34fb"
  );
  // Get the characteristics
  ssid_characteristic.value = await service.value.getCharacteristic(
    "0000ff01-0000-1000-8000-00805f9b34fb"
  );
  password_characteristic.value = await service.value.getCharacteristic(
    "0000ff02-0000-1000-8000-00805f9b34fb"
  );
  mqtt_characteristic.value = await service.value.getCharacteristic(
    "0000ff03-0000-1000-8000-00805f9b34fb"
  );
  name_characteristic.value = await service.value.getCharacteristic(
    "0000ff04-0000-1000-8000-00805f9b34fb"
  );
  status_characteristic.value = await service.value.getCharacteristic(
    "0000ff05-0000-1000-8000-00805f9b34fb"
  );

  await ssid_characteristic.value.readValue();
  await password_characteristic.value.readValue();
  await mqtt_characteristic.value.readValue();
  await name_characteristic.value.readValue();
  // await status_characteristic.value.readValue();
  // Log the data
  logData();
};
const DisconnectDevice = async () => {
  console.log("Button clicked");
  isConnected.value = false;
};

const setName =async () =>{ 
  console.log("setName");
  logData();
  // Check if we are connected to the device
  if (!isConnected.value) return;
  // Get the name from the input field
  const name = document.getElementById("name");
  // Check if the name is valid
  if (!name.value) return;
  await name_characteristic.value.writeValue(
    new TextEncoder().encode(name.value)
  );
  // Log the data
  logData();
};

const toggleShowPass = () => {
  const password = document.getElementById("password");
  if (password.type === "password") {
    showPass.value = true;
    password.type = "text";
  } else {
    showPass.value = false;
    password.type = "password";
  }
};

// Write the ssid and password to the device
const setWifi = async () => {
  console.log("setWifi");
  logData();
  // Check if we are connected to the device
  if (!isConnected.value) return;
  // Get the ssid and password from the input fields
  const ssid = document.getElementById("ssid");
  const password = document.getElementById("password");
  // Check if the ssid and password are valid
  if (!ssid.value || !password.value) return;
  // Write the ssid and password to the characteristics
  await ssid_characteristic.value.writeValue(
    new TextEncoder().encode(ssid.value)
  );
  await password_characteristic.value.writeValue(
    new TextEncoder().encode(password.value)
  );
  logData();
};

// Write the mqtt broker ip to the device
const getIP = async (hostname) => {
  return new Promise((resolve, reject) => {
    const url = `https://dns.google/resolve?name=${hostname}&type=A`;
    fetch(url)
      .then(response => response.json())
      .then(data => {
        if (ipRegex.test(data.Answer[0].data))
        {
          console.log("valid ip "+ data.Answer[0].data);
          resolve(data.Answer[0].data);
        }
        else
        {
          console.log("ip "+ data.Answer[0].data);
          resolve(getIP(data.Answer[0].data));
        }
      });
  });
}

// Write the mqtt broker ip to the device
const setMqtt = async () => {
  console.log("setMqtt");
  logData();
  // Check if we are connected to the device
  if (!isConnected.value) return;
  // Get the ip from the input field
  const ip = document.getElementById("ip");
  const port = document.getElementById("port");
  // Check if the ip is valid
  if (!ip.value) return;
  // Check if port is present else use default port
  if (!port.value) {port.value = "1883";}
  // if ip is ip address keep value
  const ipAddress = ref();
  if (ipRegex.test(ip.value)) 
  {
    ipAddress.value = ip.value;
    console.log("ip "+ ip.value);
  }
  // if ip is dns resolve to ip address
  if (!ipRegex.test(ip.value) && dnsRegex.test(ip.value)) 
  {
    ipAddress.value = await getIP(ip.value)
    console.log("ipd "+ ipAddress.value);
  }
  // if ip is not valid return
  if (!ipAddress.value){ error.value={"name":"Mqtt Broker" , "message":"invalid"};return;}
  error.value=null;
  // Write the ip to the characteristic
  const fullAdress = (ipAddress.value + ":" + port.value);
  console.log("fullAdress "+ fullAdress);
  await mqtt_characteristic.value.writeValue(
    new TextEncoder().encode(fullAdress)
  );
  logData();
};

// Log the data to the console
const logData = async () => {
  console.log("---------------------------------");
  console.log("isSupported:", isSupported.value);
  console.log("isConnected:", isConnected.value);
  console.log("Device:", device.value);
  console.log("Server:", server.value);
  console.log("Service", service.value);
  console.log("ssid_characteristic:", ssid_characteristic.value);
  console.log("password_characteristic:", password_characteristic.value);
  console.log("mqtt_characteristic:", mqtt_characteristic.value);
  console.log("status_characteristic:", status_characteristic.value);
  //console.log('Error:', error.value)
  console.log("---------------------------------");
};
</script>
