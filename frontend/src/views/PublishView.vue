<template>
  <div class="fade-in">
    <div class="page-container" style="max-width:800px;padding-top:32px;padding-bottom:60px;">
      <div class="page-header">
        <h1 class="page-title">{{ isEdit ? '编辑发布' : '发布信息' }}</h1>
        <p class="page-subtitle">{{ isEdit ? '修改您发布的物品信息' : '填写详细信息，帮助更快找到物品' }}</p>
      </div>

      <!-- Type Selector -->
      <div v-if="!isEdit" class="tab-bar" style="margin-bottom:24px;">
        <div class="tab-item" :class="{ active: form.type === 'found' }" @click="form.type = 'found'">
          🟢 失物招领（我捡到了）
        </div>
        <div class="tab-item" :class="{ active: form.type === 'lost' }" @click="form.type = 'lost'">
          🔴 寻物启事（我丢失了）
        </div>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="submit">
        <div class="form-section">
          <div class="form-section-title">基本信息</div>
          <el-form-item label="物品标题" prop="title">
            <el-input v-model="form.title" placeholder="例：黑色华为手机、学生证（张三）" maxlength="100" show-word-limit />
          </el-form-item>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <el-form-item label="物品分类" prop="category">
              <el-select v-model="form.category" placeholder="请选择分类" style="width:100%;">
                <el-option v-for="c in categories" :key="c.name" :label="`${c.icon} ${c.name}`" :value="c.name" />
              </el-select>
            </el-form-item>
            <el-form-item :label="form.type === 'found' ? '拾取时间' : '丢失时间'" prop="happened_at">
              <el-date-picker v-model="form.happened_at" type="datetime" placeholder="选择时间" style="width:100%;" format="YYYY-MM-DD HH:mm" value-format="YYYY-MM-DDTHH:mm:ss" />
            </el-form-item>
          </div>
          <el-form-item :label="form.type === 'found' ? '拾取地点' : '丢失地点'" prop="location">
            <el-input v-model="form.location" placeholder="例：图书馆一楼、教学楼B203" />
          </el-form-item>
          <el-form-item label="详细描述" prop="description">
            <el-input v-model="form.description" type="textarea" :rows="4" placeholder="请详细描述物品特征、颜色、品牌等信息，描述越详细越容易找到" maxlength="500" show-word-limit />
          </el-form-item>
        </div>

        <div class="form-section" style="margin-top:20px;">
          <div class="form-section-title">联系方式</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
            <el-form-item label="联系电话">
              <el-input v-model="form.contact_phone" placeholder="手机号码" />
            </el-form-item>
            <el-form-item label="微信号">
              <el-input v-model="form.contact_wechat" placeholder="微信号（选填）" />
            </el-form-item>
          </div>
          <div style="font-size:13px;color:var(--text-muted);">💡 至少填写一种联系方式，方便对方联系您</div>
        </div>

        <div class="form-section" style="margin-top:20px;">
          <div class="form-section-title">上传图片</div>
          <el-upload
            v-model:file-list="fileList"
            action="#"
            list-type="picture-card"
            :auto-upload="false"
            :limit="5"
            accept="image/*"
            :on-exceed="() => ElMessage.warning('最多上传5张图片')"
          >
            <el-icon><Plus /></el-icon>
            <template #tip>
              <div style="font-size:12px;color:var(--text-muted);margin-top:8px;">最多上传5张图片，支持 JPG/PNG/WEBP，每张不超过5MB</div>
            </template>
          </el-upload>
        </div>

        <div style="margin-top:24px;display:flex;gap:12px;justify-content:flex-end;">
          <el-button @click="$router.back()">取消</el-button>
          <el-button type="primary" native-type="submit" :loading="submitting" size="large">
            {{ isEdit ? '保存修改' : '发布信息' }}
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { itemApi } from '@/api'

const route = useRoute()
const router = useRouter()
const formRef = ref()
const submitting = ref(false)
const fileList = ref([])

const isEdit = ref(!!route.query.edit)

const form = ref({
  type: route.query.type || 'found',
  title: '',
  category: '',
  description: '',
  location: '',
  happened_at: '',
  contact_phone: '',
  contact_wechat: '',
})

const rules = {
  title: [{ required: true, message: '请输入物品标题', trigger: 'blur' }],
  category: [{ required: true, message: '请选择物品分类', trigger: 'change' }],
  description: [{ required: true, message: '请填写详细描述', trigger: 'blur' }],
  location: [{ required: true, message: '请填写地点', trigger: 'blur' }],
  happened_at: [{ required: true, message: '请选择时间', trigger: 'change' }],
}

const categories = [
  { name: '证件', icon: '🪪' }, { name: '电子产品', icon: '📱' },
  { name: '书籍文具', icon: '📚' }, { name: '钥匙', icon: '🔑' },
  { name: '钱包', icon: '👛' }, { name: '衣物', icon: '👕' }, { name: '其他', icon: '📦' },
]

async function loadItem() {
  if (!isEdit.value) return
  try {
    const { data } = await itemApi.detail(route.query.edit)
    form.value = {
      type: data.type,
      title: data.title,
      category: data.category,
      description: data.description,
      location: data.location,
      happened_at: data.happened_at,
      contact_phone: data.contact_phone || '',
      contact_wechat: data.contact_wechat || '',
    }
  } catch {
    ElMessage.error('加载失败')
  }
}

async function submit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    const fd = new FormData()
    Object.entries(form.value).forEach(([k, v]) => { if (v) fd.append(k, v) })
    fileList.value.forEach((f) => {
      if (f.raw) fd.append('uploaded_images', f.raw)
    })
    if (isEdit.value) {
      await itemApi.update(route.query.edit, fd)
      ElMessage.success('修改成功')
      router.push(`/items/${route.query.edit}`)
    } else {
      const { data } = await itemApi.create(fd)
      ElMessage.success('发布成功！')
      router.push(`/items/${data.id}`)
    }
  } catch (e) {
    const msg = e.response?.data
    if (typeof msg === 'object') {
      const first = Object.values(msg)[0]
      ElMessage.error(Array.isArray(first) ? first[0] : String(first))
    } else {
      ElMessage.error('发布失败，请检查填写内容')
    }
  } finally {
    submitting.value = false
  }
}

onMounted(loadItem)
</script>
