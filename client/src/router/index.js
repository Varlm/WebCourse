import { createRouter, createWebHistory } from 'vue-router'
import Groups from '../components/Groups.vue'
import Artifacts from '../components/Artifacts.vue'
import Halls from '../components/Halls.vue'
import Curators from '../components/Curators.vue'
import Exhibitions from '../components/Exhibitions.vue'

const routes = [
  { path: '/groups', component: Groups },
  { path: '/artifacts', component: Artifacts },
  { path: '/halls', component: Halls },
  { path: '/curators', component: Curators },
  { path: '/exhibitions', component: Exhibitions },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
