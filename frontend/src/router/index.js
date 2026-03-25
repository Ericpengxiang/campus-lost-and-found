import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/', name: 'Home', component: () => import('@/views/HomeView.vue') },
  { path: '/login', name: 'Login', component: () => import('@/views/LoginView.vue') },
  { path: '/register', name: 'Register', component: () => import('@/views/RegisterView.vue') },
  { path: '/found', name: 'Found', component: () => import('@/views/ItemListView.vue'), props: { type: 'found' } },
  { path: '/lost', name: 'Lost', component: () => import('@/views/ItemListView.vue'), props: { type: 'lost' } },
  { path: '/search', name: 'Search', component: () => import('@/views/SearchView.vue') },
  { path: '/items/:id', name: 'ItemDetail', component: () => import('@/views/ItemDetailView.vue') },
  { path: '/publish', name: 'Publish', component: () => import('@/views/PublishView.vue'), meta: { requiresAuth: true } },
  { path: '/profile', name: 'Profile', component: () => import('@/views/ProfileView.vue'), meta: { requiresAuth: true } },
  { path: '/admin', name: 'Admin', component: () => import('@/views/AdminView.vue'), meta: { requiresAuth: true, requiresAdmin: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  if (!auth.user && localStorage.getItem('access_token')) {
    await auth.fetchMe()
  }
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next({ name: 'Login', query: { redirect: to.fullPath } })
  }
  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return next({ name: 'Home' })
  }
  next()
})

export default router
