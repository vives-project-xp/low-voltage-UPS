// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: ['@nuxtjs/tailwindcss','@nuxtjs/color-mode','nuxt-icons'],
  css: ['~/assets/css/main.css'],
  colorMode: {    preference: 'system', // default value of $colorMode.preference    
  fallback: 'dark', // fallback value if not system preference found    
  hid: 'nuxt-color-mode-script',
  globalName: '__NUXT_COLOR_MODE__',    
  componentName: 'ColorScheme',    
  classPrefix: '',    
  classSuffix: '-mode',    
  storageKey: 'nuxt-color-mode',
  },
})
