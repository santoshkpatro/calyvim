<script setup>
import {
  LayoutDashboard,
  Bug,
  Timer,
  FolderKanban,
  CalendarDays,
  BookOpenText,
  BarChartBig,
  Target,
  Users,
  Settings,
  Star,
  LifeBuoy,
  FileText,
  User,
  Bell,
  Search,
} from 'lucide-vue-next'

import { RouterView, useRoute, RouterLink } from 'vue-router'
import { useAppStore } from '@/stores/app'
import TeamSwitcher from '@/components/TeamSwitcher.vue'

const route = useRoute()
const appStore = useAppStore()

const menuItems = [
  { name: 'Home', icon: LayoutDashboard, color: 'text-violet-600', routePath: '' },
  { name: 'Issues', icon: Bug, color: 'text-red-600', routePath: 'issues' },
  { name: 'Sprints', icon: Timer, color: 'text-orange-500', routePath: 'sprints' },
  { name: 'Projects', icon: FolderKanban, color: 'text-yellow-600', routePath: 'projects' },
  { name: 'Calendar', icon: CalendarDays, color: 'text-green-600', routePath: 'calendar' },
  { name: 'Wikis', icon: BookOpenText, color: 'text-cyan-600', routePath: 'wikis' },
  { name: 'Insights', icon: BarChartBig, color: 'text-emerald-600', routePath: 'insights' },
  { name: 'Goals', icon: Target, color: 'text-blue-600', routePath: 'goals' },
  { name: 'Team Members', icon: Users, color: 'text-rose-500', routePath: 'team-members' },
  { name: 'Settings', icon: Settings, color: 'text-gray-700', routePath: 'settings' },
]
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
          <TeamSwitcher :teamId="route.params.teamId" />
        </div>

        <!-- Menu -->
        <nav class="flex flex-col mt-2 space-y-2">
          <template v-for="item in menuItems" :key="item.name">
            <RouterLink
              :to="`/team/${route.params.teamId}/${item.routePath}`"
              class="flex items-center space-x-2 px-2 py-1 rounded-md cursor-pointer hover:bg-[#D8DBD3] no-underline"
            >
              <component :is="item.icon" class="w-4 h-4" :class="item.color" />
              <span class="hidden lg:inline text-sm text-gray-900">{{ item.name }}</span>
            </RouterLink>
          </template>
        </nav>
      </div>

      <!-- Bottom Section -->
      <div class="flex flex-col space-y-2 mt-4">
        <div
          class="flex items-center space-x-2 px-2 py-1 rounded-md cursor-pointer hover:bg-[#D8DBD3]"
        >
          <Star class="w-4 h-4 text-yellow-500" />
          <span class="hidden lg:inline text-sm text-gray-900">Star us on GitHub</span>
        </div>

        <div
          class="flex items-center space-x-2 px-2 py-1 rounded-md cursor-pointer hover:bg-[#D8DBD3]"
        >
          <LifeBuoy class="w-4 h-4 text-sky-600" />
          <span class="hidden lg:inline text-sm text-gray-900">Help & Support</span>
        </div>

        <div
          class="flex items-center space-x-2 px-2 py-1 rounded-md cursor-pointer hover:bg-[#D8DBD3]"
        >
          <FileText class="w-4 h-4 text-indigo-600" />
          <span class="hidden lg:inline text-sm text-gray-900">Docs</span>
        </div>

        <!-- Profile -->
        <div class="flex items-center gap-2 px-2 py-1 mt-2">
          <User class="w-5 h-5 text-gray-800" />
          <!-- <img src="/dummy-avatar.png" class="w-6 h-6 rounded-full" /> -->
          <span class="hidden lg:inline text-sm font-medium text-gray-900">Santosh</span>
        </div>
      </div>
    </aside>

    <!-- Main Content Area with Top Bar -->
    <div class="flex-1 flex flex-col">
      <!-- Top Bar -->
      <div
        class="flex items-center justify-between bg-[#E4E7DF] px-6 py-3 border-b border-gray-300"
      >
        <!-- Breadcrumb / Title -->
        <div class="text-sm text-gray-700 font-medium">
          Dashboard / <span class="text-gray-900">Current Page</span>
        </div>

        <!-- Right Controls -->
        <div class="flex items-center space-x-4">
          <!-- Search -->
          <div class="cursor-pointer p-2 rounded hover:bg-[#D8DBD3]">
            <Search class="w-5 h-5 text-gray-700" />
          </div>

          <!-- Notifications -->
          <div class="cursor-pointer p-2 rounded hover:bg-[#D8DBD3]">
            <Bell class="w-5 h-5 text-gray-700" />
          </div>

          <!-- CalyAI Button -->
          <a-button>Caly AI</a-button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="flex-1 px-6 py-5 bg-[#F3F4EF]">
        <RouterView />
      </div>
    </div>
  </div>
</template>
