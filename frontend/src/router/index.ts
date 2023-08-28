import { nextDay } from 'date-fns';
import { scroll } from 'quasar';
import { createRouter, createWebHistory } from 'vue-router'
import type {RouterScrollBehavior, RouteRecordRaw, Router, NavigationGuard} from 'vue-router' 
// import type { ScrollPositionNormalized }from 'vue-router'
// import Vue from 'vue'
import { useCookies } from 'vue3-cookies'
import { store } from '../store/store'
import type { Sessions } from '@/assets/interfaces';

const { cookies }  = useCookies();


const router: Router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  
  routes: [
    {
      path: '/',
      name: 'landing-page',
      component: () => import('../views/LandingPage.vue'),
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('../views/Home.vue'),
      meta: {
        auth: true,
        title: 'Home',
      },
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/Search.vue'),
      props: route => ({ query: route.query.q })
    },
    {
      path: '/explore',
      name: 'explore',
      component: () => import('../views/Explore.vue'),
      meta: {
        auth: true,
        title: 'Explore'
      }
    },
    {
      path: '/notifications',
      name: 'notifications',
      component: () => import('../views/NotificationsView.vue'),
      meta: {
        auth: true,
        title: 'Notifications'
      },
      children : [
        {
          path: '',
          alias: '*',
          name: 'all-notif',
          component: () => import('../components/Notifications/All.vue'),
          meta: {
            auth: true,
            title: 'All Notifications'
          },
        },
        {
          path: 'mentions',
          alias: 'mentions/*',
          name: 'mentions',
          component: () => import('../components/Notifications/Mentions.vue'),
          meta: {
            auth: true,
            title: 'Mentions'
          },
        },
      ],
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
      meta: {
        hideForAuth: true,
        title: 'Login',
      }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue'),
      meta: {
        hideForAuth: true,
        title: 'Register',
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
      meta: {
        auth: true,
        title: 'Profile'
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
      meta: {
        auth: true,
      }
    },
    {
      path: '/:pathMatch(.*)*',
      component: () => import('../views/PageNotFound.vue'),
      meta: {
        title: 'Page not foun'
      }
    },
    {
      path: '/verify/email',
      component: () => import('@/views/VerifyEmail.vue'),
      meta: {
        title: 'Email Verification'
      }
    },
    {
      path: '/reset/password',
      component: () => import('@/views/ForgotPass.vue'),
      meta: {
        hideForAuth: true,
        title: 'Reset Password'
      }
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/settings/settings.vue'),
      meta: {
        auth: true,
        title: 'Settings'
      },
      children: [
        {
          path: 'account',
          name: 'account',
          component: () => import('@/views/settings/account.vue'),
          meta: {
            auth: true,
            title: 'Your Account'
          }
        },
        {
          path: 'account-information',
          name: 'account-information',
          // alias: '/settings/account-information',
          component: () => import('@/views/settings/accounts/accountInfo.vue'),
          meta: {
            auth: true,
            title: 'Account Information'
          }

        },
        {
          path: 'change-password',
          name: 'change-password',
          // alias: '/settings/change-password',
          component: () => import('@/views/settings/accounts/passwordChange.vue'),
          meta: {
            auth: true,
            title: 'Change Password'
          }
        },
        {
          path: 'deactive-account',
          name: 'deactive-account',
          // alias: '/settings/deactive-account',
          component: () => import('@/views/settings/accounts/deactiveAccount.vue'),
          meta: {
            auth: true,
            title: 'Deactive Account'
          }
        },
        {
          path: 'delete-account',
          name: 'delete-account',
          // alias: '/settings/delete-account',
          component: () => import('@/views/settings/accounts/deleteAccount.vue'),
          meta: {
            auth: true,
            title: 'Delete Account'
          }
        },
        {
          path: 'notification-settings',
          name: 'notification-settings',
          alias: ['/settings/notification-settings', '/notifications-settings'],
          component: () => import('@/views/settings/notificationSettings.vue'),
          meta: {
            auth: true,
            title: 'Notification Settings'
          }
        },
        {
          path: 'notification-settings/followed_users',
          name: 'individual-notif-settings',
          alias: ['/settings/notificiation-settings/followed_users', '/notifications-settings/followed_users'],
          component: () => import('@/views/settings/notificationSetting/individualNotifications.vue'),
          meta: {
            auth: true,
            title: 'Followed User Settings'
          }
        },
        {
          path: 'privacy-settings',
          name: 'privacy-settings',
          component: () => import('@/views/settings/privacySettings.vue'),
          meta: {
            auth: true,
            title: 'Privacy Settings'
          }
        }, 
        {
          path: 'sessions',
          name: 'sessions',
          component: () => import('@/views/settings/sessions.vue'),
          meta: {
            auth: true,
            title: 'Sessions'
          }
        },
        {
          path: 'sessions/:key',
          name: 'session',
          component: () => import('@/views/settings/session/session.vue'),
          meta: {
            auth: true,
            title: 'Session Detail'
          }
        },

      ]
    },
    // {
    //   path: '/settings/account',
    //   name: 'account',
    //   component: () => import('@/views/settings/account.vue'),
    // },
    
  ]
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
