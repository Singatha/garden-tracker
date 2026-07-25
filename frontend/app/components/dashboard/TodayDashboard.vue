<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import type { Dashboard, GardenTask, Planting } from '~/types'

defineProps<{
  firstName: string
  dashboard: Dashboard | null
  tasks: GardenTask[]
  today: string
  plantingName: (id: number | null) => string
  areaName: (id: number) => string
}>()

defineEmits<{
  addTask: []
  completeTask: [id: number]
}>()
</script>

<template>
  <section class="welcome">
    <div>
      <p class="eyebrow">Today in the garden</p>
      <h2>Good to see you, {{ firstName }}.</h2>
      <p>Here’s what deserves your attention today.</p>
    </div>
    <div class="stat">
      <strong>{{ dashboard?.active_plantings || 0 }}</strong>
      <span>active plantings</span>
    </div>
  </section>

  <div class="dashboard-grid">
    <Card class="panel task-panel">
      <CardHeader class="flex-row items-center justify-between border-b">
        <div><p class="eyebrow">Care list</p><CardTitle>Tasks</CardTitle></div>
        <Button size="icon" variant="secondary" aria-label="Add task" @click="$emit('addTask')">+</Button>
      </CardHeader>
      <CardContent>
        <div v-if="!tasks.length" class="empty-small"><span>✓</span><p>Nothing due. Enjoy the garden.</p></div>
        <article v-for="task in tasks" :key="task.id" class="task-row">
          <Button size="icon-sm" variant="outline" :aria-label="`Complete ${task.title}`" @click="$emit('completeTask', task.id)">✓</Button>
          <div><strong>{{ task.title }}</strong><p>{{ plantingName(task.planting_id) }}</p></div>
          <time :class="{ overdue: task.due_on < today }">{{ task.due_on === today ? 'Today' : task.due_on }}</time>
        </article>
      </CardContent>
    </Card>

    <Card class="panel">
      <CardHeader class="border-b"><p class="eyebrow">Coming along</p><CardTitle>Upcoming harvests</CardTitle></CardHeader>
      <CardContent>
        <div v-if="!dashboard?.upcoming_harvests.length" class="empty-small"><span>♧</span><p>Add expected harvest dates to see what’s next.</p></div>
        <article v-for="planting in dashboard?.upcoming_harvests" :key="planting.id" class="harvest-row">
          <span class="crop-avatar">{{ planting.crop.slice(0, 1) }}</span>
          <div><strong>{{ planting.crop }}</strong><p>{{ planting.variety || areaName(planting.growing_area_id) }}</p></div>
          <time>{{ planting.expected_harvest_on }}</time>
        </article>
      </CardContent>
    </Card>
  </div>
</template>
