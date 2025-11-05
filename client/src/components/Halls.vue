<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const halls = ref([])
const name = ref('')
const group_id = ref(null)

async function loadHalls() {
  const r = await axios.get('/api/halls/')
  halls.value = r.data
}

async function createHall() {
  await axios.post('/api/halls/', { name, group_id })
  name.value = ''
  group_id.value = null
  await loadHalls()
}

async function deleteHall(id) {
  await axios.delete(`/api/halls/${id}/`)
  await loadHalls()
}

onBeforeMounted(loadHalls)
</script>

<template>
  <div>
    <h2>Halls</h2>
    <input v-model="name" placeholder="Название">
    <input v-model.number="group_id" placeholder="Group ID">
    <button @click="createHall">Добавить</button>

    <ul>
      <li v-for="h in halls" :key="h.id">
        {{ h.name }} (Group: {{ h.group?.name }})
        <button @click="deleteHall(h.id)">Удалить</button>
      </li>
    </ul>
  </div>
</template>
