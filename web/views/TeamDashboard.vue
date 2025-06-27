<script setup>
import {
  LayoutDashboard,
  Bug,
  AlarmClock,
  Bell,
  Settings,
  Activity,
  Users,
  Folder,
} from 'lucide-vue-next'
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="flex min-h-screen bg-gray-50">
    <!-- Sidebar -->
    <aside
      class="w-16 sm:w-20 lg:w-64 bg-white border-r border-gray-200 flex flex-col items-center lg:items-start py-4 px-2 space-y-4 transition-all"
    >
      <!-- Logo -->
      <div class="flex items-center space-x-2">
        <LayoutDashboard class="w-6 h-6 text-violet-600" />
        <span class="hidden lg:inline text-xl font-semibold text-violet-600">Calyvim</span>
      </div>

      <!-- Menu -->
      <nav class="flex flex-col w-full mt-6 space-y-2">
        <div
          class="flex items-center space-x-3 hover:bg-gray-100 px-3 py-2 rounded-md cursor-pointer group"
        >
          <LayoutDashboard class="w-5 h-5 text-gray-600 group-hover:text-violet-600" />
          <span class="hidden lg:inline text-sm text-gray-800 group-hover:text-violet-600"
            >Home</span
          >
        </div>

        <div
          class="flex items-center space-x-3 hover:bg-gray-100 px-3 py-2 rounded-md cursor-pointer group"
        >
          <Bug class="w-5 h-5 text-gray-600 group-hover:text-violet-600" />
          <span class="hidden lg:inline text-sm text-gray-800 group-hover:text-violet-600"
            >Issues</span
          >
        </div>

        <div
          class="flex items-center space-x-3 hover:bg-gray-100 px-3 py-2 rounded-md cursor-pointer group"
        >
          <AlarmClock class="w-5 h-5 text-gray-600 group-hover:text-violet-600" />
          <span class="hidden lg:inline text-sm text-gray-800 group-hover:text-violet-600"
            >Sprints</span
          >
        </div>

        <div
          class="flex items-center space-x-3 hover:bg-gray-100 px-3 py-2 rounded-md cursor-pointer group"
        >
          <Bell class="w-5 h-5 text-gray-600 group-hover:text-violet-600" />
          <span class="hidden lg:inline text-sm text-gray-800 group-hover:text-violet-600"
            >Notifications</span
          >
        </div>

        <div
          class="flex items-center space-x-3 hover:bg-gray-100 px-3 py-2 rounded-md cursor-pointer group"
        >
          <Settings class="w-5 h-5 text-gray-600 group-hover:text-violet-600" />
          <span class="hidden lg:inline text-sm text-gray-800 group-hover:text-violet-600"
            >Settings</span
          >
        </div>

        <div
          class="flex items-center space-x-3 hover:bg-gray-100 px-3 py-2 rounded-md cursor-pointer group"
        >
          <Activity class="w-5 h-5 text-gray-600 group-hover:text-violet-600" />
          <span class="hidden lg:inline text-sm text-gray-800 group-hover:text-violet-600"
            >Timeline</span
          >
        </div>

        <div
          class="flex items-center space-x-3 hover:bg-gray-100 px-3 py-2 rounded-md cursor-pointer group"
        >
          <Users class="w-5 h-5 text-gray-600 group-hover:text-violet-600" />
          <span class="hidden lg:inline text-sm text-gray-800 group-hover:text-violet-600"
            >Team</span
          >
        </div>

        <div
          class="flex items-center space-x-3 hover:bg-gray-100 px-3 py-2 rounded-md cursor-pointer group"
        >
          <Folder class="w-5 h-5 text-gray-600 group-hover:text-violet-600" />
          <span class="hidden lg:inline text-sm text-gray-800 group-hover:text-violet-600"
            >Projects</span
          >
        </div>
      </nav>
    </aside>

    <!-- Main content -->
    <div class="flex-1 p-6">
      <!-- Placeholder content -->
      <h1 class="text-2xl font-bold">
        <router-view></router-view>
      </h1>
    </div>
  </div>
</template>
