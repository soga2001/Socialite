<script lang="ts">
import {defineComponent, ref} from 'vue';
import { useQuasar } from 'quasar';
import Sidebar from '@/components/Navbars/sidebar.vue';
import TopNav from '@/components/Navbars/topnav.vue';
import BottomNav from '@/components/Navbars/bottomnav.vue';
import Unauthenticated from '@/components/unauthenticated.vue';

export default defineComponent({
  title: 'Main',
  data() {
      return {
        $q: useQuasar(),
        scrollY: 0,
        topNavHeight: (document.getElementById("top-nav") as HTMLDivElement)?.offsetHeight,
        scrollPos: {
          "/home": 0,
          "/settings": 0,
          "/explore": 0,
        } as { [key: string]: number },
      };
  },
  name: 'Main',
  setup() {
  },
  created() {
  },
  mounted() {
    const element = (document.getElementById("main-div") as HTMLDivElement)
    element.addEventListener("scroll", this.scroll)
  },
  activated() {
    const element = (document.getElementById("main-div") as HTMLDivElement)
    element.addEventListener("scroll", this.scroll)
  },
  computed: {
  },
  methods: {
    scroll() {
      const element = (document.getElementById("main-div") as HTMLDivElement);
      (this.scrollPos[(this.$route.fullPath)]) = element.scrollTop
    },
    isMobile() {
      return this.$q.screen.lt.sm
    }
  },
  components: { Sidebar, TopNav, BottomNav, Unauthenticated },
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
    '$route': function() {
      // const element = (document.getElementById("main-div") as HTMLDivElement);
      // element.scrollTop = this.scrollPos[(this.$route.fullPath)]
      this.$nextTick(() => {
        const element = document.getElementById("main-div") as HTMLDivElement;
        element.scrollTop = this.scrollPos[this.$route.fullPath];
      });
    },
  }
})
</script>

<template>
  <div :class="!isMobile() ? 'main' : 'mobile w-full fixed grid min-h-viewport max-h-viewport h-full'">
    <div v-if="!isMobile()" class="relative min-h-viewport h-full w-full bg-theme">
      <Sidebar/>
    </div>
    <div v-if="isMobile()" class="z-100 row-1 border-b">
      <TopNav/>
    </div>
    <div id="main-div" :on-scroll="scroll" :class="(isMobile() && 'mobile-main min-h-full grid-row-2') + ' h-full w-full'">
      <div class="border-l border-r">
        <RouterView v-slot="{Component}">
          <KeepAlive :max="3" :include="['home','user-profile', 'search', 'explore']">
            <component :is="Component" />
          </KeepAlive>
        </RouterView>
      </div>

      <div v-if="!isMobile()" class="right-bar sticky top-0 h-fit px-4 py-2 max-w-xs">
        <div v-if="!$store.state.authenticated" class="border rounded-sm w-fit">
          <Unauthenticated />
        </div>
      </div>
    </div>
    <nav v-if="isMobile()" class="row-3 z-2">
      <BottomNav/>
    </nav>
  </div>
</template>

<style scoped>
.main {
  display: grid;
  width: 100%;
  transform: transition 1s;
  position: fixed;
  overflow: scroll;
  overflow-y: scroll;
  height: 100%;
  grid-template-columns: auto 1fr;
}

.mobile {
  grid-template-rows: auto 1fr auto;
}

.mobile-main {
  overflow: hidden;
  overflow-y: scroll;
}

#main-div {
  overflow: scroll;
  overflow-y: scroll;
  height: 100%;
  width: 100%;
  display: grid;
  grid-template-columns: 600px 1fr;
}


/* Extra small devices (phones, 600px and down) */
@media only screen and (max-width: 600px) {
  .main {
    grid-template-columns: 80px 1fr;
  }

  #main-div {
    grid-template-columns: 1fr 0px;
  }

  .right-bar {
    display: none;
  }
}

/* Small devices (portrait tablets and large phones, 600px and up) */
@media only screen and (min-width: 600px) {
  .main {
    grid-template-columns: auto 1fr;
  }

  #main-div {
    grid-template-columns: 1fr 0px;
  }

  .right-bar {
    display: none;
  }
}

/* Medium devices (landscape tablets, 768px and up) */
@media only screen and (min-width: 710px) {
  .main {
    grid-template-columns: auto 1fr;
  }

  #main-div {
    grid-template-columns: 600px 0px;
  }

  .right-bar {
    display: none;
  }
} 

/* Large devices (laptops/desktops, 992px and up) */
@media only screen and (min-width: 992px) {
  .main {
    grid-template-columns: auto 1fr;
  }

  #main-div {
    grid-template-columns: 600px 1fr;
  }

  .right-bar {
    display: block;
  }
} 

/* Extra large devices (large laptops and desktops, 1200px and up) */
@media only screen and (min-width: 1200px) {
  .main {
    grid-template-columns: 350px 1fr;
  }

  #main-div {
    grid-template-columns: 600px 1fr;
  }

  .right-bar {
    display: block;
  }
}

</style>