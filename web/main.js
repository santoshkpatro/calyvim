import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { checkAuthStatus } from '@/utils/auth'
import { useAppStore } from '@/stores/app'

import App from './App.vue'
import router from './router'

async function init() {
  const app = createApp(App)
  app.use(createPinia())

  const appStore = useAppStore()
  const user = await checkAuthStatus()
  if (user) {
    appStore.setUser(user)
  } else {
    appStore.clear()
  }

  app.use(router)
  app.mount('#app')
}

// app.use(router)

// app.mount('#app')

init()
