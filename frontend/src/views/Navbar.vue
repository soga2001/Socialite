<script lang="ts">
import { useCookies } from 'vue3-cookies';
import { defineComponent } from 'vue'
import {http} from '../assets/http'
import { RouterLink, RouterView } from 'vue-router';
import router from '../router';
import { store, useStore } from '../store/store';
import $ from 'jquery'
import Search from '../views/Search/Search.vue'


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
        this.cookies.set('theme', 'light')
        document.documentElement.setAttribute('data-theme', 'light')
      }
      else {
        // this.cookies.set('theme', 'light')
        this.cookies.set('theme', 'dark')
        document.documentElement.setAttribute('data-theme', 'dark')
      }
      this.$store.commit('setTheme', !this.$store.state.dark)
    },
    logout() {
      http.post('users/logout/', {
        "access_token":this.cookies.get('access_token'),
        "refresh_token":this.cookies.get('refresh_token')
      }, {
        headers: {
          'Authorization': `Bearer ${this.cookies.get('access_token')}`
        }
      }).then((res) => {

        /*
       this.cookies.set('access_token', res.data.access_token, {expires: res.data.at_lifetime, secure: true})
       this.cookies.set('refresh_token', res.data.refresh_token, {expires: res.data.rt_lifetime, secure: true})
       this.cookies.set('loggedIn', 'true', {expires: res.data.at_lifetime, secure: true})
       this.cookies.set('user', res.data.user, {expires: res.data.at_lifetime, secure: true})
        this.$store.commit('authenticate', true)
        this.$store.commit('setUser', res.data.user)
        */
        this.cookies.remove('access_token')
        this.cookies.remove('refresh_token')
        this.cookies.remove('user')
        this.cookies.remove('loggedIn')
        this.$store.commit('authenticate', false)
        this.$store.commit('setDefaultUser')
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
    this.theme =this.cookies.get('theme') === 'dark'
    this.$store.commit('setTheme', this.theme)
    document.documentElement.setAttribute('data-theme', this.theme ? 'dark': 'light')

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
        <RouterLink to="/home" class="brand">
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

        <RouterLink :to="{name: 'user-profile', params: {id: $store.state.user.id}}" :exact="true" v-if="$store.state.authenticated" class="nav__link" active-class="active" exact-active-class="exact-active">
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
      
        <!-- <q-item class="theme">
          <q-toggle dense size="50px" v-on:click="switchTheme" v-model="theme" color="grey" icon-color="black" checked-icon="nights_stay" unchecked-icon="wb_sunny" />
        </q-item> -->
      <q-item>
        <label class="switch">
          <input type="checkbox" @click="switchTheme" v-model="theme">
          <span class="slider"></span>
        </label>
      </q-item>
      
      <q-btn no-caps flat round class="dropdown" v-if="$store.state.authenticated">
        <!-- <q-icon name="account_circle" /> -->
        <q-item class="hide">
          <q-item-section avatar>
            <img class="avatar" v-if="$store.state.user.profile.avatar" :src="$store.state.user.profile.avatar"/>
            <q-icon size="50px" v-else name="account_circle" class="avatar__icon" />
          </q-item-section>

          <q-item-section>
            <q-item-label>{{ $store.state.user.first_name + ' ' + $store.state.user.last_name }}</q-item-label>
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
    </q-list>
    </nav>
  </header>
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
  height: 100%;
  display: flex;
  justify-content: center;
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
  /* color: var(--color-heading) !important; */
  font-weight: 900;
  /* background-color: var(--color-background-mute); */
  border-radius: 30px;
}

.nav__link.exact-active {
  color: var(--color-heading) !important;
  background-color: var(--color-background-mute);
  border-radius: 30px;
}

.nav__link:hover {
  background-color: var(--color-background-mute);
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

.dropdown {
  color: var(--color-text);
  font-weight: 900;
  width: 100%;
  display: flex;
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

@media (max-width: 1023px) {
  .show {
    display:block;
  }

  .hide {
    display: none;
  }

  .nav__link:hover {
    background-color: var(--color-background-mute) !important;
  }

  .nav__link {
    width: 100%;
    display: flex;
    border-radius: 50%;
    /* padding: 10px; */
  }
  .dropdown:hover {
    background-color: transparent !important;
    /* border-radius: 30px; */
  }
}


/* Reference: https://uiverse.io/alexruix/splendid-liger-23 */
/* theme */
/* The switch - the box around the slider */
.switch {
  font-size: 17px;
  position: relative;
  display: inline-block;
  width: 2.5em;
  height: 1.5em;
}

/* Hide default HTML checkbox */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* The slider */
.slider {
  --background: #28096b;
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: white;
  -webkit-transition: .5s;
  transition: .5s;
  border: 1px solid var(--color-text);
  border-radius: 30px;
}

.slider:before {
  position: absolute;
  content: "";
  height: .9em;
  width: 1em;
  border-radius: 50%;
  left: 10%;
  bottom: 15%;
  -webkit-box-shadow: inset -4px 15px 0px 15px #ffb700;
          box-shadow: inset -4px 15px 0px 15px #ffb700;
  background: rgb(92, 92, 92);
  -webkit-transition: .5s;
  transition: .5s;
}

input:checked + .slider {
  background-color: var(--color-background);
}

input:checked + .slider:before {
  -webkit-transform: translateX(100%);
      -ms-transform: translateX(100%);
          transform: translateX(100%);
  /* -webkit-box-shadow: inset 15px -4px 0px 15px #fff000;
          box-shadow: inset 15px -4px 0px 15px #fff000; */
  -webkit-box-shadow: inset 8px -4px 0px 0px white;
  box-shadow: inset -8px -3px 0px 0px white;
}

</style>
