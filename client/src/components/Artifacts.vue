<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const artifacts = ref([])
const name = ref('')
const group_id = ref(null)

async function loadArtifacts() {
  const r = await axios.get('/api/museum/')
  artifacts.value = r.data
}

async function createArtifact() {
  await axios.post('/api/museum/', { name, group_id })
  name.value = ''
  group_id.value = null
  await loadArtifacts()
}

async function deleteArtifact(id) {
  await axios.delete(`/api/museum/${id}/`)
  await loadArtifacts()
}

onBeforeMounted(loadArtifacts)
</script>

<template>
  <div>
    <h2>Artifacts</h2>
    <input v-model="name" placeholder="Название">
    <input v-model.number="group_id" placeholder="Group ID">
    <button @click="createArtifact">Добавить</button>

    <ul>
      <li v-for="a in artifacts" :key="a.id">
        {{ a.name }} (Group: {{ a.group?.name }})
        <button @click="deleteArtifact(a.id)">Удалить</button>
      </li>
    </ul>
  </div>
</template>
