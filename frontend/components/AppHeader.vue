<template>
  <header class="flex justify-between border-2">
    <p>Header</p>
    <nav>
      <ul class="flex gap-4">
        <li><button class="btn"><NuxtLink to="/">Home</NuxtLink></button></li>
        <li><button class="btn"><NuxtLink to="/setup">Setup</NuxtLink></button></li>
        <li><button class="btn"><NuxtLink to="/about">About</NuxtLink></button></li>
        <li><button class="btn"><NuxtLink to="/contact">Contact</NuxtLink></button></li>
      </ul>
    </nav>
  </header>
</template>