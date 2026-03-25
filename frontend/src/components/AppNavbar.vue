<template>
  <nav class="navbar">
    <div class="navbar-inner">
      <router-link to="/" class="navbar-brand">
        <div class="navbar-brand-icon">🎒</div>
        <span class="navbar-brand-text">校园失物招领</span>
      </router-link>

      <div class="navbar-nav">
        <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">首页</router-link>
        <router-link to="/found" class="nav-link" :class="{ active: $route.path === '/found' }">失物招领</router-link>
        <router-link to="/lost" class="nav-link" :class="{ active: $route.path === '/lost' }">寻物启事</router-link>
        <router-link to="/search" class="nav-link" :class="{ active: $route.path === '/search' }">搜索</router-link>
      </div>

      <div class="nav-actions">
        <template v-if="auth.isAuthenticated">
          <el-badge :value="unreadCount || 0" :hidden="!unreadCount" class="badge-item">
            <router-link to="/publish">
              <el-button type="primary" size="small">
                <el-icon><Plus /></el-icon> 发布
              </el-button>
            </router-link>
          </el-badge>
          <el-dropdown @command="handleCommand">
            <div class="user-avatar-wrap">
              <img v-if="auth.user?.avatar_url" :src="auth.user.avatar_url" class="user-avatar" />
              <div v-else class="user-avatar-placeholder">{{ auth.user?.username?.[0]?.toUpperCase() }}</div>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon> 个人中心
                </el-dropdown-item>
                <el-dropdown-item v-if="auth.isAdmin" command="admin">
                  <el-icon><Setting /></el-icon> 管理后台
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon> 退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <router-link to="/login">
            <el-button size="small">登录</el-button>
          </router-link>
          <router-link to="/register">
            <el-button type="primary" size="small">注册</el-button>
          </router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { userApi } from '@/api'

const auth = useAuthStore()
const router = useRouter()
const unreadCount = ref(0)

async function fetchUnread() {
  if (!auth.isAuthenticated) return
  try {
    const { data } = await userApi.unreadCount()
    unreadCount.value = data.count
  } catch {}
}

function handleCommand(cmd) {
  if (cmd === 'profile') router.push('/profile')
  else if (cmd === 'admin') router.push('/admin')
  else if (cmd === 'logout') {
    auth.logout()
    router.push('/')
  }
}

onMounted(fetchUnread)
</script>

<style scoped>
.user-avatar-wrap { cursor: pointer; }
.user-avatar { width: 36px; height: 36px; border-radius: 50%; object-fit: cover; border: 2px solid var(--primary); }
.user-avatar-placeholder { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, var(--primary), var(--secondary)); display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 15px; }
.badge-item { margin-right: 8px; }
</style>
