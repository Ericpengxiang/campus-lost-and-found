<template>
  <div class="fade-in">
    <div class="page-container">
      <div class="page-header">
        <h1 class="page-title">{{ props.type === 'found' ? '🟢 失物招领' : '🔴 寻物启事' }}</h1>
        <p class="page-subtitle">{{ props.type === 'found' ? '以下是校园内捡到的物品，请认领' : '以下是同学们丢失的物品，请帮助找回' }}</p>
      </div>

      <!-- Filter Bar -->
      <div class="filter-bar">
        <el-select v-model="filters.category" placeholder="全部分类" clearable style="width:140px;" @change="loadItems(1)">
          <el-option v-for="c in categories" :key="c" :label="c" :value="c" />
        </el-select>
        <el-select v-model="filters.status" placeholder="全部状态" clearable style="width:120px;" @change="loadItems(1)">
          <el-option label="进行中" value="active" />
          <el-option label="已匹配" value="matched" />
          <el-option label="已关闭" value="closed" />
        </el-select>
        <el-input
          v-model="filters.keyword"
          placeholder="搜索关键词..."
          clearable
          style="width:220px;"
          @keyup.enter="loadItems(1)"
          @clear="loadItems(1)"
        >
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
        <el-button type="primary" @click="loadItems(1)">搜索</el-button>
        <div style="margin-left:auto;">
          <router-link :to="`/publish?type=${props.type}`">
            <el-button type="primary">
              <el-icon><Plus /></el-icon> 发布{{ props.type === 'found' ? '失物招领' : '寻物启事' }}
            </el-button>
          </router-link>
        </div>
      </div>

      <!-- Category Quick Filter -->
      <div class="category-quick">
        <span
          class="cat-tag"
          :class="{ active: !filters.category }"
          @click="filters.category = ''; loadItems(1)"
        >全部</span>
        <span
          v-for="c in categories" :key="c"
          class="cat-tag"
          :class="{ active: filters.category === c }"
          @click="filters.category = c; loadItems(1)"
        >{{ c }}</span>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="grid-4">
        <el-skeleton v-for="i in 8" :key="i" animated>
          <template #template>
            <el-skeleton-item variant="image" style="height:180px;border-radius:12px 12px 0 0;" />
            <div style="padding:16px;">
              <el-skeleton-item variant="text" style="width:60%;margin-bottom:8px;" />
              <el-skeleton-item variant="text" style="width:80%;" />
            </div>
          </template>
        </el-skeleton>
      </div>

      <!-- Items Grid -->
      <div v-else-if="items.length" class="grid-4">
        <ItemCard v-for="item in items" :key="item.id" :item="item" />
      </div>

      <!-- Empty -->
      <div v-else class="empty-state">
        <div class="empty-state-icon">{{ props.type === 'found' ? '📭' : '🔍' }}</div>
        <div class="empty-state-title">暂无{{ props.type === 'found' ? '失物招领' : '寻物启事' }}信息</div>
        <div class="empty-state-desc">成为第一个发布者吧！</div>
        <router-link :to="`/publish?type=${props.type}`" class="btn btn-primary" style="margin-top:20px;">
          立即发布
        </router-link>
      </div>

      <!-- Pagination -->
      <div class="pagination" v-if="total > pageSize">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="prev, pager, next"
          @current-change="loadItems"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { itemApi } from '@/api'
import ItemCard from '@/components/ItemCard.vue'

const props = defineProps({ type: { type: String, default: 'found' } })
const route = useRoute()

const items = ref([])
const loading = ref(true)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)

const filters = ref({
  category: route.query.category || '',
  keyword: route.query.keyword || '',
  status: '',
})

const categories = ['证件', '电子产品', '书籍文具', '钥匙', '钱包', '衣物', '其他']

async function loadItems(page = 1) {
  loading.value = true
  currentPage.value = page
  try {
    const params = {
      type: props.type,
      page,
      ...(filters.value.category && { category: filters.value.category }),
      ...(filters.value.keyword && { keyword: filters.value.keyword }),
      ...(filters.value.status && { status: filters.value.status }),
    }
    const { data } = await itemApi.list(params)
    items.value = data.results || []
    total.value = data.count || 0
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

watch(() => props.type, () => {
  filters.value = { category: '', keyword: '', status: '' }
  loadItems(1)
})

onMounted(() => loadItems(1))
</script>

<style scoped>
.category-quick { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
.cat-tag { padding: 6px 16px; border-radius: 20px; font-size: 13px; font-weight: 500; cursor: pointer; background: white; border: 1px solid var(--border); color: var(--text-secondary); transition: all .15s; }
.cat-tag:hover, .cat-tag.active { background: var(--primary); color: white; border-color: var(--primary); }
</style>
