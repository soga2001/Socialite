<script lang="ts">
import { useCookies } from 'vue3-cookies';
import { defineComponent } from 'vue'
import {http} from '../../assets/http'
import { RouterLink } from 'vue-router';
import router from '../../router';
import Spills from '../Spills.vue';
import {logout} from '@/composables/logout'
export default defineComponent({
    data() {
        return {
            theme: false,
            dark_mode: false,
            include: ["home", "explore"],
            iconSize: "5rem",
            navSlideIn: false,
            post: false,

            report_bug: false,
            theme_toggle: false,

            bug: '',
            bug_replication: '',

        };
    },
    setup() {
        const { cookies } = useCookies();
        return { cookies };
    },
    computed: {
        navStyle(): {
            justifyContent: string;
        } {
            return {
                justifyContent: this.$store.state.authenticated ? "right" : "center"
            };
        },
        slideIn(): {
            width: string;
        } {
            return {
                width: this.navSlideIn ? "250px" : "0vh"
            };
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
            this.theme = !this.theme;
            this.$store.commit("setTheme", !this.$store.state.dark);
        },
        logout() {
            logout()
        },
        openNav() {
            this.navSlideIn = true;
        },
        closeNav() {
            this.navSlideIn = false;
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
        onCancel() {
          this.report_bug = false;
          this.bug = '',
          this.bug_replication = ''
        }
    },
    created() {
        this.theme = this.cookies.get("theme") === "dark";
        this.$store.commit("setTheme", this.theme);
        document.documentElement.setAttribute("data-theme", this.theme ? "dark" : "light");
    },
    mounted() {
    },
    watch: {
      '$route': function() {

      },
      // watch quasar dev's screen size changes in vue3 component ?
    },
    components: { Spills }
})
</script>

<template>
    <header>
        <nav class="nav" :style="navStyle">
            <q-list class="list text-2xl">
                <div class="pt-2">
                  <RouterLink to="/" class="nav__link">
                      <q-item :clickable="false" class="hide">
                        <q-item-section avatar>
                          <q-btn flat round>
                            <i-home size="2rem" :fill="$route.fullPath == '/home' ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                          </q-btn>
                        </q-item-section>
                      </q-item>

                      <div class="show p-2">
                        <i-home size="2rem" :fill="$route.fullPath == '/home' ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                      </div>
                  </RouterLink>
                  <RouterLink to="/home" class="nav__link" active-class="active text-heading" v-if="$store.state.authenticated">
                      <q-item class="hide">
                        <q-item-section avatar>
                            <i-home size="2rem" :fill="$route.fullPath == '/home' ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                        </q-item-section>

                        <q-item-section class="bold">
                            Home
                        </q-item-section>
                      </q-item>
                      <div class="show p-2">
                        <i-home size="2rem" :fill="$route.fullPath == '/home' ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                      </div>
                  </RouterLink>

                  <RouterLink to="/explore" class="nav__link" active-class="active">
                      <q-item class="hide">
                      <q-item-section avatar>
                          <i-explore size="2rem" :fill="$route.fullPath == '/explore' ? 'var(--color-heading)' : 'none'" :stroke="$route.fullPath == '/explore' ? 'none' : 'var(--color-heading)'" />
                      </q-item-section>

                      <q-item-section class="bold">
                          Explore
                      </q-item-section>
                      </q-item>
                      <div class="show p-2">
                        <i-explore class="show" size="2rem" :fill="$route.fullPath == '/explore' ? 'var(--color-heading)' : 'none'" :stroke="$route.fullPath == '/explore' ? 'none' : 'var(--color-heading)'" />                      
                      </div>
                  </RouterLink>
                  <RouterLink v-if="$store.state.authenticated" to="/notifications" class="nav__link relative" active-class="active">
                      <q-item class="hide relative">
                        <q-item-section avatar class="relative">
                          <!-- <div class="relative">
                            <q-badge class="bg-web-theme" rounded floating />
                          </div> -->
                          <q-avatar class="relative p-0 m-0">
                            <i-notif size="2rem" :fill="$route.matched[0].name == `notifications` ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                            <q-badge class="bg-web-theme" rounded floating />
                          </q-avatar>
                        </q-item-section>

                        <q-item-section class="bold relative">
                            Notifications
                        </q-item-section>
                        
                      </q-item>
                      <div class="show relative">
                        <i-notif class="show" size="2rem" :fill="$route.matched[0].name == `notifications` ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                        <q-badge class="bg-web-theme" rounded floating />
                      </div>
                  </RouterLink>

                  <RouterLink :to="{name: 'user-profile', params: {username: $store.state.user.username}}" :exact="true" v-if="$store.state.authenticated" class="nav__link" active-class="active" exact-active-class="exact-active">
                      <q-item class="hide">
                        <q-item-section avatar>
                            <i-profile size="2rem" :fill="($route.path.startsWith(`/${$store.state.user.username}`) && $route.matched[0].name === 'user-profile') ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                        </q-item-section>

                        <q-item-section class="bold">
                            Profile
                        </q-item-section>
                      </q-item>
                      <div class="show p-2">
                        <i-profile size="2rem" :fill="($route.path.startsWith(`/${$store.state.user.username}`) && $route.matched[0].name === 'user-profile') ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                      </div>
                  </RouterLink>

                  <RouterLink to="/settings" v-if="$store.state.authenticated" class="nav__link" active-class="active">
                      <q-item class="hide">
                        <q-item-section avatar>
                            <i-settings size="2rem" :fill="$route.matched[0].name == 'settings' ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                        </q-item-section>

                        <q-item-section class="bold">
                            Settings
                        </q-item-section>
                      </q-item>
                      <div class="show p-2">
                        <i-settings size="2rem" :fill="$route.matched[0].name == 'settings' ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />                        
                      </div>
                  </RouterLink>
                  <div class="nav__link" v-if="$store.state.authenticated">
                    <q-btn no-caps dense rounded flat class=" p-0" >
                      <q-item class="hide">
                        <q-item-section avatar>
                            <!-- <q-icon size="1.5rem" :color="( $store.state.dark ? 'white' : 'black')" class="border-brighter-3 rounded" name="more_horiz" /> -->
                            <i-more-circle size="2rem"/>
                        </q-item-section>

                        <q-item-section class="text-2xl">
                            More
                        </q-item-section>
                      </q-item>
                      <div class="show p-2">
                        <q-icon size="2rem" :color="( $store.state.dark ? 'white' : 'black')" class="border-brighter-3 rounded" name="more_horiz" />                        
                      </div>


                      
                      <q-menu cover square max-width="300px" class="w-full border rounded-sm" anchor="bottom left">
                          <q-list class="bg-theme rounded-sm" dense>
                            <q-item clickable v-close-popup tabindex="0" v-on:click="report_bug = true">
                                <q-item-section avatar>
                                  <q-avatar size="3.5rem">
                                    <q-icon size="2rem" :color="$store.state.dark ? 'white' : 'black'" name="bug_report" />
                                  </q-avatar>
                                </q-item-section>
                                <q-item-section>
                                <q-item-label class="text-2xl text-heading weight-700">Report Bugs</q-item-label>
                                </q-item-section>
                            </q-item>
                            <q-item clickable v-close-popup tabindex="0" v-on:click="switchTheme">
                                <q-item-section avatar>
                                  <q-avatar size="3.5rem">
                                    <Transition>
                                      <q-icon v-if="$store.state.dark" size="2rem" color="white" name="dark_mode" />
                                      <q-icon v-else size="2rem" color="black" name="light_mode" />
                                    </Transition>
                                  </q-avatar>
                                </q-item-section>
                                <q-item-section>
                                <q-item-label class="text-2xl text-heading weight-700">Theme</q-item-label>
                                </q-item-section>
                            </q-item>
                          </q-list>
                      </q-menu>
                    </q-btn>
                  </div>


                  
                  <div v-if="$store.state.authenticated" class="w-full flex justify-center" @click="post = !post">
                   <button class=" hide w-full px-15 py-3 text-xl rounded-lg border-none pointer btn-themed weight-900 ">Spill</button>
                   <q-btn class="show btn-themed text-heading" round flat icon="add"/>
                  </div>

                  <q-dialog class="min-h-sm" v-model="post" position="top" persistent>
                    <div class="mt-12 bg-theme box-shadow w-full min-h-fit max-w-sm h-fit overflow-visible rounded-sm" >
                      <div class="p-2">
                        <Item dense :vert-icon-center="true">
                          <template #title>
                            <div class="text-2xl weight-900">Spill</div>
                          </template>
                          <template #icon>
                            <i-close size="2rem" class="pointer" @click="post = false"/>
                          </template>
                        </Item>
                      </div>
                      <hr class="border"/>
                      <div class="">
                        <Spills :rows="4"/>
                      </div>
                    </div>
                   </q-dialog>

                   <q-dialog class="min-h-sm" v-model="report_bug" position="top" persistent>
                    <div class="mt-12 bg-theme box-shadow w-full min-h-fit max-w-sm h-fit overflow-visible rounded-sm" >
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
                      <hr class="border"/>
                      <div class="flex flex-rows">
                        <div class="flex flex-rows gap-2 p-2 ml-auto">
                          <button class="px-7 py-2 border-none rounded text-base text-heading weight-900" @click="onCancel">Cancel</button>
                          <button class="px-7 py-2 border-none pointer bg-web-theme rounded text-base text-heading weight-900" @click="reportBug">Submit</button>
                        </div>
                      </div>
                    </div>
                   </q-dialog>

                  <RouterLink to="/login" class="nav__link" active-class="active" v-if="!$store.state.authenticated">
                      <q-item class="hide">
                      <q-item-section avatar>
                          <i-login size="3rem" :fill="$route.fullPath == `/login` ? 'var(--color-heading)' : 'none'" stroke="var(--color-heading)" />
                      </q-item-section>

                      <q-item-section class="bold">
                          Login
                      </q-item-section>
                      </q-item>
                      <i-login class="show" size="3rem" :fill="$route.fullPath == `/login` ? 'var(--color-heading)' : 'none'" stroke="var(--color-heading)" />
                  </RouterLink>

                  <RouterLink to="/Register" class="nav__link" active-class="active" v-if="!$store.state.authenticated">
                      <q-item class="hide">
                      <q-item-section avatar>
                          <q-icon class="icon" name="o_app_registration" />
                      </q-item-section>

                      <q-item-section class="bold">
                          Register
                      </q-item-section>
                      </q-item>
                      <q-avatar size="iconSize" icon="app_registration" class="show icon">
                      <q-tooltip anchor="top middle" self="bottom middle">
                          Register
                      </q-tooltip>
                      </q-avatar>
                  </RouterLink>
                </div>

                <div class="rest__nav ">
                    <!-- <q-item> 
                      <q-item-section avatar top>
                        <theme-toggle/>
                      </q-item-section>

                      <q-item-section class="hide">
                        <q-item-label lines="1">
                          <span class="text-bold text-heading text-xl">Theme</span>
      
                        </q-item-label>
                        <q-item-label caption lines="1">
                          <transition name="fade" mode="out-in">
                              <span class="text-body weight-700" v-if="$store.state.dark">Dark</span>
                              <span class="text-body weight-700" v-else>Light</span>
                          </transition>
                        </q-item-label>
                      </q-item-section>
                    </q-item> -->

                    <div class="dropdown-btn flex w-full justify-center">
                        <q-btn no-caps dense rounded flat class="dropdown" v-if="$store.state.authenticated">
                          <div class="hide item">
                            <Item dense avatarSize="3rem">
                                <template #avatar>
                                  <img v-if="$store.state.user.avatar" :src="$store.state.user.avatar"/>
                                  <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" />
                                </template>
                                <template #title>
                                  <div class="flex items-center gap-1">
                                    <span class="text-xl text-heading weight-900">{{ $store.state.user.full_name}}</span>
                                    <q-icon v-if="$store.state.user.private" class="vert-align-middle "  :color="$store.state.dark ? 'white' : 'black'" size="1.3rem" name="lock">
                                        <q-tooltip :delay="1000" class="bg-theme text-heading box-shadow text-sm">
                                            Private
                                        </q-tooltip>
                                    </q-icon>
                                  </div>
                                </template>
                                <template #caption>
                                  <span class="subtitle">@{{ $store.state.user.username }}</span>
                                </template>
                                <template #icon>
                                  <q-icon class="text-heading" name="more_vert" />
                                </template>
                            </Item>
                          </div>

                        <div class="show item p-0 m-0">
                          <Item :border="false" dense avatarSize="3rem" >
                              <template #avatar>
                                <img v-if="$store.state.user.avatar" :src="$store.state.user.avatar"/>
                                <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="w-full h-full" />
                              </template>
                          </Item>
                        </div>
                        
                        <q-menu fit square anchor="bottom left">
                            <q-list class="bg-theme border" dense>
                            <q-item clickable v-close-popup tabindex="0" v-on:click="logout">
                                <q-item-section avatar>
                                  <q-avatar icon="logout" />
                                </q-item-section>
                                <q-item-section>
                                <q-item-label>Logout</q-item-label>
                                </q-item-section>
                            </q-item>
                            </q-list>
                        </q-menu>
                        </q-btn>
                    </div>
                </div>
            </q-list>
        </nav>
    </header>
    
</template>

<style scoped lang="scss">

/*mixin*/
@mixin trim{text-overflow:ellipsis; white-space:nowrap; overflow:hidden; display:block;}
@mixin scroll{overflow-y:auto; scrollbar-width:thin; /*-webkit-overflow-scrolling:touch;*/}


header {
  @include scroll();
  position:sticky; top:0; max-height:100vh; overflow:auto;
  @media #{$break1}{
    display: none;
  }
  @media #{$break2} {
    padding: 0px;
  }
  @media #{$break3}, #{$break4}{
    padding:0 10px; 
  }
  @media #{$break5open}{
    // min-width:88px; 
    // width:300px; 
    padding-#{$end-direction}: 10px;  
  }
}

.nav {
  height: 100vh;
  height: 100dvh;
  width: 100%;
  display: flex;
  justify-content: right;
  background-color: transparent;
  
}


  

.item {
  height: fit-content;
}

.logout {
  padding: 0 28px;
  font-size: 25px;
  color: var(--color-heading);
}

.follow {
  display: flex;
}



.nav .brand {
  width: fit-content;
  font-size: 25px;
  font-weight: 300;
  width: 100%;
  color: var(--color-heading);
  margin-top: 0 !important;
}

.nav .brand:hover {
  background-color: transparent !important;
}

.nav .logo {
  font-weight: 900;
  color: var(--color-heading);
}

.list {
  padding: 0;
  margin: 0;
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
  
  font-weight: 700 !important;
}

.nav__link {
  color: var(--color-text);
  font-weight: 300;
  width: fit-content;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 15px 0;
}


.nav__link.active {
  color: var(--color-heading) !important;
  font-weight: 900;
  /* background-color: var(--color-background-mute); */
  border-radius: 30px;
}

.nav__link.active .bold {
  font-weight: 900;
  color: var(--color-heading);
}

.nav__link.exact-active {
  color: var(--color-heading) !important;
  /* background-color: var(--color-background-mute); */
  border-radius: 30px;
}

.nav__link:hover {
  background-color: var(--color-background-soft);
  color: var(--color-heading);
  font-weight: 900;
  border-radius: 30px;
}


/* .nav__link:hover .bold {
  font-weight: 900;
} */


.dropdown__main {
  background-color: var(--color-background-mute);
  /* color: var(--text-heading); */
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.username {
  color: var(--color-text);
}



/* nav icons */

.show {
  display: none;
}

// @media #{$break2}, #{$break3}, #{$break4}{
  //     width:68px; padding:0 10px; 
  // }

  @media #{$break2}, #{$break3} {
  .show {
    display:flex;
  }

  .nav {
    padding: 0;
    margin: 0;
  }

  .item {
    min-width: 0;
  }

  .hide {
    display: none;
  }

  .nav__link:hover {
    background-color: transparent !important;
  }

  .nav__link {
    width: 100%;
    display: flex;
    border-radius: 50%;
    /* padding: 10px; */
  }
}


/* Reference: https://uiverse.io/alexruix/splendid-liger-23 */

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>