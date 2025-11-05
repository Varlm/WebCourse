<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const groups = ref([])
const name = ref('')

async function loadGroups() {
  const r = await axios.get('/api/groups/')
  groups.value = r.data
}

async function createGroup() {
  await axios.post('/api/groups/', { name: name.value })
  name.value = ''
  await loadGroups()
}

async function deleteGroup(id) {
  await axios.delete(`/api/groups/${id}/`)
  await loadGroups()
}

onBeforeMounted(loadGroups)
</script>

<template>
  <div>
    <h2>Groups</h2>
    <input v-model="name" placeholder="Название">
    <button @click="createGroup">Добавить</button>
    
    <ul>
      <li v-for="g in groups" :key="g.id">
        {{ g.name }}
        <button @click="deleteGroup(g.id)">Удалить</button>
      </li>
    </ul>
  </div>
</template>
