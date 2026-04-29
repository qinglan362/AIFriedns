<script setup>
import {onMounted, ref} from "vue";
import api from "@/js/http/api.js";

const characters = ref([])

const props = defineProps(['characterId'])
const characterId = ref(props.characterId)

onMounted(async () => {
  try {
    const res = await api.get('/api/knowledge/get_one_character_all/', {
      params: {
        character_id: characterId.value,
      }
    })
    const data = res.data
    console.log(data)
    if (data.result === 'success') {
      characters.value = data.knowledges
    }
  } catch (err) {
  }
})

// 格式化函数
function formatTime(isoStr) {
  const date = new Date(isoStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}
async function  deleteItem(knowledgeId){
  console.log(knowledgeId)
  try {
    const res = await  api.post('/api/knowledge/delete_one_knowledge/', {
        knowledge_id: knowledgeId,
    })
    const data = res.data
    console.log(data)
  } catch (err) {
  }
}

</script>

<template>
  <ul class="list bg-base-100 rounded-box shadow-md">

    <li class="p-4 pb-2 text-xs opacity-60 tracking-wide">该角色所有知识库文件</li>

    <li class="list-row" v-for="(item, index) in characters" :key="item.id">
      <div class="text-4xl font-thin opacity-30 tabular-nums">{{ String(index + 1).padStart(2, '0') }}</div>
      <div><img class="size-10 rounded-box" :src="item.character.photo"/></div>
      <div class="list-col-grow">
        <div>{{ item.knowledge.fileName }}{{item.knowledge.fileType}}</div>
        <div class="text-xs uppercase font-semibold opacity-60">{{ formatTime(item.knowledge.createTime) }}</div>
      </div>
      <button class="btn btn-sm btn-circle btn-ghost" @click="deleteItem(item.id)">✕</button>
    </li>
  </ul>
</template>

<style scoped>

</style>