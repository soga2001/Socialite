<script lang="ts">
import {defineComponent, ref} from 'vue';
import { http } from '@/assets/http';
import { useStore } from '@/store/store';
import { Cookies, useQuasar } from 'quasar';
import Sidebar from '@/components/Navbars/sidebar.vue';
import TopNav from '@/components/Navbars/topnav.vue';
import BottomNav from '@/components/Navbars/bottomnav.vue';

export default defineComponent({
  title: 'Main',
  data() {
      return {
        $q: useQuasar(),
        scrollY: 0,
        topNavHeight: (document.getElementById("top-nav") as HTMLDivElement)?.offsetHeight
      };
  },
  name: 'Main',
  created() {
    // console.log(screen.width)
  },
  mounted() {
    const element = (document.getElementById("main-div") as HTMLDivElement)
    element.addEventListener("scroll", function() {
      console.log('x')
    })
  },
  activated() {
  },
  computed: {
  },
  methods: {
    scroll(e: any) {
      console.log(e)
    },
  },
  components: { Sidebar, TopNav, BottomNav },
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
    },
  }
})
</script>

<template>
  <div :class="!$isMobile() ? 'main' : 'mobile relative grid min-h-viewport max-h-viewport h-full'">
    <div v-if="!$isMobile()" class="relative min-h-viewport h-full w-full bg-theme">
      <Sidebar/>
    </div>
    <div v-if="$isMobile()" class="z-100 row-1 border-b">
      <TopNav/>
    </div>
    <div id="main-div" :on-scroll="scroll" :class="$store.state.desktop ? 'border-l border-r' : 'mobile-main min-h-full grid-row-2' + ' h-full'">
      <RouterView v-slot="{Component}">
        <KeepAlive :max="3" :include="['home','user-profile', 'search', 'explore']">
          <component :is="Component" :key="$route.fullPath"/>
        </KeepAlive>
      </RouterView>
    </div>
    <nav v-if="$isMobile()" class="row-3 z-2">
      <BottomNav/>
    </nav>
    <div v-if="!$isMobile()" class="main--right">
    </div>
  </div>
</template>

<style scoped>
.main {
  position: relative;
  display: grid;
}

.mobile {
  grid-template-rows: auto 1fr auto;
}

.mobile-main {
  overflow: hidden;
  overflow-y: scroll;
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