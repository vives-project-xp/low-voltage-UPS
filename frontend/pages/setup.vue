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

<script>
export default {
  data: () => ({
    isSupported: false,
    isConnected: false,
    device: null,
    server: null,
    service: null,
    ssid_characteristic: null,
    password_characteristic: null,
    mqtt_characteristic: null,
    error: null,
  }),
  methods: {
    // Check if bluetooth is supported (browser)
    async checkSupported() {
      this.isSupported = await navigator.bluetooth.getAvailability()
    },

    // connect to the device and get the characteristics
    async requestDevice() {
      console.log('Button clicked')
      // Request the device
      this.device = await navigator.bluetooth.requestDevice({
        filters: [{ namePrefix: "UPS" }],
        optionalServices: ["000000ff-0000-1000-8000-00805f9b34fb"],
      })
      // Connect to the device
      this.server = await this.device.gatt.connect()
      // Check if we are connected to the device
      this.isConnected = this.device.gatt.connected
      if (!this.isConnected) return
      // Get the service
      this.service = await this.server.getPrimaryService('000000ff-0000-1000-8000-00805f9b34fb')
      // Get the characteristics
      this.ssid_characteristics = await this.service.getCharacteristic('0000ff01-0000-1000-8000-00805f9b34fb')
      this.password_characteristic = await this.service.getCharacteristic('0000ff02-0000-1000-8000-00805f9b34fb')
      this.mqtt_characteristic = await this.service.getCharacteristic('0000ff03-0000-1000-8000-00805f9b34fb')
      this.status_characteristic = await this.service.getCharacteristic('0000ff04-0000-1000-8000-00805f9b34fb')
      // Log the data
      this.logData()
    },

    // Write the ssid and password to the device
    async setWifi(){
      this.logData()
      // Check if we are connected to the device
      if (!this.isConnected) return
      // Get the ssid and password from the input fields
      const ssid = document.getElementById('ssid')
      const password = document.getElementById('password')
      // Check if the ssid and password are valid
      if (!ssid.value || !password.value) return
      // Write the ssid and password to the characteristics
      await this.status_characteristic.writeValue(new TextEncoder().encode(ssid.value))
      await this.password_characteristic.writeValue(new TextEncoder().encode(password.value))
      this.logData()
    },

    // Write the mqtt broker ip address to the device
    async setMqtt(){
      this.logData()
      // Check if we are connected to the device
      if (!this.isConnected) return
      // Get the ip address from the input field
      const ip = document.getElementById('ip')
      // Check if the ip address is valid
      if (!ip.value) return
      // Write the ip address to the characteristic
      await this.mqtt_characteristic.writeValue(new TextEncoder().encode(ip.value))
      this.logData()
    },

    // Log the data to the console
    async logData() {
      console.log("---------------------------------")
      console.log('isSupported:', this.isSupported)
      console.log('isConnected:', this.isConnected)
      console.log('Device:', this.device)
      console.log('Server:', this.server)
      console.log('Service', this.service)
      console.log('ssid_characteristic:', this.ssid_characteristic)
      console.log('password_characteristic:', this.password_characteristic)
      console.log('mqtt_characteristic:', this.mqtt_characteristic)
      console.log('status_characteristic:', this.status_characteristic)
      //console.log('Error:', error.value)
      console.log("---------------------------------")
    }
  },
  // run the checkSupported function when the page is mounted (created)
  beforeMount() {
    this.checkSupported()
  },
}
</script>