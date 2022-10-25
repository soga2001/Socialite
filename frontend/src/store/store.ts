
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
  posts_main: Array<Post>
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
      profile: {
        bio: '',
        avatar: '',
      },
      groups: [],
      user_permissions: [],
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
      profile: {
        bio: '',
        avatar: '',
      },
      groups: [],
      user_permissions: [],
    },
  },
  mutations: {
    authenticate(state, payload) {
        state.authenticated = payload
    },
    setUser(state, payload) {
      state.user = payload
    },
    setTheme(state, payload) {
      state.dark = payload
    },
    setMainPosts(state, payload) {
      state.posts_main = [...state.posts_main, ...payload]
    }
  }
})

export function useStore() {
    return baseUseStore(key)
}