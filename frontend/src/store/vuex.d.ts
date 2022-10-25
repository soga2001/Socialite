import type { Post } from '@/assets/interfaces'
import { Store } from 'vuex'

declare module '@vue/runtime-core' {
  // declare your own store states
  interface State {
    authenticated: boolean
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
    dark: true,
    posts_main: Array<Post>
  }

  // provide typings for `this.$store`
  interface ComponentCustomProperties {
    $store: Store<State>
  }
}