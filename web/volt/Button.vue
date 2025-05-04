<template>
  <Button
    unstyled
    :pt="theme"
    :ptOptions="{
      mergeProps: ptViewMerge,
    }"
  >
    <template v-for="(_, slotName) in $slots" v-slot:[slotName]="slotProps">
      <slot :name="slotName" v-bind="slotProps ?? {}" />
    </template>
  </Button>
</template>

<script setup lang="ts">
import Button, { type ButtonPassThroughOptions, type ButtonProps } from 'primevue/button'
import { computed } from 'vue'
import { ptViewMerge } from './utils'

interface Props extends /* @vue-ignore */ ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
})

const theme = computed<ButtonPassThroughOptions>(() => {
  switch (props.variant) {
    case 'secondary':
      return {
        root: `
          inline-flex items-center justify-center
          px-1.5 py-0.5 text-sm font-medium rounded-sm
          bg-surface-100 text-surface-900 border border-surface-300
          hover:bg-surface-200 active:bg-surface-300
          disabled:opacity-50 disabled:pointer-events-none
          transition-colors duration-150
          focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-surface-400
        `,
        label: `text-sm`,
        loadingIcon: `animate-spin`,
        pcBadge: {
          root: `min-w-4 h-4 leading-4 bg-white text-surface-700 text-[10px] font-bold rounded-full`,
        },
      }

    case 'danger':
      return {
        root: `
          inline-flex items-center justify-center
          px-1.5 py-0.5 text-sm font-medium rounded-sm
          bg-red-600 text-white border border-red-600
          hover:bg-red-700 active:bg-red-800
          disabled:opacity-50 disabled:pointer-events-none
          transition-colors duration-150
          focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-500
        `,
        label: `text-sm`,
        loadingIcon: `animate-spin`,
        pcBadge: {
          root: `min-w-4 h-4 leading-4 bg-white text-red-700 text-[10px] font-bold rounded-full`,
        },
      }

    default: // primary
      return {
        root: `
          inline-flex items-center justify-center
          px-1.5 py-0.5 text-sm font-medium rounded-sm
          bg-primary text-white border border-primary
          hover:bg-primary-600 active:bg-primary-700
          disabled:opacity-50 disabled:pointer-events-none
          transition-colors duration-150
          focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-500
        `,
        label: `text-sm`,
        loadingIcon: `animate-spin`,
        pcBadge: {
          root: `min-w-4 h-4 leading-4 bg-white text-primary text-[10px] font-bold rounded-full`,
        },
      }
  }
})
</script>
