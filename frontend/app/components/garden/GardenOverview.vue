<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { NativeSelect, NativeSelectOption } from '@/components/ui/native-select'
import type { Area, Planting } from '~/types'

defineProps<{
  areas: Area[]
  plantings: Planting[]
  filter: string
}>()

defineEmits<{
  addArea: []
  updateFilter: [value: string]
  updateStatus: [planting: Planting, status: string]
}>()
</script>

<template>
  <section class="section-heading">
    <div><p class="eyebrow">What’s growing</p><h2>My garden</h2></div>
    <div class="heading-actions">
      <NativeSelect :model-value="filter" aria-label="Filter plantings by status" @change="$emit('updateFilter', ($event.target as HTMLSelectElement).value)">
        <NativeSelectOption value="all">All plantings</NativeSelectOption>
        <NativeSelectOption value="growing">Growing</NativeSelectOption>
        <NativeSelectOption value="planned">Planned</NativeSelectOption>
        <NativeSelectOption value="finished">Finished</NativeSelectOption>
        <NativeSelectOption value="failed">Failed</NativeSelectOption>
      </NativeSelect>
      <Button variant="secondary" @click="$emit('addArea')">+ Add area</Button>
    </div>
  </section>

  <div v-if="!areas.length" class="empty-hero compact">
    <h2>Start with a growing area</h2><p>Add a bed, container, row, or greenhouse section.</p>
    <Button @click="$emit('addArea')">Add an area</Button>
  </div>
  <div class="area-grid">
    <Card v-for="area in areas" :key="area.id" class="area-card">
      <CardHeader>
        <span class="area-type">{{ area.area_type }}</span>
        <CardTitle>{{ area.name }}</CardTitle>
      </CardHeader>
      <CardContent class="planting-list">
        <article v-for="planting in plantings.filter((item) => item.growing_area_id === area.id)" :key="planting.id">
          <span class="crop-avatar">{{ planting.crop.slice(0, 1) }}</span>
          <div><strong>{{ planting.crop }}</strong><p>{{ planting.variety || planting.method.replace('_', ' ') }} · {{ planting.quantity }}</p></div>
          <NativeSelect
            class="status-select"
            :model-value="planting.status"
            :aria-label="`Status for ${planting.crop}`"
            @change="$emit('updateStatus', planting, ($event.target as HTMLSelectElement).value)"
          >
            <NativeSelectOption v-for="status in ['planned','growing','harvested','finished','failed']" :key="status" :value="status">{{ status }}</NativeSelectOption>
          </NativeSelect>
        </article>
        <p v-if="!plantings.some((item) => item.growing_area_id === area.id)" class="muted">No matching plantings.</p>
      </CardContent>
    </Card>
  </div>
</template>
