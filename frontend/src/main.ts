import { createApp } from 'vue'
import {store, key} from './store/store'
import App from './App.vue'
import router from './router'
import timeago from 'vue-timeago3'

const app = createApp(App)

app.use(router)
app.use(store, key)
app.use(timeago)


app.mount('#app')