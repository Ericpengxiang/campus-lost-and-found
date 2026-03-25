import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userApi } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.is_staff || false)

  async function fetchMe() {
    const token = localStorage.getItem('access_token')
    if (!token) return
    try {
      loading.value = true
      const { data } = await userApi.me()
      user.value = data
    } catch {
      user.value = null
    } finally {
      loading.value = false
    }
  }

  async function login(username, password) {
    const { data } = await userApi.login({ username, password })
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    await fetchMe()
  }

  async function register(formData) {
    const { data } = await userApi.register(formData)
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    user.value = data.user
  }

  function logout() {
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return { user, loading, isAuthenticated, isAdmin, fetchMe, login, register, logout }
})
