<script setup>
import {
  LayoutDashboard,
  Timer,
  FolderKanban,
  BookOpenText,
  BarChartBig,
  Target,
  Users,
  Settings,
  FileText,
  LifeBuoy,
  Star,
  Bug,
  Activity,
  CalendarDays,
  Layers,
  ArrowRight,
  ChevronRight,
} from 'lucide-vue-next'

import { ref, computed } from 'vue'
import { RouterView, useRoute, RouterLink } from 'vue-router'
import { useAppStore } from '@/stores/app'
import TeamSwitcher from '@/components/TeamSwitcher.vue'

const route = useRoute()
const appStore = useAppStore()

const currentTeam = computed(() => appStore.teams.find((t) => t.id === route.params.teamId))

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

const rightSidebarItems = [
  {
    name: 'Docs',
    icon: FileText,
    href: 'https://calyvim.com/docs',
    external: true,
  },
  {
    name: 'Help',
    icon: LifeBuoy,
    href: 'https://calyvim.com/docs',
    external: true,
  },
  {
    name: 'Bug',
    icon: Bug,
    href: 'https://github.com/santoshkpatro/calyvim/issues',
    external: true,
  },
  {
    name: 'Star',
    icon: Star,
    href: 'https://github.com/santoshkpatro/calyvim',
    external: true,
  },
  {
    name: 'Status',
    icon: Activity,
    href: 'https://status.calyvim.com',
    external: true,
  },
]

const breadcrumps = ref([
  {
    icon: Layers,
    name: currentTeam.value.name,
    route: `/team/${route.params.teamId}/`,
  },
])

const updateBreadcrumps = (crumps) => {
  // TODO; Always have deafultBreadcrump as first item
  breadcrumps.value = [
    {
      icon: Layers,
      name: currentTeam.value.name,
      route: `/team/${route.params.teamId}/`,
    },
    ...crumps,
  ]
}
</script>

<template>
  <div class="flex h-screen bg-[#F3F4EF] overflow-hidden">
    <!-- Left Sidebar -->
    <aside
      class="w-16 sm:w-20 lg:w-64 bg-[#E4E7DF] flex flex-col justify-between py-3 px-2 lg:px-4 border-r border-gray-300"
    >
      <div>
        <!-- Team Switcher (no extra top margin) -->
        <div class="px-2 py-1 text-sm text-gray-900 font-semibold cursor-pointer">
          <TeamSwitcher :teamId="route.params.teamId" />
        </div>

        <!-- Menu -->
        <nav class="flex flex-col mt-2 space-y-2">
          <template v-for="item in menuItems" :key="item.name">
            <RouterLink
              :to="`/team/${route.params.teamId}/${item.routePath}`"
              class="flex items-center space-x-2 px-2 py-1 rounded-md cursor-pointer hover:bg-[#D8DBD3] no-underline"
            >
              <component :is="item.icon" class="w-4 h-4 text-gray-700" />
              <span class="hidden lg:inline text-sm text-gray-900">{{ item.name }}</span>
            </RouterLink>
          </template>
        </nav>
      </div>

      <!-- Organization Info -->
      <div class="px-2 py-1 mt-4 text-xs text-gray-800 border-t border-gray-300 pt-3">
        Organization: Acme Inc.
      </div>
    </aside>

    <!-- Center Content Area -->
    <div class="flex-1 flex flex-col overflow-hidden border-r border-gray-300">
      <!-- Top Bar -->
      <div
        class="flex items-center justify-between bg-[#E4E7DF] px-6 py-3 border-b border-gray-300"
      >
        <!-- Breadcrumb -->
        <div class="flex items-center space-x-2 text-sm text-gray-700 font-medium">
          <div
            class="flex items-center space-x-1"
            v-for="(crumb, index) in breadcrumps"
            :key="index"
          >
            <component :is="crumb.icon" class="w-4 h-4 text-gray-500" />
            <RouterLink :to="crumb.route" class="hover:underline text-gray-800 no-underline">
              {{ crumb.name }}
            </RouterLink>
            <ChevronRight v-if="index < breadcrumps.length - 1" class="w-4 h-4" />
          </div>
        </div>

        <!-- Search and Profile -->
        <div class="flex items-center space-x-4">
          <a-input-search placeholder="Search" class="!w-48 !rounded !bg-[#E4E7DF]" allow-clear />

          <div class="flex items-center space-x-2">
            <div
              class="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center text-gray-800 font-semibold"
            >
              S
            </div>
            <div
              class="hidden lg:block leading-tight text-xs text-right"
              v-if="appStore.isLoggedIn"
            >
              <div class="text-gray-900 font-medium">{{ appStore.user.displayName }}</div>
              <div class="text-gray-600">{{ appStore.user.email }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Scrollable Content -->
      <div class="flex-1 overflow-auto px-6 py-5 bg-[#F3F4EF]">
        <RouterView @update-breadcrumps="updateBreadcrumps" />
      </div>
    </div>

    <!-- Right Mini Sidebar -->
    <aside class="w-12 bg-[#E4E7DF] border-l border-gray-300 flex flex-col items-center py-4">
      <div class="flex flex-col items-center space-y-8 flex-1 justify-center">
        <template v-for="item in rightSidebarItems" :key="item.name">
          <a
            :href="item.href"
            :target="item.external ? '_blank' : '_self'"
            :rel="item.external ? 'noopener noreferrer' : ''"
            class="group flex flex-col items-center cursor-pointer hover:bg-[#D8DBD3] p-2 rounded-md transition-colors duration-200 no-underline"
            :title="item.name"
          >
            <!-- Rotated Icon -->
            <component
              :is="item.icon"
              class="w-4 h-4 text-gray-600 group-hover:text-gray-800 mb-2 transform rotate-90"
            />

            <!-- Rotated Text -->
            <span
              class="text-xs text-gray-600 group-hover:text-gray-800 font-medium tracking-wider"
              style="writing-mode: vertical-rl; text-orientation: mixed"
            >
              {{ item.name }}
            </span>
          </a>
        </template>
      </div>
    </aside>
  </div>
</template>
