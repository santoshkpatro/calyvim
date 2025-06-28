<script setup>
import { useAppStore } from '@/stores/app'
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const appStore = useAppStore()
const router = useRouter()

onMounted(async () => {
  const team = appStore.teams[0]
  if (team) {
    router.push({ name: 'home', params: { teamId: team.id } })
  }
})
</script>

<template>
  <div></div>
</template>
