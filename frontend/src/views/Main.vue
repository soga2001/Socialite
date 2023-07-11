<script lang="ts">
import {defineComponent, ref} from 'vue';
import { useQuasar } from 'quasar';
import Sidebar from '@/components/Navbars/sidebar.vue';
import TopNav from '@/components/Navbars/topnav.vue';
import BottomNav from '@/components/Navbars/bottomnav.vue';
import Unauthenticated from '@/components/unauthenticated.vue';
import { useRoute, useRouter } from 'vue-router';

export default defineComponent({
  title: 'Main',
  data() {
      return {
        $q: useQuasar(),
        scrollY: 0,
        topNavHeight: (document.getElementById("top-nav") as HTMLDivElement)?.offsetHeight,
        bottomNavHeight: (document.getElementById("bottom-nav") as HTMLDivElement)?.offsetHeight,
        scrollPos: new Map(),
        scrollHeight: new Map(),
        scrollPosition: 0,
        height: 0,
        mobile: false,
        spill: false,
        hideNav: false,
        pages: ['user-profile', 'view-spill']

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
  },
  computed: {
    hideNavBar() {
      const component = this.$route.matched[0].name || this.$route.name || ''
      if(this.pages.includes(component.toString())) {
        return true
      }
      return false
    }
  },
  methods: {
    setData() {
      const element = (document.getElementById("main-div") as HTMLDivElement)
      if(!this.scrollPos.get(this.$route.name)) {
        this.scrollPos.set(this.$route.name, element.scrollTop);
        this.scrollPosition = element.scrollTop
      }
      if(!this.scrollHeight.get(this.$route.name)) {
        this.scrollHeight.set(this.$route.name, element.scrollHeight - element.clientHeight)
        this.height = element.scrollHeight - element.clientHeight
      }
      
    },
    scroll() {
      const element = (document.getElementById("main-div") as HTMLDivElement);
      this.scrollPos.set(this.$route.name, element.scrollTop);
      this.scrollPosition = element.scrollTop
      this.scrollHeight.set(this.$route.name, element.scrollHeight - element.clientHeight)
      this.height = element.scrollHeight - element.clientHeight
      
    },
    isMobile() {
      this.mobile = this.$q.screen.lt.sm
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
      // console.log((this.scrollPos))
      // console.log(this.scrollHeight)
      console.log(this.$route.meta.depth)
      this.setData()
      this.$nextTick(() => {
        const element = document.getElementById("main-div") as HTMLDivElement;
        element.scrollTop = this.scrollPos.get(this.$route.name);
        this.scrollPosition = this.scrollPos.get(this.$route.name);
        this.height = this.scrollHeight.get(this.$route.name)
        this.bottomNavHeight = ((this.$refs.bottomBar as HTMLDivElement)?.offsetHeight + 10) || 10
        this.topNavHeight = ((this.$refs.topNav as HTMLDivElement)?.offsetHeight) || 0
      });
    },
    mobile(mobile) {
      this.$nextTick(() => {
        this.bottomNavHeight = ((this.$refs.bottomBar as HTMLDivElement)?.offsetHeight + 10) || 10
        this.topNavHeight = ((this.$refs.topNav as HTMLDivElement)?.offsetHeight) || 0
      })
    }
  },
})
</script>

<template>
  <div :class="!isMobile() ? 'main' : 'fixed w-full h-full'">
    <div v-if="!$q.screen.lt.sm" class="min-h-viewport h-full w-full bg-theme">
      <Sidebar/>
    </div>

    <div ref="topNav" :hidden="hideNavBar" v-if="isMobile()" class="sticky top-0 w-full z-5 border-b bg-theme-opacity overflow-visible">
      <TopNav/>
    </div>
    <div id="main-div" class="h-full w-full relative">
      <div :style="{paddingBottom: `${bottomNavHeight + topNavHeight}px`}"  class="border-l border-r">
        <RouterView v-slot="{Component}" >
          <KeepAlive :max="4" :include="['home', 'search', 'explore', 'user-profile', 'view-spill']" >
            <component :is="Component" :key="$route.matched[0].name !== 'user-profile' ? $route.fullPath : null"  :height="height" :scrollPosition="scrollPosition" />
          </KeepAlive>
        </RouterView>
      </div>

  

      

      <!-- <div v-if="$q.screen.lt.sm" class="right-bar sticky top-0 h-fit px-4 py-2 max-w-xs">
        <div v-if="!$store.state.authenticated" class="border rounded-sm w-fit">
          <Unauthenticated />
        </div>
      </div> -->
    </div>
    <nav v-if="$q.screen.lt.sm && !hideNavBar" ref="bottomBar" class="sticky bottom-0 w-full z-2">
      <BottomNav/>
    </nav>

    <div ref="spillButton" class="fixed box-shadow right-1 bg-theme rounded-lg" :style="{bottom: `${bottomNavHeight}px`}" v-if="isMobile() && $route.name !== 'view-spill'">
      <q-btn size="16px" class="show btn-themed text-heading" round flat icon="add" @click="spill = true"/>
    </div>

    <q-dialog class="min-h-sm" v-model="spill" persistent :maximized="$q.screen.lt.sm ? true : false">
        <div class="bg-theme w-full h-fit overflow-visible" >
          <div class="p-2">
            <Item dense :vert-icon-center="true">
              <template #title>
                <div class="text-2xl weight-900">Spill</div>
              </template>
              <template #icon>
                <i-close size="2rem" class="pointer" @click="spill = false"/>
              </template>
            </Item>
          </div>
          <hr class="border"/>
          <div class="">
            <Spills :rows="4"/>
          </div>
        </div>
      </q-dialog>
      
  </div>

  
</template>

<style scoped>

* {
  padding: 0;
  margin: 0;
}
.main {
  display: grid;
  width: 100%;
  position: fixed;
  height: 100%;
  grid-template-columns: auto 600px auto;
}

.mobile {
  width: 100%;
  transform: transition 1s;
  position: fixed;
  height: 100%;
}

.mobile-main {
  overflow: hidden;
  overflow-y: scroll;
  height: 100%;
}

#main-div {
  overflow: scroll;
  overflow-y: scroll;
  height: 100%;
  width: 100%;
  display: grid;
  grid-template-columns: 600px;
}


/* Extra small devices (phones, 600px and down) */
@media only screen and (max-width: 600px) {

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
    grid-template-columns: 600px;
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


.fade-enter-active,
.fade-leave-active {
  transition: opacity 2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

</style>