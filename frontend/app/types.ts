export interface User {
  id: number
  email: string
  name: string
}

export interface Garden {
  id: number
  name: string
  location: string | null
}

export interface Area {
  id: number
  name: string
  area_type: string
  notes: string | null
}

export interface Planting {
  id: number
  growing_area_id: number
  crop: string
  variety: string | null
  quantity: number
  method: string
  planted_on: string
  expected_harvest_on: string | null
  status: string
}

export interface GardenTask {
  id: number
  planting_id: number | null
  title: string
  due_on: string
  completed_at: string | null
  notes: string | null
}

export interface Harvest {
  id: number
  planting_id: number
  harvested_on: string
  quantity: number
  unit: string
}

export interface GardenActivity {
  id: number
  planting_id: number
  event_type: string
  occurred_on: string
  notes: string | null
}

export interface Dashboard {
  active_plantings: number
  overdue_tasks: GardenTask[]
  due_today: GardenTask[]
  upcoming_harvests: Planting[]
}
