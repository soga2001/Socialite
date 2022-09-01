
// Store reference: https://vuex.vuejs.org/
import type { InjectionKey } from 'vue'
import { createStore, Store, useStore as baseUseStore } from 'vuex'

// define your typings for the store state
export interface State {
  loggedIn: boolean
}

// define injection key
export const key: InjectionKey<Store<State>> = Symbol()

export const store = createStore<State>({
  state: {
    loggedIn: false
  },
  mutations: {
    changeLoggedIn(state, payload) {
        state.loggedIn = payload
    }
  }
})

export function useStore() {
    return baseUseStore(key)
}