<template>
  <div class="card item-card" @click="$router.push(`/items/${item.id}`)">
    <img v-if="item.first_image" :src="item.first_image" class="item-img" :alt="item.title" />
    <div v-else class="item-img-placeholder">{{ categoryIcon }}</div>
    <div class="item-info">
      <div style="display:flex;gap:6px;margin-bottom:8px;">
        <span class="badge" :class="item.type === 'found' ? 'badge-found' : 'badge-lost'">
          {{ item.type === 'found' ? '🟢 失物招领' : '🔴 寻物启事' }}
        </span>
        <span class="badge badge-active">{{ item.category }}</span>
      </div>
      <div class="item-title">{{ item.title }}</div>
      <div class="item-meta" style="margin-bottom:4px;">
        <el-icon><Location /></el-icon> {{ item.location }}
      </div>
      <div class="item-meta">
        <el-icon><Clock /></el-icon> {{ formatDate(item.happened_at) }}
      </div>
    </div>
    <div class="item-footer">
      <span style="font-size:13px;color:var(--text-muted);">
        <el-icon><View /></el-icon> {{ item.view_count }}
      </span>
      <span style="font-size:12px;color:var(--text-muted);">{{ formatRelative(item.created_at) }}</span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ item: Object })

const CATEGORY_ICONS = {
  '证件': '🪪', '电子产品': '📱', '书籍文具': '📚',
  '钥匙': '🔑', '钱包': '👛', '衣物': '👕', '其他': '📦'
}

const categoryIcon = computed(() => CATEGORY_ICONS[props.item?.category] || '📦')

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
</script>

<script>
import { computed } from 'vue'
</script>
