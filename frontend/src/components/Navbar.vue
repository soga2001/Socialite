<script lang="ts">
import { useCookies } from 'vue3-cookies';
import { defineComponent } from 'vue'
import {http} from '../assets/http'
import { RouterLink, RouterView } from 'vue-router';
import router from '../router';
import { useStore } from '../store/store';
import Item from './Item.vue';
import { Crypter } from '@/assets/crypter';


export default defineComponent({
    data() {
        return {
            theme: false,
            dark_mode: false,
            include: ["home", "explore"],
            iconSize: "5rem"
        };
    },
    setup() {
        const store = useStore();
        const { cookies } = useCookies();
        return { cookies };
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
            http.post("users/logout/", {
                "access_token": this.cookies.get("access_token"),
                "refresh_token": this.cookies.get("refresh_token")
            }, {
                headers: {
                    "Authorization": "Bearer "  + Crypter.decrypt(this.cookies.get("access_token"))
                }
            }).then((res) => {
                this.cookies.remove("access_token");
                this.cookies.remove("refresh_token");
                this.cookies.remove("user");
                this.cookies.remove("loggedIn");
                this.$store.commit("authenticate", false);
                this.$store.commit("setDefaultUser");
                router.push("/home");
            }).catch((err) => {
                console.log(err);
            });
        },
        onload(e: any) {
            console.log(e);
        }
    },
    created() {
        this.theme = this.cookies.get("theme") === "dark";
        this.$store.commit("setTheme", this.theme);
        document.documentElement.setAttribute("data-theme", this.theme ? "dark" : "light");
    },
    mounted() {
    },
    watch: {},
    components: { Item }
})

</script>

<template>
  <header>
    <nav class="nav" v-if="$store.state.desktop">
      <q-list class="list">
        <RouterLink to="/home" class="brand">
          <q-item class="hide">
            <q-item-section avatar>
              BB
            </q-item-section>
          </q-item>
          <q-avatar rounded :size="iconSize" icon="BB" class="show"/>
        </RouterLink>
        <RouterLink to="/home" class="nav__link" active-class="active">
          <q-item class="hide">
            <q-item-section avatar>
              <q-icon size="2rem" :name="$route.fullPath == '/home' ? 'house' : 'o_house'"/>
            </q-item-section>

            <q-item-section class="bold">
              Home
            </q-item-section>
          </q-item>
          <q-avatar size="iconSize" :icon="$route.fullPath == '/home' ? 'house' : 'o_house'" class="show">
            <q-tooltip anchor="top middle" self="bottom middle">
              Home
            </q-tooltip>
          </q-avatar>
        </RouterLink>

        <RouterLink to="/explore" class="nav__link" active-class="active">
          <q-item class="hide">
            <q-item-section avatar>
              <q-icon :name="$route.fullPath == '/explore' ? 'explore' : 'o_explore'" />
            </q-item-section>

            <q-item-section class="bold">
              Explore
            </q-item-section>
          </q-item>
          <q-avatar size="iconSize" :icon="$route.fullPath == '/explore' ? 'explore' : 'o_explore'" class="show">
            <q-tooltip anchor="top middle" self="bottom middle">
              Explore
            </q-tooltip>
          </q-avatar>
        </RouterLink>

        <RouterLink to="/search" class="nav__link" active-class="active">
          <q-item class="hide">
            <q-item-section avatar>
              <q-icon :name="$route.fullPath == '/search' ? 'search' : 'o_search'" />
            </q-item-section>

            <q-item-section class="bold">
              Search
            </q-item-section>
          </q-item>
          <q-avatar size="iconSize" :icon="$route.fullPath == '/search' ? 'searcg' : 'o_search'" class="show">
            <q-tooltip anchor="top middle" self="bottom middle">
              Search
            </q-tooltip>
          </q-avatar>
        </RouterLink>

        <RouterLink :to="{name: 'user-profile', params: {username: $store.state.user.username}}" :exact="true" v-if="$store.state.authenticated" class="nav__link" active-class="active" exact-active-class="exact-active">
          <q-item class="hide">
            <q-item-section avatar>
              <q-icon :name="$route.fullPath == `/profile/user/${$store.state.user.username}/` ? 'account_circle' : 'o_account_circle'" />
            </q-item-section>

            <q-item-section class="bold">
              Profile
            </q-item-section>
          </q-item>
          <q-avatar size="iconSize" :icon="$route.fullPath == `/profile/user/${$store.state.user.id}/` ? 'account_circle' : 'o_account_circle'" class="show">
            <q-tooltip anchor="top middle" self="bottom middle">
              Profile
            </q-tooltip>
          </q-avatar>
        </RouterLink>

        <RouterLink to="/settings" v-if="$store.state.authenticated" class="nav__link" active-class="active">
          <q-item class="hide">
            <q-item-section avatar>
              <q-icon :name="$route.fullPath == '/settings' ? 'settings' : 'o_settings'" />
            </q-item-section>

            <q-item-section class="bold">
              Settings
            </q-item-section>
          </q-item>
          <q-avatar size="iconSize" :icon="$route.fullPath == '/settings' ? 'settings' : 'o_settings'" class="show">
            <q-tooltip anchor="top middle" self="bottom middle">
              Settings
            </q-tooltip>
          </q-avatar>
        </RouterLink>

        <RouterLink to="/login" class="nav__link" active-class="active" v-if="!$store.state.authenticated">
          <q-item class="hide">
            <q-item-section avatar>
              <q-icon name="login" />
            </q-item-section>

            <q-item-section class="bold">
              Login
            </q-item-section>
          </q-item>
          <q-avatar size="iconSize" icon="login" class="show">
            <q-tooltip anchor="top middle" self="bottom middle">
              Login
            </q-tooltip>
          </q-avatar>
        </RouterLink>

        <RouterLink to="/Register" class="nav__link" active-class="active" v-if="!$store.state.authenticated">
          <q-item class="hide">
            <q-item-section avatar>
              <q-icon name="o_app_registration" />
            </q-item-section>

            <q-item-section class="bold">
              Register
            </q-item-section>
          </q-item>
          <q-avatar size="iconSize" icon="app_registration" class="show">
            <q-tooltip anchor="top middle" self="bottom middle">
              Register
            </q-tooltip>
          </q-avatar>
        </RouterLink>

      <q-item class="toggleWrapper">
        <input type="checkbox" v-model="theme" @click="switchTheme" class="dn" id="dn">
        <label for="dn" class="toggle">
            <span class="toggle__handler">
                <span class="crater crater--1"></span>
                <span class="crater crater--2"></span>
                <span class="crater crater--3"></span>
            </span>
            <span class="star star--1"></span>
            <span class="star star--2"></span>
            <span class="star star--3"></span>
            <span class="star star--4"></span>
            <span class="star star--5"></span>
            <span class="star star--6"></span>
        </label>
      </q-item>
      <!-- <Item :avatar="$store.state.user.profile.avatar" :title="$store.state.user.first_name + ' ' + $store.state.user.last_name" :subtitle="$store.state.user.username" icon="more_vert"/> -->
      <div class="dropdown-btn">
        <q-btn no-caps flat round class="dropdown" v-if="$store.state.authenticated">
          <q-item class="hide">
            <q-item-section avatar>
              <img class="avatar" v-if="$store.state.user.profile.avatar" :src="$store.state.user.profile.avatar"/>
              <q-icon size="iconSize" v-else name="o_person" class="avatar__icon" />
            </q-item-section>

            <q-item-section>
              <q-item-label>{{ $store.state.user.first_name + ' ' + $store.state.user.last_name }}</q-item-label>
              <q-item-label caption class="username">@{{ $store.state.user.username }}</q-item-label>
            </q-item-section>

            <q-item-section side >
              <q-icon name="o_more_horiz"  />
            </q-item-section>
          </q-item>

          <q-avatar size="40px" class="show">
            <img v-if="$store.state.user.profile.avatar" :src="$store.state.user.profile.avatar"/>
            <q-icon v-else name="o_person" class="avatar__icon" />
          </q-avatar> 
          <q-menu fit square self="top left" anchor="bottom left">
            <q-list class="dropdown__main" dense>
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
    </q-list>
    </nav>

    <nav v-else class="mobile-nav">
      <RouterLink to="/home" class="nav__link" active-class="active">
        <q-avatar size="iconSize" :icon="$route.fullPath == '/home' ? 'house' : 'o_house'" class="">
          <q-tooltip anchor="top middle" self="bottom middle">
            Home
          </q-tooltip>
        </q-avatar>
      </RouterLink>
      <RouterLink to="/explore" class="nav__link" active-class="active">
        <q-avatar size="iconSize" :icon="$route.fullPath == '/explore' ? 'explore' : 'o_explore'" class="">
          <q-tooltip anchor="top middle" self="bottom middle">
            Explore
          </q-tooltip>
        </q-avatar>
      </RouterLink>
      <RouterLink to="/search" class="nav__link" active-class="active">
          <q-avatar size="iconSize" :icon="$route.fullPath == '/search' ? 'search' : 'o_search'" class="show">
            <q-tooltip anchor="top middle" self="bottom middle">
              Search
            </q-tooltip>
          </q-avatar>
        </RouterLink>
        <RouterLink :to="{name: 'user-profile', params: {username: $store.state.user.username}}" :exact="true" v-if="$store.state.authenticated" class="nav__link" active-class="active" exact-active-class="exact-active">
          <q-avatar size="iconSize" :icon="$route.fullPath == `/profile/user/${$store.state.user.id}/` ? 'account_circle' : 'o_account_circle'" class="">
            <q-tooltip anchor="top middle" self="bottom middle">
              Profile
            </q-tooltip>
          </q-avatar>
        </RouterLink>

        <RouterLink to="/settings" v-if="$store.state.authenticated" class="nav__link" active-class="active">
          <q-avatar size="iconSize" :icon="$route.fullPath == '/settings' ? 'settings' : 'o_settings'" class="">
            <q-tooltip anchor="top middle" self="bottom middle">
              Settings
            </q-tooltip>
          </q-avatar>
        </RouterLink>

        <RouterLink to="/login" class="nav__link" active-class="active" v-if="!$store.state.authenticated">
          <q-avatar size="iconSize" icon="login" class="">
            <q-tooltip anchor="top middle" self="bottom middle">
              Login
            </q-tooltip>
          </q-avatar>
        </RouterLink>

        <RouterLink to="/Register" class="nav__link" active-class="active" v-if="!$store.state.authenticated">
          <q-avatar size="iconSize" icon="app_registration" class="">
            <q-tooltip anchor="top middle" self="bottom middle">
              Register
            </q-tooltip>
          </q-avatar>
        </RouterLink>
      <!-- <Item :avatar="$store.state.user.profile.avatar" :title="$store.state.user.username" /> -->
      <div class="dropdown-btn">

        <q-btn no-caps flat round class="dropdown" v-if="$store.state.authenticated">
          <q-item class="hide">
            <q-item-section avatar>
              <img class="avatar" v-if="$store.state.user.profile.avatar" :src="$store.state.user.profile.avatar"/>
              <q-icon size="iconSize" v-else name="o_person" class="avatar__icon" />
            </q-item-section>

            <q-item-section>
              <q-item-label>{{ $store.state.user.first_name + ' ' + $store.state.user.last_name }}</q-item-label>
              <q-item-label caption class="username">@{{ $store.state.user.username }}</q-item-label>
            </q-item-section>

            <q-item-section side >
              <q-icon name="o_more_horiz"  />
            </q-item-section>
          </q-item>

          <q-avatar size="40px" class="show">
            <img v-if="$store.state.user.profile.avatar" :src="$store.state.user.profile.avatar"/>
            <q-icon v-else name="o_person" class="avatar__icon" />
          </q-avatar> 
          <q-menu fit square self="top left" anchor="bottom left">
            <q-list class="dropdown__main" dense>
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
    </nav>
  </header>
</template>

<style scoped>
@import '@/assets/base.css';


header {
  position: -webkit-sticky;
	position: sticky;
  max-height: 100vh;
  height: 100%;
  width: 100%;
	top: 0;
  z-index: 999;
  overflow-y: scroll;
  /* padding-right: calc(var(--section-gap) / 2); */
}

.nav {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  background-color: transparent;
  position: relative;
  
}

.mobile-nav {
  position: fixed;
  background-color: var(--color-background);
  border-top: 1px solid var(--color-text);
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 0;
  /* width: 100%; */
  display: inline-flex;
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

a {
  text-decoration: none;
  transition: 0.2s;
  width: 100%;
  font-size: 2rem;
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

.nav__link:hover {
  background-color: var(--color-background-mute);
  color: var(--color-heading);
  font-weight: 900;
  border-radius: 30px;
}

.nav__link:hover .bold {
  font-weight: 900;
}

.dropdown-btn {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.dropdown:hover {
  /* background-color: hsla(hue, saturation, lightness, alpha); */
  /* background-color: var(--color-background-mute); */
  border-radius: 30px;
}

.dropdown__main {
  background-color: var(--color-background-mute);
  color: var(--text-heading);
}

.nav_avatar {
  margin: 30px 0;
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

@media (min-width: 993px) {

}

@media (max-width: 992px) {
  .show {
    display:block;
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

  .dropdown {
    border: 1px solid var(--color-text);
  }
  .dropdown:hover {
    /* background-color: hsla(hue, saturation, lightness, alpha); */
    background-color: transparent !important;
  }
}


/* Reference: https://uiverse.io/alexruix/splendid-liger-23 */
/* theme */
/* The switch - the box around the slider */

/* Theme toggle */


.toggleWrapper input {
  position: absolute;
  left: -99em;
}

.toggle {
  cursor: pointer;
  display: inline-block;
  position: relative;
  width: 45px;
  height: 25px;
  background-color: #83d8ff;
  border-radius: 84px;
  transition: background-color 200ms cubic-bezier(0.445, 0.05, 0.55, 0.95);
}

.toggle__handler {
  display: inline-block;
  position: relative;
  z-index: 1;
  top: 1.7px;
  left: 3px;
  width: 21px;
  height: 21px;
  background-color: #f5d418;
  border-radius: 50px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, .3);
  transition: all 400ms cubic-bezier(0.68, -0.55, 0.265, 1.55);
  transform: rotate(-45deg);
}

.toggle__handler .crater {
  position: absolute;
  background-color: #e8cda5;
  opacity: 0;
  transition: opacity 200ms ease-in-out;
  border-radius: 100%;
}

.toggle__handler .crater--1 {
  top: 9px;
  left: 5px;
  width: 2px;
  height: 2px;
}

.toggle__handler .crater--2 {
  top: 14px;
  left: 11px;
  width: 3px;
  height: 3px;
}

.toggle__handler .crater--3 {
  top: 5px;
  left: 12.5px;
  width: 4px;
  height: 4px;
}

.star {
  position: absolute;
  background-color: rgb(255, 255, 255);
  /* font-weight: 900; */
  transition: all 300ms cubic-bezier(0.445, 0.05, 0.55, 0.95);
  border-radius: 50%;
}

.star--1 {
  top: 5px;
  left: 17.5px;
  z-index: 0;
  width: 15px;
  height: 1.5px;
}

.star--2 {
  top: 9px;
  left: 14px;
  z-index: 1;
  width: 15px;
  height: 1.5px;
}

.star--3 {
  top: 13.5px;
  left: 20px;
  z-index: 0;
  width: 15px;
  height: 1.5px;
}

.star--4, .star--5, .star--6 {
  opacity: 0;
  transition: all 300ms 0 cubic-bezier(0.445, 0.05, 0.55, 0.95);
}

.star--4 {
  top: 8px;
  left: 5.5px;
  z-index: 0;
  width: 1px;
  height: 1px;
  transform: translate3d(3px, 0, 0);
}

.star--5 {
  top: 16px;
  left: 8.5px;
  z-index: 0;
  width: 1.5px;
  height: 1.5px;
  transform: translate3d(3px, 0, 0);
}

.star--6 {
  top: 18px;
  left: 14px;
  z-index: 0;
  width: 1px;
  height: 1px;
  transform: translate3d(3px, 0, 0);
}

input:checked + .toggle {
  background-color: #475668;
}

input:checked + .toggle:before {
  color: #475668;
}

input:checked + .toggle:after {
  color: #fff;
}

input:checked + .toggle .toggle__handler {
  background-color: #ffe5b5;
  transform: translate3d(17px, 0, 0) rotate(0);
}

input:checked + .toggle .toggle__handler .crater {
  opacity: 1;
}

input:checked + .toggle .star--1 {
  width: 1px;
  height: 1px;
}

input:checked + .toggle .star--2 {
  width: 2px;
  height: 2px;
  transform: translate3d(-5px, 0, 0);
}

input:checked + .toggle .star--3 {
  width: 2px;
  height: 2px;
  transform: translate3d(-7px, 0, 0);
}

input:checked + .toggle .star--4, input:checked + .toggle .star--5, input:checked + .toggle .star--6 {
  opacity: 1;
  transform: translate3d(0, 0, 0);
}

input:checked + .toggle .star--4 {
  transition: all 300ms 200ms cubic-bezier(0.445, 0.05, 0.55, 0.95);
}

input:checked + .toggle .star--5 {
  transition: all 300ms 300ms cubic-bezier(0.445, 0.05, 0.55, 0.95);
}

input:checked + .toggle .star--6 {
  transition: all 300ms 400ms cubic-bezier(0.445, 0.05, 0.55, 0.95);
}
 
</style>
