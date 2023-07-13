<script lang="ts">
import { useCookies } from 'vue3-cookies';
import { defineComponent } from 'vue'
import {http} from '../../assets/http'
import { RouterLink } from 'vue-router';
import router from '../../router';
import Spills from '../Spills.vue';
export default defineComponent({
    data() {
        return {
            theme: false,
            dark_mode: false,
            include: ["home", "explore"],
            iconSize: "5rem",
            navSlideIn: false,
            post: false,
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
            this.$store.commit("setTheme", !this.$store.state.dark);
        },
        logout() {
            http.post("users/logout/").then((res) => {
                this.navSlideIn = false;
                this.$store.commit("authenticate", false);
                this.$store.commit("setDefaultUser");
                router.push("/login");
            }).catch((err) => {
                console.log(err);
            });
        },
        openNav() {
            this.navSlideIn = true;
        },
        closeNav() {
            this.navSlideIn = false;
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
    },
    components: { Spills }
})
</script>

<template>
    <header>
        <nav class="nav sticky" :style="navStyle">
            <q-list class="list">
                <div class="">
                  <!-- <RouterLink to="/home" class="brand">
                      <q-item class="hide">
                      <q-item-section avatar>
                          BB
                      </q-item-section>
                      </q-item>
                      <q-avatar rounded :size="iconSize" icon="BB" class="show"/>
                  </RouterLink> -->
                  <RouterLink to="/home" class="nav__link" active-class="active" v-if="$store.state.authenticated">
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

                      <!-- <Item dense class="hide">
                        <template #avatar>
                          <i-home size="10px" :fill="$route.fullPath == '/home' ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                        </template>
                        <template #title>
                          <div class="text-h6">Home</div>
                        </template>
                      </Item>
                      <Item class="show">
                        <template #avatar>
                          <i-home size="2rem" :fill="$route.fullPath == '/home' ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                        </template>
                      </Item> -->
                  </RouterLink>

                  <RouterLink to="/explore" class="nav__link" active-class="active">
                      <q-item class="hide">
                      <q-item-section avatar>
                          <!-- <q-icon class="icon" :name="$route.fullPath == '/explore' ? 'explore' : 'o_explore'" /> -->
                          <i-explore size="2rem" :fill="$route.fullPath == '/explore' ? 'var(--color-heading)' : 'none'" :stroke="$route.fullPath == '/explore' ? 'none' : 'var(--color-heading)'" />
                      </q-item-section>

                      <q-item-section class="bold">
                          Explore
                      </q-item-section>
                      </q-item>
                      <div class="show p-2">
                        <i-explore class="show" size="2rem" :fill="$route.fullPath == '/explore' ? 'var(--color-heading)' : 'none'" :stroke="$route.fullPath == '/explore' ? 'none' : 'var(--color-heading)'" />                      
                      </div>
                      <!-- <i-explore class="show" size="2rem" :fill="$route.fullPath == '/explore' ? 'var(--color-heading)' : 'none'" :stroke="$route.fullPath == '/explore' ? 'none' : 'var(--color-heading)'" /> -->
                  </RouterLink>
                  <RouterLink v-if="$store.state.authenticated" to="/notifications" class="nav__link relative" active-class="active">
                      <q-item class="hide relative">
                        <q-item-section avatar>
                            <!-- <q-icon class="icon" :name="$route.fullPath == '/notifications' ? 'notifications' : 'o_notifications'" /> -->
                            <i-notif size="2rem" :fill="$route.matched[0].name == `notifications` ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                        </q-item-section>

                        <q-item-section class="bold relative">
                            Notifications
                        </q-item-section>
                        <q-badge class="bg-web-theme" rounded floating />
                      </q-item>
                      <div class="show relative">
                        <i-notif class="show" size="2rem" :fill="$route.fullPath == '/notifications' ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                        <q-badge class="bg-web-theme" rounded floating />
                      </div>

                  </RouterLink>



                  <RouterLink to="/search" class="nav__link" active-class="active">
                      <q-item class="hide">
                        <q-item-section avatar>
                            <!-- <q-icon class="icon search" :name="$route.fullPath == '/search' ? 'search' : 'o_search'" /> -->
                            <i-search size="2rem" :fill="$route.fullPath == '/search' ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                        </q-item-section>

                        <q-item-section class="bold">
                            Search
                        </q-item-section>
                      
                      </q-item>
                      <div class="show p-2">
                        <i-search class="show" size="2rem" :fill="$route.fullPath == '/search' ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                      </div>
                      <!-- <i-search class="show" size="2rem" :fill="$route.fullPath == '/search' ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" /> -->
                  </RouterLink>

                  <RouterLink :to="{name: 'user-profile', params: {username: $store.state.user.username}}" :exact="true" v-if="$store.state.authenticated" class="nav__link" active-class="active" exact-active-class="exact-active">
                      <q-item class="hide">
                        <q-item-section avatar>
                            <!-- <q-icon class="icon" :name="$route.fullPath == `/${$store.state.user.username}/` ? 'account_circle' : 'o_account_circle'" /> -->
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
                          <!-- <q-icon class="icon" :name="$route.fullPath == '/settings' ? 'settings' : 'o_settings'" /> -->
                          <i-settings size="2rem" :fill="$route.fullPath == '/settings' ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />
                      </q-item-section>

                      <q-item-section class="bold">
                          Settings
                      </q-item-section>
                      </q-item>
                      <div class="show p-2">
                        <i-settings size="2rem" :fill="$route.fullPath == '/settings' ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" />                        
                      </div>
                      <!-- <i-settings class="show" size="2rem" :fill="$route.fullPath == '/settings' ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'" /> -->
                  </RouterLink>
                  
                  <div v-if="$store.state.authenticated" class="w-full py-2 px-5" @click="post = !post">
                   <button class=" hide w-full px-15 py-3 text-xl rounded-lg border-none pointer btn-themed weight-900 ">Spill</button>
                   <q-btn class="show btn-themed text-heading" round flat icon="add"/>
                  </div>

                  <q-dialog class="min-h-sm" v-model="post" position="top" persistent>
                    <div class="mt-12 bg-theme box-shadow w-full min-h-fit max-w-sm h-fit overflow-visible" >
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

                  <RouterLink to="/login" class="nav__link" active-class="active" v-if="!$store.state.authenticated">
                      <q-item class="hide">
                      <q-item-section avatar>
                          <!-- <q-icon class="icon" name="login" /> -->
                          <i-login size="3rem" :fill="$route.fullPath == `/login` ? 'var(--color-heading)' : 'none'" stroke="var(--color-heading)" />
                      </q-item-section>

                      <q-item-section class="bold">
                          Login
                      </q-item-section>
                      </q-item>
                      <!-- <q-avatar size="iconSize" icon="login" class="show icon">
                      <q-tooltip anchor="top middle" self="bottom middle">
                          Login
                      </q-tooltip>
                      </q-avatar> -->
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

                <div class="rest__nav">
                    <theme-toggle/>
                    <div class="dropdown-btn flex w-full justify-center">
                        <q-btn no-caps dense rounded flat class="dropdown" v-if="$store.state.authenticated">
                          <div class="hide item">
                            <Item dense avatarSize="3rem">
                                <template #avatar>
                                  <img v-if="$store.state.user.avatar" :src="$store.state.user.avatar"/>
                                  <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" />
                                </template>
                                <template #title>
                                  <span class="text-xl text-heading weight-900">{{ $store.state.user.first_name + ' ' + $store.state.user.last_name }}</span>
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

<style scoped>
@import '@/assets/base.css';

header {
  position: -webkit-sticky;
  position: sticky;
  max-height: 100vh;
  max-height: 100dvh;
  height: 100%;
  top: 0;
  z-index: 20;
  overflow-y: scroll;
}

.nav {
  height: 100vh;
  height: 100dvh;
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 0 16px;
  background-color: transparent;
  position: relative;
  
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
  /* background-color: var(--color-background-mute); */
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


@media (max-width: 880px) {
  .show {
    display:flex;
  }

  .nav {
    padding: 0;
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
/* theme */
/* The switch - the box around the slider */

/* Theme toggle */

</style>