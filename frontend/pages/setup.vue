<template>
  <section>
    <PageTitle title="Setup" />
    <!-- Alerts -->
    <div class="flex flex-col items-center gap-2">
      <!-- Error alert -->
      <div v-if="error" class="alert alert-error shadow-lg w-fit max-w-full">
        <div>
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span>{{error.name}}: {{error.message}}</span>
        </div>
      </div>
      <!-- Warning alert -->
      <div v-if="!isSupported"  class="alert alert-warning shadow-lg w-fit">
        <div>
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
          <span>
            <p>Warning: Your browser does not support Bluetooth!</p>
            <p>The only Bluetooth supported browser is Google chrome.</p>
          </span>
        </div>
      </div>
      <!-- Success alert -->
      <div v-if="isConnected" class="alert alert-success shadow-lg w-2/4">
        <div>
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span>Succesfully connected to {{ device.name }}</span>
        </div>
      </div>
    </div>
    <!-- Setup section -->
    <div class="flex flex-col p-4 gap-8 items-center">
      <!-- Bluetooth -->
      <div class="flex flex-col gap-4 w-1/4">
        <h2 class="text-2xl font-bold text-center">1. Bluetooth</h2>
        <div class="flex flex-col gap-2">
          <button v-if="!isConnected" id="BtnConnect" class="btn btn-primary w-full" @click="requestDevice()">
            Connect
          </button>
          <button v-if="isConnected" id="BtnConnect" class="btn btn-primary w-full" @click="DisconnectDevice()">
            DisConnect
          </button>
        </div>
      </div>
      <!-- Wifi -->
      <div class="flex flex-col gap-4 w-1/4">
        <h2 class="text-2xl font-bold text-center">2. Wifi credentials</h2>
        <div class="flex flex-col gap-2">
          <input id="ssid" type="text" placeholder="Network SSID Name" class="input input-bordered input-md w-full" />
          <input id="password" type="password" placeholder="Password" class="input input-bordered input-md w-full" />
          <button 
            class="btn btn-primary w-full"
            @click="setWifi()"
          >
            Send Wifi credentials
          </button>
        </div>
      </div>
      <!-- Mqtt broker -->
      <div class="flex flex-col gap-4 w-1/4">
        <h2 class="text-2xl font-bold text-center">3. Mqtt broker</h2>
        <div class="flex flex-col gap-2">
        <div>
          <input disabled type="text" placeholder="mqtt://" value="mqtt://" class="input input-bordered input-md w-1/4" />
          <input id="ip" type="text" placeholder="Ip address" class="input input-bordered input-md w-2/4" />
          <input id="port" type="text" placeholder="1883" class="input input-bordered input-md w-1/4" />
        </div>
          <button class="btn btn-primary w-full"
            @click="setMqtt()">
            send Mqtt ip address 
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted } from 'vue';

const isSupported = ref(false)
const isConnected = ref(false)
const device = ref()
const server = ref()
const service = ref()
const ssid_characteristic = ref()
const password_characteristic = ref()
const mqtt_characteristic = ref()
const status_characteristic = ref()
const error = ref()

// Check if bluetooth is supported (browser)
const checkSupported = async () => {
  isSupported.value = await navigator.bluetooth.getAvailability()
}

// run the checkSupported function when the page is mounted (created)
onMounted(() => {
  checkSupported()
});

// connect to the device and get the characteristics
const requestDevice = async () => {
  console.log('Button clicked')
  // Request the device
  device.value = await navigator.bluetooth.requestDevice({
    filters: [{ namePrefix: "UPS" }],
    optionalServices: ["000000ff-0000-1000-8000-00805f9b34fb"],
  })
  // Connect to the device
  server.value = await device.value.gatt.connect()
  // Check if we are connected to the device
  isConnected.value = device.value.gatt.connected
  if (!isConnected.value) return
  // Get the service
  service.value = await server.value.getPrimaryService('000000ff-0000-1000-8000-00805f9b34fb')
  // Get the characteristics
  ssid_characteristic.value     = await service.value.getCharacteristic('0000ff01-0000-1000-8000-00805f9b34fb')
  password_characteristic.value = await service.value.getCharacteristic('0000ff02-0000-1000-8000-00805f9b34fb')
  mqtt_characteristic.value     = await service.value.getCharacteristic('0000ff03-0000-1000-8000-00805f9b34fb')
  status_characteristic.value   = await service.value.getCharacteristic('0000ff04-0000-1000-8000-00805f9b34fb')
  
  await ssid_characteristic.value.readValue()
  await password_characteristic.value.readValue()
  await mqtt_characteristic.value.readValue()
  //await status_characteristic.value.readValue()
  // Log the data
  logData()
}
const DisconnectDevice = async () => {
  console.log('Button clicked')
  isConnected.value=false;
}

// Write the ssid and password to the device
const setWifi = async () => {
  console.log("setWifi")
  logData()
  // Check if we are connected to the device
  if (!isConnected.value) return
  // Get the ssid and password from the input fields
  const ssid = document.getElementById('ssid')
  const password = document.getElementById('password')
  // Check if the ssid and password are valid
  if (!ssid.value || !password.value) return
  // Write the ssid and password to the characteristics
  await ssid_characteristic.value.writeValue(new TextEncoder().encode(ssid.value))
  await password_characteristic.value.writeValue(new TextEncoder().encode(password.value))
  logData()
}

// Write the mqtt broker ip to the device
const setMqtt = async () => {
  console.log("setMqtt")
  logData()
  // Check if we are connected to the device
  if (!isConnected.value) return
  // Get the ip from the input field
  const ip = document.getElementById('ip')
  const port = document.getElementById('port')
  // Check if the ip is valid
  if (!ip.value) return
  if (!port.value) port.value="1883"
  // Write the ip to the characteristic
  console.log(ip.value,":",port.value)
  await mqtt_characteristic.value.writeValue(new TextEncoder().encode(ip.value,":",port.value))
  logData()
}

// Log the data to the console
const logData = async () => {
  console.log("---------------------------------")
  console.log('isSupported:', isSupported.value)
  console.log('isConnected:', isConnected.value)
  console.log('Device:', device.value)
  console.log('Server:', server.value)
  console.log('Service', service.value)
  console.log('ssid_characteristic:', ssid_characteristic.value)
  console.log('password_characteristic:', password_characteristic.value)
  console.log('mqtt_characteristic:', mqtt_characteristic.value)
  console.log('status_characteristic:', status_characteristic.value)
  //console.log('Error:', error.value)
  console.log("---------------------------------")
}
</script>