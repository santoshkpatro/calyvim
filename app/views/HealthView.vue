<script setup></script>

<template>
  <div class="flex items-center justify-center h-screen bg-green-400">
    <div>
      <h1 class="text-2xl font-bold mb-4">Health Check</h1>
      <p class="text-lg">The application is running smoothly!</p>
      <p class="text-sm text-gray-500">Last checked: {{ new Date().toLocaleTimeString() }}</p>
    </div>
  </div>
</template>
