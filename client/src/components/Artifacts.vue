<script setup>
import { ref, computed , onBeforeMount, onMounted} from 'vue'
import axios from 'axios'
import { useUserInfoStore } from '../stores/user_info_store';
import { storeToRefs } from 'pinia'

const userInfoStore=useUserInfoStore();
const{
  username
}=storeToRefs(userInfoStore)

</script>

<template>
  <div>
    <h1>Страница артефактов</h1>
    {{username }}
  </div>
</template>