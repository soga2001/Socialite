<script lang="ts">
import {defineComponent, ref, type CSSProperties} from 'vue';
import { TouchSwipe, useQuasar } from 'quasar';
import Sidebar from '@/components/Navbars/sidebar.vue';
import TopNav from '@/components/Navbars/topnav.vue';
import BottomNav from '@/components/Navbars/bottomnav.vue';
import Unauthenticated from '@/components/unauthenticated.vue';
import { useRoute, useRouter } from 'vue-router';
import convertTime from '@/assets/convertTime'

import type { Notifications } from '@/assets/interfaces';

export default defineComponent({
  title: 'Main',
  data() {
      return {
        $q: useQuasar(),
        scrollY: 0,
        topNavHeight: (this.$refs.topNav as HTMLDivElement)?.offsetHeight,
        bottomNavHeight: (this.$refs.bottomBar as HTMLDivElement)?.offsetHeight,
        scrollPos: new Map(),
        scrollHeight: new Map(),
        scrollPosition: 0,
        height: 0,
        mobile: false,
        spill: false,
        hideNav: false,
        pages: ['user-profile', 'view-spill'],
        lastScrollPos: 0,
        hideTopNav: false,

        websocket: null as WebSocket | null,
        // websocket: new WebSocket(`wss://localhost:8000/ws/user_notif/${this.$store.state.user.id}/`),



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
    if(this.$refs.bottomBar) {
      this.bottomNavHeight = ((this.$refs.bottomBar as HTMLDivElement)?.offsetHeight + 10) || 0

    }
    this.websocketOpen()
  },
  activated() {
  },
  computed: {
    hideNavBar() {
      const component = this.$route.matched[0].name || this.$route.name || ''
      if(this.pages.includes(component as string)) {
        return true
      }
      return false
    },
  },
  methods: {
    setData() {
      const element = (document.getElementById("main-div") as HTMLDivElement)
      if(element) {

        if(!this.scrollPos.get(this.$route.name)) {
          this.scrollPos.set(this.$route.name, element.scrollTop);
          this.scrollPosition = element.scrollTop
        }
        if(!this.scrollHeight.get(this.$route.name)) {
          this.scrollHeight.set(this.$route.name, element.scrollHeight - element.clientHeight)
          this.height = element.scrollHeight - element.clientHeight
        }
      }
      
    },
    scroll() {
      const element = (document.getElementById("main-div") as HTMLDivElement);
      // && element.scrollTop > this.topNavHeight
      if(this.lastScrollPos < element.scrollTop ) {
        this.hideTopNav = true
      } else {
        this.hideTopNav = false
      }

      this.lastScrollPos = element.scrollTop
      this.scrollPos.set(this.$route.name, element.scrollTop);
      this.scrollPosition = element.scrollTop
      this.scrollHeight.set(this.$route.name, element.scrollHeight - element.clientHeight)
      this.height = element.scrollHeight - element.clientHeight
      
    },
    isMobile() {
      this.mobile = this.$q.screen.lt.sm
      return this.$q.screen.lt.sm
    },
    async websocketOpen() {
      console.log(this.$store.state.user.id)
      this.websocket = new WebSocket(`wss://localhost:8000/ws/user_notif/${this.$store.state.user.id}/`)
      this.websocketMessage()

      this.websocket.onopen = (e) => {
      }
    },
    async websocketClose() {
      if(!this.websocket) {
        return
      }
      this.websocket.close()

      this.websocket.onclose = (e) => {
        console.log('Websocket closed')
      }
    },
    async websocketMessage() {
      if(!this.websocket) {
        return
      }
      this.websocket.onmessage = (e) => {
        console.log(e)
        const data = JSON.parse(e.data)
        // console.log(data)
        if(data.type === 'posted') {
          const message = JSON.parse(data.message) as Notifications
          console.log(message)
          // this.$store.commit('setNotification', data.notification)
          this.$q.notify({
            progress: true,
            html: true,
            classes: 'bg-theme border',
            group: message.verb,
            message: `
              <div class="flex flex-cols items-center gap-2">
                <div>
                  <img class="rounded-full" src="${message.actor_avatar}" alt="avatar" width="50px" height="50px"/>
                </div>
                  <div class="flex flex-rows min-w-52">
                    <div class="w-full text-xl weight-900 text-heading"> 
                      @${message.actor}
                    <div>
                    <div class="w-full text-base text-body weight-600">
                      ${message.description}
                    </div>
                    <div>
                      <div class="w-full text-sm text-lighter text-normal">
                        ${convertTime(message.timestamp)}
                      </div>
                    </div>
                  </div>
              <div/>
            `,
            actions: [
              { label: 'View', class: 'bg-heading weight-900', handler: () => { this.$router.push('/notifications') } },
              { label: 'Dismiss', color: 'white' }
            ],
          })
        }
        else if(data.type === 'message') {
          this.$store.commit('setMessages', data.message)
        }
      }
    },
    alert() {
      console.log('here')
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
      this.$nextTick(() => {
        this.hideTopNav = false;
        const element = document.getElementById("main-div") as HTMLDivElement;
        element.scrollTop = this.scrollPos.get(this.$route.name);
        this.scrollPosition = this.scrollPos.get(this.$route.name);
        this.height = this.scrollHeight.get(this.$route.name)
        this.bottomNavHeight = ((this.$refs.bottomBar as HTMLDivElement)?.offsetHeight + 10) || 10
      });
    },
    '$q.screen.lt.sm'() {
      this.$nextTick(() => {
        this.bottomNavHeight = ((this.$refs.bottomBar as HTMLDivElement)?.offsetHeight + 10) || 10
      })
    },
    lastScrollPos() {
      const topNav = (this.$refs.topNav as HTMLDivElement)
      const bottomNav = (this.$refs.bottomBar as HTMLDivElement)
      const spillBtn = (this.$refs.spillButton as HTMLDivElement)
      const topNavPos = ((this.topNavHeight < this.lastScrollPos) && `${-this.topNavHeight}`)
      const bottomNavPos = ((this.bottomNavHeight < this.lastScrollPos) && `${-this.bottomNavHeight + 10}`)


      if(topNav) {
        if(this.hideTopNav) {
          topNav.style.transform = `translate3d(0px, 0px, 0px) translateY(${topNavPos}px)`;
        
        } 
        else {
          topNav.removeAttribute('style')
        }
      }

      if(bottomNav) {
        if(this.hideTopNav) {
          bottomNav.style.transform = `translate3d(0px, 0px, 0px) translateY(${-bottomNavPos}px)`;
          spillBtn.style.transform = `translate3d(0px, 0px, 0px) translateY(${-bottomNavPos}px)`;
        } 
        else {
          bottomNav.removeAttribute('style')
          spillBtn.style.removeProperty('transform')
        }
      }
    },
  },
})
</script>

<template>
  <div :class="!isMobile() ? 'main' : 'fixed w-full h-viewport'">
    <div v-if="!$q.screen.lt.sm" class="min-h-viewport h-full w-full">
      <Sidebar/>
    </div>

    <div  ref="mainDiv"  id="main-div" class="w-full">
      <div>
        <div ref="topNav" v-if="!hideNavBar" id="top-nav" :class="{'border-b': $route.matched[0].name != 'notification'}" class="sticky top-0 w-full h-fit bg-transparent bg-blur-1 z-20">
          <TopNav @update:navHeight="topNavHeight = $event"/>
        </div>
        <div :style="{paddingBottom: `${bottomNavHeight - 10}px`}"  class="w-full min-h-viewport border-l border-r">
          <RouterView v-slot="{Component}" >
            <KeepAlive :max="6" :include="['home', 'search', 'explore', 'user-profile', 'view-spill', 'notifications']" >
              <component :is="Component" :key="!['user-profile', 'notifications'].includes(($route.matched[0].name) as string) ? $route.fullPath : null"  :height="height" :scrollPosition="scrollPosition" />
            </KeepAlive>
          </RouterView>
        </div>
      </div>
      
    </div>
    <nav v-if="$q.screen.lt.sm && !hideNavBar" ref="bottomBar" class="sticky bottom-0 w-full z-5">
      <BottomNav/>
    </nav>

    <div ref="spillButton" class="fixed z-15 box-shadow right-1 bg-theme rounded-lg" :style="{bottom: `${bottomNavHeight}px`}" v-if="isMobile() && $route.name !== 'view-spill'">
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
  transition: .1s ease-in-out;
}
.main {
  display: grid;
  width: 100%;
  position: fixed;
  height: 100%;
  grid-template-columns: auto 600px auto;
}


/* #top-nav {
  transition: .5s;
} */

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
  grid-template-columns: auto 1fr;
}

.transform {
  transform: translateY(0);
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


.topNav-enter-active,
.topNav-leave-active {
  transition: all 1s ease;
}

.topNav-enter-from,
.topNav-leave-to {
  transform: translateY(-100%);
}

</style>