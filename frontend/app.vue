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

  beforeMount() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      // const { pending, data: user } = await useFetch(`${backend_baseURL}/users/user_from_cookie/`, {credentials: 'include'
      // });
      // if(user.value) {
      //   this.user = (user.value as {user: User, success: boolean}).user as User;
      //   console.log(this.user)
      // } 
      const {pending, data: user} = await useFetch('/api/user')
      console.log(user)
      // await http.get(`${backend_baseURL}/users/user_from_cookie/`).then((res) => {
      //   this.user = res.data as User;
      //   console.log(this.user)
      // }).catch((err) => {
      //   console.log(err)
      // })
    },
  },
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
