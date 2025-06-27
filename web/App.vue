<script setup>
import { RouterView } from 'vue-router'

const theme = {
  token: {
    colorPrimary: '#1f1f1f',

    // UI Feel
    borderRadius: 4,
    fontFamily: 'Inter, sans-serif',
  },
}
</script>

<template>
  <a-config-provider :theme="theme">
    <router-view />
  </a-config-provider>
</template>

<style scoped></style>
