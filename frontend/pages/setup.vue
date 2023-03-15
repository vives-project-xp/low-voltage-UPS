<template>
  <section>
    <h1 class="text-2xl font-bold p-4 text-center">Setup</h1>
    <div class="flex flex-col p-4 gap-8 items-center">
      <div class="flex flex-col gap-4 w-72">
        <h2 class="text-2xl font-bold text-center">1. Bluetooth</h2>
        <div class="flex flex-col gap-2">
          <button class="btn btn-primary w-full">Connect</button>
        </div>
      </div>
      <div class="flex flex-col gap-4 w-72">
        <h2 class="text-2xl font-bold text-center">2. Wifi credentials</h2>
        <div class="flex flex-col gap-2">
          <input id="ssid" type="text" placeholder="Network Name" class="input input-bordered input-md w-full" />
          <input type="password" placeholder="Password" class="input input-bordered input-md w-full" />
          <button class="btn btn-primary w-full">Update</button>
        </div>
      </div>
      <div class="flex flex-col gap-4 w-72">
        <h2 class="text-2xl font-bold text-center">3. Mqtt broker</h2>
        <div class="flex flex-col gap-2">
          <input id="ip" type="text" placeholder="Ip address" class="input input-bordered input-md w-full" />
          <button class="btn btn-primary w-full">Update</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>

</script>