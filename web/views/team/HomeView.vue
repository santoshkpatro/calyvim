<script setup>
import { Bug, LayoutDashboard } from 'lucide-vue-next'
import { useRoute } from 'vue-router'
import { onMounted } from 'vue'

const route = useRoute()

const emit = defineEmits(['update-breadcrumps'])

onMounted(() => {
  emit('update-breadcrumps', [{ name: 'Home', route: route.path, icon: LayoutDashboard }])
})
</script>

<template>
  <div>Home</div>
</template>
