<template>
  <div class="fade-in" v-if="item">
    <div class="page-container" style="padding-top:32px;padding-bottom:60px;">
      <!-- Breadcrumb -->
      <el-breadcrumb separator="/" style="margin-bottom:20px;">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{ path: item.type === 'found' ? '/found' : '/lost' }">
          {{ item.type === 'found' ? '失物招领' : '寻物启事' }}
        </el-breadcrumb-item>
        <el-breadcrumb-item>{{ item.title }}</el-breadcrumb-item>
      </el-breadcrumb>

      <div class="detail-layout">
        <!-- Left: Main Content -->
        <div>
          <!-- Images -->
          <div class="detail-images">
            <el-carousel v-if="item.images?.length" height="360px" :autoplay="false">
              <el-carousel-item v-for="img in item.images" :key="img.id">
                <img :src="img.image_url" style="width:100%;height:360px;object-fit:cover;" />
              </el-carousel-item>
            </el-carousel>
            <div v-else class="no-image">
              <span>{{ categoryIcon }}</span>
              <p>暂无图片</p>
            </div>
          </div>

          <!-- Info Card -->
          <div class="card" style="margin-top:20px;">
            <div class="card-body">
              <div style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;">
                <span class="badge" :class="item.type === 'found' ? 'badge-found' : 'badge-lost'" style="font-size:14px;padding:6px 14px;">
                  {{ item.type === 'found' ? '🟢 失物招领' : '🔴 寻物启事' }}
                </span>
                <span class="badge badge-active" style="font-size:14px;padding:6px 14px;">{{ item.category }}</span>
                <span class="badge" :class="`badge-${item.status}`" style="font-size:14px;padding:6px 14px;">{{ item.status_display }}</span>
              </div>
              <h1 style="font-size:24px;font-weight:700;color:var(--text-primary);margin-bottom:20px;">{{ item.title }}</h1>

              <div class="info-grid">
                <div class="info-item">
                  <span class="info-label"><el-icon><Location /></el-icon> 地点</span>
                  <span class="info-value">{{ item.location }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label"><el-icon><Clock /></el-icon> 时间</span>
                  <span class="info-value">{{ formatDate(item.happened_at) }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label"><el-icon><View /></el-icon> 浏览</span>
                  <span class="info-value">{{ item.view_count }} 次</span>
                </div>
                <div class="info-item">
                  <span class="info-label"><el-icon><Calendar /></el-icon> 发布</span>
                  <span class="info-value">{{ formatDate(item.created_at) }}</span>
                </div>
              </div>

              <div style="margin-top:20px;">
                <div style="font-size:15px;font-weight:600;color:var(--text-primary);margin-bottom:10px;">📋 详细描述</div>
                <div style="font-size:15px;color:var(--text-secondary);line-height:1.8;white-space:pre-wrap;">{{ item.description }}</div>
              </div>
            </div>
          </div>

          <!-- Messages -->
          <div class="card" style="margin-top:20px;" v-if="auth.isAuthenticated && item.user?.id !== auth.user?.id">
            <div class="card-body">
              <h3 style="font-size:17px;font-weight:600;margin-bottom:16px;">💬 留言联系</h3>
              <div class="messages-list" v-if="messages.length">
                <div v-for="msg in messages" :key="msg.id" class="message-item" :class="{ 'my-msg': msg.from_user.id === auth.user?.id }">
                  <div class="msg-avatar">{{ msg.from_user.username?.[0]?.toUpperCase() }}</div>
                  <div class="msg-content">
                    <div class="msg-meta">{{ msg.from_user.username }} · {{ formatRelative(msg.created_at) }}</div>
                    <div class="msg-text">{{ msg.content }}</div>
                  </div>
                </div>
              </div>
              <div v-else style="color:var(--text-muted);font-size:14px;margin-bottom:16px;">暂无留言，成为第一个留言的人</div>
              <div style="display:flex;gap:8px;margin-top:12px;">
                <el-input v-model="newMessage" placeholder="输入留言内容..." :rows="2" type="textarea" style="flex:1;" />
                <el-button type="primary" @click="sendMessage" :loading="sending" style="height:auto;align-self:flex-end;">发送</el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Sidebar -->
        <div>
          <!-- Publisher Info -->
          <div class="card" style="margin-bottom:16px;">
            <div class="card-body">
              <h3 style="font-size:16px;font-weight:600;margin-bottom:16px;">👤 发布者信息</h3>
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
                <img v-if="item.user?.avatar_url" :src="item.user.avatar_url" style="width:48px;height:48px;border-radius:50%;object-fit:cover;" />
                <div v-else style="width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,var(--primary),var(--secondary));display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:20px;">
                  {{ item.user?.username?.[0]?.toUpperCase() }}
                </div>
                <div>
                  <div style="font-weight:600;font-size:15px;">{{ item.user?.first_name || item.user?.username }}</div>
                  <div style="font-size:13px;color:var(--text-secondary);">{{ item.user?.department || '校园用户' }}</div>
                </div>
              </div>
              <div v-if="item.contact_phone" class="contact-item">
                <el-icon><Phone /></el-icon>
                <span>{{ item.contact_phone }}</span>
              </div>
              <div v-if="item.contact_wechat" class="contact-item">
                <span>💬</span>
                <span>微信：{{ item.contact_wechat }}</span>
              </div>
              <div v-if="!item.contact_phone && !item.contact_wechat" style="color:var(--text-muted);font-size:13px;">请通过留言联系</div>
            </div>
          </div>

          <!-- AI Match Button -->
          <div class="card" style="margin-bottom:16px;" v-if="auth.isAuthenticated && item.user?.id === auth.user?.id">
            <div class="card-body">
              <h3 style="font-size:16px;font-weight:600;margin-bottom:12px;">🤖 智能匹配</h3>
              <p style="font-size:13px;color:var(--text-secondary);margin-bottom:16px;">AI 将自动分析并找出可能匹配的物品</p>
              <el-button type="primary" style="width:100%;" @click="runMatch" :loading="matching">
                {{ matching ? '匹配中...' : '开始智能匹配' }}
              </el-button>
              <div v-if="matchResults.length" style="margin-top:16px;">
                <div style="font-size:14px;font-weight:600;margin-bottom:8px;">找到 {{ matchResults.length }} 个可能匹配</div>
                <div v-for="m in matchResults" :key="m.id" class="match-result" @click="$router.push(`/items/${m.id}`)">
                  <div style="font-size:13px;font-weight:500;">匹配度 {{ m.score }}%</div>
                  <div style="font-size:12px;color:var(--text-secondary);">{{ m.reason }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Owner Actions -->
          <div class="card" v-if="auth.isAuthenticated && item.user?.id === auth.user?.id">
            <div class="card-body">
              <h3 style="font-size:16px;font-weight:600;margin-bottom:12px;">⚙️ 管理操作</h3>
              <div style="display:flex;flex-direction:column;gap:8px;">
                <router-link :to="`/publish?edit=${item.id}`">
                  <el-button style="width:100%;" plain>
                    <el-icon><Edit /></el-icon> 编辑信息
                  </el-button>
                </router-link>
                <el-button style="width:100%;" type="success" plain @click="closeItem" v-if="item.status === 'active'">
                  <el-icon><Check /></el-icon> 标记已解决
                </el-button>
                <el-button style="width:100%;" type="danger" plain @click="deleteItem">
                  <el-icon><Delete /></el-icon> 删除发布
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="loading" style="padding:80px;text-align:center;">
    <el-skeleton animated style="max-width:800px;margin:0 auto;" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { itemApi, matchApi } from '@/api'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const item = ref(null)
const loading = ref(true)
const messages = ref([])
const newMessage = ref('')
const sending = ref(false)
const matching = ref(false)
const matchResults = ref([])

const CATEGORY_ICONS = {
  '证件': '🪪', '电子产品': '📱', '书籍文具': '📚',
  '钥匙': '🔑', '钱包': '👛', '衣物': '👕', '其他': '📦'
}
const categoryIcon = computed(() => CATEGORY_ICONS[item.value?.category] || '📦')

function formatDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
function formatRelative(d) {
  if (!d) return ''
  const diff = Date.now() - new Date(d).getTime()
  const h = Math.floor(diff / 3600000)
  if (h < 1) return '刚刚'
  if (h < 24) return `${h}小时前`
  return `${Math.floor(h / 24)}天前`
}

async function loadItem() {
  try {
    const { data } = await itemApi.detail(route.params.id)
    item.value = data
  } catch {
    ElMessage.error('物品不存在')
    router.push('/')
  } finally {
    loading.value = false
  }
}

async function loadMessages() {
  if (!auth.isAuthenticated) return
  try {
    const { data } = await itemApi.messages(route.params.id)
    messages.value = data.results || data || []
  } catch {}
}

async function sendMessage() {
  if (!newMessage.value.trim()) return
  sending.value = true
  try {
    await itemApi.sendMessage(route.params.id, {
      content: newMessage.value,
      to_user_id: item.value.user.id,
    })
    newMessage.value = ''
    await loadMessages()
    ElMessage.success('留言发送成功')
  } catch {
    ElMessage.error('发送失败，请重试')
  } finally {
    sending.value = false
  }
}

async function runMatch() {
  matching.value = true
  matchResults.value = []
  try {
    const { data } = await matchApi.runMatch(item.value.id)
    // Backend returns array of match objects with found_item/lost_item and score/reason
    const matches = data.matches || data || []
    matchResults.value = matches.map(m => {
      const oppositeItem = item.value.type === 'found' ? m.lost_item : m.found_item
      return {
        id: oppositeItem?.id,
        matchId: m.id,
        title: oppositeItem?.title,
        score: m.score,
        reason: m.reason,
      }
    }).filter(m => m.id)
    if (matchResults.value.length) {
      ElMessage.success(`找到 ${matchResults.value.length} 个可能匹配！`)
    } else {
      ElMessage.info(data.message || '暂未找到匹配结果')
    }
  } catch {
    ElMessage.error('匹配失败，请稍后重试')
  } finally {
    matching.value = false
  }
}

async function closeItem() {
  try {
    await itemApi.update(item.value.id, { status: 'closed' })
    item.value.status = 'closed'
    ElMessage.success('已标记为已解决')
  } catch {
    ElMessage.error('操作失败')
  }
}

async function deleteItem() {
  try {
    await ElMessageBox.confirm('确定要删除这条发布吗？', '确认删除', { type: 'warning' })
    await itemApi.delete(item.value.id)
    ElMessage.success('删除成功')
    router.push('/profile')
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

onMounted(() => {
  loadItem()
  loadMessages()
})
</script>

<style scoped>
.detail-images { border-radius: var(--radius-lg); overflow: hidden; background: #f1f5f9; }
.no-image { height: 360px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; font-size: 72px; color: var(--text-muted); }
.no-image p { font-size: 14px; }
.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.info-item { display: flex; flex-direction: column; gap: 4px; padding: 12px; background: #f8fafc; border-radius: 8px; }
.info-label { font-size: 12px; color: var(--text-muted); display: flex; align-items: center; gap: 4px; }
.info-value { font-size: 14px; font-weight: 500; color: var(--text-primary); }
.contact-item { display: flex; align-items: center; gap: 8px; padding: 10px 12px; background: #f8fafc; border-radius: 8px; font-size: 14px; margin-bottom: 8px; }
.messages-list { max-height: 300px; overflow-y: auto; margin-bottom: 12px; display: flex; flex-direction: column; gap: 12px; }
.message-item { display: flex; gap: 10px; }
.message-item.my-msg { flex-direction: row-reverse; }
.msg-avatar { width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, var(--primary), var(--secondary)); display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 14px; flex-shrink: 0; }
.msg-content { max-width: 80%; }
.msg-meta { font-size: 12px; color: var(--text-muted); margin-bottom: 4px; }
.msg-text { background: #f1f5f9; padding: 8px 12px; border-radius: 8px; font-size: 14px; line-height: 1.5; }
.my-msg .msg-text { background: #dbeafe; }
.match-result { padding: 10px 12px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; margin-bottom: 8px; cursor: pointer; transition: all .15s; }
.match-result:hover { background: #dcfce7; }
</style>
