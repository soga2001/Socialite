import { fileURLToPath, URL } from 'url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { quasar, transformAssetUrls } from '@quasar/vite-plugin'
// import mkcert from 'vite-plugin-mkcert'

// https://vitejs.dev/config/



// https://vitejs.dev/config/
export default defineConfig({
  // server: { https: true },
  plugins: [
    vue({
      template: { transformAssetUrls }
    }),
    quasar({
      sassVariables: 'src/quasar-variables.sass'
    }),
    // mkcert(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      'vue': 'vue/dist/vue.esm-bundler',
    },
  },
  css: {
    preprocessorOptions: {
      // scss: {
      //   additionalData: `@import 'src/quasar-variables.scss';`, // Add the import statement here
      // },
    },
  },
  build: {
    sourcemap: false,
  },
})