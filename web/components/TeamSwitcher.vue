<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ChevronDown, Disc, Plus } from 'lucide-vue-next'
import { useAppStore } from '@/stores/app'
import { message } from 'ant-design-vue'

const props = defineProps({
  teamId: {
    type: String,
    required: true,
  },
})

const router = useRouter()
const appStore = useAppStore()

const visible = ref(false)
const teamSearch = ref('')

const currentTeam = computed(() => appStore.teams.find((t) => t.id === props.teamId))

const filteredTeams = computed(() => {
  const search = teamSearch.value.toLowerCase()

  const all = appStore.teams
  const current = all.find((t) => t.id === props.teamId)
  const matches = all.filter((t) => t.name.toLowerCase().includes(search) && t.id !== props.teamId)

  // If current team exists and matches search or not — keep it first
  return current ? [current, ...matches] : matches
})

function selectTeam(team) {
  if (team.id !== props.teamId) {
    router.push({ name: 'home', params: { teamId: team.id } })
  }
  visible.value = false
}

function createNewTeam() {
  visible.value = false
  message.info('Open "Create Team" modal or redirect as needed')
  // You can emit, open modal, or route to a team creation page here
}
</script>

<template>
  <a-dropdown v-model:open="visible" trigger="click">
    <!-- Trigger -->
    <a
      class="ant-dropdown-link flex items-center space-x-1 !text-gray-900 hover:!text-black hover:!bg-[#D6D9D1] px-1.5 py-1 rounded-md transition-colors"
      @click.prevent
    >
      <span class="font-semibold truncate">{{ currentTeam?.name }}</span>
      <ChevronDown class="w-4 h-4" />
    </a>

    <!-- Overlay -->
    <template #overlay>
      <div class="w-80 bg-white rounded shadow-md border border-gray-200 p-3 space-y-2" @click.stop>
        <!-- Search -->
        <a-input
          v-model:value="teamSearch"
          placeholder="Search teams..."
          allow-clear
          class="w-full"
          @click.stop
        />

        <!-- Label -->
        <div class="text-xs font-medium text-gray-500 px-1">Teams</div>

        <!-- Team list -->
        <div class="max-h-60 overflow-y-auto space-y-1">
          <div
            v-for="team in filteredTeams"
            :key="team.id"
            @click="selectTeam(team)"
            class="flex items-center justify-between px-2 py-1.5 rounded cursor-pointer hover:bg-[#F3F4EF] text-sm"
          >
            <!-- Left: Icon + name -->
            <div class="flex items-center space-x-2">
              <Disc v-if="team.id === currentTeam?.id" class="w-3 h-3 text-violet-600" />
              <div v-else class="w-3 h-3"></div>
              <span class="truncate">{{ team.name }}</span>
            </div>

            <!-- Right: Role tag -->
            <a-tag color="default" class="capitalize m-0">
              {{ team.memberRole }}
            </a-tag>
          </div>
          <div
            @click="createNewTeam"
            class="flex items-center space-x-2 text-sm cursor-pointer hover:bg-[#F3F4EF] px-2 py-1.5 rounded transition-colors"
          >
            <Plus class="w-4 h-4" />
            <span>Create New Team</span>
          </div>
        </div>
      </div>
    </template>
  </a-dropdown>
</template>
