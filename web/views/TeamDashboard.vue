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
  User,
} from 'lucide-vue-next'

import { RouterView, useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'
import TeamSwitcher from '@/components/TeamSwitcher.vue'

const route = useRoute()
const appStore = useAppStore()
</script>

<template>
  <div class="flex min-h-screen bg-[#F3F4EF]">
    <!-- Sidebar -->
    <aside
      class="w-16 sm:w-20 lg:w-64 bg-[#E4E7DF] flex flex-col justify-between py-3 px-1.5 lg:px-3 transition-all"
    >
      <div>
        <!-- Team Info -->
        <div class="mt-2 flex items-center space-x-2 px-2 py-1 rounded-md text-sm text-gray-900">
          <team-switcher :teamId="route.params.teamId"></team-switcher>
        </div>

        <!-- Menu -->
        <nav class="flex flex-col mt-2 space-y-2">
          <div
            class="flex items-center space-x-2 px-2 py-1 rounded-md cursor-pointer hover:bg-[#D8DBD3]"
          >
            <LayoutDashboard class="w-4 h-4 text-gray-700" />
            <span class="hidden lg:inline text-sm text-gray-900">Home</span>
          </div>

          <div
            class="flex items-center space-x-2 px-2 py-1 rounded-md cursor-pointer hover:bg-[#D8DBD3]"
          >
            <Bug class="w-4 h-4 text-gray-700" />
            <span class="hidden lg:inline text-sm text-gray-900">Issues</span>
          </div>

          <div
            class="flex items-center space-x-2 px-2 py-1 rounded-md cursor-pointer hover:bg-[#D8DBD3]"
          >
            <AlarmClock class="w-4 h-4 text-gray-700" />
            <span class="hidden lg:inline text-sm text-gray-900">Sprints</span>
          </div>

          <div
            class="flex items-center space-x-2 px-2 py-1 rounded-md cursor-pointer hover:bg-[#D8DBD3]"
          >
            <Bell class="w-4 h-4 text-gray-700" />
            <span class="hidden lg:inline text-sm text-gray-900">Notifications</span>
          </div>

          <div
            class="flex items-center space-x-2 px-2 py-1 rounded-md cursor-pointer hover:bg-[#D8DBD3]"
          >
            <Settings class="w-4 h-4 text-gray-700" />
            <span class="hidden lg:inline text-sm text-gray-900">Settings</span>
          </div>

          <div
            class="flex items-center space-x-2 px-2 py-1 rounded-md cursor-pointer hover:bg-[#D8DBD3]"
          >
            <Activity class="w-4 h-4 text-gray-700" />
            <span class="hidden lg:inline text-sm text-gray-900">Timeline</span>
          </div>

          <div
            class="flex items-center space-x-2 px-2 py-1 rounded-md cursor-pointer hover:bg-[#D8DBD3]"
          >
            <Users class="w-4 h-4 text-gray-700" />
            <span class="hidden lg:inline text-sm text-gray-900">Team</span>
          </div>

          <div
            class="flex items-center space-x-2 px-2 py-1 rounded-md cursor-pointer hover:bg-[#D8DBD3]"
          >
            <Folder class="w-4 h-4 text-gray-700" />
            <span class="hidden lg:inline text-sm text-gray-900">Projects</span>
          </div>
        </nav>
      </div>

      <!-- Static User Info -->
      <div class="flex items-center space-x-2 px-2 py-1 rounded-md text-sm text-gray-900">
        <User class="w-4 h-4 text-gray-800" />
        <span class="hidden lg:inline">Santosh</span>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 px-6 py-5 bg-[#F3F4EF]">
      <RouterView />
    </div>
  </div>
</template>
