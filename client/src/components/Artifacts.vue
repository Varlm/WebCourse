<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'

// reactive state
const artifacts = ref([])
const name = ref('')
const group_id = ref(null)
const artifactPictureRef = ref()
const artifactAddImageUrl = ref('')
const isLoading = ref(false)
const editingArtifactId = ref(null)

// === загрузка списка артефактов ===
async function loadArtifacts() {
  try {
    const r = await axios.get('http://127.0.0.1:8000/api/museum/')
    const data = Array.isArray(r.data.results) ? r.data.results : r.data
    artifacts.value = data.filter(a => a && a.name)
  } catch (error) {
    console.error('Ошибка загрузки артефактов:', error)
  }
}

// === добавление / редактирование ===
async function saveArtifact() {
  if (!name.value) { alert('Введите название'); return }

  isLoading.value = true
  try {
    const formData = new FormData()
    formData.append('name', name.value)
    if (group_id.value !== null && group_id.value !== '') formData.append('group_id', group_id.value)
    if (artifactPictureRef.value?.files[0]) formData.append('picture', artifactPictureRef.value.files[0])

    if (editingArtifactId.value) {
      await axios.put(`http://127.0.0.1:8000/api/museum/${editingArtifactId.value}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    } else {
      await axios.post('http://127.0.0.1:8000/api/museum/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
    }

    resetForm()
    await loadArtifacts()
  } catch (error) {
    console.error('Ошибка сохранения артефакта:', error)
    alert('Ошибка при сохранении')
  } finally {
    isLoading.value = false
  }
}

// === удаление ===
async function deleteArtifact(id) {
  if (!confirm('Удалить этот артефакт?')) return
  try {
    await axios.delete(`http://127.0.0.1:8000/api/museum/${id}/`)
    await loadArtifacts()
  } catch (error) {
    console.error('Ошибка удаления артефакта:', error)
    alert('Ошибка при удалении')
  }
}

// === предпросмотр изображения ===
function artifactAddPictureChange() {
  const file = artifactPictureRef.value?.files[0]
  if (!file) { artifactAddImageUrl.value = ''; return }
  if (!file.type.startsWith('image/')) { alert('Выберите изображение'); artifactPictureRef.value.value=''; return }
  if (file.size > 5*1024*1024) { alert('Максимальный размер — 5MB'); artifactPictureRef.value.value=''; return }
  artifactAddImageUrl.value = URL.createObjectURL(file)
}

// === редактирование ===
function editArtifact(a) {
  editingArtifactId.value = a.id
  name.value = a.name
  group_id.value = a.group_id
  artifactAddImageUrl.value = a.picture || ''
  if (artifactPictureRef.value) artifactPictureRef.value.value = ''
}

// === сброс формы ===
function resetForm() {
  editingArtifactId.value = null
  name.value = ''
  group_id.value = null
  artifactAddImageUrl.value = ''
  if (artifactPictureRef.value) artifactPictureRef.value.value = ''
}

onBeforeMount(loadArtifacts)
</script>

<template>
  <div class="artifacts-page">
    <h1>Артефакты</h1>

    <!-- форма добавления / редактирования -->
    <form @submit.prevent="saveArtifact" class="artifact-form">
      <input v-model="name" placeholder="Название артефакта *" required>
      <input v-model.number="group_id" placeholder="ID группы" type="number">
      <input type="file" ref="artifactPictureRef" accept="image/*" @change="artifactAddPictureChange">

      <button type="submit" :disabled="isLoading">
        {{ editingArtifactId ? 'Сохранить' : 'Добавить' }}
      </button>
      <button type="button" @click="resetForm" :disabled="isLoading" class="secondary">Очистить</button>
    </form>

    <!-- предпросмотр -->
    <div v-if="artifactAddImageUrl" class="preview">
      <img :src="artifactAddImageUrl" alt="Предпросмотр">
      <button @click="artifactAddImageUrl=''; artifactPictureRef.value.value=''" class="secondary">✕</button>
    </div>

    <!-- список артефактов -->
    <div v-if="artifacts.length" class="artifacts-list">
      <div v-for="a in artifacts" :key="a?.id" class="artifact-card">
        <div v-if="a?.picture">
          <img :src="a.picture" :alt="a.name" class="artifact-image">
        </div>
        <div v-else class="no-image">
          📷 Нет изображения
        </div>
        <h3>{{ a.name }}</h3>
        <small>ID группы: {{ a.group?.name || a.group_id || '—' }}</small>
        <button @click="editArtifact(a)">Редактировать</button>
        <button @click="deleteArtifact(a.id)" class="delete">Удалить</button>
      </div>
    </div>

    <div v-else class="empty">
      <p>📭 Артефактов пока нет</p>
      <small>Добавьте первый артефакт</small>
    </div>
  </div>
</template>

<style scoped>
.artifacts-page {
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

.artifact-form {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-bottom: 1.5rem;
}

.artifact-form input {
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

button:hover { background: #4338ca; }
button.secondary {
  background: #e5e7eb;
  color: #333;
}
button.secondary:hover { background: #d1d5db; }

.preview {
  text-align: center;
  margin-bottom: 1rem;
}
.preview img { max-width: 200px; border-radius: 8px; margin-right: 0.5rem; }

.artifacts-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
}

.artifact-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 0.75rem;
  text-align: center;
  background: #fafafa;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.artifact-image {
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

.artifact-card h3 {
  margin: 0.3rem 0;
  font-size: 1rem;
  flex-grow: 1;
}

.artifact-card small {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
}

.artifact-card button {
  margin-top: 0.3rem;
}

button.delete {
  background: #ef4444;
}
button.delete:hover { background: #dc2626; }

.empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>
