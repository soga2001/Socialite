import { createApp } from 'vue'
import {store, key} from './store/store'
import App from './App.vue'
import router from './router'
import timeago from 'vue-timeago3'
import { vue3Debounce } from 'vue-debounce'
import { Quasar } from 'quasar'
// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'
import '@quasar/extras/material-icons-outlined/material-icons-outlined.css'
import '@quasar/extras/material-icons-round/material-icons-round.css'
import '@quasar/extras/material-icons-sharp/material-icons-sharp.css'
import '@quasar/extras/material-symbols-outlined/material-symbols-outlined.css'
import '@quasar/extras/material-symbols-rounded/material-symbols-rounded.css'
import '@quasar/extras/material-symbols-sharp/material-symbols-sharp.css'
import '@quasar/extras/mdi-v6/mdi-v6.css'
import '@quasar/extras/fontawesome-v5/fontawesome-v5.css'
import '@quasar/extras/fontawesome-v6/fontawesome-v6.css'
import '@quasar/extras/ionicons-v4/ionicons-v4.css'
import '@quasar/extras/eva-icons/eva-icons.css'
import '@quasar/extras/themify/themify.css'
import '@quasar/extras/line-awesome/line-awesome.css'
import '@quasar/extras/bootstrap-icons/bootstrap-icons.css'
// Import Quasar css
import 'quasar/dist/quasar.css'
import 'jquery'

const app = createApp(App)

app.use(router)
app.use(store, key)
app.use(timeago)
app.use(Quasar, {
    plugins: {}, // import Quasar plugins and add here
    config: {
      extras: [
        'material-icons',
        'mdi-v6',
        'ionicons-v4', // last webfont was available in v4.6.3
        'eva-icons',
        'fontawesome-v6',
        'themify',
        'line-awesome',
        'bootstrap-icons'
      ],
    }
  })
app.directive('debounce', vue3Debounce({ lock: true }))


app.mount('#app')