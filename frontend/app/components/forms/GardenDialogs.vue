<script setup lang="ts">
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  NativeSelect,
  NativeSelectOption,
} from '@/components/ui/native-select'
import { Textarea } from '@/components/ui/textarea'
import type { Area, Planting } from '~/types'

type ModalKind = 'garden' | 'area' | 'planting' | 'task' | 'activity' | 'harvest' | null

defineProps<{
  modal: ModalKind
  busy: boolean
  formError: string
  areas: Area[]
  plantings: Planting[]
  gardenForm: { name: string; location: string }
  areaForm: { name: string; area_type: string; notes: string }
  plantingForm: {
    growing_area_id: number
    crop: string
    variety: string
    quantity: number
    method: string
    planted_on: string
    expected_harvest_on: string
  }
  taskForm: { title: string; due_on: string; planting_id: number; notes: string }
  activityForm: { planting_id: number; event_type: string; occurred_on: string; notes: string }
  harvestForm: { planting_id: number; harvested_on: string; quantity: number; unit: string; notes: string }
  areaName: (id: number) => string
}>()

defineEmits<{
  close: []
  submit: [kind: Exclude<ModalKind, null>]
}>()
</script>

<template>
  <ModalForm v-if="modal === 'garden'" title="Create a garden" @close="$emit('close')">
    <form @submit.prevent="$emit('submit', 'garden')">
      <div class="grid gap-2"><Label for="garden-name">Garden name</Label><Input id="garden-name" v-model="gardenForm.name" required placeholder="Home garden" /></div>
      <div class="grid gap-2"><Label for="garden-location">Location</Label><Input id="garden-location" v-model="gardenForm.location" placeholder="Backyard" /></div>
      <Alert v-if="formError" variant="destructive"><AlertDescription>{{ formError }}</AlertDescription></Alert>
      <Button class="w-full" :disabled="busy">{{ busy ? 'Creating…' : 'Create garden' }}</Button>
    </form>
  </ModalForm>

  <ModalForm v-if="modal === 'area'" title="Add a growing area" @close="$emit('close')">
    <form @submit.prevent="$emit('submit', 'area')">
      <div class="grid gap-2"><Label for="area-name">Name</Label><Input id="area-name" v-model="areaForm.name" required placeholder="Sunny raised bed" /></div>
      <div class="grid gap-2">
        <Label for="area-type">Type</Label>
        <NativeSelect id="area-type" v-model="areaForm.area_type">
          <NativeSelectOption v-for="type in ['bed','container','row','greenhouse','other']" :key="type" :value="type">{{ type }}</NativeSelectOption>
        </NativeSelect>
      </div>
      <div class="grid gap-2"><Label for="area-notes">Notes</Label><Textarea id="area-notes" v-model="areaForm.notes" placeholder="Morning sun, drip irrigation…" /></div>
      <Alert v-if="formError" variant="destructive"><AlertDescription>{{ formError }}</AlertDescription></Alert>
      <Button class="w-full" :disabled="busy">{{ busy ? 'Adding…' : 'Add area' }}</Button>
    </form>
  </ModalForm>

  <ModalForm v-if="modal === 'planting'" title="Add a planting" @close="$emit('close')">
    <form @submit.prevent="$emit('submit', 'planting')">
      <div class="grid gap-2">
        <Label for="planting-area">Growing area</Label>
        <NativeSelect id="planting-area" v-model="plantingForm.growing_area_id" required>
          <NativeSelectOption :value="0" disabled>Select an area</NativeSelectOption>
          <NativeSelectOption v-for="area in areas" :key="area.id" :value="area.id">{{ area.name }}</NativeSelectOption>
        </NativeSelect>
      </div>
      <div class="form-row">
        <div class="grid gap-2"><Label for="planting-crop">Crop</Label><Input id="planting-crop" v-model="plantingForm.crop" required placeholder="Tomato" /></div>
        <div class="grid gap-2"><Label for="planting-variety">Variety</Label><Input id="planting-variety" v-model="plantingForm.variety" placeholder="Roma" /></div>
      </div>
      <div class="form-row">
        <div class="grid gap-2"><Label for="planting-quantity">Quantity</Label><Input id="planting-quantity" v-model.number="plantingForm.quantity" type="number" min="1" /></div>
        <div class="grid gap-2"><Label for="planting-method">Method</Label><NativeSelect id="planting-method" v-model="plantingForm.method"><NativeSelectOption value="direct_sown">Direct sown</NativeSelectOption><NativeSelectOption value="transplanted">Transplanted</NativeSelectOption><NativeSelectOption value="existing">Existing plant</NativeSelectOption></NativeSelect></div>
      </div>
      <div class="form-row">
        <div class="grid gap-2"><Label for="planted-on">Planted on</Label><Input id="planted-on" v-model="plantingForm.planted_on" type="date" required /></div>
        <div class="grid gap-2"><Label for="harvest-on">Expected harvest</Label><Input id="harvest-on" v-model="plantingForm.expected_harvest_on" type="date" /></div>
      </div>
      <Alert v-if="!areas.length || formError" variant="destructive"><AlertDescription>{{ formError || 'Add a growing area before adding a planting.' }}</AlertDescription></Alert>
      <Button class="w-full" :disabled="busy || !areas.length">{{ busy ? 'Adding…' : 'Add planting' }}</Button>
    </form>
  </ModalForm>

  <ModalForm v-if="modal === 'task'" title="Add a garden task" @close="$emit('close')">
    <form @submit.prevent="$emit('submit', 'task')">
      <div class="grid gap-2"><Label for="task-title">Task</Label><Input id="task-title" v-model="taskForm.title" required placeholder="Water the tomatoes" /></div>
      <div class="form-row">
        <div class="grid gap-2"><Label for="task-date">Due date</Label><Input id="task-date" v-model="taskForm.due_on" type="date" required /></div>
        <div class="grid gap-2"><Label for="task-planting">Planting</Label><NativeSelect id="task-planting" v-model="taskForm.planting_id"><NativeSelectOption :value="0">Whole garden</NativeSelectOption><NativeSelectOption v-for="planting in plantings" :key="planting.id" :value="planting.id">{{ planting.crop }} · {{ areaName(planting.growing_area_id) }}</NativeSelectOption></NativeSelect></div>
      </div>
      <div class="grid gap-2"><Label for="task-notes">Notes</Label><Textarea id="task-notes" v-model="taskForm.notes" /></div>
      <Alert v-if="formError" variant="destructive"><AlertDescription>{{ formError }}</AlertDescription></Alert>
      <Button class="w-full" :disabled="busy">{{ busy ? 'Adding…' : 'Add task' }}</Button>
    </form>
  </ModalForm>

  <ModalForm v-if="modal === 'activity'" title="Log garden activity" @close="$emit('close')">
    <form @submit.prevent="$emit('submit', 'activity')">
      <div class="grid gap-2"><Label for="activity-planting">Planting</Label><NativeSelect id="activity-planting" v-model="activityForm.planting_id" required><NativeSelectOption v-for="planting in plantings" :key="planting.id" :value="planting.id">{{ planting.crop }} · {{ areaName(planting.growing_area_id) }}</NativeSelectOption></NativeSelect></div>
      <div class="form-row">
        <div class="grid gap-2"><Label for="activity-type">Activity</Label><NativeSelect id="activity-type" v-model="activityForm.event_type"><NativeSelectOption value="watered">Watered</NativeSelectOption><NativeSelectOption value="fertilized">Fertilized</NativeSelectOption><NativeSelectOption value="pruned">Pruned</NativeSelectOption><NativeSelectOption value="transplanted">Transplanted</NativeSelectOption><NativeSelectOption value="pest_observed">Pest observed</NativeSelectOption><NativeSelectOption value="disease_observed">Disease observed</NativeSelectOption><NativeSelectOption value="note">General note</NativeSelectOption><NativeSelectOption value="removed">Removed</NativeSelectOption></NativeSelect></div>
        <div class="grid gap-2"><Label for="activity-date">Date</Label><Input id="activity-date" v-model="activityForm.occurred_on" type="date" required /></div>
      </div>
      <div class="grid gap-2"><Label for="activity-notes">Notes</Label><Textarea id="activity-notes" v-model="activityForm.notes" placeholder="What did you notice?" /></div>
      <Alert v-if="formError" variant="destructive"><AlertDescription>{{ formError }}</AlertDescription></Alert>
      <Button class="w-full" :disabled="busy">{{ busy ? 'Saving…' : 'Save to journal' }}</Button>
    </form>
  </ModalForm>

  <ModalForm v-if="modal === 'harvest'" title="Record a harvest" @close="$emit('close')">
    <form @submit.prevent="$emit('submit', 'harvest')">
      <div class="grid gap-2"><Label for="harvest-planting">Planting</Label><NativeSelect id="harvest-planting" v-model="harvestForm.planting_id" required><NativeSelectOption v-for="planting in plantings" :key="planting.id" :value="planting.id">{{ planting.crop }} · {{ areaName(planting.growing_area_id) }}</NativeSelectOption></NativeSelect></div>
      <div class="form-row">
        <div class="grid gap-2"><Label for="harvest-amount">Amount</Label><Input id="harvest-amount" v-model.number="harvestForm.quantity" type="number" min="0.01" step="0.01" required /></div>
        <div class="grid gap-2"><Label for="harvest-unit">Unit</Label><NativeSelect id="harvest-unit" v-model="harvestForm.unit"><NativeSelectOption v-for="unit in ['kg','g','items','bunches','cups']" :key="unit" :value="unit">{{ unit }}</NativeSelectOption></NativeSelect></div>
      </div>
      <div class="grid gap-2"><Label for="harvest-date">Harvested on</Label><Input id="harvest-date" v-model="harvestForm.harvested_on" type="date" required /></div>
      <div class="grid gap-2"><Label for="harvest-notes">Notes</Label><Textarea id="harvest-notes" v-model="harvestForm.notes" /></div>
      <Alert v-if="formError" variant="destructive"><AlertDescription>{{ formError }}</AlertDescription></Alert>
      <Button class="w-full" :disabled="busy">{{ busy ? 'Saving…' : 'Save harvest' }}</Button>
    </form>
  </ModalForm>
</template>
