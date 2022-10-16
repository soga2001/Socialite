import { createApp } from 'vue'
import {store, key} from './store/store'
import App from './App.vue'
import router from './router'
import timeago from 'vue-timeago3'
import { vue3Debounce } from 'vue-debounce'
// import VueCryptojs from 'vue-cryptojs';

const app = createApp(App)

app.use(router)
app.use(store, key)
app.use(timeago)
app.directive('debounce', vue3Debounce({ lock: true }))


app.mount('#app')