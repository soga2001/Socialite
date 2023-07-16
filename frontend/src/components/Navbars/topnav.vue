<script lang="ts">
import { useCookies } from 'vue3-cookies';
import { defineComponent } from 'vue'
import {http} from '../../assets/http'
import { RouterLink, RouterView } from 'vue-router';
import router from '../../router';
import { useStore } from '../../store/store';
import Item from '../Item.vue';
// import Themetoggle from '../themetoggle.vue';
import ProfileIcon from '@/icons/i-profile.vue'

import Search from '@/views/Search.vue';
export default defineComponent({
  data() {
      return {
          theme: false,
          dark_mode: false,
          include: ["home", "explore"],
          iconSize: "5rem",
          navSlideIn: false
      };
  },
  setup() {
      const { cookies } = useCookies();
      return { cookies };
  },
  computed: {
    navStyle(): {justifyContent: string} {
      return {
        justifyContent: this.$store.state.authenticated ? "right" : "center"
      }
    },
    slideIn(): {width: string} {
      return {
          width: this.navSlideIn ? '70vw' : '0vw'
      }
    }
    

  },
  methods: {
      switchTheme(e: any) {
          if (this.theme) {
              this.cookies.set("theme", "light");
              document.documentElement.setAttribute("data-theme", "light");
          }
          else {
              this.cookies.set("theme", "dark");
              document.documentElement.setAttribute("data-theme", "dark");
          }
          this.$store.commit("setTheme", !this.$store.state.dark);
      },
      logout() {
          http.post("users/logout/").then((res) => {
            this.navSlideIn = false
            this.$store.commit("authenticate", false);
            this.$store.commit("setDefaultUser");
            router.push("/login");
          }).catch((err) => {
              console.log(err);
          });
      },
      openNav() {
        this.navSlideIn = true
      },
      closeNav() {
        this.navSlideIn = false
      }
  },
  created() {
      this.theme = this.cookies.get("theme") === "dark";
      this.$store.commit("setTheme", this.theme);
      document.documentElement.setAttribute("data-theme", this.theme ? "dark" : "light");
  },
  mounted() {
    const topNav = this.$refs.topNav as HTMLDivElement;
    this.$emit('update:navHeight', topNav?.offsetHeight)
  },
  watch: {
  },
  components: { Item, ProfileIcon, Search }
})
</script>

<template>
    <nav  class="bg-theme-opacity">
      <div ref="topNav" class="topNav p-2 bg-transparent" v-if="$store.state.authenticated && $q.screen.lt.sm">
          <div class="dropdown-btn z-1000 w-full bg-transparent">
            <Item align-items="center" dense v-if="$store.state.authenticated" class="w-full bg-transparent">
                <template #avatar>
                  <div @click="openNav">
                    <img v-if="$store.state.user.avatar" :src="$store.state.user.avatar"/>
                    <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" />
                  </div>
                </template>
                <template v-if="['explore', 'search'].includes(($route.name)?.toString() || ' ')" #title>
                  <Search dense/>
                </template>
                <template v-if="['all-notif', 'mentions'].includes(($route.name)?.toString() || ' ')" #title>
                  <div class="text-2xl weight-900 text-heading">
                    Notifications
                  </div>
                </template>
                
                <template #icon v-if="['explore', 'search'].includes(($route.name)?.toString() || ' ')">
                  <q-btn flat round dense icon="settings" size="16px" class="border" @click.stop="" />
                </template>
                <template #icon v-else>
                </template>
            </Item>
              <div class="brand text-2xl weight-900 text-heading" v-if="!['explore', 'search', 'all-notif', 'mentions'].includes(($route.name)?.toString() || ' ')">
                Socialite
              </div>
          </div>

          <div class="overlay bg-blur-1" v-if="navSlideIn" @click="closeNav"></div>

          <div class="slide-in-nav list" :style="slideIn">
            <div class="rest_nav">
              <Item class="item">
                <template #title>
                  Account Info
                </template>
                <template #icon>
                  <q-btn flat round dense icon="close" size="16px" @click="closeNav" />
                </template>
              </Item>
              <div>
                <Item :vert-icon-center="true">
                  <template #avatar>
                    <div class="pointer" @click="() => {$router.push({name: 'user-profile', params: {username: $store.state.user.username}}), closeNav()}">
                      <img v-if="$store.state.user.avatar" :src="$store.state.user.avatar"/>
                      <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" />
                    </div>
                  </template>
                  <template #icon>
                    <q-btn flat round dense icon="add" size="16px" class="border" @click.stop="" />
                  </template>
                </Item>
              </div>
              
              <Item class="item">
                <template #title>
                  {{ $store.state.user.first_name + ' ' + $store.state.user.last_name }}
                </template>
                <template #caption>
                  @{{ $store.state.user.username }}
                </template>
              </Item>
              <div class="text-base flex items-center ml-2 gap-3">
                <span class="text-body btn"><span class="text-heading weight-900">{{ $store.state.user.total_followers }} </span> Followers</span> 
                <span class="text-body btn"><span class="text-heading weight-900">{{ $store.state.user.total_following }} </span> Following</span>
              </div>
                    

              <RouterLink @click="closeNav" :to="{name: 'user-profile', params: {username: $store.state.user.username}}" :exact="true" v-if="$store.state.authenticated" class="nav__link w-full rounded-none" active-class="active" exact-active-class="exact-active">
                <q-item>
                  <q-item-section avatar>
                      <i-profile size="2rem" :fill="$route.path.startsWith(`/${$store.state.user.username}`) ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                  </q-item-section>

                  <q-item-section class="bold">
                      Profile
                  </q-item-section>
                </q-item>
              </RouterLink>
            </div>
            <div class="pb-3 w-full">
              <q-item class="logout" clickable v-close-popup @click="logout">
                <q-item-section avatar>
                  <i-logout size="3rem" fill="none" stroke="var(--color-heading)" />
                </q-item-section>
                <q-item-section class="bold">
                  Logout
                </q-item-section>
              </q-item>
            </div>
          </div>
      </div>
        <header v-if="$route.matched[0].name == 'notifications'" ref="header" class="w-full z-5 border-b">
        <div v-if="!$q.screen.lt.sm" >
          <Item>
            <template #title>
              <span class="text-2xl weight-900">Notifications</span>
            </template>
            <template #icon>
              <q-btn flat round dense icon="settings" size="16px" @click.stop="" />
            </template>
          </Item>
        </div>
        <q-tabs
            class=" w-full text-lg text-capitalize"
            ref="tabs"
        >
            <q-route-tab class="text-capitalize" active-class="active" :to="{name: 'all-notif'}" exact replace>
                <span>All</span>
            </q-route-tab>
            <q-route-tab class="text-capitalize" active-class="active"  :to="{name: 'mentions'}" exact replace>
                <span>Mentions</span>
            </q-route-tab>
        </q-tabs>
      </header>
    </nav>
</template>


<style scoped>
@import '@/assets/base.css';

/* .nav {
  transition-delay: .25s;
  transition: backdrop-filter .25s linear;
} */


.topNav .dropdown-btn img {
  width: 3rem;
}


.item {
  height: fit-content;
}
.item img {
  width: 3rem;
  height: 3rem;
}

.slide-in-nav {
  height: 100%;
  width: 0;
  position: fixed;
  z-index: 999;
  top: 0;
  left: 0;
  bottom: 0;
  background-color: var(--color-background);
  border-right: 3px solid var(--color-border);
  overflow-x: hidden;
  transition: 0.25s;
  /* padding-top: .1rem; */

  display: grid;
}

.brand {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.slide-in-nav a {
  padding: 0 10px 0 10px;
  text-decoration: none;
  font-size: 25px;
  /* color: #818181; */
  color: var(--color-heading);
  display: block;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* background-color: var(--color-hover); */
  background-color: rgba(0,0,0,0.5);
  z-index: 999; /* Set the z-index to a value higher than the slide-in menu */
}

.slide-in-nav a:hover {
  color: #f1f1f1;
}

.logout {
  padding: 0 28px;
  font-size: 25px;
  color: var(--color-heading);
}

.follow {
  display: flex;
}

.list {
  display: grid;
  grid-template-rows: 1fr auto;
}

.rest__nav {
  margin-bottom: 1rem;
}

a {
  text-decoration: none;
  transition: 0.2s;
  width: 100%;
  font-size: calc(.8em + 1vw);;
}

.nav__link {
  color: var(--color-text);
  font-weight: 300;
  width: fit-content;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 10px 0;
}


.nav__link.active {
  color: var(--color-heading) !important;
  font-weight: 900;
  border-radius: 30px;
}

.nav__link.active .bold {
  font-weight: 900;
}

.nav__link.exact-active {
  color: var(--color-heading) !important;
  /* background-color: var(--color-background-mute); */
  border-radius: 30px;
}


.nav__link.active .icon {
  /* color: var(--color-heading); */
  -webkit-text-stroke: 1px var(--color-text);
}
.nav__link.active .icon.search {
  -webkit-text-stroke: 2px var(--color-text);
}

.nav__link:hover {
  background-color: var(--color-background-mute);
  color: var(--color-heading);
  font-weight: 900;
  border-radius: 30px;
}

.dropdown-btn {
  width: 100%;
  display: flex;
}

.top-nav .dropdown {
  position: relative;
  display: inline-block;
}

.dropdown__main {
  background-color: var(--color-background-mute);
  color: var(--text-heading);
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.username {
  color: var(--color-text);
}
 
</style>