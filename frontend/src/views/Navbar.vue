<script lang="ts">
import { useCookies } from 'vue3-cookies';
import { defineComponent } from 'vue'
import {http} from '../assets/http'
import { RouterLink, RouterView } from 'vue-router';
import router from '../router';
import { useStore } from '../store/store';
import $ from 'jquery'
import Search from '../views/Search/Search.vue'
import { Cookies } from 'quasar';


export default defineComponent({
  data() {
    return {
      theme: false,
      include: ['home', 'explore']
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
        Cookies.set('theme', 'dark')
        document.documentElement.setAttribute('data-theme', 'dark')
      }
      else {
        Cookies.set('theme', 'light')
        document.documentElement.setAttribute('data-theme', 'light')
      }
      this.$store.commit('setTheme', !this.$store.state.dark)
    },
    logout() {
      http.post('users/logout/', {
        "access_token": Cookies.get('access_token'),
        "refresh_token": Cookies.get('refresh_token')
      }, {
        headers: {
          'Authorization': `Bearer ${Cookies.get('access_token')}`
        }
      }).then((res) => {
        Cookies.remove('access_token')
        Cookies.remove('refresh_token')
        Cookies.remove('user')
        Cookies.remove('loggedIn')
        this.$store.commit('authenticate', false)
        this.$store.commit('setUser', this.$store.state.defaultUser)
        router.push('/')
      }).catch((err) => {
        console.log(err)
      })
    },
    onload(e: any) {
      console.log(e)
    }
  },
  created() {
    this.theme = Cookies.get('theme') === 'dark'
    this.$store.commit('setTheme', this.theme)
    document.documentElement.setAttribute('data-theme', this.theme ? 'dark': 'light')

    this.$store.commit('authenticate',JSON.parse(Cookies.get("loggedIn")) || false)
    if(Cookies.get('user')) {
      this.$store.commit('setUser', Cookies.get('user'))
    }
  },
  mounted() {
  },
  components: {Search}
})

</script>

<template>
  <header>
    <q-toolbar class="nav">
      <q-btn stretch flat class="brand" to="/" >Based<span class="logo">Book</span></q-btn>
      <q-space/>
      <q-toggle v-on:click="switchTheme" v-model="theme" color="grey" keep-color checked-icon="nights_stay" unchecked-icon="wb_sunny" />
      <q-tabs shrink >
        <q-separator :dark="theme" vertical />
        <q-route-tab
          icon="cottage"
          to="/"
          class="nav__link"
          active-class="active"
        >
          <q-tooltip :offset="[0,0]">Home</q-tooltip>
        </q-route-tab>
        <q-separator :dark="theme" vertical />
        <q-route-tab
          icon="login"
          to="/login"
          exact
          v-if="!$store.state.authenticated"
          class="nav__link"
          active-class="active"
        >
          <q-tooltip :offset="[0,0]">Login</q-tooltip>
        </q-route-tab>
        <q-separator :dark="theme" vertical />
        <q-route-tab
          icon="app_registration"
          to="/register"
          exact
          v-if="!$store.state.authenticated"
          class="nav__link"
          active-class="active"
        >
          <q-tooltip :offset="[0,0]">Register</q-tooltip>
        </q-route-tab>
      </q-tabs>
      <q-btn-dropdown class="dropdown" stretch flat v-if="$store.state.authenticated" no-caps>
        <template v-slot:label>
          <div class="row items-center no-wrap">
            <q-avatar class="avatar" v-if="$store.state.user.profile.avatar">
              <img :src="$store.state.user.profile.avatar"/>
            </q-avatar>
            <q-avatar class="avatar" v-if="!$store.state.user.profile.avatar" icon="account_circle"/>
            <div class="text-center">
              {{$store.state.user.username}}
            </div>
          </div>
        </template>
        <q-list class="dropdown__main" dense>
          <q-item clickable v-close-popup tabindex="0" class="nav__link" active-class="active" :to="{name: 'user-profile', query: {id: $store.state.user.id}}">
            <q-item-section avatar>
              <q-avatar icon="account_circle"/>
            </q-item-section>
            <q-item-section>
              Profile
            </q-item-section>
          </q-item>
          <q-item clickable v-close-popup tabindex="0" to="/settings" class="nav__link" active-class="active">
            <q-item-section avatar>
              <q-avatar icon="manage_accounts" />
            </q-item-section>
            <q-item-section>
              Setting
            </q-item-section>
          </q-item>
          <q-separator v-if="theme" dark spaced />
          <q-separator v-if="!theme" light spaced />
          <q-item clickable v-close-popup tabindex="0" v-on:click="logout">
            <q-item-section avatar>
              <q-avatar icon="logout" />
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
  <RouterView v-slot="{Component}">
    <KeepAlive :max="5" :include="['Home','User']">
      <component :is="Component" :key="$route.fullPath"/>
    </KeepAlive>
  </RouterView>
</template>

<style>
@import '@/assets/base.css';
* {
  scroll-behavior: smooth;
}

html {
  height: 100%;
}

body {
  place-items: center;
  position: relative;
  height: 100%;
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
  position: -webkit-sticky;
  position: sticky;
  top: 0;
}

a {
  text-decoration: none;
  color: hsla(160, 100%, 37%, 1);
  transition: 0.2s;
  /* line-height: 2; */
}

.nav .brand {
  width: fit-content;
  font-size: large;
  font-weight: 100;
}

.brand:hover {
  background-color: transparent !important;
}


.nav .logo {
  font-weight: 900;
  color: var(--color-heading);
}

/* .nav__link.router-link-exact-active {
  color: var(--color-heading) !important;
  font-weight: 900;
} */

.nav__link {
  color: var(--color-text);
}

.nav__link.active {
  /* background-color: rgba(255, 0, 0, .2); */
  /* color: rgb(193, 50, 50); */
  color: var(--color-heading);
  background-color: hsla(0, 0%, 57%, 0.2);
}

.dropdown__main {
  background-color: var(--color-background);
  color: var(--text-heading);
}

.avatar {
  margin: 0 10px;
}


</style>
