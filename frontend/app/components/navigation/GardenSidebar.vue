<script setup lang="ts">
import {
  BookOpenIcon,
  CalendarDaysIcon,
  LayoutDashboardIcon,
  SettingsIcon,
  SproutIcon,
} from '@lucide/vue'

type ViewName = 'today' | 'garden' | 'journal' | 'harvests' | 'settings'

defineProps<{ activeView: ViewName; userName: string }>()

const items = [
  { value: 'today', icon: LayoutDashboardIcon, label: 'Today' },
  { value: 'garden', icon: SproutIcon, label: 'My garden' },
  { value: 'journal', icon: BookOpenIcon, label: 'Journal' },
  { value: 'harvests', icon: CalendarDaysIcon, label: 'Harvests' },
  { value: 'settings', icon: SettingsIcon, label: 'Settings' },
]
</script>

<template>
  <aside class="sidebar">
    <NuxtLink to="/today" class="brand" aria-label="Gardenwise home">
      <strong>Gardenwise</strong>
    </NuxtLink>
    <nav aria-label="Main navigation">
      <NuxtLink
        v-for="item in items"
        :key="item.value"
        :to="`/${item.value}`"
        :class="{ active: activeView === item.value }"
        :aria-current="activeView === item.value ? 'page' : undefined"
      >
        <component :is="item.icon" aria-hidden="true" />{{ item.label }}
      </NuxtLink>
    </nav>
    <NuxtLink
      to="/settings"
      class="profile-link"
      :class="{ active: activeView === 'settings' }"
      :aria-current="activeView === 'settings' ? 'page' : undefined"
    >
      <span class="profile-avatar">{{ userName.slice(0, 1).toUpperCase() }}</span>
      <span><strong>{{ userName }}</strong><small>Profile settings</small></span>
      <SettingsIcon aria-hidden="true" />
    </NuxtLink>
  </aside>
</template>
