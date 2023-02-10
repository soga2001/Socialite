
// Store reference: https://vuex.vuejs.org/
import type { InjectionKey } from 'vue'
import { createStore, Store, useStore as baseUseStore } from 'vuex'
import type { Post, User } from '@/assets/interfaces'

// define your typings for the store state
export interface State {
  authenticated: boolean,
  user: User
  defaultUser: User,
  dark: boolean,
  posts_main: Array<Post>,
  desktop: boolean
}

// define injection key
export const key: InjectionKey<Store<State>> = Symbol()

export const store = createStore<State>({
  state: {
    authenticated: false,
    dark: false,
    posts_main: Array<Post>(),
    defaultUser: {
      id: 0,
      email: '',
      username: '',
      first_name: '',
      last_name: '',
      last_login: '',
      is_active: false,
      is_staff: false,
      is_superuser: false,
      total_followers: 0,
      total_following: 0,
      total_posted: 0,
      profile: {
        bio: '',
        avatar: '',
      },
      groups: [],
      user_permissions: [],
      date_joined: ''
    },
    user: {
      id: 0,
      email: '',
      username: '',
      first_name: '',
      last_name: '',
      last_login: '',
      is_active: false,
      is_staff: false,
      is_superuser: false,
      total_followers: 0,
      total_following: 0,
      total_posted: 0,
      profile: {
        bio: '',
        avatar: '',
      },
      groups: [],
      user_permissions: [],
      date_joined: ''
    },
    desktop: true

  },
  mutations: {
    authenticate(state, payload) {
        state.authenticated = payload
    },
    setUser(state, payload) {
      state.user = payload
    },
    setDefaultUser(state) {
      state.user = state.defaultUser
    },
    setTheme(state, payload) {
      state.dark = payload
    },
    setMainPosts(state, payload) {
      state.posts_main = [...state.posts_main, ...payload]
    },
    setDesktop(state, payload) {
      state.desktop = payload
    }
  }
})

export function useStore() {
    return baseUseStore(key)
}