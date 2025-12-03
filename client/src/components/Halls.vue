<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

const halls = ref([])
const name = ref('')
const group_id = ref(null)
const hallPictureRef = ref()
const hallAddImageUrl = ref('')
const isLoading = ref(false)
const editingHallId = ref(null)


async function loadHalls() {
  try {
    const r = await axios.get('http://127.0.0.1:8000/api/halls/')
    const data = Array.isArray(r.data.results) ? r.data.results : r.data
    halls.value = data.filter(h => h && h.name)
  } catch (error) {
    console.error('Ошибка загрузки залов:', error)
  }
}


async function saveHall() {
  if (!name.value) { 
    alert('Введите название'); 
    return 
  }

  isLoading.value = true
  try {
    const formData = new FormData()
    formData.append('name', name.value)
    if (group_id.value !== null && group_id.value !== '') {
      formData.append('group_id', group_id.value)
    }

    if (hallPictureRef.value?.files[0]) {
      formData.append('picture', hallPictureRef.value.files[0])
    }

    if (editingHallId.value) {
      await axios.put(`http://127.0.0.1:8000/api/halls/${editingHallId.value}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    } else {
      await axios.post('http://127.0.0.1:8000/api/halls/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    }

    resetForm()
    await loadHalls()
  } catch (error) {
    console.error('Ошибка сохранения холла:', error)
    if (error.response?.data) console.error('Response data:', error.response.data)
    alert('Ошибка при сохранении (см. консоль)')
  } finally {
    isLoading.value = false
  }
}

// === удаление ===
async function deleteHall(id) {
  if (!confirm('Удалить этот зал?')) return
  try {
    await axios.delete(`http://127.0.0.1:8000/api/halls/${id}/`)
    await loadHalls()
  } catch (error) {
    console.error('Ошибка удаления холла:', error)
    alert('Ошибка при удалении холла')
  }
}

// === предпросмотр изображения ===
function hallAddPictureChange() {
  const file = hallPictureRef.value?.files[0]
  if (!file) { hallAddImageUrl.value = ''; return }

  if (!file.type.startsWith('image/')) { alert('Выберите изображение'); hallPictureRef.value.value = ''; return }
  if (file.size > 5*1024*1024) { alert('Максимальный размер — 5MB'); hallPictureRef.value.value=''; return }

  hallAddImageUrl.value = URL.createObjectURL(file)
}

// === редактирование ===
function editHall(h) {
  editingHallId.value = h.id
  name.value = h.name
  group_id.value = h.group?.id || null
  hallAddImageUrl.value = h.picture || ''
  if (hallPictureRef.value) hallPictureRef.value.value = ''
}

// === сброс формы ===
function resetForm() {
  editingHallId.value = null
  name.value = ''
  group_id.value = null
  hallAddImageUrl.value = ''
  if (hallPictureRef.value) hallPictureRef.value.value = ''
}

onBeforeMount(loadHalls)
</script>

<template>
  <div class="halls-page">
    <h1>Залы</h1>

    <form @submit.prevent="saveHall" class="hall-form">
      <input v-model="name" placeholder="Название зала *" required>
      <input v-model.number="group_id" placeholder="ID группы" type="number">
      <input type="file" ref="hallPictureRef" accept="image/*" @change="hallAddPictureChange">

      <button type="submit" :disabled="isLoading">{{ editingHallId ? 'Сохранить' : 'Добавить' }}</button>
      <button type="button" @click="resetForm" :disabled="isLoading" class="secondary">Очистить</button>
    </form>

    <div v-if="hallAddImageUrl" class="preview">
      <img :src="hallAddImageUrl" alt="Предпросмотр">
      <button @click="hallAddImageUrl = ''; hallPictureRef.value.value = ''">✕</button>
    </div>

    <div v-if="halls.length" class="halls-list">
      <div v-for="h in halls" :key="h?.id" class="hall-card">
        <div v-if="h?.picture">
          <img :src="h.picture" :alt="h.name" class="hall-image">
        </div>
        <div v-else class="no-image">
          📷 Нет изображения
        </div>
        <h3>{{ h.name }}</h3>
        <small>ID группы: {{ h.group?.name || h.group || '—' }}</small>
        <button @click="editHall(h)">Редактировать</button>
        <button @click="deleteHall(h.id)" class="delete">Удалить</button>
      </div>
    </div>

    <div v-else class="empty">
      <p>📭 Залов пока нет</p>
      <small>Добавьте первый зал</small>
    </div>
  </div>
</template>

<style scoped>
.halls-page {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
  font-family: system-ui, sans-serif;
  color: #333;
}

h1 {
  text-align: center;
  margin-bottom: 1.5rem;
}

.hall-form {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-bottom: 1.5rem;
}

.hall-form input {
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}

button {
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  background: #4f46e5;
  color: white;
  font-weight: 500;
  transition: 0.2s;
}

button:hover {
  background: #4338ca;
}

button.secondary {
  background: #e5e7eb;
  color: #333;
}

button.secondary:hover {
  background: #d1d5db;
}

.preview {
  text-align: center;
  margin-bottom: 1rem;
}

.preview img {
  max-width: 200px;
  border-radius: 8px;
  margin-right: 0.5rem;
}

.halls-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}

.hall-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 0.75rem;
  text-align: center;
  background: #fafafa;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.hall-image {
  width: 100%;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  object-fit: cover;
  height: 150px;
}

.no-image {
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f0f0;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.hall-card h3 {
  margin: 0.3rem 0;
  font-size: 1rem;
  flex-grow: 1;
}

.hall-card small {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
}

button.delete {
  background: #ef4444;
  margin-top: auto;
}

button.delete:hover {
  background: #dc2626;
}

.empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>
