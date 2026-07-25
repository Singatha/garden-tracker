import type { User } from '~/types'

interface TokenResponse {
  access_token: string
  token_type: string
  user: User
}

export const useSession = () => {
  const token = useCookie<string | null>('garden-token', {
    maxAge: 60 * 60 * 24,
    sameSite: 'lax',
  })
  const user = useState<User | null>('garden-user', () => null)
  return { token, user }
}

export const useApi = () => {
  const config = useRuntimeConfig()
  const { token } = useSession()

  const request = async <T>(path: string, options: Record<string, unknown> = {}) => {
    return await $fetch<T>(`${config.public.apiBase}${path}`, {
      ...options,
      headers: {
        ...(token.value ? { Authorization: `Bearer ${token.value}` } : {}),
        ...((options.headers as Record<string, string>) || {}),
      },
    })
  }

  const authenticate = async (
    mode: 'login' | 'register',
    payload: { email: string; password: string; name?: string },
  ) => {
    const result = await request<TokenResponse>(`/auth/${mode}`, {
      method: 'POST',
      body: payload,
    })
    token.value = result.access_token
    return result.user
  }

  return { request, authenticate }
}
