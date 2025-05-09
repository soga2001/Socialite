<script lang="ts">
import { defineComponent } from 'vue'
import {http} from '../../assets/http'
import { RouterLink, useRoute, useRouter } from 'vue-router';

import Search from '@/views/Search.vue';
import { logout } from '@/composables/logout';
import { useQuasar } from 'quasar';

export default defineComponent({
  data() {
      return {
        $q: useQuasar(),
        $router: useRouter(),
        $route: useRoute(),
        $store: this.$store,
        theme: false,
        dark_mode: false,
        include: ["home", "explore"],
        iconSize: "5rem",
        navSlideIn: false,
        screen: {},

        report_bug: false,
        bug: '',
        bug_replication: '',
      };
  },
  setup() {
    const $q = useQuasar()
    const screen = $q.screen

    return {
      $q,
      screen
    }
  },
  computed: {
    navStyle(): {justifyContent: string} {
      return {
        justifyContent: this.$store.state.authenticated ? "right" : "center"
      }
    },
    // slideIn(): {width: string} {
    //   return {
    //       width: this.navSlideIn ? '70vw' : '0vw'
    //   }
    // }
    

  },
  methods: {
      switchTheme(e: any) {
        if (this.theme) {
                this.$q.cookies.set("theme", "light");
                document.documentElement.setAttribute("data-theme", "light");
            }
            else {
                this.$q.cookies.set("theme", "dark");
                document.documentElement.setAttribute("data-theme", "dark");
            }
            this.theme = !this.theme;
            this.$store.commit("setTheme", !this.$store.state.dark);
      },
      logout() {
          logout()
          this.navSlideIn = false
      },
      openNav() {
        this.navSlideIn = true
      },
      closeNav() {
        this.navSlideIn = false
      },
      onCancel() {
        this.report_bug = false;
        this.bug = '',
        this.bug_replication = ''
      },
      async reportBug() {
        await http.post('bugs/report_bugs/', {
          bug: this.bug,
          bug_replication: this.bug_replication
        }).then((res) => {
          if(res.data.success) {
            this.bug = ''
            this.bug_replication = ''
            this.report_bug = false
            this.$q.notify({
              type: 'positive',
              message: `<span class="text-white text-xl">${res.data.message}</span>`,
              icon: 'info',
              iconColor: 'white',
              html: true,
            })
          }
          else {
            this.$q.notify({
              type: 'negative',
              message: `<span class="text-white text-xl">${res.data.message}</span>`,
              icon: 'error',
              iconColor: 'white',
              html: true,
            })
          }
        }).catch((err) => {
          console.log(err)
        })
      },
  },
  created() {
      this.theme = this.$q.cookies.get("theme") === "dark";
      this.$store.commit("setTheme", this.theme);
      document.documentElement.setAttribute("data-theme", this.theme ? "dark" : "light");
  },
  mounted() {
    const topNav = this.$refs.topNav as HTMLDivElement;
    this.$emit('update:navHeight', topNav?.offsetHeight)
  },
  watch: {
    '$q.screen.lt.sm': async function() {
      await this.$nextTick()
      const topNav = this.$refs.topNav as HTMLDivElement;
      this.$emit('update:navHeight', topNav?.offsetHeight)
    },
  },
  components: { Search }
})
</script>

<template>
    <nav class="">
      <div class="bg-theme-opacity bg-blur-1">
        <div ref="topNav" class="topNav bg-transparent p-2" v-if="$q.screen.lt.sm">
          <div class="dropdown-btn w-full">
            <Item align-items="center" avatar-size="2.5rem" dense class="w-full bg-transparent">
              <template #avatar v-if="['settings'].includes(($route.matched[0].name)?.toString() || ' ') && $route.name?.toString() !== 'settings'">
                <q-btn flat round color="red" icon="arrow_back " @click="$router.back"/>
              </template>
              <template #avatar v-else>
                <q-avatar size="2.5rem" v-if="$store.state.authenticated" @click="openNav" class="pointer">
                  <img v-if="$store.state.user.avatar" :src="$store.state.user.avatar"/>
                  <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" />
                </q-avatar>
                <q-avatar v-else size="2.5rem">
                  <i-spill size="2rem" />
                </q-avatar>

              </template>
              <template v-if="['explore', 'search'].includes(($route.name)?.toString() || ' ')" #title>
                <Search dense/>
              </template>
              <template #title v-if="['settings'].includes(($route.matched[0].name)?.toString() || ' ')">
                <div class="text-2xl weight-900 text-heading">
                  {{$route.meta.title}}
                </div>
              </template>
              <template v-if="['all-notif', 'mentions'].includes(($route.name)?.toString() || ' ')" #title>
                <div class="text-2xl weight-900 text-heading">
                  Notifications
                </div>
              </template>
              
              <template #icon v-if="['explore', 'search'].includes(($route.name)?.toString() || ' ')">
                <q-btn flat round dense icon="settings" size="16px" class="border" @click.stop="" />
              </template>
              <template #icon  v-if="['all-notif', 'mentions'].includes(($route.name)?.toString() || ' ')">
                <RouterLink @click="closeNav" :to="{name: 'notification-settings'}" :exact="true" class="nav__link w-full rounded" active-class="active" exact-active-class="exact-active">
                  <q-icon size="2rem" name="settings" />
                </RouterLink>
              </template>
              <template #icon v-else>
                <q-btn flat round dense icon="" size="16px"  />
              </template>

            </Item>
            <div class="brand text-2xl weight-900 text-heading" v-if="!['explore', 'search', 'all-notif', 'mentions'].includes(($route.name)?.toString() || ' ') && !['settings'].includes(($route.matched[0].name)?.toString() || ' ')">
              Socialite
            </div>
          </div>
        </div>
        <header v-if="$route.matched[0]?.name == 'notifications' && $store.state.authenticated" ref="header" class="sticky top-0 m-0 max-h-12 overflow-visible bg-theme-opacity">
          <div :style="{height: '64px'}" v-if="!$q.screen.lt.sm" >
            <Item>
              <template #title>
                <span class="text-2xl weight-900">Notifications</span>
              </template>
              <!-- <template #icon>
                <RouterLink @click="closeNav" :to="{name: 'notification-settings'}" :exact="true" class="nav__link w-full rounded p-2" active-class="active" exact-active-class="exact-active">
                  <q-icon size="1.5rem" name="settings" />
                </RouterLink>
              </template> -->
              <template #icon>
                <q-btn :to="{name: 'notification-settings'}" flat round dense icon="settings" size="16px" class="border" @click.stop="" />
              </template>
            </Item>
          </div>
          <q-tabs
              class=" w-full"
              ref="tabs"
              indicator-color="purple-13"
          >
              <q-route-tab class="text-capitalize text-xl" active-class="active" :to="{name: 'all-notif'}" exact replace>
                  <span>All</span>
              </q-route-tab>
              <q-route-tab class="text-capitalize text-xl" active-class="active"  :to="{name: 'mentions'}" exact replace>
                  <span>Mentions</span>
              </q-route-tab>
          </q-tabs>
        </header>
        <header v-if="$route.matched[0]?.name == 'home' && !$q.screen.lt.sm" ref="header" class="text-2xl weight-900">
          <Item>
              <template #title>
                <span class="text-2xl weight-900">Home</span>
              </template>
              <!-- <template #icon>
                <q-btn flat round dense icon="settings" size="16px" @click.stop="" />
              </template> -->
            </Item>
        </header>
        <header class="sticky top-0 p-2 m-0 max-h-12 overflow-visible bg-theme-opacity" v-if="!$q.screen.lt.sm && $route.matched[0]?.name == 'explore'">
          <Item align-items="center" dense class="w-full overflow-visible bg-transparent">
              <template v-if="$route.name=='explore'" #title>
                <SearchBar dense />
              </template>
              <template #icon>
                <q-btn flat round dense icon="settings" size="16px" class="border" @click.stop="" />
              </template>
            </Item>
        </header>
      </div>

      <q-dialog class="w-viewport h-viewport"  :maximized="true" v-model="navSlideIn" :position="'left'">
        <div>
          <div class="overlay bg-blur-1" @click="closeNav"></div>

          <div class="slide-in-nav list">
            <div class="rest_nav">
              <Item class="item ">
                <template #title>
                  <span class="weight-900 text-xl text-heading" >Account Info</span>
                </template>
                <template #icon>
                  <i-close class="pointer" fill="var(--color-heading)" stroke="none" size="2rem" @click="closeNav" />
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
                  <span class="weight-900"> 
                    {{ $store.state.user.full_name }}
                  </span>
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
              <q-item clickable tabindex="0" @click.stop="report_bug = true">
                  <q-item-section avatar>
                    <q-avatar size="3.5rem">
                      <q-icon size="2rem" :color="$store.state.dark ? 'white' : 'black'" name="o_bug_report" />
                    </q-avatar>
                  </q-item-section>
                  <q-item-section>
                  <q-item-label class="text-2xl text-body weight-700">Report Bugs</q-item-label>
                  </q-item-section>
              </q-item>
              <q-item clickable tabindex="0" v-on:click="switchTheme">
                  <q-item-section avatar>
                    <q-avatar size="3.5rem">
                      <Transition>
                        <q-icon v-if="$store.state.dark" size="2rem" color="white" name="o_dark_mode" />
                        <q-icon v-else size="2rem" color="black" name="o_light_mode" />
                      </Transition>
                    </q-avatar>
                  </q-item-section>
                  <q-item-section>
                  <q-item-label class="text-2xl text-body weight-700">Theme</q-item-label>
                  </q-item-section>
              </q-item>

              <!-- <q-list class="bg-theme rounded-sm" dense>
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
                <q-item clickable tabindex="0" @click.stop="report_bug = true">
                    <q-item-section avatar>
                      <q-avatar size="3.5rem">
                        <q-icon size="2rem" :color="$store.state.dark ? 'white' : 'black'" name="o_bug_report" />
                      </q-avatar>
                    </q-item-section>
                    <q-item-section>
                    <q-item-label class="text-2xl text-body weight-700">Report Bugs</q-item-label>
                    </q-item-section>
                </q-item>
                <q-item clickable tabindex="0" v-on:click="switchTheme">
                    <q-item-section avatar>
                      <q-avatar size="3.5rem">
                        <Transition>
                          <q-icon v-if="$store.state.dark" size="2rem" color="white" name="o_dark_mode" />
                          <q-icon v-else size="2rem" color="black" name="o_light_mode" />
                        </Transition>
                      </q-avatar>
                    </q-item-section>
                    <q-item-section>
                    <q-item-label class="text-2xl text-body weight-700">Theme</q-item-label>
                    </q-item-section>
                </q-item>
              </q-list> -->
            </div>
            <q-dialog :class="{'min-h-sm': !$q.screen.lt.sm}" v-model="report_bug" position="top" persistent :maximized="$q.screen.lt.sm">
                    <div :class="{'mt-12': !$q.screen.lt.sm, 'h-fit': !$q.screen.lt.sm, 'min-h-viewport': $q.screen.lt.sm}" class="bg-theme box-shadow w-full h-full min-h-fit max-w-sm  overflow-visible rounded-sm" >
                      <div class="p-2">
                        <Item dense :vert-icon-center="true">
                          <template #title>
                            <div class="text-2xl weight-900">Bug Report</div>
                          </template>
                          <template #icon>
                            <i-close size="2rem" class="pointer" @click="onCancel"/>
                          </template>
                        </Item>
                      </div>
                      <hr class="border"/>
                      <div class="">
                        <form @submit.prevent="" class="flex flex-col gap-2 p-2">
                          <!-- <input class="w-full p-2 text-xl text-heading" type="text" placeholder="Bug"/> -->
                          <Input showCharCounts :charLimit="30" @update:val="bug = $event" input_type="text" input_label="Bug" id="first_name" class="w-full my-2" />
                          <Textarea showCharCounts :charLimit="255" maxHeight="176" height="200px" @update:val="bug_replication = $event" input_type="text" input_label="How to replicate" id="username" class="w-full my-2" />
                        </form>
                      </div>
                      <div class="flex flex-rows sticky bottom-0">
                        <div class="flex flex-rows gap-2 p-2 ml-auto">
                          <button class="px-7 py-2 border-none rounded text-base text-heading weight-900" @click="onCancel">Cancel</button>
                          <button class="px-7 py-2 border-none pointer bg-web-theme rounded text-base text-heading weight-900" @click="reportBug">Submit</button>
                        </div>
                      </div>
                    </div>
                   </q-dialog>
            <div class="pb-3 w-full">
              <!-- <q-item>
                  <q-item-section avatar top>
                    <theme-toggle/>
                  </q-item-section>

                  <q-item-section class="hide">
                    <q-item-label lines="1">
                      <span class="text-bold text-heading text-xl">Theme</span>
  
                    </q-item-label>
                    <q-item-label caption lines="1">
                      <span class="text-body weight-800">{{ $store.state.dark ? 'Dark' : 'Light' }}</span>
                    </q-item-label>
                  </q-item-section>
                </q-item> -->
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
      </q-dialog>
    </nav>
</template>


<style scoped lang='scss'>

.active {

  span {
    color: var(--color-heading);
    font-weight: 900;
  }
}


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
  min-width: 250px;
  width: 60vw;
  z-index: 999;
  background-color: var(--color-background);
  border-right: 3px solid var(--color-border);
  overflow-x: hidden;
  transition: 0.25s;
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
  font-size: calc(.8em + 1vw);
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