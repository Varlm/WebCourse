<script setup>
import { ref, computed , onBeforeMount, onMounted} from 'vue'
import axios from 'axios'
import { useUserInfoStore } from '../stores/user_info_store';
import { storeToRefs } from 'pinia'


const groups = ref([]); 
const halls = ref([]);
const hallToAdd = ref({});
const userInfoStore=useUserInfoStore();
const hallToEdit = ref({});
const hallPictureRef = ref();
const hallAddImageUrl=ref()
const imagePreviewUrl = ref(null);
const imagePreviewTitle = ref('');
const hallEditPictureRef = ref();
const hallEditImageUrl = ref();
const users = ref([])
const selectedUser = ref(null)
const stats = ref({}) 

function hallEditPictureChange() {
  if (hallEditPictureRef.value?.files?.[0]) {
    hallEditImageUrl.value = URL.createObjectURL(hallEditPictureRef.value.files[0]);
  } else {
    hallEditImageUrl.value = null;
  }
}
const loading = ref(false)
const{
  username,
  is_superuser
}=storeToRefs(userInfoStore)

const groupDict = computed(() => {
  const dict = {}
  for (const g of groups.value) {
    dict[g.id] = g.name
  }
  return dict
})

async function fetchHalls() {
  loading.value = true;

  const params = {};
  if (is_superuser.value) {
    if (selectedUser.value) {
      params.user = selectedUser.value;
    } else {
      params.all_users = true; 
    }
  }

  const r = await axios.get('/api/halls/', { params });
  halls.value = r.data;

  loading.value = false;
}


async function fetchGroups() {
    const response = await axios.get("/api/groups/"); 
    console.log('Эпохи:', response.data);
    groups.value = response.data;

}

async function fetchUsers() {
  if (!is_superuser.value) return

  const r = await axios.get('/api/users/all')
  users.value = r.data
}

async function fetchStats() {
  const r = await axios.get('/api/artifacts/stats/')
  stats.value = r.data
}

async function onLoadClick(params) {
  await fetchHalls()
}
onBeforeMount(async()=>{
  await fetchHalls()
  await fetchGroups()
  await fetchUsers()
  await fetchStats()
})

async function onHallsAdd() {
  const formData = new FormData();

  formData.append('name', hallToAdd.value.name);
  formData.append(
    'group_id',
    Number(hallToAdd.value.group_id)
  );

  if (hallsPictureRef.value?.files?.[0]) {
    formData.append('picture', hallsPictureRef.value.files[0]);
  }

  await axios.post('/api/halls/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });

  await fetchHalls();
}

async function onRemoveClick(hall) {
  await axios.delete(`/api/halls/${hall.id}/`);
  await fetchHalls(); 
}

async function onHallEditClick(hall) {
  hallToEdit.value = {
    id: hall.id,
    name: hall.name,
    group_id: hall.group.id,
    picture: hall.picture
  };

  hallEditImageUrl.value = null;
}

async function onUpdateHall() {
  const formData = new FormData();

  formData.append('name', hallToEdit.value.name);
  formData.append(
    'group_id',
    Number(hallToEdit.value.group_id)
  );

  if (hallEditPictureRef.value?.files?.[0]) {
    formData.append('picture', hallEditPictureRef.value.files[0]);
  }

  await axios.put(
    `/api/halls/${hallToEdit.value.id}/`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }
  );

  await fetchHalls();
}

async function hallsAddPictureChange(params) {
  hallAddImageUrl.value=URL.createObjectURL(hallsPictureRef.value.files[0])
}

function openImagePreview(hall) {
  imagePreviewUrl.value = hall.picture;
  imagePreviewTitle.value = hall.name;
}



</script>

<template>
  <div>
    <h1>Выставки</h1>
    {{ username }}



    <form @submit.prevent.stop="onArtifactAdd" class="p-3 border rounded shadow-sm">
      <div class="d-flex flex-column gap-3">
        <div class="d-flex gap-3 flex-wrap">
          <div class="flex-grow-1">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="artifactToAdd.name"
                required
              />
              <label>Название</label>
            </div>
          </div>

          <div style="min-width: 150px;">
            <div class="form-floating">
              <select class="form-select" v-model="artifactToAdd.group_id" required>
                <option :value="g.id" v-for="g in groups" :key="g.id">
                  {{ g.name }}
                </option>
              </select>
              <label>Эпоха</label>
            </div>
          </div>
        </div>

        <div>
          <input
            class="form-control"
            type="file"
            ref="artifactsPictureRef"
            @change="artifactsAddPictureChange"
          />
        </div>

        <div v-if="artifactAddImageUrl">
          <img :src="artifactAddImageUrl" style="max-height:120px;" alt="Превью" class="img-thumbnail"/>
        </div>

        <div>
          <button type="submit" class="btn btn-primary">
            Добавить
          </button>
        </div>
      </div>
    </form>

    <div v-if="is_superuser" class="mt-3 mb-3">
      <label class="form-label">Фильтр по пользователю</label>
      <select class="form-select" v-model="selectedUser" @change="fetchArtifacts">
        <option :value="null">Все пользователи</option>
        <option v-for="u in users" :key="u.id" :value="u.id">
          {{ u.username }}
        </option>
      </select>
    </div>


    <div class="mb-3">
      <h3>Статистика:</h3>
      <p>Всего артефактов: {{ stats.count }}</p>
      <p>Среднее ID: {{ stats.avg }}</p>
      <p>Минимальный ID: {{ stats.min }}</p>
      <p>Максимальный ID: {{ stats.max }}</p>
    </div>
    <div class="container mt-4">
      <h2 class="mb-4">Артефакты</h2>

      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border"></div>
      </div>

      <div v-else-if="!artifacts.length" class="alert alert-secondary">
        Артефакты не найдены
      </div>

      <div class="row g-4">
        <div v-for="artifact in artifacts" :key="artifact.id" class="col-lg-4 col-md-6">
          <div class="card h-100 shadow-sm">
            <div class="card-body">
              <h5 class="card-title">{{ artifact.name }}</h5>
              <p class="card-text text-muted">
                <strong>Эпоха:</strong> {{ artifact.group.name }}
              </p>

              <div v-if="artifact.picture" class="mt-2">
                <img
                  :src="artifact.picture"
                  class="img-thumbnail"
                  style="max-height:60px; cursor:pointer;"
                  @click="openImagePreview(artifact)"
                  data-bs-toggle="modal"
                  data-bs-target="#imagePreviewModal"
                />
              </div>

              <button
                class="btn btn-success btn-sm mt-2 me-2"
                @click="onArtifactEditClick(artifact)"
                data-bs-toggle="modal"
                data-bs-target="#editArtifactModal"
              >
                Редактировать
              </button>

              <button
                class="btn btn-danger btn-sm mt-2"
                @click="onRemoveClick(artifact)"
              >
                Удалить
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editArtifactModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать артефакт</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body">
            <div class="row g-2">
              <div class="col">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="artifactToEdit.name"
                  />
                  <label>Название</label>
                </div>
              </div>

              <div class="col-auto">
                <div class="form-floating">
                  <select class="form-select" v-model="artifactToEdit.group_id">
                    <option :value="g.id" v-for="g in groups" :key="g.id">
                      {{ g.name }}
                    </option>
                  </select>
                  <label>Эпоха</label>
                </div>
              </div>

              <div class="col-12 mt-2">
                <input
                  class="form-control"
                  type="file"
                  ref="artifactEditPictureRef"
                  @change="artifactEditPictureChange"
                />
              </div>

              <div v-if="artifactEditImageUrl" class="mt-2">
                <img :src="artifactEditImageUrl" style="max-height:120px;" class="img-thumbnail" alt="Превью"/>
              </div>

              <div v-else-if="artifactToEdit.picture" class="mt-2">
                <img :src="artifactToEdit.picture" style="max-height:120px;" class="img-thumbnail" alt="Старая картинка"/>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Закрыть
            </button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateArtifact">
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="imagePreviewModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ imagePreviewTitle }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>

          <div class="modal-body text-center">
            <img :src="imagePreviewUrl" class="img-fluid rounded" alt="Просмотр изображения"/>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>
