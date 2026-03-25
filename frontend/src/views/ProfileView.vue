<template>
  <div class="fade-in">
    <div class="page-container" style="padding-top:32px;padding-bottom:60px;">
      <div class="page-header">
        <h1 class="page-title">个人中心</h1>
      </div>

      <div class="profile-layout">
        <!-- Left: Profile Card -->
        <div>
          <div class="profile-card">
            <img v-if="auth.user?.avatar_url" :src="auth.user.avatar_url" class="profile-avatar" />
            <div v-else class="profile-avatar-placeholder">{{ auth.user?.username?.[0]?.toUpperCase() }}</div>
            <div class="profile-name">{{ auth.user?.first_name || auth.user?.username }}</div>
            <div class="profile-meta">{{ auth.user?.user_type === 'staff' ? '教职工' : '学生' }}</div>
            <div class="profile-meta" v-if="auth.user?.department">{{ auth.user?.department }}</div>
            <div class="profile-meta" v-if="auth.user?.student_id">学号：{{ auth.user?.student_id }}</div>
            <div style="margin-top:20px;display:flex;flex-direction:column;gap:8px;">
              <div class="profile-stat-row">
                <span>发布总数</span>
                <strong>{{ myItems.length }}</strong>
              </div>
              <div class="profile-stat-row">
                <span>失物招领</span>
                <strong>{{ myItems.filter(i => i.type === 'found').length }}</strong>
              </div>
              <div class="profile-stat-row">
                <span>寻物启事</span>
                <strong>{{ myItems.filter(i => i.type === 'lost').length }}</strong>
              </div>
              <div class="profile-stat-row">
                <span>成功匹配</span>
                <strong>{{ myMatches.filter(m => m.status === 'confirmed').length }}</strong>
              </div>
            </div>
            <el-button style="width:100%;margin-top:20px;" @click="showEditProfile = true">
              <el-icon><Edit /></el-icon> 编辑资料
            </el-button>
          </div>
        </div>

        <!-- Right: Content -->
        <div>
          <div class="tab-bar">
            <div class="tab-item" :class="{ active: tab === 'items' }" @click="tab = 'items'">我的发布</div>
            <div class="tab-item" :class="{ active: tab === 'matches' }" @click="tab = 'matches'; loadMatches()">匹配记录</div>
            <div class="tab-item" :class="{ active: tab === 'messages' }" @click="tab = 'messages'">消息中心</div>
          </div>

          <!-- My Items -->
          <div v-if="tab === 'items'">
            <div style="display:flex;gap:8px;margin-bottom:16px;">
              <span class="cat-tag" :class="{ active: itemTypeFilter === '' }" @click="itemTypeFilter = ''">全部</span>
              <span class="cat-tag" :class="{ active: itemTypeFilter === 'found' }" @click="itemTypeFilter = 'found'">失物招领</span>
              <span class="cat-tag" :class="{ active: itemTypeFilter === 'lost' }" @click="itemTypeFilter = 'lost'">寻物启事</span>
            </div>
            <div v-if="itemsLoading">
              <el-skeleton v-for="i in 3" :key="i" animated style="margin-bottom:12px;" />
            </div>
            <div v-else-if="filteredItems.length">
              <div v-for="item in filteredItems" :key="item.id" class="my-item-row">
                <img v-if="item.first_image" :src="item.first_image" class="my-item-img" />
                <div v-else class="my-item-img-placeholder">{{ CATEGORY_ICONS[item.category] || '📦' }}</div>
                <div class="my-item-info">
                  <div style="display:flex;gap:6px;margin-bottom:6px;">
                    <span class="badge" :class="item.type === 'found' ? 'badge-found' : 'badge-lost'">{{ item.type === 'found' ? '失物招领' : '寻物启事' }}</span>
                    <span class="badge" :class="`badge-${item.status}`">{{ item.status_display }}</span>
                  </div>
                  <div style="font-size:15px;font-weight:600;margin-bottom:4px;">{{ item.title }}</div>
                  <div style="font-size:13px;color:var(--text-secondary);">📍 {{ item.location }} · {{ formatDate(item.happened_at) }}</div>
                  <div style="font-size:12px;color:var(--text-muted);margin-top:4px;">👁 {{ item.view_count }} 次浏览 · {{ formatRelative(item.created_at) }}</div>
                </div>
                <div class="my-item-actions">
                  <router-link :to="`/items/${item.id}`">
                    <el-button size="small" plain>查看</el-button>
                  </router-link>
                  <router-link :to="`/publish?edit=${item.id}`">
                    <el-button size="small" plain>编辑</el-button>
                  </router-link>
                  <el-button size="small" type="danger" plain @click="deleteItem(item)">删除</el-button>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <div class="empty-state-icon">📭</div>
              <div class="empty-state-title">暂无发布记录</div>
              <router-link to="/publish" class="btn btn-primary" style="margin-top:16px;">立即发布</router-link>
            </div>
          </div>

          <!-- Matches -->
          <div v-if="tab === 'matches'">
            <div v-if="matchesLoading"><el-skeleton v-for="i in 3" :key="i" animated style="margin-bottom:12px;" /></div>
            <div v-else-if="myMatches.length">
              <div v-for="m in myMatches" :key="m.id" class="match-row">
                <div class="match-items">
                  <div class="match-item-mini" @click="$router.push(`/items/${m.found_item.id}`)">
                    <span class="badge badge-found" style="font-size:11px;">失物招领</span>
                    <div style="font-size:14px;font-weight:500;margin-top:4px;">{{ m.found_item.title }}</div>
                    <div style="font-size:12px;color:var(--text-secondary);">{{ m.found_item.location }}</div>
                  </div>
                  <div class="match-arrow">⟺</div>
                  <div class="match-item-mini" @click="$router.push(`/items/${m.lost_item.id}`)">
                    <span class="badge badge-lost" style="font-size:11px;">寻物启事</span>
                    <div style="font-size:14px;font-weight:500;margin-top:4px;">{{ m.lost_item.title }}</div>
                    <div style="font-size:12px;color:var(--text-secondary);">{{ m.lost_item.location }}</div>
                  </div>
                </div>
                <div class="match-meta">
                  <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                    <el-progress :percentage="m.score" :color="m.score >= 80 ? '#10b981' : m.score >= 60 ? '#f59e0b' : '#94a3b8'" style="width:120px;" />
                    <span style="font-size:13px;font-weight:600;">{{ m.score }}% 匹配</span>
                    <span class="badge" :class="m.status === 'confirmed' ? 'badge-matched' : m.status === 'rejected' ? 'badge-closed' : 'badge-active'">
                      {{ m.status_display }}
                    </span>
                  </div>
                  <div style="font-size:13px;color:var(--text-secondary);">{{ m.reason }}</div>
                  <div v-if="m.status === 'pending'" style="display:flex;gap:8px;margin-top:8px;">
                    <el-button size="small" type="success" @click="updateMatch(m, 'confirmed')">确认匹配</el-button>
                    <el-button size="small" type="danger" plain @click="updateMatch(m, 'rejected')">不是这个</el-button>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <div class="empty-state-icon">🤖</div>
              <div class="empty-state-title">暂无匹配记录</div>
              <div class="empty-state-desc">在物品详情页点击「智能匹配」开始匹配</div>
            </div>
          </div>

          <!-- Messages placeholder -->
          <div v-if="tab === 'messages'" class="empty-state">
            <div class="empty-state-icon">💬</div>
            <div class="empty-state-title">消息中心</div>
            <div class="empty-state-desc">在物品详情页查看和发送留言</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Profile Dialog -->
    <el-dialog v-model="showEditProfile" title="编辑个人资料" width="500px">
      <el-form :model="profileForm" label-position="top">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <el-form-item label="姓名">
            <el-input v-model="profileForm.first_name" />
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="profileForm.phone" />
          </el-form-item>
        </div>
        <el-form-item label="院系/部门">
          <el-input v-model="profileForm.department" />
        </el-form-item>
        <el-form-item label="个人简介">
          <el-input v-model="profileForm.bio" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditProfile = false">取消</el-button>
        <el-button type="primary" @click="saveProfile" :loading="savingProfile">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { itemApi, matchApi, userApi } from '@/api'

const auth = useAuthStore()
const tab = ref('items')
const myItems = ref([])
const myMatches = ref([])
const itemsLoading = ref(true)
const matchesLoading = ref(false)
const itemTypeFilter = ref('')
const showEditProfile = ref(false)
const savingProfile = ref(false)

const CATEGORY_ICONS = { '证件': '🪪', '电子产品': '📱', '书籍文具': '📚', '钥匙': '🔑', '钱包': '👛', '衣物': '👕', '其他': '📦' }

const profileForm = ref({
  first_name: auth.user?.first_name || '',
  phone: auth.user?.phone || '',
  department: auth.user?.department || '',
  bio: auth.user?.bio || '',
})

const filteredItems = computed(() => {
  if (!itemTypeFilter.value) return myItems.value
  return myItems.value.filter(i => i.type === itemTypeFilter.value)
})

function formatDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}
function formatRelative(d) {
  if (!d) return ''
  const diff = Date.now() - new Date(d).getTime()
  const h = Math.floor(diff / 3600000)
  if (h < 1) return '刚刚'
  if (h < 24) return `${h}小时前`
  return `${Math.floor(h / 24)}天前`
}

async function loadMyItems() {
  try {
    const { data } = await itemApi.myItems()
    myItems.value = data.results || []
  } catch {} finally { itemsLoading.value = false }
}

async function loadMatches() {
  if (myMatches.value.length) return
  matchesLoading.value = true
  try {
    const { data } = await matchApi.myMatches()
    myMatches.value = data.results || data || []
  } catch {} finally { matchesLoading.value = false }
}

async function deleteItem(item) {
  try {
    await ElMessageBox.confirm(`确定删除「${item.title}」？`, '确认删除', { type: 'warning' })
    await itemApi.delete(item.id)
    myItems.value = myItems.value.filter(i => i.id !== item.id)
    ElMessage.success('删除成功')
  } catch (e) { if (e !== 'cancel') ElMessage.error('删除失败') }
}

async function updateMatch(match, status) {
  try {
    await matchApi.updateStatus(match.id, { status })
    match.status = status
    match.status_display = status === 'confirmed' ? '已确认' : '已拒绝'
    ElMessage.success(status === 'confirmed' ? '已确认匹配！' : '已标记为不匹配')
  } catch { ElMessage.error('操作失败') }
}

async function saveProfile() {
  savingProfile.value = true
  try {
    const fd = new FormData()
    Object.entries(profileForm.value).forEach(([k, v]) => { if (v !== undefined) fd.append(k, v) })
    await userApi.updateProfile(fd)
    await auth.fetchMe()
    showEditProfile.value = false
    ElMessage.success('资料已更新')
  } catch { ElMessage.error('保存失败') } finally { savingProfile.value = false }
}

onMounted(loadMyItems)
</script>

<style scoped>
.profile-stat-row { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--border); font-size: 14px; color: var(--text-secondary); }
.profile-stat-row strong { color: var(--text-primary); font-size: 16px; }
.cat-tag { padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 500; cursor: pointer; background: white; border: 1px solid var(--border); color: var(--text-secondary); transition: all .15s; }
.cat-tag:hover, .cat-tag.active { background: var(--primary); color: white; border-color: var(--primary); }
.my-item-row { display: flex; gap: 16px; padding: 16px; background: white; border-radius: var(--radius); border: 1px solid var(--border); margin-bottom: 12px; align-items: center; transition: box-shadow .2s; }
.my-item-row:hover { box-shadow: var(--shadow); }
.my-item-img { width: 80px; height: 80px; border-radius: 8px; object-fit: cover; flex-shrink: 0; }
.my-item-img-placeholder { width: 80px; height: 80px; border-radius: 8px; background: #f1f5f9; display: flex; align-items: center; justify-content: center; font-size: 32px; flex-shrink: 0; }
.my-item-info { flex: 1; min-width: 0; }
.my-item-actions { display: flex; flex-direction: column; gap: 6px; flex-shrink: 0; }
.match-row { background: white; border-radius: var(--radius); border: 1px solid var(--border); padding: 16px; margin-bottom: 12px; }
.match-items { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.match-item-mini { flex: 1; padding: 12px; background: #f8fafc; border-radius: 8px; cursor: pointer; transition: background .15s; }
.match-item-mini:hover { background: #eff6ff; }
.match-arrow { font-size: 20px; color: var(--primary); flex-shrink: 0; }
.match-meta { padding-top: 12px; border-top: 1px solid var(--border); }
</style>
