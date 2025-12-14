<script setup>
import { ref, computed , onBeforeMount, onMounted} from 'vue'
import axios from 'axios'
import { useUserInfoStore } from '../stores/user_info_store';
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router';


const router=useRouter();
const userInfoStore=useUserInfoStore();
const username=ref();
const password=ref();
const{
  is_authenticated
}=storeToRefs(userInfoStore)

async function onLoginFormSubmit(){
  const r = await axios.post("/api/users/login/",{
      username:username.value,
      password:password.value,
  })
  username.value='';
  password.value='';
  await userInfoStore.fetchUserInfo()
  if(is_authenticated.value){
    router.push("/home")
  }
}

</script>

<template>
  <div>
  <form  @submit.stop.prevent="onLoginFormSubmit" class="form d-flex flex-column" style="gap: 8px">
  <input placeholder="логин" class="form-control" type="text" v-model="username">
  <input placeholder="пароль" class="form-control" type="password" v-model="password">
  <button class="btn btn-info">Войти</button>

</form>
  </div>
</template>