<script setup lang="ts">
import TodayDashboard from '@/components/dashboard/TodayDashboard.vue'
import GardenDialogs from '@/components/forms/GardenDialogs.vue'
import GardenOverview from '@/components/garden/GardenOverview.vue'
import HarvestJournal from '@/components/harvest/HarvestJournal.vue'
import GardenJournal from '@/components/journal/GardenJournal.vue'
import GardenSidebar from '@/components/navigation/GardenSidebar.vue'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { NativeSelect, NativeSelectOption } from '@/components/ui/native-select'
import { Skeleton } from '@/components/ui/skeleton'
import { toast } from 'vue-sonner'
import type {
  Area,
  Dashboard,
  Garden,
  GardenActivity,
  GardenTask,
  Harvest,
  Planting,
} from '~/types'

const { token, user } = useSession()
const { request } = useApi()
const gardens = ref<Garden[]>([])
const selectedGardenId = ref<number | null>(null)
const areas = ref<Area[]>([])
const plantings = ref<Planting[]>([])
const tasks = ref<GardenTask[]>([])
const harvests = ref<Harvest[]>([])
const activities = ref<GardenActivity[]>([])
const dashboard = ref<Dashboard | null>(null)
const activeView = ref<'today' | 'garden' | 'journal' | 'harvests'>('today')
const modal = ref<'garden' | 'area' | 'planting' | 'task' | 'activity' | 'harvest' | null>(null)
const plantingFilter = ref<'all' | 'growing' | 'planned' | 'finished' | 'failed'>('all')
const error = ref('')
const formError = ref('')
const loading = ref(false)
const submitting = ref(false)
const today = new Date().toISOString().slice(0, 10)

const gardenForm = reactive({ name: '', location: '' })
const areaForm = reactive({ name: '', area_type: 'bed', notes: '' })
const plantingForm = reactive({
  growing_area_id: 0, crop: '', variety: '', quantity: 1,
  method: 'direct_sown', planted_on: today, expected_harvest_on: '',
})
const taskForm = reactive({ title: '', due_on: today, planting_id: 0, notes: '' })
const harvestForm = reactive({ planting_id: 0, harvested_on: today, quantity: 1, unit: 'kg', notes: '' })
const activityForm = reactive({
  planting_id: 0,
  event_type: 'watered',
  occurred_on: today,
  notes: '',
})

const selectedGarden = computed(() => gardens.value.find((item) => item.id === selectedGardenId.value))
const openTasks = computed(() => [...tasks.value].sort((a, b) => a.due_on.localeCompare(b.due_on)))
const visiblePlantings = computed(() =>
  plantingFilter.value === 'all'
    ? plantings.value
    : plantings.value.filter((item) => item.status === plantingFilter.value),
)
const areaName = (id: number) => areas.value.find((item) => item.id === id)?.name || 'Unknown area'
const plantingName = (id: number | null) => {
  if (!id) return 'Whole garden'
  const item = plantings.value.find((entry) => entry.id === id)
  return item ? `${item.crop}${item.variety ? ` · ${item.variety}` : ''}` : 'Planting'
}

async function restoreSession() {
  if (!token.value) return
  try {
    user.value = await request('/auth/me')
    await loadGardens()
  } catch {
    token.value = null
    user.value = null
  }
}

async function loadGardens() {
  gardens.value = await request<Garden[]>('/gardens')
  if (!selectedGardenId.value) selectedGardenId.value = gardens.value[0]?.id || null
  if (selectedGardenId.value) await loadGardenData()
}

async function loadGardenData() {
  if (!selectedGardenId.value) return
  loading.value = true
  const base = `/gardens/${selectedGardenId.value}`
  try {
    ;[areas.value, plantings.value, tasks.value, harvests.value, activities.value, dashboard.value] = await Promise.all([
      request<Area[]>(`${base}/areas`),
      request<Planting[]>(`${base}/plantings`),
      request<GardenTask[]>(`${base}/tasks`),
      request<Harvest[]>(`${base}/harvests`),
      request<GardenActivity[]>(`${base}/activities`),
      request<Dashboard>(`${base}/dashboard`),
    ])
    if (!plantingForm.growing_area_id) plantingForm.growing_area_id = areas.value[0]?.id || 0
    const firstPlantingId = plantings.value[0]?.id
    if (firstPlantingId) {
      if (!taskForm.planting_id) taskForm.planting_id = firstPlantingId
      if (!harvestForm.planting_id) harvestForm.planting_id = firstPlantingId
      if (!activityForm.planting_id) activityForm.planting_id = firstPlantingId
    }
  } catch (reason: any) {
    error.value = reason?.data?.detail || 'Could not load your garden.'
  } finally {
    loading.value = false
  }
}

async function createGarden() {
  submitting.value = true
  formError.value = ''
  try {
    await request('/gardens', { method: 'POST', body: gardenForm })
    modal.value = null
    await loadGardens()
    selectedGardenId.value = gardens.value.at(-1)?.id || gardens.value[0]?.id || null
    await loadGardenData()
    toast.success('Garden created')
  } catch (reason: any) {
    formError.value = reason?.data?.detail || 'Could not create the garden.'
  } finally {
    submitting.value = false
  }
}

async function createResource(kind: 'area' | 'planting' | 'task' | 'activity' | 'harvest') {
  if (!selectedGardenId.value) return
  submitting.value = true
  formError.value = ''
  try {
    const forms = { area: areaForm, planting: plantingForm, task: taskForm, activity: activityForm, harvest: harvestForm }
    const paths = { area: 'areas', planting: 'plantings', task: 'tasks', activity: 'activities', harvest: 'harvests' }
    const body: Record<string, unknown> = { ...forms[kind] }
    if (kind === 'planting' && !body.expected_harvest_on) delete body.expected_harvest_on
    if (kind === 'task' && !body.planting_id) body.planting_id = null
    await request(`/gardens/${selectedGardenId.value}/${paths[kind]}`, { method: 'POST', body })
    modal.value = null
    await loadGardenData()
    toast.success(`${kind.charAt(0).toUpperCase() + kind.slice(1)} saved`)
  } catch (reason: any) {
    formError.value = reason?.data?.detail || `Could not save the ${kind}.`
  } finally {
    submitting.value = false
  }
}

async function completeTask(id: number) {
  try {
    await request(`/gardens/${selectedGardenId.value}/tasks/${id}/complete`, { method: 'POST' })
    await loadGardenData()
    toast.success('Task completed')
  } catch {
    toast.error('Could not complete the task')
  }
}

async function changePlantingStatus(planting: Planting, status: string) {
  try {
    await request(`/gardens/${selectedGardenId.value}/plantings/${planting.id}`, {
      method: 'PATCH',
      body: { status },
    })
    await loadGardenData()
    toast.success(`${planting.crop} marked as ${status}`)
  } catch {
    toast.error(`Could not update ${planting.crop}`)
  }
}

function submitDialog(kind: 'garden' | 'area' | 'planting' | 'task' | 'activity' | 'harvest') {
  if (kind === 'garden') return createGarden()
  return createResource(kind)
}

function closeDialog() {
  if (submitting.value) return
  formError.value = ''
  modal.value = null
}

function updatePlantingFilter(value: string) {
  if (['all', 'growing', 'planned', 'finished', 'failed'].includes(value)) {
    plantingFilter.value = value as typeof plantingFilter.value
  }
}

function logout() {
  token.value = null
  user.value = null
  gardens.value = []
}

onMounted(restoreSession)
watch(selectedGardenId, loadGardenData)
</script>

<template>
  <AuthPanel v-if="!user" @authenticated="loadGardens" />

  <div v-else class="app-shell">
    <GardenSidebar
      :active-view="activeView"
      :user-name="user.name"
      @navigate="activeView = $event"
      @logout="logout"
    />

    <main class="workspace">
      <header class="topbar">
        <div>
          <p class="eyebrow">{{ selectedGarden?.location || 'Your growing space' }}</p>
          <NativeSelect v-if="gardens.length" v-model="selectedGardenId" class="garden-picker" aria-label="Selected garden">
            <NativeSelectOption v-for="garden in gardens" :key="garden.id" :value="garden.id">{{ garden.name }}</NativeSelectOption>
          </NativeSelect>
          <h1 v-else>Your first garden</h1>
        </div>
        <Button @click="modal = gardens.length ? 'planting' : 'garden'">
          {{ gardens.length ? '+ Add planting' : '+ Create garden' }}
        </Button>
      </header>

      <Alert v-if="error" variant="destructive" class="mb-4">
        <AlertDescription>{{ error }}</AlertDescription>
      </Alert>
      <div v-if="loading" class="grid gap-4" aria-label="Loading garden">
        <Skeleton class="h-36 rounded-2xl" />
        <div class="grid gap-4 md:grid-cols-2"><Skeleton class="h-72 rounded-2xl" /><Skeleton class="h-72 rounded-2xl" /></div>
      </div>

      <section v-else-if="!gardens.length" class="empty-hero">
        <span class="empty-icon">⌑</span>
        <h2>Give your garden a home</h2>
        <p>Create a garden, then add beds or containers and record what you are growing.</p>
        <Button @click="modal = 'garden'">Create my garden</Button>
      </section>

      <TodayDashboard
        v-else-if="activeView === 'today'"
        :first-name="user.name.split(' ')[0] || user.name"
        :dashboard="dashboard"
        :tasks="openTasks"
        :today="today"
        :planting-name="plantingName"
        :area-name="areaName"
        @add-task="modal = 'task'"
        @complete-task="completeTask"
      />
      <GardenOverview
        v-else-if="activeView === 'garden'"
        :areas="areas"
        :plantings="visiblePlantings"
        :filter="plantingFilter"
        @add-area="modal = 'area'"
        @update-filter="updatePlantingFilter"
        @update-status="changePlantingStatus"
      />
      <GardenJournal
        v-else-if="activeView === 'journal'"
        :activities="activities"
        :can-add="Boolean(plantings.length)"
        :planting-name="plantingName"
        @add="modal = 'activity'"
      />
      <HarvestJournal
        v-else
        :harvests="harvests"
        :can-add="Boolean(plantings.length)"
        :planting-name="plantingName"
        @add="modal = 'harvest'"
      />
    </main>

    <GardenDialogs
      :modal="modal"
      :busy="submitting"
      :form-error="formError"
      :areas="areas"
      :plantings="plantings"
      :garden-form="gardenForm"
      :area-form="areaForm"
      :planting-form="plantingForm"
      :task-form="taskForm"
      :activity-form="activityForm"
      :harvest-form="harvestForm"
      :area-name="areaName"
      @close="closeDialog"
      @submit="submitDialog"
    />
  </div>
</template>
