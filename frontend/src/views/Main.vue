<script lang="ts">
import {defineComponent, ref} from 'vue';
import  type {Post} from '@/assets/interfaces';
import { http } from '@/assets/http';
import PostsMap from '../components/PostsMap.vue';
import PostView from '../components/PostView.vue';
import Search from './Search.vue';
import { useStore } from '@/store/store';
import Navbar from '../components/Navbar.vue';
import { Cookies, useQuasar } from 'quasar';

export default defineComponent({
  title: 'Main',
  data() {
      return {
        $q: useQuasar(),

      };
  },
  name: 'Main',
  setup() {
    const store = useStore()
  },
  created() {
    
  },
  mounted() {
  },
  methods: {
  },
  components: { PostsMap, PostView, Search, Navbar },
  watch: {
    '$store.state.authenticated': function () {
      if(this.$store.state.authenticated) {
        this.$q.notify({
          progress: true,
          type: 'positive',
          message: 'Login successful!',
          timeout: 2000,
          position: 'top-right',
          actions: [
            {
              icon: 'close',
              color: 'red',
            }
          ]
        })
      } else {
          this.$q.notify({
            progress: true,
            type: 'positive',
            message: 'Logout successful!',
            timeout: 2000,
            position: 'top-right',
            actions: [
              {
                icon: 'close',
                color: 'white',
              }
            ]
          })
        }
    }
  }
})
</script>

<template>
  <div :class="$store.state.desktop ? 'main' : 'mobile'">
    <div :class="!$store.state.desktop && 'mobile-' + 'navbar'">
      <Navbar />
    </div>
    <div :class="$store.state.desktop ? 'main--center' : 'mobile-main'">
      <RouterView v-slot="{Component}">
        <KeepAlive :max="3" :include="['home','user-profile', 'search']">
          <component :is="Component" :key="$route.fullPath"/>
        </KeepAlive>
      </RouterView>
    </div>
    <div v-if="!$store.state.desktop" class="main--right">
    </div>
  </div>
</template>

<style scoped>
.main {
  position: relative;
  display: grid;
}

.mobile {
  position: relative;
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 12fr;
}

.mobile-navbar {
  position: relative;
  grid-column: 1;
  grid-row: 10 / span 2;
  background-color: var(--color-background);
  border-right: 2px solid var(--color-border);
}

.navbar {
  position: relative;

  height: 100%;
  min-height: 100vh;
  background-color: var(--color-background);
  border-right: 2px solid var(--color-border);
}

.main--center {
  border-left: 2px solid var(--color-border);
  border-right: 2px solid var(--color-border);
  height: 100%;
  min-height: 100vh;
}

.mobile-main {
  border-left: 2px solid var(--color-border);
  border-right: 2px solid var(--color-border);
  height: 100%;
  grid-row: 1 / span 9;
}

.mobile-nav {
  overflow: hidden;
  position: fixed;
  bottom: 0;
  width: 100%;
  z-index: 999;
}

/* Extra small devices (phones, 600px and down) */
@media only screen and (max-width: 600px) {
  .main {
    grid-template-columns: 60px 1fr 0;
  }
}

/* Small devices (portrait tablets and large phones, 600px and up) */
@media only screen and (min-width: 600px) {
  .main {
    grid-template-columns: auto 1fr 0;
  }
}

/* Medium devices (landscape tablets, 768px and up) */
@media only screen and (min-width: 768px) {
  .main {
    grid-template-columns: 1fr 600px 1fr;
  }
} 

/* Large devices (laptops/desktops, 992px and up) */
@media only screen and (min-width: 992px) {
  .main {
    grid-template-columns: 1fr 600px 1fr;
  }
} 

/* Extra large devices (large laptops and desktops, 1200px and up) */
@media only screen and (min-width: 1200px) {
  .main {
    grid-template-columns: 1fr 600px 1fr;
  }
}

</style>
