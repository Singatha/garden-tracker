<script setup lang="ts">
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const emit = defineEmits<{ authenticated: [] }>()
const { authenticate } = useApi()
const { user } = useSession()

const mode = ref<'login' | 'register'>('register')
const form = reactive({ name: '', email: '', password: '' })
const error = ref('')
const busy = ref(false)

async function submit() {
  error.value = ''
  busy.value = true
  try {
    user.value = await authenticate(mode.value, form)
    emit('authenticated')
  } catch (reason: any) {
    error.value = reason?.data?.detail || 'Something went wrong. Please try again.'
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <main class="auth-page">
    <section class="auth-story">
      <div class="brand-mark">P<span>&</span>S</div>
      <p class="eyebrow">Your garden, remembered</p>
      <h1>Grow with a little more confidence.</h1>
      <p class="lede">
        Keep track of what is planted, what needs doing, and everything your garden gives back.
      </p>
      <div class="illustration" aria-hidden="true">
        <span class="sun" />
        <span class="leaf leaf-one">◒</span>
        <span class="leaf leaf-two">◒</span>
        <span class="stem" />
      </div>
    </section>

    <Card class="auth-card rounded-none border-0 shadow-none">
      <CardHeader class="px-0">
        <p class="eyebrow">{{ mode === 'register' ? 'Begin your garden journal' : 'Welcome back' }}</p>
        <CardTitle class="font-serif text-4xl font-normal">{{ mode === 'register' ? 'Create your account' : 'Sign in' }}</CardTitle>
      </CardHeader>
      <CardContent class="px-0">
      <form @submit.prevent="submit">
        <div v-if="mode === 'register'" class="grid gap-2">
          <Label for="auth-name">Your name</Label>
          <Input id="auth-name" v-model="form.name" required autocomplete="name" placeholder="Alex Gardener" />
        </div>
        <div class="grid gap-2">
          <Label for="auth-email">Email</Label>
          <Input id="auth-email" v-model="form.email" required type="email" autocomplete="email" placeholder="you@example.com" />
        </div>
        <div class="grid gap-2">
          <Label for="auth-password">Password</Label>
          <Input id="auth-password" v-model="form.password" required minlength="8" type="password" autocomplete="current-password" placeholder="At least 8 characters" />
        </div>
        <Alert v-if="error" variant="destructive">
          <AlertDescription>{{ error }}</AlertDescription>
        </Alert>
        <Button class="w-full" :disabled="busy">
          {{ busy ? 'Just a moment…' : mode === 'register' ? 'Start growing' : 'Sign in' }}
        </Button>
      </form>
      <Button variant="link" class="mt-4 w-full" @click="mode = mode === 'register' ? 'login' : 'register'">
        {{ mode === 'register' ? 'Already have an account? Sign in' : 'New here? Create an account' }}
      </Button>
      </CardContent>
    </Card>
  </main>
</template>
