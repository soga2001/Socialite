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
        $q: useQuasar()
      };
  },
  name: 'Main',
  setup() {
    const store = useStore()
  },
  created() {
    // this.$store.commit('authenticate',JSON.parse(Cookies.get("loggedIn")) || false)
    // if(Cookies.get('user')) {
    //   this.$store.commit('setUser', Cookies.get('user'))
    // }
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
            type: 'positive',
            message: 'Login successful!',
            timeout: 1000,
            position: 'bottom-left'
            // avatar: 'https://cdn.quasar.dev/img/boy-avatar.png',
        })
      } else {
          this.$q.notify({
              // progress: true,
              type: 'positive',
              message: 'Logout successful!',
              timeout: 1000,
              position: 'bottom-left'
              // avatar: 'https://cdn.quasar
          })
        }
    }
  }
})
</script>

<template>
  <div class="home row">
    <div class="nav col-2 col-lg-3 col-md-4">
       <Navbar />
    </div>
    <div class="main__center col-10 col-lg-5 col-md-5">
      <RouterView v-slot="{Component}">
        <KeepAlive :max="3" :include="['home','user-profile', 'search']">
          <component :is="Component" :key="$route.fullPath"/>
        </KeepAlive>
      </RouterView>
    </div>
    <div class="home__sides right col-lg-2">
    
    </div>
  </div>
</template>

<style scoped>
.home {
  position: relative;
  height: 100%;
  min-height: 100vh;
}
.nav {
  z-index: 999;
  display: flex;
  flex-direction: column;
}

.main__center {
  border-left: 2px solid var(--color-border);
  border-right: 2px solid var(--color-border);
  height: 100%;
}

.posts {
  margin: 20px 0;
}

/* @media screen and (min-width: 1220px){
  .home {
    display: grid;
    grid-template-columns: auto minmax(500px, 600px) auto;
    align-items: center;
  }

  .home__sides {
    height: 100%;
    position: sticky;
  }
}


@media screen and (min-width: 860px) and (max-width: 1220px){
  .home {
    display: grid;
    grid-template-columns: minmax(500px, 600px) auto;
    justify-content: center;
  }

  .home__sides {
    display: none;
  }

}

@media screen and (min-width: 400px) and (max-width: 859px){
  .home {
    display: grid;
    grid-template-columns: minmax(500px, 600px) auto;
    justify-content: center;
  }

  .home__sides.right {
    display: none;
  }

}

.loading {
  color: var(--color-heading);
} */
</style>
