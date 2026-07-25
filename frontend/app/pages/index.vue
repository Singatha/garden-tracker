<script setup lang="ts">
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
const loading = ref(false)
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
  await request('/gardens', { method: 'POST', body: gardenForm })
  modal.value = null
  await loadGardens()
  selectedGardenId.value = gardens.value.at(-1)?.id || gardens.value[0]?.id || null
  await loadGardenData()
}

async function createResource(kind: 'area' | 'planting' | 'task' | 'activity' | 'harvest') {
  if (!selectedGardenId.value) return
  const forms = { area: areaForm, planting: plantingForm, task: taskForm, activity: activityForm, harvest: harvestForm }
  const paths = { area: 'areas', planting: 'plantings', task: 'tasks', activity: 'activities', harvest: 'harvests' }
  const body: Record<string, unknown> = { ...forms[kind] }
  if (kind === 'planting' && !body.expected_harvest_on) delete body.expected_harvest_on
  if (kind === 'task' && !body.planting_id) body.planting_id = null
  await request(`/gardens/${selectedGardenId.value}/${paths[kind]}`, { method: 'POST', body })
  modal.value = null
  await loadGardenData()
}

async function completeTask(id: number) {
  await request(`/gardens/${selectedGardenId.value}/tasks/${id}/complete`, { method: 'POST' })
  await loadGardenData()
}

async function changePlantingStatus(planting: Planting, status: string) {
  await request(`/gardens/${selectedGardenId.value}/plantings/${planting.id}`, {
    method: 'PATCH',
    body: { status },
  })
  await loadGardenData()
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
    <aside class="sidebar">
      <div class="brand"><span class="brand-mark small">P<span>&</span>S</span><strong>Plot & Sprout</strong></div>
      <nav aria-label="Main navigation">
        <button :class="{ active: activeView === 'today' }" @click="activeView = 'today'"><span>☀</span> Today</button>
        <button :class="{ active: activeView === 'garden' }" @click="activeView = 'garden'"><span>⌑</span> My garden</button>
        <button :class="{ active: activeView === 'journal' }" @click="activeView = 'journal'"><span>≋</span> Journal</button>
        <button :class="{ active: activeView === 'harvests' }" @click="activeView = 'harvests'"><span>♧</span> Harvests</button>
      </nav>
      <div class="sidebar-bottom">
        <p>{{ user.name }}</p>
        <button class="text-button" @click="logout">Sign out</button>
      </div>
    </aside>

    <main class="workspace">
      <header class="topbar">
        <div>
          <p class="eyebrow">{{ selectedGarden?.location || 'Your growing space' }}</p>
          <select v-if="gardens.length" v-model="selectedGardenId" aria-label="Selected garden">
            <option v-for="garden in gardens" :key="garden.id" :value="garden.id">{{ garden.name }}</option>
          </select>
          <h1 v-else>Your first garden</h1>
        </div>
        <button class="button primary" @click="modal = gardens.length ? 'planting' : 'garden'">
          {{ gardens.length ? '+ Add planting' : '+ Create garden' }}
        </button>
      </header>

      <p v-if="error" class="error">{{ error }}</p>
      <div v-if="loading" class="loading">Tending your records…</div>

      <section v-else-if="!gardens.length" class="empty-hero">
        <span class="empty-icon">⌑</span>
        <h2>Give your garden a home</h2>
        <p>Create a garden, then add beds or containers and record what you are growing.</p>
        <button class="button primary" @click="modal = 'garden'">Create my garden</button>
      </section>

      <template v-else-if="activeView === 'today'">
        <section class="welcome">
          <div>
            <p class="eyebrow">Saturday in the garden</p>
            <h2>Good to see you, {{ user.name.split(' ')[0] }}.</h2>
            <p>Here’s what deserves your attention today.</p>
          </div>
          <div class="stat">
            <strong>{{ dashboard?.active_plantings || 0 }}</strong>
            <span>active plantings</span>
          </div>
        </section>

        <div class="dashboard-grid">
          <section class="panel task-panel">
            <header><div><p class="eyebrow">Care list</p><h3>Tasks</h3></div><button class="icon-button add" @click="modal = 'task'">+</button></header>
            <div v-if="!openTasks.length" class="empty-small"><span>✓</span><p>Nothing due. Enjoy the garden.</p></div>
            <article v-for="task in openTasks" :key="task.id" class="task-row">
              <button class="check" :aria-label="`Complete ${task.title}`" @click="completeTask(task.id)">✓</button>
              <div><strong>{{ task.title }}</strong><p>{{ plantingName(task.planting_id) }}</p></div>
              <time :class="{ overdue: task.due_on < today }">{{ task.due_on === today ? 'Today' : task.due_on }}</time>
            </article>
          </section>

          <section class="panel">
            <header><div><p class="eyebrow">Coming along</p><h3>Upcoming harvests</h3></div></header>
            <div v-if="!dashboard?.upcoming_harvests.length" class="empty-small"><span>♧</span><p>Add expected harvest dates to see what’s next.</p></div>
            <article v-for="planting in dashboard?.upcoming_harvests" :key="planting.id" class="harvest-row">
              <span class="crop-avatar">{{ planting.crop.slice(0, 1) }}</span>
              <div><strong>{{ planting.crop }}</strong><p>{{ planting.variety || areaName(planting.growing_area_id) }}</p></div>
              <time>{{ planting.expected_harvest_on }}</time>
            </article>
          </section>
        </div>
      </template>

      <template v-else-if="activeView === 'garden'">
        <section class="section-heading">
          <div><p class="eyebrow">What’s growing</p><h2>My garden</h2></div>
          <div class="heading-actions">
            <select v-model="plantingFilter" aria-label="Filter plantings by status">
              <option value="all">All plantings</option>
              <option value="growing">Growing</option>
              <option value="planned">Planned</option>
              <option value="finished">Finished</option>
              <option value="failed">Failed</option>
            </select>
            <button class="button secondary" @click="modal = 'area'">+ Add area</button>
          </div>
        </section>
        <div v-if="!areas.length" class="empty-hero compact">
          <h2>Start with a growing area</h2><p>Add a bed, container, row, or greenhouse section.</p>
          <button class="button primary" @click="modal = 'area'">Add an area</button>
        </div>
        <div class="area-grid">
          <section v-for="area in areas" :key="area.id" class="area-card">
            <header><span class="area-type">{{ area.area_type }}</span><h3>{{ area.name }}</h3></header>
            <div class="planting-list">
              <article v-for="planting in visiblePlantings.filter((item) => item.growing_area_id === area.id)" :key="planting.id">
                <span class="crop-avatar">{{ planting.crop.slice(0, 1) }}</span>
                <div><strong>{{ planting.crop }}</strong><p>{{ planting.variety || planting.method.replace('_', ' ') }} · {{ planting.quantity }}</p></div>
                <select
                  class="status-select"
                  :value="planting.status"
                  :aria-label="`Status for ${planting.crop}`"
                  @change="changePlantingStatus(planting, ($event.target as HTMLSelectElement).value)"
                >
                  <option v-for="status in ['planned','growing','harvested','finished','failed']" :key="status">{{ status }}</option>
                </select>
              </article>
              <p v-if="!visiblePlantings.some((item) => item.growing_area_id === area.id)" class="muted">No matching plantings.</p>
            </div>
          </section>
        </div>
      </template>

      <template v-else-if="activeView === 'journal'">
        <section class="section-heading">
          <div><p class="eyebrow">A history you can learn from</p><h2>Garden journal</h2></div>
          <button class="button primary" :disabled="!plantings.length" @click="modal = 'activity'">+ Log activity</button>
        </section>
        <section class="panel">
          <div v-if="!activities.length" class="empty-small tall">
            <span>≋</span><h3>No garden notes yet</h3>
            <p>Log watering, feeding, pruning, pests, and observations.</p>
          </div>
          <article v-for="activity in activities" :key="activity.id" class="journal-row">
            <time>{{ activity.occurred_on }}</time>
            <span class="journal-dot" />
            <div>
              <strong>{{ activity.event_type.replaceAll('_', ' ') }}</strong>
              <p>{{ plantingName(activity.planting_id) }}</p>
              <p v-if="activity.notes" class="journal-note">{{ activity.notes }}</p>
            </div>
          </article>
        </section>
      </template>

      <template v-else>
        <section class="section-heading">
          <div><p class="eyebrow">What the garden gave</p><h2>Harvest journal</h2></div>
          <button class="button primary" :disabled="!plantings.length" @click="modal = 'harvest'">+ Record harvest</button>
        </section>
        <section class="panel">
          <div v-if="!harvests.length" class="empty-small tall"><span>♧</span><h3>Your harvest story starts here</h3><p>Record the first thing you pick from the garden.</p></div>
          <article v-for="harvest in harvests" :key="harvest.id" class="harvest-row">
            <span class="crop-avatar">{{ plantingName(harvest.planting_id).slice(0, 1) }}</span>
            <div><strong>{{ plantingName(harvest.planting_id) }}</strong><p>{{ harvest.harvested_on }}</p></div>
            <strong>{{ harvest.quantity }} {{ harvest.unit }}</strong>
          </article>
        </section>
      </template>
    </main>

    <ModalForm v-if="modal === 'garden'" title="Create a garden" @close="modal = null">
      <form @submit.prevent="createGarden">
        <label>Garden name<input v-model="gardenForm.name" required placeholder="Home garden"></label>
        <label>Location<input v-model="gardenForm.location" placeholder="Backyard"></label>
        <button class="button primary full">Create garden</button>
      </form>
    </ModalForm>
    <ModalForm v-if="modal === 'area'" title="Add a growing area" @close="modal = null">
      <form @submit.prevent="createResource('area')">
        <label>Name<input v-model="areaForm.name" required placeholder="Sunny raised bed"></label>
        <label>Type<select v-model="areaForm.area_type"><option v-for="type in ['bed','container','row','greenhouse','other']" :key="type">{{ type }}</option></select></label>
        <label>Notes<textarea v-model="areaForm.notes" placeholder="Morning sun, drip irrigation…"></textarea></label>
        <button class="button primary full">Add area</button>
      </form>
    </ModalForm>
    <ModalForm v-if="modal === 'planting'" title="Add a planting" @close="modal = null">
      <form @submit.prevent="createResource('planting')">
        <label>Growing area<select v-model="plantingForm.growing_area_id" required><option :value="0" disabled>Select an area</option><option v-for="area in areas" :key="area.id" :value="area.id">{{ area.name }}</option></select></label>
        <div class="form-row"><label>Crop<input v-model="plantingForm.crop" required placeholder="Tomato"></label><label>Variety<input v-model="plantingForm.variety" placeholder="Roma"></label></div>
        <div class="form-row"><label>Quantity<input v-model="plantingForm.quantity" type="number" min="1"></label><label>Method<select v-model="plantingForm.method"><option value="direct_sown">Direct sown</option><option value="transplanted">Transplanted</option><option value="existing">Existing plant</option></select></label></div>
        <div class="form-row"><label>Planted on<input v-model="plantingForm.planted_on" type="date" required></label><label>Expected harvest<input v-model="plantingForm.expected_harvest_on" type="date"></label></div>
        <p v-if="!areas.length" class="error">Add a growing area before adding a planting.</p>
        <button class="button primary full" :disabled="!areas.length">Add planting</button>
      </form>
    </ModalForm>
    <ModalForm v-if="modal === 'task'" title="Add a garden task" @close="modal = null">
      <form @submit.prevent="createResource('task')">
        <label>Task<input v-model="taskForm.title" required placeholder="Water the tomatoes"></label>
        <div class="form-row"><label>Due date<input v-model="taskForm.due_on" type="date" required></label><label>Planting<select v-model="taskForm.planting_id"><option :value="0">Whole garden</option><option v-for="planting in plantings" :key="planting.id" :value="planting.id">{{ planting.crop }} · {{ areaName(planting.growing_area_id) }}</option></select></label></div>
        <label>Notes<textarea v-model="taskForm.notes"></textarea></label>
        <button class="button primary full">Add task</button>
      </form>
    </ModalForm>
    <ModalForm v-if="modal === 'activity'" title="Log garden activity" @close="modal = null">
      <form @submit.prevent="createResource('activity')">
        <label>Planting<select v-model="activityForm.planting_id" required><option v-for="planting in plantings" :key="planting.id" :value="planting.id">{{ planting.crop }} · {{ areaName(planting.growing_area_id) }}</option></select></label>
        <div class="form-row">
          <label>Activity<select v-model="activityForm.event_type"><option value="watered">Watered</option><option value="fertilized">Fertilized</option><option value="pruned">Pruned</option><option value="transplanted">Transplanted</option><option value="pest_observed">Pest observed</option><option value="disease_observed">Disease observed</option><option value="note">General note</option><option value="removed">Removed</option></select></label>
          <label>Date<input v-model="activityForm.occurred_on" type="date" required></label>
        </div>
        <label>Notes<textarea v-model="activityForm.notes" placeholder="What did you notice?"></textarea></label>
        <button class="button primary full">Save to journal</button>
      </form>
    </ModalForm>
    <ModalForm v-if="modal === 'harvest'" title="Record a harvest" @close="modal = null">
      <form @submit.prevent="createResource('harvest')">
        <label>Planting<select v-model="harvestForm.planting_id" required><option v-for="planting in plantings" :key="planting.id" :value="planting.id">{{ planting.crop }} · {{ areaName(planting.growing_area_id) }}</option></select></label>
        <div class="form-row"><label>Amount<input v-model="harvestForm.quantity" type="number" min="0.01" step="0.01" required></label><label>Unit<select v-model="harvestForm.unit"><option>kg</option><option>g</option><option>items</option><option>bunches</option><option>cups</option></select></label></div>
        <label>Harvested on<input v-model="harvestForm.harvested_on" type="date" required></label>
        <label>Notes<textarea v-model="harvestForm.notes"></textarea></label>
        <button class="button primary full">Save harvest</button>
      </form>
    </ModalForm>
  </div>
</template>
