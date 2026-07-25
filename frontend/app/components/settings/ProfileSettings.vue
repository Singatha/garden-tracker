<script setup lang="ts">
import { LogOutIcon, UserRoundIcon } from '@lucide/vue'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { toast } from 'vue-sonner'
import type { User } from '~/types'

const props = defineProps<{ user: User }>()
const emit = defineEmits<{ updated: [user: User]; logout: [] }>()
const { request } = useApi()

const name = ref(props.user.name)
const saving = ref(false)

async function saveProfile() {
  saving.value = true
  try {
    const updated = await request<User>('/auth/me', {
      method: 'PATCH',
      body: { name: name.value },
    })
    emit('updated', updated)
    toast.success('Profile updated')
  } catch (reason: any) {
    toast.error(reason?.data?.detail || 'Could not update your profile')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <section class="settings-page">
    <div class="section-heading">
      <div>
        <p class="eyebrow">Your account</p>
        <h2>Profile settings</h2>
        <p class="settings-intro">Manage how your name appears and access your account controls.</p>
      </div>
    </div>

    <div class="settings-grid">
      <Card>
        <CardHeader>
          <span class="settings-icon"><UserRoundIcon /></span>
          <CardTitle>Personal information</CardTitle>
          <CardDescription>Your email is used to sign in. Your name appears throughout Gardenwise.</CardDescription>
        </CardHeader>
        <form @submit.prevent="saveProfile">
          <CardContent class="grid gap-5">
            <div class="grid gap-2">
              <Label for="profile-name">Display name</Label>
              <Input id="profile-name" v-model="name" required autocomplete="name" />
            </div>
            <div class="grid gap-2">
              <Label for="profile-email">Email address</Label>
              <Input id="profile-email" :model-value="user.email" type="email" disabled />
              <p class="field-help">Email changes are not supported yet.</p>
            </div>
          </CardContent>
          <CardFooter class="justify-end border-t pt-6">
            <Button :disabled="saving || name.trim() === user.name">
              {{ saving ? 'Saving…' : 'Save changes' }}
            </Button>
          </CardFooter>
        </form>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Session</CardTitle>
          <CardDescription>Sign out on this device. Your garden records will remain saved.</CardDescription>
        </CardHeader>
        <CardFooter>
          <Button variant="outline" @click="$emit('logout')">
            <LogOutIcon /> Sign out
          </Button>
        </CardFooter>
      </Card>
    </div>
  </section>
</template>
