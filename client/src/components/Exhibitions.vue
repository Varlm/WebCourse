<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const exhibitions = ref([])
const title = ref('')
const date = ref('')

async function loadExhibitions() {
  const r = await axios.get('/api/exhibitions/')
  exhibitions.value = r.data
}

async function createExhibition() {
  await axios.post('/api/exhibitions/', { title, date })
  title.value = ''
  date.value = ''
  await loadExhibitions()
}

async function deleteExhibition(id) {
  await axios.delete(`/api/exhibitions/${id}/`)
  await loadExhibitions()
}

onBeforeMounted(loadExhibitions)
</script>

<template>
  <div>
    <h2>Exhibitions</h2>
    <input v-model="title" placeholder="Название выставки">
    <input type="date" v-model="date" placeholder="Дата">
    <button @click="createExhibition">Добавить</button>

    <ul>
      <li v-for="e in exhibitions" :key="e.id">
        {{ e.title }} ({{ e.date }})
        <button @click="deleteExhibition(e.id)">Удалить</button>
      </li>
    </ul>
  </div>
</template>
