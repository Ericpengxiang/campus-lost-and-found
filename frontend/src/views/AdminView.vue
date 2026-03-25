<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <div class="admin-sidebar">
      <div style="padding:16px 20px;border-bottom:1px solid var(--border);margin-bottom:8px;">
        <div style="font-size:16px;font-weight:700;color:var(--text-primary);">⚙️ 管理后台</div>
        <div style="font-size:12px;color:var(--text-muted);margin-top:2px;">校园失物招领平台</div>
      </div>
      <a class="admin-sidebar-item" :class="{ active: activeMenu === 'dashboard' }" @click="activeMenu = 'dashboard'">
        <el-icon><DataAnalysis /></el-icon> 数据概览
      </a>
      <a class="admin-sidebar-item" :class="{ active: activeMenu === 'items' }" @click="activeMenu = 'items'; loadAdminItems()">
        <el-icon><List /></el-icon> 内容管理
      </a>
      <a class="admin-sidebar-item" :class="{ active: activeMenu === 'users' }" @click="activeMenu = 'users'; loadUsers()">
        <el-icon><User /></el-icon> 用户管理
      </a>
      <a class="admin-sidebar-item" :class="{ active: activeMenu === 'matches' }" @click="activeMenu = 'matches'; loadAdminMatches()">
        <el-icon><Connection /></el-icon> 匹配记录
      </a>
      <div style="margin-top:auto;padding:16px 20px;border-top:1px solid var(--border);margin-top:20px;">
        <router-link to="/" class="admin-sidebar-item" style="padding:8px 0;">
          <el-icon><ArrowLeft /></el-icon> 返回前台
        </router-link>
      </div>
    </div>

    <!-- Main Content -->
    <div class="admin-main">
      <!-- Dashboard -->
      <div v-if="activeMenu === 'dashboard'">
        <h2 style="font-size:22px;font-weight:700;margin-bottom:24px;">数据概览</h2>
        <div class="grid-4" style="margin-bottom:24px;">
          <div class="stat-card">
            <div class="stat-card-value" style="color:var(--primary);">{{ stats.user_count || 0 }}</div>
            <div class="stat-card-label">注册用户</div>
          </div>
          <div class="stat-card">
            <div class="stat-card-value" style="color:var(--found-color);">{{ stats.found_count || 0 }}</div>
            <div class="stat-card-label">失物招领</div>
          </div>
          <div class="stat-card">
            <div class="stat-card-value" style="color:var(--lost-color);">{{ stats.lost_count || 0 }}</div>
            <div class="stat-card-label">寻物启事</div>
          </div>
          <div class="stat-card">
            <div class="stat-card-value" style="color:var(--success);">{{ stats.matched_count || 0 }}</div>
            <div class="stat-card-label">成功匹配</div>
          </div>
        </div>
        <div class="grid-2">
          <div class="stat-card">
            <div style="font-size:16px;font-weight:600;margin-bottom:16px;">分类统计</div>
            <div v-for="(count, cat) in stats.category_stats" :key="cat" style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border);">
              <span style="font-size:14px;">{{ cat }}</span>
              <div style="display:flex;align-items:center;gap:8px;">
                <el-progress :percentage="Math.round(count / (stats.found_count + stats.lost_count) * 100) || 0" style="width:100px;" :show-text="false" />
                <span style="font-size:13px;font-weight:500;width:30px;text-align:right;">{{ count }}</span>
              </div>
            </div>
          </div>
          <div class="stat-card">
            <div style="font-size:16px;font-weight:600;margin-bottom:16px;">状态分布</div>
            <div style="display:flex;flex-direction:column;gap:12px;">
              <div class="status-stat">
                <span class="badge badge-active">进行中</span>
                <div style="flex:1;margin:0 12px;"><el-progress :percentage="Math.round((stats.active_count || 0) / ((stats.found_count || 0) + (stats.lost_count || 0)) * 100) || 0" :show-text="false" /></div>
                <span style="font-size:14px;font-weight:600;">{{ stats.active_count || 0 }}</span>
              </div>
              <div class="status-stat">
                <span class="badge badge-matched">已匹配</span>
                <div style="flex:1;margin:0 12px;"><el-progress :percentage="Math.round((stats.matched_count || 0) / ((stats.found_count || 0) + (stats.lost_count || 0)) * 100) || 0" :show-text="false" color="#10b981" /></div>
                <span style="font-size:14px;font-weight:600;">{{ stats.matched_count || 0 }}</span>
              </div>
              <div class="status-stat">
                <span class="badge badge-closed">已关闭</span>
                <div style="flex:1;margin:0 12px;"><el-progress :percentage="Math.round((stats.closed_count || 0) / ((stats.found_count || 0) + (stats.lost_count || 0)) * 100) || 0" :show-text="false" color="#94a3b8" /></div>
                <span style="font-size:14px;font-weight:600;">{{ stats.closed_count || 0 }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Items Management -->
      <div v-if="activeMenu === 'items'">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
          <h2 style="font-size:22px;font-weight:700;">内容管理</h2>
          <div style="display:flex;gap:8px;">
            <el-select v-model="itemFilter.type" placeholder="全部类型" clearable style="width:120px;" @change="loadAdminItems(1)">
              <el-option label="失物招领" value="found" />
              <el-option label="寻物启事" value="lost" />
            </el-select>
            <el-select v-model="itemFilter.status" placeholder="全部状态" clearable style="width:120px;" @change="loadAdminItems(1)">
              <el-option label="进行中" value="active" />
              <el-option label="已匹配" value="matched" />
              <el-option label="已关闭" value="closed" />
            </el-select>
            <el-input v-model="itemFilter.keyword" placeholder="搜索..." clearable style="width:180px;" @keyup.enter="loadAdminItems(1)" />
          </div>
        </div>
        <el-table :data="adminItems" style="width:100%;border-radius:12px;overflow:hidden;" v-loading="itemsLoading">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column label="物品" min-width="200">
            <template #default="{ row }">
              <div style="display:flex;align-items:center;gap:10px;">
                <img v-if="row.first_image" :src="row.first_image" style="width:40px;height:40px;border-radius:6px;object-fit:cover;" />
                <div v-else style="width:40px;height:40px;border-radius:6px;background:#f1f5f9;display:flex;align-items:center;justify-content:center;font-size:18px;">📦</div>
                <div>
                  <div style="font-size:14px;font-weight:500;">{{ row.title }}</div>
                  <div style="font-size:12px;color:var(--text-muted);">{{ row.category }} · {{ row.location }}</div>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="类型" width="100">
            <template #default="{ row }">
              <span class="badge" :class="row.type === 'found' ? 'badge-found' : 'badge-lost'">
                {{ row.type === 'found' ? '失物招领' : '寻物启事' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="90">
            <template #default="{ row }">
              <span class="badge" :class="`badge-${row.status}`">{{ row.status_display }}</span>
            </template>
          </el-table-column>
          <el-table-column label="发布者" width="100">
            <template #default="{ row }">{{ row.user?.username }}</template>
          </el-table-column>
          <el-table-column label="浏览" width="70" prop="view_count" />
          <el-table-column label="发布时间" width="130">
            <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
          </el-table-column>
          <el-table-column label="操作" width="160" fixed="right">
            <template #default="{ row }">
              <el-button size="small" plain @click="$router.push(`/items/${row.id}`)">查看</el-button>
              <el-button v-if="row.status !== 'closed'" size="small" type="warning" plain @click="adminCloseItem(row)">关闭</el-button>
              <el-button size="small" type="danger" plain @click="adminDeleteItem(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination" v-if="itemsTotal > 20">
          <el-pagination v-model:current-page="itemsPage" :page-size="20" :total="itemsTotal" layout="prev, pager, next" @current-change="loadAdminItems" />
        </div>
      </div>

      <!-- Users Management -->
      <div v-if="activeMenu === 'users'">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
          <h2 style="font-size:22px;font-weight:700;">用户管理</h2>
          <el-input v-model="userSearch" placeholder="搜索用户名..." clearable style="width:200px;" @keyup.enter="loadUsers(1)" />
        </div>
        <el-table :data="users" style="width:100%;border-radius:12px;overflow:hidden;" v-loading="usersLoading">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column label="用户" min-width="180">
            <template #default="{ row }">
              <div style="display:flex;align-items:center;gap:10px;">
                <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,var(--primary),var(--secondary));display:flex;align-items:center;justify-content:center;color:white;font-weight:700;">
                  {{ row.username?.[0]?.toUpperCase() }}
                </div>
                <div>
                  <div style="font-size:14px;font-weight:500;">{{ row.first_name || row.username }}</div>
                  <div style="font-size:12px;color:var(--text-muted);">@{{ row.username }}</div>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="类型" width="90">
            <template #default="{ row }">
              <span class="badge badge-active">{{ row.user_type === 'staff' ? '教职工' : '学生' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="department" label="院系" width="120" />
          <el-table-column prop="email" label="邮箱" min-width="160" />
          <el-table-column label="发布数" width="80" prop="items_count" />
          <el-table-column label="注册时间" width="130">
            <template #default="{ row }">{{ formatDate(row.date_joined) }}</template>
          </el-table-column>
          <el-table-column label="状态" width="90">
            <template #default="{ row }">
              <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">{{ row.is_active ? '正常' : '禁用' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120" fixed="right">
            <template #default="{ row }">
              <el-button size="small" :type="row.is_active ? 'danger' : 'success'" plain @click="toggleUser(row)">
                {{ row.is_active ? '禁用' : '启用' }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination" v-if="usersTotal > 20">
          <el-pagination v-model:current-page="usersPage" :page-size="20" :total="usersTotal" layout="prev, pager, next" @current-change="loadUsers" />
        </div>
      </div>

      <!-- Matches -->
      <div v-if="activeMenu === 'matches'">
        <h2 style="font-size:22px;font-weight:700;margin-bottom:20px;">匹配记录</h2>
        <el-table :data="adminMatches" style="width:100%;border-radius:12px;overflow:hidden;" v-loading="matchesLoading">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column label="失物招领" min-width="160">
            <template #default="{ row }">
              <div style="cursor:pointer;color:var(--primary);" @click="$router.push(`/items/${row.found_item.id}`)">{{ row.found_item.title }}</div>
            </template>
          </el-table-column>
          <el-table-column label="寻物启事" min-width="160">
            <template #default="{ row }">
              <div style="cursor:pointer;color:var(--primary);" @click="$router.push(`/items/${row.lost_item.id}`)">{{ row.lost_item.title }}</div>
            </template>
          </el-table-column>
          <el-table-column label="匹配度" width="120">
            <template #default="{ row }">
              <el-progress :percentage="row.score" :color="row.score >= 80 ? '#10b981' : '#f59e0b'" />
            </template>
          </el-table-column>
          <el-table-column label="状态" width="90">
            <template #default="{ row }">
              <span class="badge" :class="row.status === 'confirmed' ? 'badge-matched' : row.status === 'rejected' ? 'badge-closed' : 'badge-active'">{{ row.status_display }}</span>
            </template>
          </el-table-column>
          <el-table-column label="匹配时间" width="130">
            <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { itemApi, matchApi, userApi } from '@/api'

const activeMenu = ref('dashboard')
const stats = ref({})

// Items
const adminItems = ref([])
const itemsLoading = ref(false)
const itemsTotal = ref(0)
const itemsPage = ref(1)
const itemFilter = ref({ type: '', status: '', keyword: '' })

// Users
const users = ref([])
const usersLoading = ref(false)
const usersTotal = ref(0)
const usersPage = ref(1)
const userSearch = ref('')

// Matches
const adminMatches = ref([])
const matchesLoading = ref(false)

function formatDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

async function loadStats() {
  try {
    const { data } = await itemApi.adminStats()
    stats.value = data
  } catch {}
}

async function loadAdminItems(page = 1) {
  itemsLoading.value = true
  itemsPage.value = page
  try {
    const params = { page, page_size: 20, admin: 1 }
    if (itemFilter.value.type) params.type = itemFilter.value.type
    if (itemFilter.value.status) params.status = itemFilter.value.status
    if (itemFilter.value.keyword) params.keyword = itemFilter.value.keyword
    const { data } = await itemApi.list(params)
    adminItems.value = data.results || []
    itemsTotal.value = data.count || 0
  } catch {} finally { itemsLoading.value = false }
}

async function loadUsers(page = 1) {
  usersLoading.value = true
  usersPage.value = page
  try {
    const params = { page, page_size: 20 }
    if (userSearch.value) params.search = userSearch.value
    const { data } = await userApi.adminList(params)
    users.value = data.results || []
    usersTotal.value = data.count || 0
  } catch {} finally { usersLoading.value = false }
}

async function loadAdminMatches() {
  matchesLoading.value = true
  try {
    const { data } = await matchApi.adminList()
    adminMatches.value = data.results || data || []
  } catch {} finally { matchesLoading.value = false }
}

async function adminCloseItem(item) {
  try {
    await itemApi.adminUpdate(item.id, { status: 'closed' })
    item.status = 'closed'
    item.status_display = '已关闭'
    ElMessage.success('已关闭')
  } catch { ElMessage.error('操作失败') }
}

async function adminDeleteItem(item) {
  try {
    await ElMessageBox.confirm(`确定删除「${item.title}」？`, '确认删除', { type: 'warning' })
    await itemApi.adminDelete(item.id)
    adminItems.value = adminItems.value.filter(i => i.id !== item.id)
    ElMessage.success('已删除')
  } catch (e) { if (e !== 'cancel') ElMessage.error('删除失败') }
}

async function toggleUser(user) {
  try {
    await userApi.adminToggle(user.id, { is_active: !user.is_active })
    user.is_active = !user.is_active
    ElMessage.success(user.is_active ? '已启用' : '已禁用')
  } catch { ElMessage.error('操作失败') }
}

onMounted(loadStats)
</script>

<style scoped>
.status-stat { display: flex; align-items: center; gap: 8px; }
</style>
