<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-logo">
        <div class="auth-logo-icon">🎒</div>
        <h1 class="auth-title">欢迎回来</h1>
        <p class="auth-subtitle">登录校园失物招领平台</p>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="submit">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" size="large" prefix-icon="User" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" size="large" prefix-icon="Lock" show-password @keyup.enter="submit" />
        </el-form-item>
        <el-button type="primary" style="width:100%;margin-top:8px;" size="large" :loading="loading" @click="submit">
          登录
        </el-button>
      </el-form>

      <div style="text-align:center;margin-top:20px;font-size:14px;color:var(--text-secondary);">
        还没有账号？
        <router-link to="/register" style="color:var(--primary);font-weight:500;">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const formRef = ref()
const loading = ref(false)

const form = ref({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function submit() {
  await formRef.value.validate()
  loading.value = true
  try {
    await auth.login(form.value.username, form.value.password)
    ElMessage.success('登录成功！')
    router.push(route.query.redirect || '/')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '用户名或密码错误')
  } finally {
    loading.value = false
  }
}
</script>
