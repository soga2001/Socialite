// https://nuxt.com/docs/api/configuration/nuxt-config

export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    '@element-plus/nuxt',
  ],
  elementPlus: {
  },
  components: [
    {
      path: '~/components',
      extensions: ['.vue'],
    }
  ],
  runtimeConfig: {
    axios: {
      baseURL: 'http://localhost:8000',
    },
  }

  
})

