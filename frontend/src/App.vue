<script lang="ts">
import { defineComponent } from 'vue'
import {http} from './assets/http'
import { RouterLink, RouterView } from 'vue-router';

export default defineComponent({
  data() {
    return {
      theme: 'dark'
    }
  },
  methods: {
    switchTheme(e: any) {
      if(this.theme==='dark'){
        this.theme = 'light'
        document.documentElement.setAttribute('data-theme', 'light')
      }
      else {
        this.theme = 'dark'
        document.documentElement.setAttribute('data-theme', 'dark')
      }
    }
  },
  created() {
  }
})

</script>

<template>
  <header>
    <!-- <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" /> -->
    <nav class="nav">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/about">Post</RouterLink>
      <div class="nav__right">
        <button id="theme" v-on:click="switchTheme">Change Theme: {{theme === 'dark' ? 'light' : "dark"}}</button>
        <RouterLink to="/login">Login</RouterLink>
        <RouterLink to="/register">Register</RouterLink>
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
}

#theme {
  background-color: transparent;
  color: var(--color-text);
  border: none;
}

</style>
