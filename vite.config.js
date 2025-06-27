import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools()],
  root: '',
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./web', import.meta.url)),
    },
  },
  server: {
    port: 3000,
  },
  build: {
    assetsDir: 'static',
  },
})
