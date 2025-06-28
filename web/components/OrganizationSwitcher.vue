<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ChevronDown, Disc, Plus } from 'lucide-vue-next'
import { useAppStore } from '@/stores/app'
import { message } from 'ant-design-vue'
import { getOrganizationsAPI } from '@/api'

const props = defineProps({
  teamOrganizationId: {
    type: String,
    required: true,
  },
})

const router = useRouter()
const appStore = useAppStore()

const visible = ref(false)

const organizations = ref([])
const loadOrganizations = async () => {
  try {
    const { data } = await getOrganizationsAPI()
    organizations.value = data.result
  } catch (error) {
    console.error('Failed to load organizations:', error)
  }
}

const currentOrganization = computed(() => {
  return organizations.value.find((org) => org.id === props.teamOrganizationId)
})

const createNewOrganization = () => {
  console.log('Open "Create Organization" modal or redirect as needed')
}

onMounted(() => {
  loadOrganizations()
})
</script>

<template>
  <a-dropdown
    v-model:open="visible"
    trigger="click"
    v-if="!!currentOrganization"
    placement="topLeft"
  >
    <a
      class="ant-dropdown-link flex items-center space-x-1 !text-gray-900 hover:!text-black hover:!bg-[#D6D9D1] px-1.5 py-1 rounded-md select-none"
      @click.prevent
    >
      <div class="flex gap-2">
        <span class="text-xs text-gray-500 font-normal leading-tight">Organization: </span>
        <span class="font-semibold truncate">{{ currentOrganization.name }}</span>
      </div>
    </a>

    <template #overlay>
      <div class="w-80 bg-white rounded shadow-md border border-gray-200 p-3 space-y-2" @click.stop>
        <div class="text-xs font-medium text-gray-500 px-1">Your organizations</div>
        <div class="max-h-60 overflow-y-auto space-y-1">
          <div
            v-for="organization in organizations"
            :key="organization.id"
            class="flex items-center justify-between px-2 py-1.5 rounded cursor-pointer hover:bg-[#F3F4EF] text-sm"
          >
            <div class="flex items-center space-x-2">
              <Disc
                v-if="organization.id === currentOrganization?.id"
                class="w-3 h-3 text-violet-600"
              />
              <div v-else class="w-3 h-3"></div>
              <span class="truncate">{{ organization.name }}</span>
            </div>

            <a-tag color="default" class="capitalize m-0">
              {{ organization.memberRole }}
            </a-tag>
          </div>

          <div
            @click="createNewOrganization"
            class="flex items-center space-x-2 text-sm cursor-pointer hover:bg-[#F3F4EF] px-2 py-1.5 rounded transition-colors"
          >
            <Plus class="w-4 h-4" />
            <span>Create New Organization</span>
          </div>
        </div>
      </div>
    </template>
  </a-dropdown>
</template>
