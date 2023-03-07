// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // modules: ['@nuxtjs/color-mode'],
  css: ['~/assets/css/main.css'],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
})
