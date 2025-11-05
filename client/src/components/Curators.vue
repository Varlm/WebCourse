<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const curators = ref([])
const user_id = ref(null)
const hall_id = ref(null)

async function loadCurators() {
  const r = await axios.get('/api/curators/')
  curators.value = r.data
}

async function createCurator() {
  await axios.post('/api/curators/', { user: user_id, hall_id })
  user_id.value = null
  hall_id.value = null
  await loadCurators()
}

async function deleteCurator(id) {
  await axios.delete(`/api/curators/${id}/`)
  await loadCurators()
}

onBeforeMounted(loadCurators)
</script>

<template>
  <div>
    <h2>Curators</h2>
    <input v-model.number="user_id" placeholder="User ID">
    <input v-model.number="hall_id" placeholder="Hall ID">
    <button @click="createCurator">Добавить</button>

    <ul>
      <li v-for="c in curators" :key="c.id">
        User: {{ c.user?.username }} (Hall: {{ c.hall?.name }})
        <button @click="deleteCurator(c.id)">Удалить</button>
      </li>
    </ul>
  </div>
</template>
