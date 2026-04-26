<script setup>
import Photo from "@/views/user/profile/components/Photo.vue";
import Username from "@/views/user/profile/components/Username.vue";
import Profile from "@/views/user/profile/components/Profile.vue";
import {useUserStore} from "@/stores/user.js";
import {ref, useTemplateRef} from "vue";
import {base64ToFile} from "@/js/utils/base64_to_file.js";
import api from "@/js/http/api.js";

const user = useUserStore()

const photoRef = useTemplateRef('photo-ref')
const usernameRef = useTemplateRef('username-ref')
const profileRef = useTemplateRef('profile-ref')
const errorMessage = ref('')

// 控制成功提示框显示/隐藏
const showSuccess = ref(false)

async function handleUpdate() {
  const photo = photoRef.value.myPhoto
  const username = usernameRef.value.myUsername.trim()
  const profile = profileRef.value.myProfile.trim()

  errorMessage.value = ''
  if (!photo) {
    errorMessage.value = '头像不能为空'
  } else if (!username) {
    errorMessage.value = '用户名不能为空'
  } else if (!profile) {
    errorMessage.value = '简介不能为空'
  } else {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('profile', profile)
    if (photo !== user.photo) {
      formData.append('photo', base64ToFile(photo, 'photo.png'))
    }
    try {
      const res = await api.post('/api/user/profile/update/', formData)
      const data = res.data
      if (data.result === 'success') {
        user.setUserInfo(data)
        // 显示成功提示
        showSuccess.value = true
        // 2秒后自动隐藏提示框
        setTimeout(() => {
          showSuccess.value = false
        }, 2000)
      } else {
        errorMessage.value = data.result
      }
    } catch (err) {
      console.log(err)
    }
  }
}

// 手动关闭提示
const closeSuccessTip = () => {
  showSuccess.value = false
}

</script>

<template>
  <div class="flex justify-center">
    <div class="card w-120 bg-base-200 shadow-sm mt-16">
      <div class="card-body">
        <h3 class="text-lg font-bold my-4">编辑资料</h3>
        <Photo ref="photo-ref" :photo="user.photo" />
        <Username ref="username-ref" :username="user.username" />
        <Profile ref="profile-ref" :profile="user.profile" />

        <p v-if="errorMessage" class="text-sm text-red-500">{{ errorMessage }}</p>


        <div class="flex justify-center">
          <button @click="handleUpdate" class="btn btn-neutral w-60 mt-2">更新</button>

          <!-- 悬浮提示：在整个卡片正中央（模态框效果） -->
        <div
              v-if="showSuccess"
              class="absolute inset-0 bg-black/5 backdrop-blur-sm flex items-center justify-center z-50"
          >
            <div role="alert" class="alert alert-success w-[80%] shadow-lg relative">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 shrink-0 stroke-current" fill="none" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>资料修改成功！</span>

              <!-- 右上角关闭叉 -->
              <button
                  @click="closeSuccessTip"
                  class="absolute top-2 right-2 btn btn-ghost btn-sm rounded-full h-6 w-6 p-0"
              >
                ✕
              </button>
            </div>
        </div>

        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
