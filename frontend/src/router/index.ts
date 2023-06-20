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
      // meta: {basePath: '/:username?'},
      redirect: {
        name: 'user-posted'
      },
      children : [
        {
          // path: getParentRouterPath(this), 
          path: '',
          alias: '*',
          name: 'user-posted',
          // meta: {basePath: getParentRouterPath(this)},
          component: () => import('../components/UserProfile/UserPosted.vue'),
        },
        {
          // path: getParentRouterPath(this) + '/likes',
          path: 'likes',
          alias: 'likes/*',
          name: 'user-liked',
          // meta: {basePath: getParentRouterPath(this) + '/likes'},
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

// router.beforeEach((to, from) => {
//   from.meta?.scrollPos && (from.meta.scrollPos.top = document.documentElement.scrollTop)
// })

router.beforeResolve((to, next) => {
  if(to.matched.some(record => record.meta.hideForAuth) && store.state.authenticated) {
    return {path: '/home'}
  }

  if(to.matched.some(record => record.meta.auth) && !store.state.authenticated) {
    return {path: '/login'}
  }
}) 

export default router
