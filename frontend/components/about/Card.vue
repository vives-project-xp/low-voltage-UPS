<template>
  <div class="bg-base-200 flex flex-col">
    <img :src="avatar" alt="avatar" class="m-8 mask mask-squircle">
    <h3 class="text-2xl text-center">{{ name }}</h3>
    <p class="p-8 text-center">{{ job }}</p>
  </div>
</template>

<script setup>
  const { name, avatar, bio } = defineProps({
    name: {
      type: String,
      required: true
    },
    avatar: {
      type: String,
      required: true
    },
    job: {
      type: String,
      required: true
    }
  })
</script>