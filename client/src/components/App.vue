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
  <div>
    Я VUE
    {{ userInfo }}

    <nav class="d-flex align-items-center" style="padding: 8px; justify-content: space-between;">
      <div class="d-flex" style="gap: 8px">
        <router-link to="/">Главная</router-link>
        <router-link to="/artifacts">Экспонаты</router-link>
        <router-link to="/curators">Экскурсоводы</router-link>
        <router-link to="/exhibitions">Экскурсии</router-link>
        <router-link to="/halls">Выставки</router-link>
      </div>

      <div class="d-flex" style="gap: 8px; align-items: center;">
        <router-link
          to="/admin"
          class="btn btn-outline-secondary btn-sm"
        >
          Вход в админку
        </router-link>

        <button
          @click="onLogout"
          v-if="is_authenticated"
          class="btn btn-danger btn-sm"
        >
          Выйти
        </button>
      </div>
    </nav>

    <router-view />
  </div>
</template>
