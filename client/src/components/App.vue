<script setup>
import { ref, computed , onBeforeMount} from 'vue'
import axios from 'axios'
import { useUserInfoStore } from '../stores/user_info_store';
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router';


const router=useRouter();
axios.defaults.withCredentials = true

const userInfoStore=useUserInfoStore();
const username=ref();
const password=ref();
const{
  is_authenticated
}=storeToRefs(userInfoStore)





async function onLogout(params) {
    const r = await axios.post("/api/users/logout/")
    userInfoStore.fetchUserInfo()
    router.push("/login");
}



</script>


<template>
Я VUE
{{ userInfo }}

  <nav class="d-flex" style="padding: 8px; justify-content: space-between;">
    <div class="d-flex" style="gap: 8px">
    <router-link to="/">Главная</router-link>
    <router-link to="/artifacts" >Страница 1</router-link>
    </div>

    <button @click="onLogout" v-if="is_authenticated">Выйти</button>
  </nav>

<router-view />

</template>
