<script lang="ts">
import { useCookies } from 'vue3-cookies';
import { defineComponent } from 'vue'
import {http} from '../../assets/http'
import { RouterLink, RouterView } from 'vue-router';
import router from '../../router';
import { useStore } from '../../store/store';
import Item from '../Item.vue';
import Themetoggle from '../themetoggle.vue';

export default defineComponent({
    
  props: {
  },
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
          width: this.navSlideIn ? '250px' : '0vh'
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
  },
  watch: {
  },
  components: { Item }
})
</script>

<template>
    <nav>
        <div class="topNav" v-if="$store.state.authenticated">
          <div class="dropdown-btn">
            <q-btn no-caps flat dense round class="dropdown" @click="openNav" v-if="$store.state.authenticated">
                <Item class="item" dense avatar-size="fit-content">
                    <template #avatar>
                      <img v-if="$store.state.user.avatar" :src="$store.state.user.avatar"/>
                      <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" />
                    </template>
                </Item>
            </q-btn>
          </div>

          <div class="overlay" v-if="navSlideIn" @click="closeNav"></div>

          <div class="slide-in-nav list" :style="slideIn">
            <div class="rest_nav">
              <Item class="item">
                <template #title>
                  Account Info
                </template>
                <template #icon>
                  <q-btn flat round dense icon="close" size="16px" @click="navSlideIn = false" />
                </template>
              </Item>
              <Item class="item" avatar-size="fit-content">
                <template #avatar>
                  <div @click="() => {$router.push({name: 'user-profile', params: {username: $store.state.user.username}}), closeNav()}">
                    <img v-if="$store.state.user.avatar" :src="$store.state.user.avatar"/>
                    <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" />
                  </div>
                </template>
                <!-- <template #icon>
                  <q-btn flat round dense icon="close" size="16px" @click="navSlideIn = false" />
                </template> -->
              </Item>
              <Item class="item">
                <template #title>
                  {{ $store.state.user.first_name + ' ' + $store.state.user.last_name }}
                </template>
                <template #caption>
                  @{{ $store.state.user.username }}
                </template>
              </Item>
              <Item class="item">
                <template #caption>
                  <div class="follow">
                    <p> <span>{{ $store.state.user.total_following }} </span> Following</p>
                    <p> <span>{{ $store.state.user.total_followers }} </span> Followers</p>
                  </div>
                </template>
              </Item>
              <!-- <hr/> -->

              <RouterLink @click="closeNav" :to="{name: 'user-profile', params: {username: $store.state.user.username}}" :exact="true" v-if="$store.state.authenticated" class="nav__link" active-class="active" exact-active-class="exact-active">
                <q-item>
                  <q-item-section avatar>
                    <q-icon class="icon" :name="$route.fullPath == `/profile/user/${$store.state.user.username}/` ? 'account_circle' : 'o_account_circle'" />
                  </q-item-section>

                  <q-item-section class="bold">
                    Profile
                  </q-item-section>
                </q-item>
              </RouterLink>
              <!-- <RouterLink to="/settings" v-if="$store.state.authenticated" class="nav__link" active-class="active">
                <q-item>
                  <q-item-section avatar>
                    <q-icon class="icon" :name="$route.fullPath == '/settings' ? 'settings' : 'o_settings'" />
                  </q-item-section>

                  <q-item-section class="bold">
                    Settings
                  </q-item-section>
                </q-item>
              </RouterLink> -->
            </div>
            <hr/>
            <div>
              <q-item class="logout" clickable v-close-popup @click="logout">
                <q-item-section avatar>
                  <q-icon name="logout" />
                </q-item-section>
                <q-item-section class="bold">
                  Logout
                </q-item-section>
              </q-item>
            </div>
          </div>
      </div>
    </nav>
</template>


<style scoped>
@import '@/assets/base.css';

header {
  position: -webkit-sticky;
	position: sticky;
  max-height: 100vh;
  max-height: 100dvh;
  height: 100%;
  width: 100%;
	top: 0;
  z-index: 20;
  overflow-y: scroll;
}

.nav {
  height: 100%;
  display: flex;
  width: 100%;  
  justify-content: center;
  padding: 0 16px;
  background-color: transparent;
  position: relative;
  
}

.topNav {
  padding: 0 10px 0 10px ;
  width: 100%;
  background-color: var(--color-background);
  margin: 0;
  z-index: 0;
  display: inline-flex;
}


.topNav .dropdown-btn {
  padding: 0;
  width: 3rem;
}

  
.bottomNav {
  width: 100%;
  background-color: var(--color-background);
  border-top: 1px solid var(--color-text);
  z-index: 0;
  display: inline-flex;
}

.mobile-nav {
  padding: 0;
}

.item {
  height: fit-content;
}
.item img {
  width: 3rem;
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
  transition: 0.5s;
  /* padding-top: .1rem; */

  display: grid;
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



/* .slide-in-nav .closebtn {
  position: absolute;
  top: 0;
  right: 0;
  font-size: 36px;
  margin-left: 50px;
} */


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

.dropdown-btn {
  width: 100%;
  /* border-radius: 30px; */
  display: flex;
  justify-content: center;
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



/* nav icons */

.show {
  display: none;
}

@media (min-width: 993px) {

}

@media (max-width: 992px) {
  .show {
    display:flex;
  }

  .nav {
    justify-content: center;
    
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