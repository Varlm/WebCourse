import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.min.css'
import App from './components/App.vue'
import router from './router'
import Cookies from 'js-cookie';
axios.defaults.withCredentials = true
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
