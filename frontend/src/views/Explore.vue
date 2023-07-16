<script lang="ts">
import {defineComponent, ref} from 'vue';
import  type {Post} from '@/assets/interfaces';
import { http } from '@/assets/http';
import PostsMap from '../components/PostsMap.vue';
import Search from './Search.vue';
import Navbar from '../components/Navbar.vue';

export default defineComponent({
  data() {
      return {
        posts: new Array<Post>(),
        input: ref(''),
        user_timestap: new Date().toISOString(),
        page: ref(0),
        hasMore: false,
        message: '',
        offset: 0,
        searchModal: false,
      };
  },
  props: {
    scrollPosition: {
      type: Number,
      default: 0,
    },
    height: {
      type: Number,
      default: 0,
    }
  },
  name: 'explore',
  created() {
    this.getData();
  },
  methods: {
    async getData() {
      http.get(`posts/explore/${this.offset}/`).then((res) => {
        if(res.data.message) {
            this.message = res.data.message
            this.hasMore = false
        }
        else {
          this.hasMore = true
        }
        if(res.data.posts) {
            this.posts = [...this.posts, ...res.data.posts]
            this.offset = (this.posts).length
        }
      }).catch((err) => {
          console.log(err);
      });
    },
    async flushSession() {
        http.get(`users/flush_session/`).then((res) => {
            this.posts = new Array<Post>()
            this.getData()
        }).catch((err) => {
            console.log(err);
        });
    },
    onLoad(index: any, done: any) {
      if(this.hasMore) {
        this.page = this.page + 1
        this.getData()
      }
      done()
    },
  },
  components: { PostsMap, Search, Navbar },
  activated() {
  },
  watch: {
    scrollPosition(scrollPosition) {
      // console.log(scrollPosition)
    },
    height(height) {
      // console.log(height)
    },
  }
})
</script>

<template>
  <div class="explore" id="explore">
    <div class="">
      <header class="sticky top-0 p-2 m-0 border-b max-h-12 overflow-visible bg-theme-opacity" v-if="!$q.screen.lt.sm">
        <Item align-items="center" dense v-if="$store.state.authenticated" class="w-full overflow-visible bg-transparent">
                <template v-if="$route.name=='explore'" #title>
                  <SearchBar />
                </template>
                <template #icon>
                  <q-btn flat round dense icon="settings" size="16px" class="border" @click.stop="" />
                </template>
            </Item>
      </header>
      <div class="grid gap-2" v-if="posts.length > 0" v-for="(post, index) in posts" :id="post.id.toString" :key="post.id">
          <PostsMap :post="post" />
        </div>
      </div>
      <div v-if="!hasMore" class="text-center message">
        <p>{{message}}</p>
        <button class="btn btn-themed border-none text-heading px-3 py-3 rounded weight-900" @click="flushSession">Reset Session Data</button>
      </div>
  </div>
</template>

<style scoped>

header {
  display: relative;
  
  width: 100%;
	top: 0;
  z-index: 10;
  /* padding: 0 10px; */

  font-size: 25px;
  font-weight: 900;
  
  color: var(--color-heading);
  /* From https://css.glass */
  /* box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1); */
  backdrop-filter: blur(50px);
  -webkit-backdrop-filter: blur(20px);
}

.message {
    padding: 1rem;
}

</style>
