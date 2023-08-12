<script lang="ts">
import { useFetch, useAsyncData } from 'nuxt/app';
// import http
import http from './assets/http';

// import User from interface
import { User } from 'assets/interfaces';
import {backend_baseURL} from './composables/backendURL';

// const data = http.get(`${backend_baseURL}/users/user_from_cookie/`).then((res) => {
//   console.log(res.data)
// }).catch((err) => {
//   console.log(err)
// })

export default {
  data() {
    return {
      user: {} as User,
    }
  },

  async beforeCreate() {
    const res = await $fetch(`${backend_baseURL}/users/user_from_cookie/`, {credentials: 'include'}).catch((err) => err.data)
    this.$store.commit('setUser', (res as {success: boolean, user: []}).user)
    
  },
  methods: {
    // async fetchData() {
    //     const res = await $fetch(`${backend_baseURL}/users/user_from_cookie/`, {credentials: 'include'}).catch((err) => err.data)
    //     console.log('here',(res as {success: boolean, user: []}).user)
    // },
  },
  watch: {
    '$store.state.user': function() {
      console.log(this.$store.state.user)
    }
  }
}

</script>

<template>
  <div class="container">
    <NuxtLayout name="custom">
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<style lang="scss">
body {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

.container {
  padding: 0;
  margin: 0;
  min-width: 100vw;
  min-height: 100vh;
  max-height: 100vw;
  max-width: 100vw;
  height: 100%;
  width: 100%;
}
</style>
