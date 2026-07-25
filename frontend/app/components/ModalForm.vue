<script setup lang="ts">
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'

defineProps<{ title: string }>()
defineEmits<{ close: [] }>()
</script>

<template>
  <Dialog :open="true" @update:open="(open) => !open && $emit('close')">
    <DialogContent class="max-h-[92vh] overflow-y-auto sm:max-w-xl">
      <DialogHeader>
        <DialogTitle>{{ title }}</DialogTitle>
        <DialogDescription>
          Add the details below. Required fields are marked by the browser.
        </DialogDescription>
      </DialogHeader>
      <slot />
    </DialogContent>
  </Dialog>
</template>
