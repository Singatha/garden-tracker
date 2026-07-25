<script setup lang="ts">
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

    <section class="auth-card">
      <p class="eyebrow">{{ mode === 'register' ? 'Begin your garden journal' : 'Welcome back' }}</p>
      <h2>{{ mode === 'register' ? 'Create your account' : 'Sign in' }}</h2>
      <form @submit.prevent="submit">
        <label v-if="mode === 'register'">
          Your name
          <input v-model="form.name" required autocomplete="name" placeholder="Alex Gardener">
        </label>
        <label>
          Email
          <input v-model="form.email" required type="email" autocomplete="email" placeholder="you@example.com">
        </label>
        <label>
          Password
          <input v-model="form.password" required minlength="8" type="password" autocomplete="current-password" placeholder="At least 8 characters">
        </label>
        <p v-if="error" class="error" role="alert">{{ error }}</p>
        <button class="button primary full" :disabled="busy">
          {{ busy ? 'Just a moment…' : mode === 'register' ? 'Start growing' : 'Sign in' }}
        </button>
      </form>
      <button class="text-button" @click="mode = mode === 'register' ? 'login' : 'register'">
        {{ mode === 'register' ? 'Already have an account? Sign in' : 'New here? Create an account' }}
      </button>
    </section>
  </main>
</template>

