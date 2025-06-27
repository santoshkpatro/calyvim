<script setup>
import { Bug } from 'lucide-vue-next'
import { useRoute } from 'vue-router'
import { onMounted } from 'vue'

const route = useRoute()

const emit = defineEmits(['update-breadcrumps'])

onMounted(() => {
  emit('update-breadcrumps', [{ name: 'Issues', route: route.path, icon: Bug }])
  emit('activate-tab', 'Issues')
})
</script>

<template>
  <div>Issues</div>
</template>
