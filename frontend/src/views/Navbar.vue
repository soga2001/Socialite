<script lang="ts">
import { useCookies } from 'vue3-cookies';
import { defineComponent } from 'vue'
import {http} from '../assets/http'
import { RouterLink, RouterView } from 'vue-router';
import router from '../router';
import { store, useStore } from '../store/store';
import $ from 'jquery'
import Search from '../views/Search/Search.vue'
import { Cookies } from 'quasar';


export default defineComponent({
  data() {
    return {
      theme: false,
      dark_mode: false,
      include: ['home', 'explore'],
      hideName: false
    }
  },
  setup() {
    const store = useStore()
    const {cookies} = useCookies();
    return {cookies}
  },
  methods: {
    switchTheme(e: any) {
      if(this.theme) {
        // this.cookies.set('theme', 'dark')
        Cookies.set('theme', 'dark')
        document.documentElement.setAttribute('data-theme', 'dark')
      }
      else {
        // this.cookies.set('theme', 'light')
        Cookies.set('theme', 'light')
        document.documentElement.setAttribute('data-theme', 'light')
      }
      this.$store.commit('setTheme', !this.$store.state.dark)
    },
    logout() {
      http.post('users/logout/', {
        "access_token": Cookies.get('access_token'),
        "refresh_token": Cookies.get('refresh_token')
      }, {
        headers: {
          'Authorization': `Bearer ${Cookies.get('access_token')}`
        }
      }).then((res) => {
        Cookies.remove('access_token')
        Cookies.remove('refresh_token')
        Cookies.remove('user')
        Cookies.remove('loggedIn')
        this.$store.commit('authenticate', false)
        this.$store.commit('setUser', this.$store.state.defaultUser)
        router.push('/home')
      }).catch((err) => {
        console.log(err)
      })
    },
    onload(e: any) {
      console.log(e)
    }
  },
  created() {
    this.theme = Cookies.get('theme') === 'dark'
    this.$store.commit('setTheme', this.theme)
    document.documentElement.setAttribute('data-theme', this.theme ? 'dark': 'light')

    this.$store.commit('authenticate',JSON.parse(Cookies.get("loggedIn")) || false)
    if(Cookies.get('user')) {
      this.$store.commit('setUser', Cookies.get('user'))
    }
  },
  mounted() {
  },
  components: {Search},
})

</script>

<template>
  <header>
    <nav class="nav">
      <q-list class="list">
        <!-- <RouterLink to="/" exact class="nav__link brand">
          B<span class="logo">B</span>
        </RouterLink> -->

        <RouterLink to="/home" class="nav__link brand">
          <q-item class="hide">
            <q-item-section avatar>
              BB
            </q-item-section>
          </q-item>
          <q-avatar rounded size="50px" icon="BB" class="show"/>
        </RouterLink>
        <RouterLink to="/home" class="nav__link" active-class="active">
          <q-item class="hide">
            <q-item-section avatar>
              <q-icon name="cottage" />
            </q-item-section>

            <q-item-section>
              Home
            </q-item-section>
          </q-item>
          <q-avatar size="50px" icon="cottage" class="show">
            <q-tooltip anchor="top middle" self="bottom middle">
              Home
            </q-tooltip>
          </q-avatar>
        </RouterLink>

        <RouterLink to="/explore" class="nav__link" active-class="active">
          <q-item class="hide">
            <q-item-section avatar>
              <q-icon name="explore" />
            </q-item-section>

            <q-item-section>
              Explore
            </q-item-section>
          </q-item>
          <q-avatar size="50px" icon="explore" class="show">
            <q-tooltip anchor="top middle" self="bottom middle">
              Explore
            </q-tooltip>
          </q-avatar>
        </RouterLink>

        <RouterLink to="/search" class="nav__link" active-class="active">
          <q-item class="hide">
            <q-item-section avatar>
              <q-icon name="search" />
            </q-item-section>

            <q-item-section>
              Search User
            </q-item-section>
          </q-item>
          <q-avatar size="50px" icon="search" class="show">
            <q-tooltip anchor="top middle" self="bottom middle">
              Search
            </q-tooltip>
          </q-avatar>
        </RouterLink>

        <RouterLink :to="{name: 'user-profile', query: {id: $store.state.user.id}}" v-if="$store.state.authenticated" class="nav__link" active-class="active">
          <q-item class="hide">
            <q-item-section avatar>
              <q-icon name="account_circle" />
            </q-item-section>

            <q-item-section>
              Profile
            </q-item-section>
          </q-item>
          <q-avatar size="50px" icon="account_circle" class="show">
            <q-tooltip anchor="top middle" self="bottom middle">
              Profile
            </q-tooltip>
          </q-avatar>
        </RouterLink>

        <RouterLink to="/settings" v-if="$store.state.authenticated" class="nav__link" active-class="active">
          <q-item class="hide">
            <q-item-section avatar>
              <q-icon name="settings" />
            </q-item-section>

            <q-item-section>
              Setting
            </q-item-section>
          </q-item>
          <q-avatar size="50px" icon="settings" class="show">
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

            <q-item-section>
              Login
            </q-item-section>
          </q-item>
          <q-avatar size="50px" icon="login" class="show">
            <q-tooltip anchor="top middle" self="bottom middle">
              Login
            </q-tooltip>
          </q-avatar>
        </RouterLink>

        <RouterLink to="/Register" class="nav__link" active-class="active" v-if="!$store.state.authenticated">
          <q-item class="hide">
            <q-item-section avatar>
              <q-icon name="app_registration" />
            </q-item-section>

            <q-item-section>
              Register
            </q-item-section>
          </q-item>
          <q-avatar size="50px" icon="app_registration" class="show">
            <q-tooltip anchor="top middle" self="bottom middle">
              Register
            </q-tooltip>
          </q-avatar>
        </RouterLink>
      
        <q-item class="theme">
          <q-toggle dense size="50px" v-on:click="switchTheme" v-model="theme" color="grey" icon-color="black" checked-icon="nights_stay" unchecked-icon="wb_sunny" />
        </q-item>
      <q-btn no-caps flat round class="dropdown" v-if="$store.state.authenticated">
        <!-- <q-icon name="account_circle" /> -->
        <q-item class="hide">
          <q-item-section avatar>
            <img v-if="$store.state.user.profile.avatar" :src="$store.state.user.profile.avatar"/>
            <q-icon size="50px" v-else name="account_circle" class="avatar__icon" />
          </q-item-section>

          <q-item-section>
            <!-- <q-item-label>{{ $store.state.user.first_name + ' ' + $store.state.user.last_name }}</q-item-label> -->
            <q-item-label>Suyogya Poudel</q-item-label>
            <q-item-label caption>@{{ $store.state.user.username }}</q-item-label>
          </q-item-section>

          <q-item-section side >
            <q-icon name="more_horiz"  />
          </q-item-section>
        </q-item>

        <q-avatar class="show">
          <img v-if="$store.state.user.profile.avatar" :src="$store.state.user.profile.avatar"/>
          <q-icon v-else name="account_circle" class="avatar__icon" />
        </q-avatar> 
      <q-menu fit self="top left" anchor="bottom left">
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
    </q-list>
    </nav>
  </header>
  <!-- <RouterView v-slot="{Component}">
    <KeepAlive :max="2" :include="['Home','User']">
      <component :is="Component" :key="$route.fullPath"/>
    </KeepAlive>
  </RouterView> -->
</template>

<style scoped>
@import '@/assets/base.css';
* {
  scroll-behavior: smooth;
}

/* body {
  place-items: center;
  position: relative;
} */

header {
  display: relative;
  position: -webkit-sticky;
	position: sticky;
  max-height: 100vh;
  height: 100%;
  width: 100%;
	top: 0;
  z-index: 999;
  /* padding-right: calc(var(--section-gap) / 2); */
}

.nav {
  /* background-color: var(--color-background); */
  display: flex;
  justify-content: right;
  background-color: transparent;
  position: relative;
  
}

a {
  text-decoration: none;
  transition: 0.2s;
  width: 100%;
  font-size: 20px;
}

.nav .brand {
  width: fit-content;
  font-size: 25px;
  font-weight: 300;
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

/* .nav__link.router-link-exact-active {
  color: var(--color-heading) !important;
  font-weight: 900;
} */

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
  font-weight: bolder;
  background-color: var(--color-background-mute);
  border-radius: 30px;
}

.nav__link:hover {
  background-color: var(--color-background-mute);
  border-radius: 30px;
}


.dropdown__main {
  background-color: var(--color-background);
  color: var(--text-heading);
}

.nav_avatar {
  margin: 30px 0;
}

.avatar {
  margin: 0 10px;
  width: 50px;
  border-radius: 50% !important;
}

img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.dropdown {
  color: var(--color-text);
  font-weight: 900;
  width: fit-content;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dropdown:hover {
  background-color: hsla(0, 0%, 57%, 0.2) !important;
  border-radius: 30px;
}

/* nav icons */

.show {
  display: none;
}

@media (max-width: 900px) {
  .show {
    display:block;
  }

  .hide {
    display: none;
  }

  /* .dropdown:hover {
    background-color: hsla(0, 0%, 57%, 0.2) !important;
    background-color: transparent;
    border-radius: 30px;
  } */
}

</style>
