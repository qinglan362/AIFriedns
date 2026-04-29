<script setup>
import Photo from "@/views/create/character/components/Photo.vue";
import Name from "@/views/create/character/components/Name.vue";
import Profile from "@/views/create/character/components/Profile.vue";
import BackgroundImage from "@/views/create/character/components/BackgroundImage.vue";
import {onMounted, ref, useTemplateRef} from "vue";
import {base64ToFile} from "@/js/utils/base64_to_file.js";
import api from "@/js/http/api.js";
import {useRoute, useRouter} from "vue-router";
import {useUserStore} from "@/stores/user.js";
import ModelChoose from "@/views/create/character/components/ModelChoose.vue";
import AddKnowledge from "@/views/create/character/components/AddKnowledge.vue";
import ShowAllKnowledge from "@/views/create/character/components/ShowAllKnowledge.vue";

const user = useUserStore()
const router = useRouter()
const route = useRoute()
const characterId = route.params.character_id
const character = ref(null)

onMounted(async () => {
  try {
    const res = await api.get('/api/create/character/get_single/', {
      params: {
        character_id: characterId,
      }
    })
    const data = res.data
    if (data.result === 'success') {
      character.value = data.character
    }
  } catch (err) {
  }
})

const photoRef = useTemplateRef('photo-ref')
const nameRef = useTemplateRef('name-ref')
const profileRef = useTemplateRef('profile-ref')
const backgroundImageRef = useTemplateRef('background-image-ref')
const modelRef = useTemplateRef('model-ref')
const knowledgeFileRef=useTemplateRef('knowledge-file-ref')


const errorMessage = ref('')

async function handleUpdate() {
  const photo = photoRef.value.myPhoto
  const name = nameRef.value.myName?.trim()
  const profile = profileRef.value.myProfile?.trim()
  const backgroundImage = backgroundImageRef.value.myBackgroundImage
  const model = modelRef.value.myModel
  const knowledgeFile=knowledgeFileRef.value.selectedFile


  errorMessage.value = ''
  if (!photo) {
    errorMessage.value = '头像不能为空'
  } else if (!name) {
    errorMessage.value = '名字不能为空'
  } else if (!profile) {
    errorMessage.value = '角色介绍不能为空'
  } else if (!backgroundImage) {
    errorMessage.value = '聊天背景不能为空'
  } else {
    const formData = new FormData()
    formData.append('character_id', characterId)
    formData.append('name', name)
    formData.append('profile', profile)
    formData.append('knowledgeFile',knowledgeFile)

    if (photo !== character.value.photo) {
      formData.append('photo', base64ToFile(photo, 'photo.png'))
    }

    if (backgroundImage !== character.value.background_image) {
      formData.append('background_image', base64ToFile(backgroundImage, 'background_image.png'))
    }

    formData.append('model', model)

    try {
      const res = await api.post('/api/create/character/update/', formData)
      const data = res.data
      if (data.result === 'success') {
        await router.push({
          name: 'user-space-index',
          params: {
            user_id: user.id,
          }
        })
      } else {
        errorMessage.value = data.result
      }
    } catch (err) {
    }
  }
}
const handleManageAllKnowledge = useTemplateRef('handleManageAllKnowledge')
function  show(){
  handleManageAllKnowledge.value.showModal()
}
</script>

<template>
  <div v-if="character" class="flex justify-center">
    <div class="card w-120 bg-base-200 shadow-sm mt-16">
      <div class="card-body">
        <h3 class="text-lg font-bold my-4">更新角色</h3>
        <Photo ref="photo-ref" :photo="character.photo" />
        <Name ref="name-ref" :name="character.name" />
        <Profile ref="profile-ref" :profile="character.profile" />


        <div class="flex items-center gap-15 my-4">
          <BackgroundImage ref="background-image-ref" :backgroundImage="character.background_image" />
          <div>
            <ModelChoose ref="model-ref" :model="character.model"  class="w-120"/>
            <add-knowledge ref="knowledge-file-ref"/>
            <button  class="btn btn-neutral w-80 mt-2" @click="show">管理知识库</button>
            <dialog ref="handleManageAllKnowledge" class="modal">
              <div class="modal-box">
                <form method="dialog">
                  <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
                </form>
                <ShowAllKnowledge :characterId="characterId"/>
              </div>
            </dialog>
          </div>
        </div>


        <p v-if="errorMessage" class="text-sm text-red-500">{{ errorMessage }}</p>

        <div class="flex justify-center">
          <button @click="handleUpdate" class="btn btn-neutral w-60 mt-2">更新</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
