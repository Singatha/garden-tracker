<script setup lang="ts">
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'

withDefaults(defineProps<{ title: string, description?: string }>(), {
  description: 'Fill in the details below and save when you are ready.',
})
defineEmits<{ close: [] }>()
</script>

<template>
  <Dialog :open="true" @update:open="(open) => !open && $emit('close')">
    <DialogContent class="max-h-[92vh] overflow-y-auto sm:max-w-xl">
      <DialogHeader>
        <DialogTitle>{{ title }}</DialogTitle>
        <DialogDescription>{{ description }}</DialogDescription>
      </DialogHeader>
      <slot />
    </DialogContent>
  </Dialog>
</template>
