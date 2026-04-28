<script setup>
import {ref, watch} from "vue";

const props = defineProps(['model'])

const myModel = ref(props.model)

watch(() => props.model, newVal => {
  myModel.value = newVal
})

defineExpose({
  myModel,
})

</script>

<template>
  <fieldset  class="fieldset">
    <legend class="fieldset-legend">模型选择</legend>
    <select  v-model="myModel"  class="select">
      <option value="deepseek-v4-flash" >deepseek-v4-flash</option>
      <option value="qwen3.6-plus">qwen3.6-plus</option>
      <option value="kimi-k2.6">kimi-k2.6</option>
      <option value="glm-5.1">glm-5.1</option>
      <option value="MiniMax-M2.5">MiniMax-M2.5</option>
    </select>
  </fieldset>
</template>

<style scoped>

</style>