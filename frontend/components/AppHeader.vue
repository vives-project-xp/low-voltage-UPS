<template>
  <header class="flex justify-between border-2 border-purple-500">
    <p class="text-purple-500">Header</p>
    <nav>
      <ul class="flex gap-4 text-purple-500">
        <li><NuxtLink to="/">Home</NuxtLink></li>
        <li><NuxtLink to="/setup">Setup</NuxtLink></li>
        <li><NuxtLink to="/about">About</NuxtLink></li>
        <li><NuxtLink to="/contact">Contact</NuxtLink></li>
      </ul>
    </nav>
  </header>
</template>