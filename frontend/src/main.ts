import { createApp } from 'vue'
import {store, key} from './store/store'
import App from './App.vue'
import router from './router'
import timeago from 'vue-timeago3'
import { vue3Debounce } from 'vue-debounce'
import { Quasar } from 'quasar'
import '@quasar/extras/material-icons/material-icons.css'
// Import Quasar css
import 'quasar/dist/quasar.css'
import 'jquery'

const app = createApp(App)

app.use(router)
app.use(store, key)
app.use(timeago)
app.use(Quasar, {
    plugins: {}, // import Quasar plugins and add here
  })
app.directive('debounce', vue3Debounce({ lock: true }))


app.mount('#app')