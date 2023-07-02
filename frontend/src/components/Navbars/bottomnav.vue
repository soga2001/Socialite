<script lang="ts">
import { useCookies } from 'vue3-cookies';
import { defineComponent } from 'vue'
import { RouterLink } from 'vue-router';

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
    

  },
  methods: {
  },
  created() {
  },
  mounted() {
  },
  watch: {
  },
  components: {}
})
</script>

<template>
    <nav>
        <div class="bottomNav">
        <slot name="bottomNav">
          <RouterLink to="/home" class="nav__link" active-class="active" v-if="$store.state.authenticated">
            <i-home size="2rem" :fill="$route.fullPath == `/home` ? 'var(--color-heading)' : 'none'" :stroke="'var(--color-heading)'"/>
          </RouterLink>

          <RouterLink to="/explore" class="nav__link" active-class="active">
            <i-explore size="2rem" :fill="$route.fullPath == `/explore` ? 'var(--color-heading)' : 'none'" :stroke="$route.fullPath == `/explore` ? 'none' : 'var(--color-heading)'"/>
          </RouterLink>
          <RouterLink to="/search" class="nav__link" active-class="active">
            <i-search size="2rem" :fill="$route.fullPath == `/search` ? 'var(--color-heading)' : 'none'" stroke="var(--color-heading)"/>
          </RouterLink>
          <RouterLink to="/notifications" class="nav__link" active-class="active">
            <i-notif size="2rem" :fill="$route.fullPath == `/notifications` ? 'var(--color-heading)' : 'none'" stroke="var(--color-heading)" />
          </RouterLink>

            <RouterLink to="/settings" v-if="$store.state.authenticated" class="nav__link" active-class="active">
              <i-settings size="2rem" :fill="$route.fullPath == `/settings` ? 'var(--color-heading)' : 'none'" :stroke="$route.fullPath == `/settings` ? 'none' : 'var(--color-heading)'" />
            </RouterLink>

            <RouterLink to="/login" class="nav__link" active-class="active" v-if="!$store.state.authenticated">
              <i-login size="3rem" :fill="$route.fullPath == `/login` ? 'var(--color-heading)' : 'none'" stroke="var(--color-heading)" />
            </RouterLink>

            <RouterLink to="/register" class="nav__link" active-class="active" v-if="!$store.state.authenticated">
              <i-register size="2.3rem" :fill="$route.fullPath == `/login` ? 'var(--color-heading)' : 'none'" stroke="var(--color-heading)" />
            </RouterLink>
        </slot>
      </div>
    </nav>
</template>

<style scoped>
@import '@/assets/base.css';



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
  background-color: var(--color-hover); /* Set the opacity value for the background */
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


 
</style>