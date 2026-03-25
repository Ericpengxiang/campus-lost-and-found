import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const original = err.config
    if (err.response?.status === 401 && !original._retry) {
      original._retry = true
      const refresh = localStorage.getItem('refresh_token')
      if (refresh) {
        try {
          const { data } = await axios.post('/api/users/token/refresh/', { refresh })
          localStorage.setItem('access_token', data.access)
          original.headers.Authorization = `Bearer ${data.access}`
          return api(original)
        } catch {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          if (!window.location.pathname.startsWith('/login')) {
            window.location.href = `/login?redirect=${encodeURIComponent(window.location.pathname)}`
          }
        }
      }
    }
    return Promise.reject(err)
  }
)

// Users
export const userApi = {
  register: (data) => api.post('/users/register/', data),
  login: (data) => api.post('/users/login/', data),
  me: () => api.get('/users/me/'),
  updateProfile: (data) => api.patch('/users/me/', data, { headers: { 'Content-Type': 'multipart/form-data' } }),
  unreadCount: () => api.get('/users/me/unread/').catch(() => ({ data: { count: 0 } })),
  adminList: (params) => api.get('/users/admin/list/', { params }),
  adminDetail: (id) => api.get(`/users/admin/${id}/`),
  adminToggle: (id, data) => api.patch(`/users/admin/${id}/`, data),
  adminDelete: (id) => api.delete(`/users/admin/${id}/`),
}

// Items
export const itemApi = {
  list: (params) => api.get('/items/', { params }),
  detail: (id) => api.get(`/items/${id}/`),
  create: (data) => api.post('/items/create/', data, { headers: { 'Content-Type': 'multipart/form-data' } }),
  update: (id, data) => {
    const isFormData = data instanceof FormData
    return api.patch(`/items/${id}/edit/`, data, {
      headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : {}
    })
  },
  delete: (id) => api.delete(`/items/${id}/edit/`),
  myItems: (params) => api.get('/items/my/', { params }),
  messages: (itemId) => api.get(`/items/${itemId}/messages/`),
  sendMessage: (itemId, data) => api.post(`/items/${itemId}/messages/`, data),
  adminList: (params) => api.get('/items/', { params: { ...params, admin: 1 } }),
  adminStats: () => api.get('/items/admin/stats/'),
  adminUpdate: (id, data) => api.patch(`/items/admin/${id}/`, data),
  adminDelete: (id) => api.delete(`/items/admin/${id}/`),
}

// Matches
export const matchApi = {
  myMatches: () => api.get('/matches/my/'),
  runMatch: (itemId) => api.post(`/matches/run/${itemId}/`),
  updateStatus: (id, data) => api.patch(`/matches/${id}/`, data),
  adminList: () => api.get('/matches/admin/list/'),
}

export default api
