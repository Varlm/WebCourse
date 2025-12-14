import { createRouter, createWebHistory } from 'vue-router'
import Artifacts from '../components/Artifacts.vue';
import Login from '../components/Login.vue';
import Home from '../components/Home.vue';
import { useUserInfoStore } from '@/stores/user_info_store';

const router = createRouter({
   history:createWebHistory(import.meta.env.BASE_URL),
   routes:[
    {
      path:"/home",
      component: Home
    },
    {
      path:"/login",
      name: "Login",
      component: Login
    },
    {
      path:"/artifacts",
      component: Artifacts
    }
   ],
  })


  router.beforeEach((to,from)=>{
    const userInfoStore=useUserInfoStore();
    if(!userInfoStore.is_authenticated && to.name!='Login'){
      return{name:'Login'}

    }


  })
export default router
