<script setup lang="ts">
defineProps<{ title: string }>()
defineEmits<{ close: [] }>()
</script>

<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <section class="modal" role="dialog" aria-modal="true" :aria-label="title">
      <header>
        <h2>{{ title }}</h2>
        <button class="icon-button" aria-label="Close" @click="$emit('close')">×</button>
      </header>
      <slot />
    </section>
  </div>
</template>

