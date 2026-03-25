<template>
  <div class="home fade-in">
    <!-- Hero -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">校园失物招领平台</h1>
        <p class="hero-subtitle">丢失了东西？捡到了物品？在这里找到答案，传递校园温情</p>
        <div class="hero-search">
          <input v-model="searchKeyword" placeholder="搜索物品名称、地点..." @keyup.enter="goSearch" />
          <button @click="goSearch">🔍 搜索</button>
        </div>
        <div class="hero-stats">
          <div class="hero-stat">
            <div class="hero-stat-num">{{ stats.found_count || 0 }}</div>
            <div class="hero-stat-label">失物招领</div>
          </div>
          <div class="hero-stat">
            <div class="hero-stat-num">{{ stats.lost_count || 0 }}</div>
            <div class="hero-stat-label">寻物启事</div>
          </div>
          <div class="hero-stat">
            <div class="hero-stat-num">{{ stats.matched_count || 0 }}</div>
            <div class="hero-stat-label">成功匹配</div>
          </div>
          <div class="hero-stat">
            <div class="hero-stat-num">{{ stats.user_count || 0 }}</div>
            <div class="hero-stat-label">注册用户</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Quick Actions -->
    <div class="page-container">
      <div class="quick-actions">
        <router-link to="/publish?type=found" class="quick-action-card found-card">
          <div class="quick-action-icon">🟢</div>
          <div>
            <div class="quick-action-title">发布失物招领</div>
            <div class="quick-action-desc">捡到物品，帮助失主找回</div>
          </div>
        </router-link>
        <router-link to="/publish?type=lost" class="quick-action-card lost-card">
          <div class="quick-action-icon">🔴</div>
          <div>
            <div class="quick-action-title">发布寻物启事</div>
            <div class="quick-action-desc">丢失物品，寻求帮助</div>
          </div>
        </router-link>
      </div>

      <!-- Categories -->
      <section class="section">
        <div class="section-header">
          <h2 class="section-title">按分类浏览</h2>
        </div>
        <div class="category-grid">
          <router-link
            v-for="cat in categories" :key="cat.name"
            :to="`/found?category=${cat.name}`"
            class="category-item"
          >
            <span class="category-icon">{{ cat.icon }}</span>
            <span class="category-name">{{ cat.name }}</span>
          </router-link>
        </div>
      </section>

      <!-- Latest Found -->
      <section class="section">
        <div class="section-header">
          <h2 class="section-title">最新失物招领</h2>
          <router-link to="/found" class="btn btn-secondary btn-sm">查看全部 →</router-link>
        </div>
        <div v-if="foundLoading" class="grid-4">
          <el-skeleton v-for="i in 4" :key="i" animated>
            <template #template>
              <el-skeleton-item variant="image" style="height:180px;border-radius:12px 12px 0 0;" />
              <div style="padding:16px;">
                <el-skeleton-item variant="text" style="width:60%;margin-bottom:8px;" />
                <el-skeleton-item variant="text" style="width:80%;" />
              </div>
            </template>
          </el-skeleton>
        </div>
        <div v-else-if="foundItems.length" class="grid-4">
          <ItemCard v-for="item in foundItems" :key="item.id" :item="item" />
        </div>
        <div v-else class="empty-state">
          <div class="empty-state-icon">📭</div>
          <div class="empty-state-title">暂无失物招领信息</div>
          <router-link to="/publish?type=found" class="btn btn-primary" style="margin-top:16px;">发布第一条</router-link>
        </div>
      </section>

      <!-- Latest Lost -->
      <section class="section" style="padding-top:0;">
        <div class="section-header">
          <h2 class="section-title">最新寻物启事</h2>
          <router-link to="/lost" class="btn btn-secondary btn-sm">查看全部 →</router-link>
        </div>
        <div v-if="lostLoading" class="grid-4">
          <el-skeleton v-for="i in 4" :key="i" animated>
            <template #template>
              <el-skeleton-item variant="image" style="height:180px;border-radius:12px 12px 0 0;" />
              <div style="padding:16px;">
                <el-skeleton-item variant="text" style="width:60%;margin-bottom:8px;" />
                <el-skeleton-item variant="text" style="width:80%;" />
              </div>
            </template>
          </el-skeleton>
        </div>
        <div v-else-if="lostItems.length" class="grid-4">
          <ItemCard v-for="item in lostItems" :key="item.id" :item="item" />
        </div>
        <div v-else class="empty-state">
          <div class="empty-state-icon">🔍</div>
          <div class="empty-state-title">暂无寻物启事</div>
        </div>
      </section>

      <!-- How it works -->
      <section class="section" style="padding-top:0;">
        <div class="section-header">
          <h2 class="section-title">使用流程</h2>
        </div>
        <div class="grid-4">
          <div class="how-step" v-for="step in steps" :key="step.num">
            <div class="how-step-num">{{ step.num }}</div>
            <div class="how-step-icon">{{ step.icon }}</div>
            <div class="how-step-title">{{ step.title }}</div>
            <div class="how-step-desc">{{ step.desc }}</div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { itemApi } from '@/api'
import ItemCard from '@/components/ItemCard.vue'

const router = useRouter()
const searchKeyword = ref('')
const stats = ref({})
const foundItems = ref([])
const lostItems = ref([])
const foundLoading = ref(true)
const lostLoading = ref(true)

const categories = [
  { name: '证件', icon: '🪪' },
  { name: '电子产品', icon: '📱' },
  { name: '书籍文具', icon: '📚' },
  { name: '钥匙', icon: '🔑' },
  { name: '钱包', icon: '👛' },
  { name: '衣物', icon: '👕' },
  { name: '其他', icon: '📦' },
]

const steps = [
  { num: '01', icon: '📝', title: '发布信息', desc: '填写物品详情、地点、时间和联系方式' },
  { num: '02', icon: '🤖', title: '智能匹配', desc: 'AI 自动分析匹配可能的失物与寻物信息' },
  { num: '03', icon: '💬', title: '联系沟通', desc: '通过留言或联系方式与对方取得联系' },
  { num: '04', icon: '🎉', title: '找回物品', desc: '确认归还，完成失物招领全流程' },
]

function goSearch() {
  if (searchKeyword.value.trim()) {
    router.push({ path: '/search', query: { keyword: searchKeyword.value } })
  }
}

async function loadData() {
  try {
    const [foundRes, lostRes] = await Promise.all([
      itemApi.list({ type: 'found', page_size: 4 }),
      itemApi.list({ type: 'lost', page_size: 4 }),
    ])
    foundItems.value = foundRes.data.results || []
    lostItems.value = lostRes.data.results || []
  } catch (e) {
    console.error(e)
  } finally {
    foundLoading.value = false
    lostLoading.value = false
  }
}

async function loadStats() {
  try {
    const { data } = await itemApi.adminStats()
    stats.value = data
  } catch {
    // stats not available for non-admin, use item counts
    try {
      const [f, l] = await Promise.all([
        itemApi.list({ type: 'found' }),
        itemApi.list({ type: 'lost' }),
      ])
      stats.value = { found_count: f.data.count, lost_count: l.data.count }
    } catch {}
  }
}

onMounted(() => {
  loadData()
  loadStats()
})
</script>

<style scoped>
.quick-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: -40px 0 0; position: relative; z-index: 10; }
.quick-action-card { display: flex; align-items: center; gap: 16px; padding: 24px 28px; border-radius: var(--radius-lg); text-decoration: none; transition: all .2s; box-shadow: var(--shadow-lg); }
.found-card { background: linear-gradient(135deg, #ecfdf5, #d1fae5); border: 2px solid #a7f3d0; }
.found-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-xl); }
.lost-card { background: linear-gradient(135deg, #fff1f2, #fee2e2); border: 2px solid #fecaca; }
.lost-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-xl); }
.quick-action-icon { font-size: 36px; }
.quick-action-title { font-size: 18px; font-weight: 700; color: var(--text-primary); }
.quick-action-desc { font-size: 13px; color: var(--text-secondary); margin-top: 4px; }
.how-step { background: white; border-radius: var(--radius); padding: 28px 24px; text-align: center; box-shadow: var(--shadow-sm); border: 1px solid var(--border); }
.how-step-num { font-size: 13px; font-weight: 700; color: var(--primary); background: #eff6ff; display: inline-block; padding: 4px 12px; border-radius: 20px; margin-bottom: 12px; }
.how-step-icon { font-size: 36px; margin-bottom: 12px; }
.how-step-title { font-size: 16px; font-weight: 600; color: var(--text-primary); margin-bottom: 8px; }
.how-step-desc { font-size: 13px; color: var(--text-secondary); line-height: 1.6; }
@media (max-width: 768px) { .quick-actions { grid-template-columns: 1fr; } }
</style>
