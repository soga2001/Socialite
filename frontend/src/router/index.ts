import { nextDay } from 'date-fns';
import { scroll } from 'quasar';
import { createRouter, createWebHistory } from 'vue-router'
import type {RouterScrollBehavior, RouteRecordRaw, Router, NavigationGuard} from 'vue-router' 
// import type { ScrollPositionNormalized }from 'vue-router'
// import Vue from 'vue'
import { useCookies } from 'vue3-cookies'
import { store } from '../store/store'
import { getParentRouterPath } from '@/assets/parentPath';

const { cookies }  = useCookies();

const router: Router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  
  routes: [
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/Search.vue'),
      props: route => ({ query: route.query.q })
    },
    {
      path: '/home',
      name: 'home',
      alias: '/',
      component: () => import('../views/Home.vue'),
      meta: {
        auth: true
      },
    },
    {
      path: '/explore',
      name: 'explore',
      component: () => import('../views/Explore.vue'),
    },
    {
      path: '/notifications',
      name: 'notifications',
      component: () => import('../views/Notifications.vue'),
      children : [
        {
          path: '',
          alias: '*',
          name: 'all-notif',
          component: () => import('../components/Notifications/All.vue')
        },
        {
          path: 'mentions',
          alias: 'mentions/*',
          name: 'mentions',
          component: () => import('../components/Notifications/Mentions.vue'),
        },
      ],
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
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/Settings.vue'),
      meta: {
        auth: true
      }
    },
    {
      path: '/:username?',
      name: 'user-profile',
      component: () => import('../views/User.vue'),
      alias: '/:username?/*',
      redirect: {
        name: 'user-posted'
      },
      children : [
        {
          path: '',
          alias: '*',
          name: 'user-posted',
          component: () => import('../components/UserProfile/UserPosted.vue'),
        },
        {
          path: 'likes',
          alias: 'likes/*',
          name: 'user-liked',
          component: () => import('../components/UserProfile/UserLiked.vue'),
        },
      ],
    },
    {
      path: '/:user/spill/:post_id?/',
      name: 'view-spill',
      component: () => import('../views/ViewSpill.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      component: () => import('../views/PageNotFound.vue'),
    }
  ]
})

router.beforeEach((to, from) => {
  
  // console.log(from)
  // from.meta?.scrollPos && (from.meta.scrollPos.top = document.documentElement.scrollTop)
})

router.beforeResolve((to, next) => {
  console.log(to.query)
  if(to.name == 'search' && Object.keys(to.query).length == 0) {
    return {path: '/explore'}
  }

  if(to.name == 'explore' && Object.keys(to.query).length == 0) {
    to.query = {}
  }
  
  if(to.matched.some(record => record.meta.hideForAuth) && store.state.authenticated) {
    return {path: '/home'}
  }
  if(to.matched.some(record => record.meta.auth) && !store.state.authenticated) {
    return {path: '/login'}
  }
}) 

export default router
