export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api/v1',
    },
  },
  app: {
    head: {
      title: 'Plot & Sprout',
      meta: [
        { name: 'description', content: 'A calm, practical tracker for your backyard garden.' },
        { name: 'theme-color', content: '#173c2b' },
      ],
    },
  },
})
