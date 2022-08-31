<script lang="ts">
import { useCookies } from 'vue3-cookies';
import { defineComponent } from 'vue'
import {http} from './assets/http'
import { RouterLink, RouterView } from 'vue-router';

export default defineComponent({
  data() {
    return {
      theme: '',
      loggedIn: false,
    }
  },
  setup() {
    const {cookies} = useCookies();
    return {cookies}
  },
  methods: {
    switchTheme(e: any) {
      if(e.target.checked) {
        this.theme = 'dark'
        this.cookies.set('theme', this.theme)
        document.documentElement.setAttribute('data-theme', 'dark')
      }
      else {
        this.theme = 'light'
        this.cookies.set('theme', this.theme)
        document.documentElement.setAttribute('data-theme', this.theme)
      }
    },
    logout() {
      console.log(this.cookies.get("access_token"))
      this.cookies.remove('access_token')
      this.cookies.remove('refresh_token')
      this.cookies.set('loggedIn', "false")
      window.location.href = '/'
      http.post('users/logout/', {
        "access_token": this.cookies.get('access_token'),
        "refresh_token": this.cookies.get('refresh_token')
      }, {
        headers: {
          'Authorization': "Bearer" +  this.cookies.get('access_token')
        }
      }).then((res) => {
        console.log(res.data)
        this.cookies.remove('access_token')
        this.cookies.remove('refresh_token')
        this.cookies.set('loggedIn', "false")
        this.$forceUpdate()
      }).catch((err) => {
        console.log(err)
      })
    }
  },
  created() {
    console.log(this.cookies.get('theme'))
    this.theme = this.cookies.get('theme') || 'dark'
    console.log(this.theme)
    document.documentElement.setAttribute('data-theme', this.theme)


    if(this.cookies.get("loggedIn") === 'true') {
      this.loggedIn = true
    }

    // http.get('users/csrf/').then(((res) => {
    //   this.cookies.set('csrf_token', res.data.csrf)
    // }))
  },
  mounted() {
    if(this.theme === 'dark') {
      (document.getElementById('checkbox') as HTMLInputElement).checked = true
    }
    else {
      (document.getElementById('checkbox') as HTMLInputElement).checked = false
    }
  },
})

</script>

<template>
  <header>
    <!-- <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" /> -->
    <nav class="nav">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/about">Post</RouterLink>
      <!-- The RouterLink below is for parameters -->
      <!-- <RouterLink :to="'/about?id=' + loggedIn">Post</RouterLink> -->
      <RouterLink to="/"></RouterLink>
      <div class="nav__right">
        <!-- <button id="theme" v-on:click="switchTheme">Change Theme: {{theme === 'dark' ? 'light' : "dark"}}</button> -->
        <div class="nav__switch">
          <span>Theme: </span>
          <label class="switch">
          <input :onclick="switchTheme" type="checkbox" id="checkbox">
          <span class="slider round"></span>
        </label>
        </div>
        <RouterLink v-if="!loggedIn" to="/login">Login</RouterLink>
        <RouterLink v-if="!loggedIn" to="/register">Register</RouterLink>
        <RouterLink v-if="loggedIn" to="/" v-on:click="logout">Logout</RouterLink>
      </div>
    </nav>
  </header>

  <RouterView />
</template>

<style>
@import '@/assets/base.css';
body {
  place-items: center;
}

header {
  display: flex;
  place-items: center;
  /* padding-right: calc(var(--section-gap) / 2); */
}

a,
.green {
  text-decoration: none;
  color: hsla(160, 100%, 37%, 1);
  transition: 0.4s;
}

@media (hover: hover) {
  a:hover {
    background-color: hsla(160, 100%, 37%, 0.2);
  }
}

nav {
  width: 100vw;
  text-align: left;
  /* margin-left: -1rem; */
  font-size: 1rem;
  padding: 1rem 1rem;
  border-bottom: 2px solid var(--color-border);
  /* margin-top: 1rem; */
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

.nav__right {
  float: right;
  display: flex;
}

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
