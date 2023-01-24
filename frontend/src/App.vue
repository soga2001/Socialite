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
