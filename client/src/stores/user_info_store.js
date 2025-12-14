
import { defineStore } from "pinia";
import axios from "axios";
import{ref,computed} from 'vue';
import Cookies from 'js-cookie';
import { onBeforeMount } from 'vue';
export const useUserInfoStore = defineStore("userInfoStore", ()=>{
  
  const userInfo = ref({});
  const username=ref();
  const is_authenticated=ref(false);
  async function fetchUserInfo(params) {
      const r = await axios.get("/api/users/my/");
      userInfo.value=r.data;
      username.value=r.data.username;
      is_authenticated.value=r.data.is_authenticated;
      axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
  }

  onBeforeMount(async()=>{    
    await fetchUserInfo();
  })
  
  return{
    fetchUserInfo,
    username,
    is_authenticated,
  }

});
