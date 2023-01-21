<script lang="ts">
import { useCookies } from 'vue3-cookies';
import { defineComponent } from 'vue'
import {http} from './assets/http'
import { RouterLink, RouterView } from 'vue-router';
import router from './router';
import { useStore } from './store/store';
import $ from 'jquery'
import Search from './views/Search.vue'
import { Cookies } from 'quasar';
import HomeView from './views/Main.vue';


export default defineComponent({
  data() {
    return {
      theme: false,
      dark_mode: false,
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
        // this.cookies.set('theme', 'dark')
        Cookies.set('theme', 'dark')
        document.documentElement.setAttribute('data-theme', 'dark')
      }
      else {
        // this.cookies.set('theme', 'light')
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
  components: { Search, HomeView },
})

</script>

<template>
  <!-- <h1>Potato</h1> -->
    <header class="app">
      <HomeView />
    <!-- <q-toolbar class="nav sticky">
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
            <q-avatar class="avatar" >
              <img v-if="$store.state.user.profile.avatar" :src="$store.state.user.profile.avatar"/>
              <q-icon v-else name="account_circle" class="avatar__icon" />
            </q-avatar>
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
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
    </q-toolbar> -->
  </header>
  
</template>

<style>
@import '@/assets/base.css';

.app {
  position: fixed;
  width: 100%;
  max-height: 100%;
  overflow-y: scroll;
}

</style>
