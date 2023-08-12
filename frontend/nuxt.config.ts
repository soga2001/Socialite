// https://nuxt.com/docs/api/configuration/nuxt-config

export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    '@element-plus/nuxt',
    '@nuxtjs/axios',
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
      baseURL: process.env.NODE_ENV === 'production' ? '' : 'http://localhost:8000',
    },
  }

  
})

