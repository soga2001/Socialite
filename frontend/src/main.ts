import { createApp } from 'vue'
import {store, key} from './store/store'
import App from './App.vue'
import router from './router'
import { vue3Debounce } from 'vue-debounce'
import VueMobileDetection from "vue-mobile-detection";

import { Quasar, Cookies, Dialog, Notify } from 'quasar'
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

// My Components
import Item from '@/components/Item.vue';
import Themetoggle from '@/components/themetoggle.vue';
import ToolTips from '@/components/ToolTips.vue';


// my icons
import HomeIcon from '@/icons/i-home.vue';
import ExploreIcon from '@/icons/i-explore.vue';
import ProfileIcon from '@/icons/i-profile.vue';
import SettingsIcon from '@/icons/i-settings.vue';
import NotifIcon from '@/icons/i-notif.vue';
import SearchIcon from '@/icons/i-search.vue';
import HeartIcon from '@/icons/i-heart.vue';
import ShareIcon from '@/icons/i-share.vue';






const app = createApp(App)

app.use(router);
app.use(store, key);
app.component('Item', Item);

// icon components
app.component('theme-toggle', Themetoggle);
app.component('home-icon', HomeIcon);
app.component('explore-icon', ExploreIcon);
app.component('profile-icon', ProfileIcon);
app.component('settings-icon', SettingsIcon);
app.component('notif-icon', NotifIcon);
app.component('search-icon', SearchIcon);
app.component('heart-icon', HeartIcon);
app.component('share-icon', ShareIcon);
app.component('tool-tips', ToolTips);



app.use(VueMobileDetection)
app.use(Quasar, {
    plugins: {Dialog, Notify }, // import Quasar plugins and add here
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