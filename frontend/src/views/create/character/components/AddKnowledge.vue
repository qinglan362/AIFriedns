<script setup>
import { ref } from 'vue'

// 绑定选中的文件
const selectedFile = ref(null)

// 文件选择变化时触发
const handleFileChange = (e) => {
  const file = e.target.files[0]
  if (!file) return

  const exts = ['.txt', '.pdf', '.docx']
  const isAllow = exts.some(ext => file.name.toLowerCase().endsWith(ext))
  if (!isAllow) {
    alert('仅支持 txt / pdf / docx 格式')
    selectedFile.value = null
    return
  }
  // 保存到 ref
  selectedFile.value = file
}

// 清空文件（可选）
const clearFile = () => {
  selectedFile.value = null
  document.querySelector('.file-input').value = ''
}
defineExpose({
  selectedFile,
})
</script>

<template>
  <fieldset class="fieldset  h-25">
    <legend class="fieldset-legend">添加知识库</legend>
    <input
        id="file-upload"
        type="file"
        class="file-input"
        accept=".txt,.pdf,.docx"
        @change="handleFileChange"
    />
    <div class="flex items-center gap-4">
      <label for="file-upload" class="label">txt, word, pdf</label>
      <div v-if="selectedFile" class="file-name">
        已选择：{{ selectedFile.name }}
        <button class="btn ml-4 bg-red-400 btn-xs" @click="clearFile">清空</button>
      </div>
    </div>
  </fieldset>
</template>

<style scoped>

</style>