
// Store reference: https://vuex.vuejs.org/
import type { InjectionKey } from 'vue'
import { createStore, Store, useStore as baseUseStore } from 'vuex'
import type { Post, User } from '@/assets/interfaces'

// define your typings for the store state
export interface State {
  authenticated: boolean,
  user: User,
  dark: boolean,
  posts_main: Array<Post>,
  desktop: boolean,
  csrf: string,
  isLoading: boolean,
}

// define injection key
export const key: InjectionKey<Store<State>> = Symbol()

export const store = createStore<State>({
  state: {
    authenticated: false,
    dark: false,
    posts_main: Array<Post>(),
    user: {} as User,
    desktop: true,
    csrf: "",
    isLoading: true,

  },
  mutations: {
    authenticate(state, payload) {
      console.log(payload)
      state.authenticated = payload
    },
    setUser(state, payload) {
      state.user = payload
    },
    setDefaultUser(state) {
      state.user = {} as User
    },
    setTheme(state, payload) {
      state.dark = payload
    },
    setMainPosts(state, payload) {
      state.posts_main = [...state.posts_main, ...payload]
    },
    setDesktop(state, payload) {
      state.desktop = payload
    },
    setCSRF(state, payload) {
      state.csrf = payload
    },
    changeAvatar(state, payload) {
      state.user.avatar = payload
    },
    changeBanner(state, payload) {
      state.user.banner = payload
    },
    setLoading(state, payload) {
      setTimeout(() => {
        state.isLoading = payload
      }, 100)
    }
  }
})

export function useStore() {
    return baseUseStore(key)
}