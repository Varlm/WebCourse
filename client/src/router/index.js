import { createRouter, createWebHistory } from 'vue-router'
import Artifacts from '../components/Artifacts.vue';
import Curators from '../components/Curators.vue';
import Exhibitions from '../components/Exhibitions.vue';
import Halls from '../components/Halls.vue';
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
      path:"/curators",
      component: Curators
    },
    {
      path:"/exhibitions",
      component: Exhibitions
    },
    {
      path:"/halls",
      component: Halls
    },
    {
      path:"/artifacts",
      component: Artifacts
    }
   ],
  })


  router.beforeEach(async (to) => {
  const userInfoStore = useUserInfoStore();

 
  if (userInfoStore.is_authenticated === false) {
      await userInfoStore.fetchUserInfo();
  }
  if (!userInfoStore.is_authenticated && to.name !== 'Login') {
    return { name: 'Login' }
  }
})
export default router
