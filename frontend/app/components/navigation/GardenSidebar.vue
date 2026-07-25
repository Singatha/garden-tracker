<script setup lang="ts">
import { Button } from '@/components/ui/button'

type ViewName = 'today' | 'garden' | 'journal' | 'harvests'

defineProps<{ activeView: ViewName; userName: string }>()
defineEmits<{ navigate: [view: ViewName]; logout: [] }>()

const items: Array<{ value: ViewName; icon: string; label: string }> = [
  { value: 'today', icon: '☀', label: 'Today' },
  { value: 'garden', icon: '⌑', label: 'My garden' },
  { value: 'journal', icon: '≋', label: 'Journal' },
  { value: 'harvests', icon: '♧', label: 'Harvests' },
]
</script>

<template>
  <aside class="sidebar">
    <div class="brand"><span class="brand-mark small">P<span>&</span>S</span><strong>Plot & Sprout</strong></div>
    <nav aria-label="Main navigation">
      <Button
        v-for="item in items"
        :key="item.value"
        variant="ghost"
        :class="{ active: activeView === item.value }"
        :aria-current="activeView === item.value ? 'page' : undefined"
        @click="$emit('navigate', item.value)"
      >
        <span>{{ item.icon }}</span>{{ item.label }}
      </Button>
    </nav>
    <div class="sidebar-bottom">
      <p>{{ userName }}</p>
      <Button variant="link" @click="$emit('logout')">Sign out</Button>
    </div>
  </aside>
</template>
