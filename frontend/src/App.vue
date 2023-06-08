<script lang="ts">
import { defineComponent } from 'vue'
import { Cookies } from 'quasar';
import Main from './views/Main.vue';
import { get_user_from_cookie } from './assets/userFromCookie';
import Loading from './components/Loading.vue';


export default defineComponent({
  data() {
    return {
      theme: false,
      dark_mode: false,
      include: ['home', 'explore'],
      class: 'app',
      loading: true,
    }
  },
  setup() {
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
    checkOS() {
      const regex = /Android|iPhone|iPad|iPod|BlackBerry|Windows Phone/i
      const width = window.innerWidth <= 597
      if(regex.test(navigator.userAgent) && width) {
        this.$store.commit('setDesktop', false)
      }
      else {
        this.$store.commit('setDesktop', true)
      }
    },
    async loadUser() {
      await get_user_from_cookie()
      setTimeout(() => {
        this.loading = false
      }, 3000)
      // this.loading = false
    }
  },
  created() {
    this.checkOS()
    this.theme = Cookies.get('theme') === 'dark'
    this.$store.commit('setTheme', this.theme)
    document.documentElement.setAttribute('data-theme', this.theme ? 'dark': 'light')
    this.loadUser()
  },
  mounted() {
    window.onresize = this.checkOS
  },
  components: { Main, Loading },
})

</script>

<template>
  <!-- <h1>Potato</h1> -->
  <div class="text-left relative" v-if="!loading">
    <Main />
  </div>
  <div class="flex items-center justify-center w-full h-viewport text-heading" v-else>
    <Loading size="5rem">
      <template v-slot:text>
        <p class="text-5xl">Loading</p>
      </template>
    </Loading>
  </div>
</template>

<style>
@import '@/assets/base.css';
@import '@/assets/global.css';

</style>
