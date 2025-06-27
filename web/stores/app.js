import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', () => {
  const user = ref(null)
  const teams = ref([])
  const selectedTeam = ref(null)

  const setUser = (newUser) => {
    user.value = newUser
  }

  const setTeams = (teamsData) => {
    teams.value = teamsData
  }

  const setSelectedTeam = (team) => {
    selectedTeam.value = team
  }

  const isLoggedIn = computed(() => !!user.value)
  const clear = () => {
    user.value = null
  }

  return {
    user,
    teams,
    setUser,
    setTeams,
    clear,
    isLoggedIn,
    selectedTeam,
    setSelectedTeam,
  }
})
