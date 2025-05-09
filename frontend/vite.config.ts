import { fileURLToPath, URL } from 'url'

import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import { quasar, transformAssetUrls } from '@quasar/vite-plugin'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({
      template: { transformAssetUrls }
    }),
    quasar({
       sassVariables: fileURLToPath(
        new URL('src/quasar-variables.sass', import.meta.url)
      )
    }),
    tailwindcss(),
    // mkcert(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      'vue': 'vue/dist/vue.esm-bundler',
    },
  },
  build: {
    sourcemap: false,
  },
  server: {
    port: 3000,
  }
})