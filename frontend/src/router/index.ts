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
      component: () => import('../views/NotificationsView.vue'),
      meta: {
        auth: true
      },
      children : [
        {
          path: '',
          alias: '*',
          name: 'all-notif',
          component: () => import('../components/Notifications/All.vue'),
          meta: {
            auth: true
          },
        },
        {
          path: 'mentions',
          alias: 'mentions/*',
          name: 'mentions',
          component: () => import('../components/Notifications/Mentions.vue'),
          meta: {
            auth: true
          },
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
    },
    {
      path: '/verify/email',
      component: () => import('@/views/VerifyEmail.vue'),
    },
    {
      path: '/reset/password',
      component: () => import('@/views/ForgotPass.vue'),
      meta: {
        hideForAuth: true
      }
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/settings/settings.vue'),
      redirect: '/settings/account',
      meta: {
        auth: true
      },
      children: [
        {
          path: 'account',
          name: 'account',
          component: () => import('@/views/settings/account.vue'),
        },
        {
          path: 'account-information',
          name: 'account-information',
          component: () => import('@/views/settings/accounts/accountInfo.vue'),
        },
        {
          path: 'change-password',
          name: 'change-password',
          component: () => import('@/views/settings/accounts/passwordChange.vue'),
        },
        {
          path: 'deactive-account',
          name: 'deactive-account',
          component: () => import('@/views/settings/accounts/deactiveAccount.vue'),
        },
        {
          path: 'delete-account',
          name: 'delete-account',
          component: () => import('@/views/settings/accounts/deleteAccount.vue'),
        }
      ]
    },
    // {
    //   path: '/settings/account',
    //   name: 'account',
    //   component: () => import('@/views/settings/account.vue'),
    // },
    
  ]
})

router.beforeEach((to, from) => {
  
  // console.log(from)
  // from.meta?.scrollPos && (from.meta.scrollPos.top = document.documentElement.scrollTop)
})

router.beforeResolve((to, next) => {
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
