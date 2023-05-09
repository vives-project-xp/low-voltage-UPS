<template>
    <div class="p-8">
        <h1 class=" p-2 text-4xl font-bold text-center">{{ title }}</h1>
    </div>
</template>

<script>
export default {
  name: 'PageTitle',
  props: {
    title: {
      type: String,
      required: true
    }
  }
}
</script>