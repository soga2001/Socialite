import type { Post } from '@/assets/interfaces'
import { Store } from 'vuex'

declare module '@vue/runtime-core' {
  // declare your own store states
  interface State {
    authenticated: boolean
    user: User
    defaultUser: User
    dark: boolean,
    posts_main: Array<Post>,
    desktop: boolean
  }

  // provide typings for `this.$store`
  interface ComponentCustomProperties {
    $store: Store<State>
  }
}