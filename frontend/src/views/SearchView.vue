<template>
  <div class="fade-in">
    <div class="page-container">
      <div class="page-header">
        <h1 class="page-title">🔍 搜索物品</h1>
      </div>

      <div class="search-box">
        <el-input
          v-model="keyword"
          placeholder="输入物品名称、描述或地点..."
          size="large"
          clearable
          @keyup.enter="doSearch"
          @clear="doSearch"
        >
          <template #prefix><el-icon style="font-size:18px;"><Search /></el-icon></template>
          <template #append>
            <el-button type="primary" @click="doSearch">搜索</el-button>
          </template>
        </el-input>
      </div>

      <div class="filter-bar" style="margin-top:16px;">
        <span style="font-size:14px;color:var(--text-secondary);">类型：</span>
        <span class="cat-tag" :class="{ active: typeFilter === '' }" @click="typeFilter = ''; doSearch()">全部</span>
        <span class="cat-tag" :class="{ active: typeFilter === 'found' }" @click="typeFilter = 'found'; doSearch()">失物招领</span>
        <span class="cat-tag" :class="{ active: typeFilter === 'lost' }" @click="typeFilter = 'lost'; doSearch()">寻物启事</span>
        <span style="font-size:14px;color:var(--text-secondary);margin-left:12px;">分类：</span>
        <span class="cat-tag" :class="{ active: catFilter === '' }" @click="catFilter = ''; doSearch()">全部</span>
        <span v-for="c in categories" :key="c" class="cat-tag" :class="{ active: catFilter === c }" @click="catFilter = c; doSearch()">{{ c }}</span>
      </div>

      <div v-if="searched" style="margin-bottom:16px;color:var(--text-secondary);font-size:14px;">
        共找到 <strong style="color:var(--primary);">{{ total }}</strong> 条结果
        <span v-if="keyword">（关键词：{{ keyword }}）</span>
      </div>

      <div v-if="loading" class="grid-4">
        <el-skeleton v-for="i in 8" :key="i" animated>
          <template #template>
            <el-skeleton-item variant="image" style="height:180px;border-radius:12px 12px 0 0;" />
            <div style="padding:16px;"><el-skeleton-item variant="text" /></div>
          </template>
        </el-skeleton>
      </div>

      <div v-else-if="items.length" class="grid-4">
        <ItemCard v-for="item in items" :key="item.id" :item="item" />
      </div>

      <div v-else-if="searched" class="empty-state">
        <div class="empty-state-icon">🔍</div>
        <div class="empty-state-title">未找到相关物品</div>
        <div class="empty-state-desc">尝试更换关键词或分类</div>
      </div>

      <div v-else class="empty-state">
        <div class="empty-state-icon">🔎</div>
        <div class="empty-state-title">输入关键词开始搜索</div>
        <div class="empty-state-desc">支持按物品名称、描述、地点搜索</div>
      </div>

      <div class="pagination" v-if="total > 12">
        <el-pagination v-model:current-page="page" :page-size="12" :total="total" layout="prev, pager, next" @current-change="doSearch" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { itemApi } from '@/api'
import ItemCard from '@/components/ItemCard.vue'

const route = useRoute()
const keyword = ref(route.query.keyword || '')
const typeFilter = ref('')
const catFilter = ref('')
const items = ref([])
const loading = ref(false)
const searched = ref(false)
const total = ref(0)
const page = ref(1)

const categories = ['证件', '电子产品', '书籍文具', '钥匙', '钱包', '衣物', '其他']

async function doSearch(p = 1) {
  if (typeof p === 'number') page.value = p
  loading.value = true
  searched.value = true
  try {
    const params = { page: page.value }
    if (keyword.value) params.keyword = keyword.value
    if (typeFilter.value) params.type = typeFilter.value
    if (catFilter.value) params.category = catFilter.value
    const { data } = await itemApi.list(params)
    items.value = data.results || []
    total.value = data.count || 0
  } catch {} finally { loading.value = false }
}

onMounted(() => {
  if (keyword.value) doSearch()
})
</script>

<style scoped>
.search-box { max-width: 700px; margin: 0 auto 24px; }
.cat-tag { padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 500; cursor: pointer; background: white; border: 1px solid var(--border); color: var(--text-secondary); transition: all .15s; }
.cat-tag:hover, .cat-tag.active { background: var(--primary); color: white; border-color: var(--primary); }
</style>
