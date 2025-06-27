<script setup>
import { ref, h } from 'vue'
import { MailOutlined, LockOutlined } from '@ant-design/icons-vue'
import { loginAPI } from '@/api'

const email = ref('')
const password = ref('')
const onLogin = async () => {
  try {
    const { data } = await loginAPI({
      email: email.value,
      password: password.value,
    })
    window.location.href = '/'
  } catch (error) {
    console.error('Login failed:', error)
  }
}
</script>

<template>
  <div class="flex min-h-screen bg-white">
    <!-- Left Illustration Block -->
    <div class="w-1/2 flex flex-col justify-center items-center px-12">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">Welcome to Calyvim</h1>
      <p class="text-gray-500 text-center max-w-sm">
        Plan tasks. Track projects. Align your operations. Built for fast-moving teams.
      </p>
    </div>

    <!-- Right Login Form -->
    <div class="w-1/2 flex justify-center items-center">
      <a-card class="w-full max-w-sm border border-gray-200 rounded-xl shadow-sm">
        <template #title>
          <div class="text-center text-xl font-semibold text-gray-800">
            Log in to your workspace
          </div>
        </template>

        <a-form layout="vertical" @submit.prevent="onLogin">
          <a-form-item label="Email">
            <a-input
              v-model:value="email"
              placeholder="you@calyvim.com"
              :prefix="h(MailOutlined)"
            />
          </a-form-item>

          <a-form-item label="Password">
            <a-input-password
              v-model:value="password"
              placeholder="••••••••"
              :prefix="h(LockOutlined)"
            />
          </a-form-item>

          <a-button type="primary" block class="mt-2" @click="onLogin"> Log in </a-button>
        </a-form>

        <div class="text-center text-sm mt-4">
          Don’t have an account?
          <a href="#" class="text-indigo-600 hover:underline">Create one</a>
        </div>
      </a-card>
    </div>
  </div>
</template>
