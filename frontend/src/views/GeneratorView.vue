<!-- src/views/GeneratorView.vue -->
<template>
  <div class="max-w-2xl mx-auto p-6">
    <h1 class="text-2xl font-bold text-center mb-6">AI 自媒体标题生成器</h1>

    <div class="mb-4">
      <label class="block mb-2 text-sm font-medium">关键词</label>
      <input
        v-model="keyword"
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="例如：减脂餐、副业、AI工具"
        @keyup.enter="generate"
      />
    </div>

    <div class="mb-6">
      <label class="block mb-2 text-sm font-medium">平台</label>
      <select
        v-model="platform"
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="xiaohongshu">小红书</option>
        <option value="douyin">抖音</option>
        <option value="gongzhonghao">公众号</option>
      </select>
    </div>

    <button
      @click="generate"
      :disabled="loading"
      class="w-full py-2.5 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 transition"
    >
      {{ loading ? '生成中...' : '🚀 生成爆款标题' }}
    </button>

    <!-- 结果展示 -->
    <div v-if="titles.length" class="mt-8">
      <h2 class="font-semibold mb-3">生成结果（点击复制）：</h2>
      <ul class="space-y-2">
        <li
          v-for="(title, index) in titles"
          :key="index"
          @click="copyTitle(title)"
          class="p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition break-words"
        >
          {{ title }}
        </li>
      </ul>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="mt-4 p-3 text-red-600 bg-red-50 rounded-lg">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const keyword = ref('')
const platform = ref('xiaohongshu')
const titles = ref([])
const loading = ref(false)
const error = ref('')

const generate = async () => {
  if (!keyword.value.trim()) {
    error.value = '请输入关键词'
    return
  }

  loading.value = true
  error.value = ''
  titles.value = []

  try {
    // 调用本地 FastAPI 后端（开发环境）
    const response = await fetch('http://localhost:8000/api/v1/titles', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        keyword: keyword.value.trim(),
        platform: platform.value
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${await response.text()}`)
    }

    const data = await response.json()
    titles.value = data.titles?.filter(t => t.trim()) || []
  } catch (err) {
    console.error(err)
    error.value = '生成失败，请检查后端是否运行'
  } finally {
    loading.value = false
  }
}

const copyTitle = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    // 可加一个 toast 提示（MVP 可省略）
  } catch (err) {
    alert('复制失败，请手动复制')
  }
}
</script>
