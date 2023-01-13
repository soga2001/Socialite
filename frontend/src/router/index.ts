import { createRouter, createWebHistory } from 'vue-router'
// import Vue from 'vue'
import { useCookies } from 'vue3-cookies'
import { store } from '../store/store'

const { cookies }  = useCookies();

const Main = () => import('../views/Main.vue')


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // {
    //   path: '/',
    //   component: Main,
    //   name: 'Main'
    // },
    {
      path: '/home',
      name: 'Home',
      component: () => import('../views/HomeViews/Home.vue')
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
      path: '/profile/user',
      name: 'user-profile',
      component: () => import('../views/UserViews/User.vue'),
      children : [
        {
          path: '/user_posted',
          name: 'user-posts',
          component: () => import('../views/UserViews/UserPosted.vue')
        },
        {
          path: '/user_liked',
          name: 'user-likes',
          component: () => import('../views/UserViews/UserLiked.vue')
        },
      ]
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/Settings/Settings.vue'),
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
      return savedPosition
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
