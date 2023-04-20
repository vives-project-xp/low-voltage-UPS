<template>
    <div class="tertiary-color p-12">
        <h1 class="text-4xl font-bold text-center">{{ title }}</h1>
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