<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import type { Harvest } from '~/types'

defineProps<{
  harvests: Harvest[]
  canAdd: boolean
  plantingName: (id: number | null) => string
}>()

defineEmits<{ add: [] }>()
</script>

<template>
  <section class="section-heading">
    <div><p class="eyebrow">What the garden gave</p><h2>Harvest journal</h2></div>
    <Button :disabled="!canAdd" @click="$emit('add')">+ Record harvest</Button>
  </section>
  <Card class="panel">
    <CardContent>
      <div v-if="!harvests.length" class="empty-small tall">
        <span>♧</span><h3>Your harvest story starts here</h3>
        <p>Record the first thing you pick from the garden.</p>
      </div>
      <article v-for="harvest in harvests" :key="harvest.id" class="harvest-row">
        <span class="crop-avatar">{{ plantingName(harvest.planting_id).slice(0, 1) }}</span>
        <div><strong>{{ plantingName(harvest.planting_id) }}</strong><p>{{ harvest.harvested_on }}</p></div>
        <strong>{{ harvest.quantity }} {{ harvest.unit }}</strong>
      </article>
    </CardContent>
  </Card>
</template>
