<script lang="ts">
import { useCookies } from 'vue3-cookies';
import { defineComponent } from 'vue'
import {http} from './assets/http'
import { RouterLink, RouterView } from 'vue-router';
import router from './router';
import { useStore } from './store/store';
import $ from 'jquery'
import Search from './views/Search/Search.vue'


export default defineComponent({
  data() {
    return {
      theme: false,
      dark_mode: false
    }
  },
  setup() {
    const store = useStore()
    const {cookies} = useCookies();
    return {cookies}
  },
  methods: {
    switchTheme(e: any) {
      if(this.theme) {
        this.cookies.set('theme', 'dark')
        document.documentElement.setAttribute('data-theme', 'dark')
      }
      else {
        this.cookies.set('theme', 'light')
        document.documentElement.setAttribute('data-theme', 'light')
      }
      this.$store.commit('setTheme', !this.$store.state.dark)
    },
    logout() {
      http.post('users/logout/', {
        "access_token": this.cookies.get('access_token'),
        "refresh_token": this.cookies.get('refresh_token')
      }, {
        headers: {
          'Authorization': `Bearer ${this.cookies.get('access_token')}`
        }
      }).then((res) => {
        this.cookies.remove('access_token')
        this.cookies.remove('refresh_token')
        this.cookies.set('loggedIn', "false")
        this.cookies.remove('user')
        this.$store.commit('authenticate', false)
        this.$store.commit('setUser', this.$store.state.defaultUser)
        router.push('/')
      }).catch((err) => {
        console.log(err)
      })
    },
    testing() {
      console.log('clicked')
    }
  },
  created() {
    this.theme = this.cookies.get('theme') == 'dark'
    this.$store.commit('setTheme', this.theme)
    document.documentElement.setAttribute('data-theme', this.theme ? 'dark': 'light')

    this.$store.commit('authenticate',JSON.parse(this.cookies.get("loggedIn")) || false)
    if(this.cookies.get('user')) {
      this.$store.commit('setUser', this.cookies.get('user'))
    }
  },
  mounted() {
    // if(this.theme === 'dark') {
    //   (document.getElementById('checkbox') as HTMLInputElement).checked = true
    // }
    // else {
    //   (document.getElementById('checkbox') as HTMLInputElement).checked = false
    // }
    $('.dropdown__button').on('click', function() {
      $('#dropdown').toggleClass('show')
    })

    $(document).mouseup(function(e: any) {
      if(!$(e.target).hasClass('dropdown__button')) {
        if($("#dropdown").hasClass('show')) {
          $('#dropdown').toggleClass('show')
        }
      }
    });

  },
  components: {Search}
})

</script>

<template>
  <header>
    <q-toolbar class="nav">
      <!-- <q-btn flat round dense icon="menu" class="q-mr-sm" /> -->
      <q-btn stretch flat class="brand" label="Based-Book" v-on:click="$router.push('/')" />

      <q-space />
      <!-- <Search /> -->
      <!-- <q-space /> -->
      <q-toggle v-on:click="switchTheme" v-model="theme" checked-icon="nights_stay" color="grey" unchecked-icon="wb_sunny" />
      <q-separator v-if="theme" dark vertical />
      <q-separator v-if="!theme" light vertical />
      <q-btn stretch flat v-on:click="$router.push('/')"><RouterLink to="/" class="nav__link">Home</RouterLink></q-btn>
      <q-separator v-if="theme" dark vertical />
      <q-separator v-if="!theme" light vertical />
      <q-btn v-if="!$store.state.authenticated"  stretch flat v-on:click="$router.push('/login')"><RouterLink to="/login" class="nav__link">Login</RouterLink></q-btn>
      <q-separator v-if="!$store.state.authenticated && theme" dark vertical />
      <q-separator v-if="!$store.state.authenticated && !theme" light vertical />
      <q-btn v-if="!$store.state.authenticated" stretch flat v-on:click="$router.push('/register')"><RouterLink to="/register" class="nav__link">Register</RouterLink></q-btn>
      <!-- <RouterLink to="/" class="nav__link">Home</RouterLink> -->
      <!-- <RouterLink to="/home" class="nav__link">Home</RouterLink> -->
      <q-btn-dropdown stretch flat :label="$store.state.user.username" v-if="$store.state.authenticated">
        <q-list class="dropdown__main">
          <q-item clickable v-close-popup tabindex="0" v-on:click="$router.push(`/profile/user?id=${$store.state.user.id}`)">
            <q-item-section avatar>
              <q-avatar icon="account_circle" color="secondary" text-color="white" />
            </q-item-section>
            <q-item-section>
              <!-- <q-item-label>Profile</q-item-label> -->
              <RouterLink :to="'/profile/user?id=' + $store.state.user.id" class="nav__link">Profile</RouterLink>
            </q-item-section>
          </q-item>
          <q-item clickable v-close-popup tabindex="0" v-on:click="$router.push('/profile')">
            <q-item-section avatar>
              <q-avatar icon="settings" color="secondary" text-color="white" />
            </q-item-section>
            <q-item-section>
              <!-- <q-item-label>Settings</q-item-label> -->
              <RouterLink to="/settings" class="nav__link">Settings</RouterLink>
            </q-item-section>
          </q-item>
          <q-separator v-if="theme" dark spaced />
          <q-separator v-if="!theme" light spaced />
          <q-item clickable v-close-popup tabindex="0" v-on:click="logout">
            <q-item-section avatar>
              <q-avatar icon="logout" color="primary" text-color="white" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Logout</q-item-label>
              <!-- <q-item-label caption>February 22, 2016</q-item-label> -->
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
    </q-toolbar>
  </header>

  <RouterView />
</template>

<style>
@import '@/assets/base.css';
body {
  place-items: center;
  position: relative;
}

header {
  display: flex;
  place-items: center;
  /* padding-right: calc(var(--section-gap) / 2); */
}

.nav {
  background-color: var(--color-background);
  box-shadow: 0px .5px 10px var(--color-text);
  z-index: 999;
}

a,
.green {
  text-decoration: none;
  color: hsla(160, 100%, 37%, 1);
  transition: 0.4s;
  line-height: 2;
}

@media (hover: hover) {
  a:hover {
    background-color: hsla(160, 100%, 37%, 0.2);
  }
}

.nav .brand {
  width: fit-content;
}

.nav a.router-link-exact-active {
  color: var(--color-heading);
  font-weight: bolder;
}

.nav a.router-link-exact-active:hover {
  background-color: transparent;
  color: rgb(59, 206, 59);
}

.nav a {
  display: inline-block;
  padding: 0 1rem;
}

.nav__right {
  float: right;
  display: flex;
}

/* Dropdown */

.divider {
  color: var(--color-text) !important;
}

.dropdown__main {
  background-color: var(--color-background) !important;
  color: var(--color-text);
}


.nav__link:hover {
  background-color: transparent;
}


/* Dropdown End */

/* Dark Theme */
/* Reference 1: https://dev.to/ananyaneogi/create-a-dark-light-mode-switch-with-css-variables-34l8 */
/* Reference 2: https://www.w3schools.com/howto/howto_css_switch.asp */
.nav__switch {
  padding: 0px 1em;
}

.switch {
  position: relative;
  display: inline-block;
  width: 30px;
  height: 17px;
}

.switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 5px;
  left: 0;
  right: 0;
  bottom: -5px;
  background-color: var(--color-switch-slider);
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 13px;
  width: 13px;
  left: 2px;
  bottom: 2px;
  background-color: var(--color-switch);
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: var(--color-switch-slider);
}

input:focus + .slider {
  box-shadow: 0 0 1px var(--color-border);
}

input:checked + .slider:before {
  -webkit-transform: translateX(13px);
  -ms-transform: translateX(13px);
  transform: translateX(12px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 17px;
}

.slider.round:before {
  border-radius: 50%;
}

</style>
