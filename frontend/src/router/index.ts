import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Post from '../views/Post.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import User from '../views/UserViews/User.vue'
import PageNotFound from '../views/PageNotFound.vue'

import { useCookies } from 'vue3-cookies'
import { store } from '../store/store'

const {cookies}  = useCookies();
const Home = () => import('../views/HomeView.vue')


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      component: Post,
      meta: {
        auth: true
      }
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: {
        hideForAuth: true
      }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: {
        hideForAuth: true
      }
    },
    {
      path: '/user',
      name: 'user',
      component: User,
    },
    {
      path: '/:pathMatch(.*)*',
      component: PageNotFound
    }
  ]
})

router.beforeEach((to, from) => {
  if(to.matched.some(record => record.meta.hideForAuth) && store.state.authenticated) {
      return {path: '/'}
  }

  if(to.matched.some(record => record.meta.auth) && !store.state.authenticated) {
    return {path: 'login'}
  }
})

export default router
