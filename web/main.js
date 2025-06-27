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
  const data = await checkAuthStatus()
  if (data) {
    appStore.setUser(data.user)
    appStore.setTeams(data.teams)
  } else {
    appStore.clear()
  }

  app.use(router)
  app.mount('#app')
}

// app.use(router)

// app.mount('#app')

init()
