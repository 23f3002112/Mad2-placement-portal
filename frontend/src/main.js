import { createApp } from 'vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import vue3GoogleLogin from 'vue3-google-login'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(router)

app.use(vue3GoogleLogin, {
  clientId: '342556146490-il49msdm0llgn6q9v2mt5qesaqsml719.apps.googleusercontent.com'
})

app.mount('#app')
