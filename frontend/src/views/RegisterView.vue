<template>
  <div class="auth-page">
    <div class="auth-card" style="max-width:520px;">
      <div class="auth-logo">
        <div class="auth-logo-icon">🎒</div>
        <h1 class="auth-title">创建账号</h1>
        <p class="auth-subtitle">加入校园失物招领平台</p>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="submit">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" placeholder="登录用户名" />
          </el-form-item>
          <el-form-item label="姓名" prop="first_name">
            <el-input v-model="form.first_name" placeholder="真实姓名" />
          </el-form-item>
        </div>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="学校邮箱（选填）" type="email" />
        </el-form-item>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <el-form-item label="用户类型" prop="user_type">
            <el-select v-model="form.user_type" style="width:100%;">
              <el-option label="学生" value="student" />
              <el-option label="教职工" value="staff" />
            </el-select>
          </el-form-item>
          <el-form-item label="学号/工号">
            <el-input v-model="form.student_id" placeholder="选填" />
          </el-form-item>
        </div>
        <el-form-item label="院系/部门">
          <el-input v-model="form.department" placeholder="例：计算机学院（选填）" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" placeholder="联系电话（选填）" />
        </el-form-item>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <el-form-item label="密码" prop="password">
            <el-input v-model="form.password" type="password" placeholder="至少6位" show-password />
          </el-form-item>
          <el-form-item label="确认密码" prop="password2">
            <el-input v-model="form.password2" type="password" placeholder="再次输入密码" show-password />
          </el-form-item>
        </div>
        <el-button type="primary" style="width:100%;margin-top:8px;" size="large" :loading="loading" @click="submit">
          注册
        </el-button>
      </el-form>

      <div style="text-align:center;margin-top:20px;font-size:14px;color:var(--text-secondary);">
        已有账号？
        <router-link to="/login" style="color:var(--primary);font-weight:500;">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const formRef = ref()
const loading = ref(false)

const form = ref({
  username: '', first_name: '', email: '', user_type: 'student',
  student_id: '', department: '', phone: '', password: '', password2: '',
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }, { min: 3, message: '用户名至少3位', trigger: 'blur' }],
  first_name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }, { min: 6, message: '密码至少6位', trigger: 'blur' }],
  password2: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, cb) => {
        if (value !== form.value.password) cb(new Error('两次密码不一致'))
        else cb()
      }, trigger: 'blur'
    }
  ],
}

async function submit() {
  await formRef.value.validate()
  loading.value = true
  try {
    await auth.register(form.value)
    ElMessage.success('注册成功！欢迎加入！')
    router.push('/')
  } catch (e) {
    const data = e.response?.data
    if (data && typeof data === 'object') {
      const first = Object.entries(data)[0]
      ElMessage.error(`${first[0]}: ${Array.isArray(first[1]) ? first[1][0] : first[1]}`)
    } else {
      ElMessage.error('注册失败，请重试')
    }
  } finally {
    loading.value = false
  }
}
</script>
