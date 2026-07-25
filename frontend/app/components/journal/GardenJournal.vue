<script setup lang="ts">
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import type { GardenActivity } from '~/types'

defineProps<{
  activities: GardenActivity[]
  canAdd: boolean
  plantingName: (id: number | null) => string
}>()

defineEmits<{ add: [] }>()
</script>

<template>
  <section class="section-heading">
    <div><p class="eyebrow">A history you can learn from</p><h2>Garden journal</h2></div>
    <Button :disabled="!canAdd" @click="$emit('add')">+ Log activity</Button>
  </section>
  <Card class="panel">
    <CardContent>
      <div v-if="!activities.length" class="empty-small tall">
        <span>≋</span><h3>No garden notes yet</h3>
        <p>Log watering, feeding, pruning, pests, and observations.</p>
      </div>
      <article v-for="activity in activities" :key="activity.id" class="journal-row">
        <time>{{ activity.occurred_on }}</time>
        <span class="journal-dot" />
        <div>
          <Badge variant="secondary">{{ activity.event_type.replaceAll('_', ' ') }}</Badge>
          <p>{{ plantingName(activity.planting_id) }}</p>
          <p v-if="activity.notes" class="journal-note">{{ activity.notes }}</p>
        </div>
      </article>
    </CardContent>
  </Card>
</template>
