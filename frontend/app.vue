<script lang="ts">
// // import http
import http from './composables/http';

// // import User from interface
import type { User } from 'assets/interfaces';



export default defineComponent({
  data() {
    return {
      
    }
  },
  setup() {
    const userStore = useUserStore();
    return {
      userStore
    }

  },
  beforeCreate() {
    if(process.server) {
      this.userStore.initStore();  
    }
  },
  methods: {
  },
})

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
store/userStore./composables/http