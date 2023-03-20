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
import Main from './views/Main.vue';
import { Crypter } from './assets/crypter';


export default defineComponent({
  data() {
    return {
      theme: false,
      dark_mode: false,
      include: ['home', 'explore'],
      class: 'app',
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
    onload(e: any) {
      console.log(e)
    },
    checkOS() {
      if(navigator.userAgent.includes('Mobile')) {
        this.$store.commit('setDesktop', false)
      }
      else {
        this.$store.commit('setDesktop', true)
      }
    }
  },
  created() {
    this.theme = Cookies.get('theme') === 'dark'
    this.$store.commit('setTheme', this.theme)
    document.documentElement.setAttribute('data-theme', this.theme ? 'dark': 'light')

    this.$store.commit('authenticate',JSON.parse(Cookies.get("loggedIn")) || false)
    if(this.cookies.get('user')) {
      this.$store.commit('setUser', JSON.parse(Crypter.decrypt(this.cookies.get('user'))))
    }

  },
  components: { Main },
  mounted() {
    // let regexp = /android|iphone|kindle|ipad/i;
    this.checkOS
    window.onresize = this.checkOS
  }
})

</script>

<template>
  <!-- <h1>Potato</h1> -->
  <header id="app">
      <Main />
  </header>
</template>

<style>
@import '@/assets/base.css';

/* #app {
  width: 100%;
  height: 100%;
  position:fixed;
  overflow-y:scroll;
  overflow-x:hidden;
} */

</style>
