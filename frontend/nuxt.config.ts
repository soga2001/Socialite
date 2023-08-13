// https://nuxt.com/docs/api/configuration/nuxt-config

export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    '@element-plus/nuxt',
    '@pinia/nuxt',
    'nuxt-quasar-ui',
  ],
  elementPlus: {
    icon: 'ElIcon',
    importStyle: 'scss',
    themes: ['dark'],
  },
  quasar: {
    plugins: [
      'BottomSheet',
      'Dialog',
      'Loading',
      'LoadingBar',
      'Notify',
      'Dark',
    ],
  extras: {
      font: 'roboto-font',
    },
    components: {
      defaults: {
        QBtn: {
          unelevated: true,
        },
      },
    },
  },
  components: [
    {
      path: '~/components',
      extensions: ['.vue'],
    }, {
      path: '~/components/~/',
      extensions: ['.vue'],
    }
  ],
  runtimeConfig: {
    axios: {
      baseURL: 'http://localhost:8000',
    },
  },
  pinia: {
    autoImports: [
      'defineStore',
    ],
  },
  imports: {
    dirs: ['store', 'assets', 'composables']
  },
  css: [
    '~/assets/css/base.css',
    '~/assets/css/global.css',
  ],
  plugins: [
    // '~/plugins/userStorePlugin',
  ]
  

  
})

