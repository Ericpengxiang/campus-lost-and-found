<template>
  <div id="app">
    <AppNavbar v-if="!isAuthPage && !isAdminPage" />
    <router-view />
    <AppFooter v-if="!isAuthPage && !isAdminPage" />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppNavbar from '@/components/AppNavbar.vue'
import AppFooter from '@/components/AppFooter.vue'

const route = useRoute()
const auth = useAuthStore()

const isAuthPage = computed(() => ['/login', '/register'].includes(route.path))
const isAdminPage = computed(() => route.path.startsWith('/admin'))

onMounted(() => {
  auth.fetchMe()
})
</script>
