import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Post from '../views/Post.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import User from '../views/UserViews/User.vue';

import { useCookies } from 'vue3-cookies'

const {cookies}  = useCookies();
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: Post
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      beforeEnter: (to, from) => {
        if(cookies.get('loggedIn') === 'true') {
          return {name: 'home'};
        }
      }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      beforeEnter: (to, from) => {
        if(cookies.get('loggedIn') === 'true') {
          return {name: 'home'};
        }
      }
    },
    {
      path: '/user',
      name: 'user',
      component: User,
    }
  ]
})

export default router
