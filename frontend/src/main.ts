import { createApp } from 'vue'
import {store, key} from './store/store'
import App from './App.vue'
import router from './router'
import { vue3Debounce } from 'vue-debounce'
import Vue3MobileDetection from "vue3-mobile-detection";
import VueCropper from 'vue-cropperjs';
import 'cropperjs/dist/cropper.css';

import { Cropper } from 'vue-advanced-cropper';
import 'vue-advanced-cropper/dist/style.css';





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
import 'quasar/src/css/index.sass'

// My Components
import Item from '@/components/Item.vue';
import ThemeToggle from './components/ThemeToggle.vue'
import ToolTips from '@/components/ToolTips.vue';
import CircularProgress from './components/circularProgress.vue'
import UploadedImage from '@/components/uploadedImg.vue';
import imageCropper from '@/components/imageCropper.vue';
import Loading from './components/Loading.vue'
import MentionLink from '@/components/MentionLink.vue';
import Timeago from './components/Timeago.vue';
import Spills from './components/Spills.vue';
import CommentMap from '@/components/CommentMap.vue';
import PostsMap from '@/components/PostsMap.vue'
import Mention from './components/Mention.vue'
import SearchBar from '@/components/SearchBar.vue';


// my icons
import HomeIcon from '@/icons/i-home.vue';
import ExploreIcon from '@/icons/i-explore.vue';
import ProfileIcon from '@/icons/i-profile.vue';
import SettingsIcon from '@/icons/i-settings.vue';
import NotifIcon from '@/icons/i-notif.vue';
import SearchIcon from '@/icons/i-search.vue';
import HeartIcon from '@/icons/i-heart.vue';
import ShareIcon from '@/icons/i-share.vue';
import LoginIcon from '@/icons/i-login.vue'
import LogoutIcon from '@/icons/i-logout.vue';
import UploadImage from '@/icons/i-uploadImg.vue';
import UploadVideo from '@/icons/i-uploadVid.vue';
import CloseIcon from '@/icons/i-close.vue';
import SpillIcon from '@/icons/i-spill.vue';
import CommentIcon from '@/icons/i-comment.vue';
import EmptyFolder from '@/icons/i-folder.vue';
import RegisterIcon from '@/icons/i-register.vue';






const app = createApp(App)

app.use(router);
app.use(store, key);
app.component('Item', Item);


app.component('cropper', VueCropper);
// app.component('adv-cropper', Cropper);
// icon components
app.component('i-home', HomeIcon);
app.component('i-explore', ExploreIcon);
app.component('i-profile', ProfileIcon);
app.component('i-settings', SettingsIcon);
app.component('i-notif', NotifIcon);
app.component('i-search', SearchIcon);
app.component('i-heart', HeartIcon);
app.component('i-share', ShareIcon);
app.component('tool-tips', ToolTips);
app.component('i-login', LoginIcon);
app.component('i-register', RegisterIcon);
app.component('i-logout', LogoutIcon);
app.component('i-close', CloseIcon);
app.component('i-spill', SpillIcon);
app.component('i-upload-img', UploadImage);
app.component('i-upload-vid', UploadVideo);
app.component('i-comment', CommentIcon);
app.component('i-folder', EmptyFolder);

// components
app.component('circular-progress', CircularProgress);
app.component('uploaded-img', UploadedImage);
app.component('theme-toggle', ThemeToggle);
app.component('image-cropper', imageCropper);
app.component('Loading', Loading);
app.component('Timeago', Timeago)
app.component('MentionLink', MentionLink)
app.component('Spills', Spills)
app.component('CommentMap', CommentMap)
app.component('Mention', Mention)
app.component('PostsMap', PostsMap)
app.component('SearchBar', SearchBar)
// app.component('adv-cropper', newCropper);




app.use(Vue3MobileDetection)
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