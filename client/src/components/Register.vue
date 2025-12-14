<script setup>
import { ref } from 'vue'
import axios from 'axios'

axios.defaults.withCredentials = true
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'

const username = ref('')
const password = ref('')
const message = ref('')

async function initSession() {
  try {
    await axios.get('http://127.0.0.1:8000/api/users/me/')
  } catch (e) {
    console.log("initSession:", e)
  }
}

async function register() {
  message.value = ""

  try {

    await initSession()

    const res = await axios.post('http://127.0.0.1:8000/api/register/', {
      username: username.value,
      password: password.value
    })

    message.value = "Пользователь создан!"
  } catch (e) {
    console.error("Ошибка регистрации:", e.response?.data || e)
    message.value = "Ошибка: " + JSON.stringify(e.response?.data)
  }
}
</script>

<template>
  <div>
    <h2>Регистрация</h2>
    <input v-model="username" placeholder="Логин">
    <input v-model="password" type="password" placeholder="Пароль">
    <button @click="register">Зарегистрироваться</button>
    <p>{{ message }}</p>
  </div>
</template>


