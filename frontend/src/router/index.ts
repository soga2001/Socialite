import { scroll } from 'quasar';
import { createRouter, createWebHistory } from 'vue-router'
// import Vue from 'vue'
import { useCookies } from 'vue3-cookies'
import { store } from '../store/store'

const { cookies }  = useCookies();

const Main = () => import('../views/Main.vue')


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  linkActiveClass: 'active',
  linkExactActiveClass: 'exact-active',
  routes: [
    // {
    //   path: '/',
    //   component: Main,
    //   name: 'Main'
    // },
    {
      path: '/search',
      name: 'Search',
      component: () => import('../views/Search.vue')
    },
    {
      path: '/home',
      name: 'Home',
      component: () => import('../views/Home.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
      meta: {
        hideForAuth: true
      }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue'),
      meta: {
        hideForAuth: true
      }
    },
    {
      path: '/profile/user/:id/',
      name: 'user-profile',
      component: () => import('../views/User.vue'),
      children : [
        {
          path: '/user_posted/:id',
          name: 'user-posts',
          component: () => import('../components/UserProfile/UserPosted.vue')
        },
        {
          path: '/user_liked/:id',
          name: 'user-likes',
          component: () => import('../components/UserProfile/UserLiked.vue')
        },
      ]
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/Settings.vue'),
      meta: {
        auth: true
      }
    },
    {
      path: '/:pathMatch(.*)*',
      component: () => import('../views/PageNotFound.vue'),
    }
  ],
  scrollBehavior (to, from, savedPosition) {
    if (savedPosition) {
      return {
        top: savedPosition.top,
        behavior: 'auto'
      }
    } else {
      return { top: 0 }
    }
  }
})

router.beforeEach((to, from) => {
  // document.title = to.meta.title as string
  // console.log(to.meta.title)
  if(to.matched.some(record => record.meta.hideForAuth) && store.state.authenticated) {
      return {path: '/'}
  }

  if(to.matched.some(record => record.meta.auth) && !store.state.authenticated) {
    return {path: '/login'}
  }

})

export default router
