import { createRouter, createWebHistory } from 'vue-router'
import { useCookies } from 'vue3-cookies'
import { store } from '../store/store'

const { cookies }  = useCookies();



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
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
      path: '/profile/user/:id',
      name: 'user-profile',
      component: () => import('../views/UserViews/User.vue'),
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
  ]
})

router.beforeEach((to, from) => {
  if(to.matched.some(record => record.meta.hideForAuth) && store.state.authenticated) {
      return {path: '/'}
  }

  if(to.matched.some(record => record.meta.auth) && !store.state.authenticated) {
    return {path: '/login'}
  }
})

export default router
