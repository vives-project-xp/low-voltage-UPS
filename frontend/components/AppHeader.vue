<template>
  <header class="flex justify-between border-2 border-black dark:border-pink-500 dark:bg-black dark:text-white">
    <p>Header</p>
    <nav>
      <ul class="flex gap-4">
        <li><NuxtLink to="/">Home</NuxtLink></li>
        <li><NuxtLink to="/setup">Setup</NuxtLink></li>
        <li><NuxtLink to="/about">About</NuxtLink></li>
        <li><NuxtLink to="/contact">Contact</NuxtLink></li>
      </ul>
    </nav>
  </header>
</template>