import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', () => {
  const user = ref(null)

  const setUser = (newUser) => {
    user.value = newUser
  }

  const isLoggedIn = computed(() => !!user.value)
  const clear = () => {
    user.value = null
  }

  return {
    user,
    setUser,
    clear,
    isLoggedIn,
  }
})
