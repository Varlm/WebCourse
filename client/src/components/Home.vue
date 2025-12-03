
<template>
  <div class="home">
    <h1>Добро пожаловать в музей!</h1>
    <p>Система управления музейными экспонатами</p>
    <div class="row mt-4">
      <div class="col-md-4 mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Артефакты</h5>
            <p class="card-text">Управление музейными артефактами</p>
            <router-link to="/artifacts" class="btn btn-primary">Перейти</router-link>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Группы</h5>
            <p class="card-text">Управление группами артефактов</p>
            <router-link to="/groups" class="btn btn-primary">Перейти</router-link>
          </div>
        </div>
      </div>
      <div class="col-md-4 mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Залы</h5>
            <p class="card-text">Управление музейными залами</p>
            <router-link to="/halls" class="btn btn-primary">Перейти</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>