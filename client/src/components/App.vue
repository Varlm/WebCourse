<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">Мой Сайт</a>
      
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
        
        <ul v-if="isLoggedIn" class="navbar-nav">
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
            </ul>

        <div v-if="!isLoggedIn" class="d-flex">
            <a href="/login" class="btn btn-primary">
                Войти
            </a>
            <a href="/register" class="btn btn-outline-primary ms-2">
                Регистрация
            </a>
        </div>
        
      </div>
    </div>
  </nav>
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
      // Здесь будет реальная логика выхода (очистка токена, перенаправление)
      console.log('Пользователь вышел из системы');
      this.isLoggedIn = false; // Обновляем состояние
      // this.$router.push('/home'); // Пример: перенаправление
    }
  }
};
</script>

<style scoped>

</style>