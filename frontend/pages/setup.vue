<template>
  <section>
    <h1 class="text-2xl font-bold p-4 text-center">Setup</h1>
    <!-- Alerts -->
    <div class="flex flex-col items-center gap-2">
      <!-- Error alert 
      <div v-if="error" class="alert alert-error shadow-lg w-fit max-w-full">
        <div>
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span>{{error.name}}: {{error.message}}</span>
        </div>
      </div>
      -->
      <!-- Warning alert -->
      <div v-if="!isSupported"  class="alert alert-warning shadow-lg w-fit">
        <div>
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
          <span>Warning: Your browser does not support Bluetooth!</span>
        </div>
      </div>
      <!-- Success alert -->
      <div v-if="isConnected" class="alert alert-success shadow-lg w-96">
        <div>
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span>Succesfully connected to {{ device.name }}</span>
        </div>
      </div>
    </div>
    <!-- Setup section -->
    <div class="flex flex-col p-4 gap-8 items-center">
      <!-- Bluetooth -->
      <div class="flex flex-col gap-4 w-72">
        <h2 class="text-2xl font-bold text-center">1. Bluetooth</h2>
        <div class="flex flex-col gap-2">
          <button 
            class="btn btn-primary w-full" 
            @click="requestDevice()"
          >
            Connect
          </button>
        </div>
      </div>
      <!-- Wifi -->
      <div class="flex flex-col gap-4 w-72">
        <h2 class="text-2xl font-bold text-center">2. Wifi credentials</h2>
        <div class="flex flex-col gap-2">
          <input id="ssid" type="text" placeholder="Network Name" class="input input-bordered input-md w-full" />
          <input id="password" type="password" placeholder="Password" class="input input-bordered input-md w-full" />
          <button 
            class="btn btn-primary w-full"
            @click="setWifi()"
          >
            Update
          </button>
        </div>
      </div>
      <!-- Mqtt broker -->
      <div class="flex flex-col gap-4 w-72">
        <h2 class="text-2xl font-bold text-center">3. Mqtt broker</h2>
        <div class="flex flex-col gap-2">
          <input id="ip" type="text" placeholder="Ip address" class="input input-bordered input-md w-full" />
          <button 
            class="btn btn-primary w-full"
            @click="setMqtt()"
          >
            Update
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>

let device
let server
let service
let characteristic
let isSupported
let isConnected

const requestDevice = async () => {
  console.log('Button clicked')
  // Check if bluetooth is supported
  isSupported = await navigator.bluetooth.getAvailability()
  if (!isSupported) return
  // Request the device
  device = await navigator.bluetooth.requestDevice({
    filters: [{ namePrefix: "UPS" }],
    optionalServices: ["000000ff-0000-1000-8000-00805f9b34fb"],
  })
  // Connect to the device
  server = await device.gatt.connect()
  // Check if we are connected to the device
  isConnected = device.gatt.connected
  if (!isConnected) return
  // Get the service
  service = await server.getPrimaryService('000000ff-0000-1000-8000-00805f9b34fb')
  // Get the characteristic
  characteristic = await service.getCharacteristic('0000ff01-0000-1000-8000-00805f9b34fb')
  // Log the data
  logData()
}

const setWifi = async () => {
  logData()
  // Check if we are connected to the device
  if (!isConnected) return
  // Get the ssid and password from the input fields
  const ssid = document.getElementById('ssid')
  const password = document.getElementById('password')
  // Check if the ssid and password are valid
  if (!ssid.value || !password.value) return
  // Write the ssid and password to the characteristic
  await characteristic.writeValue(new TextEncoder().encode(`ssid:${ssid.value},password:${password.value}`))
  logData()
}

const setMqtt = async () => {
  logData()
  // Check if we are connected to the device
  if (!isConnected) return
  // Get the ip address from the input field
  const ip = document.getElementById('ip')
  // Check if the ip address is valid
  if (!ip.value) return
  // Write the ip address to the characteristic
  await characteristic.writeValue(new TextEncoder().encode(`ip:${ip.value}`))
  logData()
}

const logData = () => {
  console.log("---------------------------------")
  console.log('Is supported:', isSupported.value)
  console.log('Is connected:', isConnected.value)
  console.log('Device:', device)
  console.log('Server:', server)
  console.log('Service', service)
  console.log('Characteristic', characteristic)
  //console.log('Error:', error.value)
  console.log("---------------------------------")
}


</script>