<template>
  <header class="flex justify-between border-2 primary-color">
    <p>Header</p>
    <nav>
      <ul class="flex gap-4">
        <li><NuxtLink to="/">Home</NuxtLink></li>
        <li><NuxtLink to="/about">About</NuxtLink></li>
        <li><NuxtLink to="/setup">Setup</NuxtLink></li>
        <li><NuxtLink to="/contact">Contact</NuxtLink></li>
        <!-- <ModeSwitch /> -->
      </ul>
    </nav>
  </header>
</template>