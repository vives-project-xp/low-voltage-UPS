<template>
    <div>
      <Switch @click="toggleTheme">
        <span
          class="pointer-events-none inline-block transform ring-0 transition duration-200 ease-in-out">
          <MoonIcon v-if="enabled" class="h-[28px] w-[28px] fill-gray-300" />
          <SunIcon v-else class="h-[28px] w-[28px] fill-yellow-500" />
        </span>
      </Switch>
    </div>
  </template>
  
  <script setup lang="ts">
  import { Switch } from "@headlessui/vue"
  import { SunIcon, MoonIcon } from "@heroicons/vue/24/solid"
  
  const { enabled, toggleTheme } = useTheme() 
  </script>