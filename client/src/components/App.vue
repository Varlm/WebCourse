<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">Мой Сайт</router-link>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
          
          <ul v-if="isLoggedIn" class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Главная</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/artifacts">Артефакты</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/groups">Группы</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/halls">Залы</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/curators">Кураторы</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/exhibitions">Выставки</router-link>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Пользователь
              </a>
              <ul class="dropdown-menu">
                  <li><router-link class="dropdown-item" to="/admin">Админка</router-link></li>
                  <li><hr class="dropdown-divider"></li>
                  <li><a class="dropdown-item" href="#" @click.prevent="logout">Выйти</a></li>
              </ul>
            </li>
          </ul>
          
          <ul v-else class="navbar-nav">
            <!-- Пусто для неавторизованных -->
          </ul>

          <div v-if="!isLoggedIn" class="d-flex">
            <router-link to="/login" class="btn btn-primary">Войти</router-link>
            <router-link to="/register" class="btn btn-outline-primary ms-2">Регистрация</router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Здесь будет отображаться контент текущего маршрута -->
    <main class="container mt-4">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: true, 
    };
  },
  methods: {
    logout() {
      console.log('Пользователь вышел из системы');
      this.isLoggedIn = false;
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
/* Стили для активных ссылок в навигации */
.router-link-active {
  font-weight: bold;
}

.navbar-brand {
  font-weight: bold;
}
</style>