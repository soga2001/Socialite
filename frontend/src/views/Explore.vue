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
        loading: true,
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
      this.loading = true
     await http.get(`posts/explore/${this.offset}/`).then((res) => {
        if(res.data.message) {
            this.message = res.data.message
            this.hasMore = false
        }
        // else {
        //   this.hasMore = true
        // }
        if(res.data.posts) {
            this.posts = [...this.posts, ...res.data.posts]
            this.offset = (this.posts).length
        }
      }).catch((err) => {
          console.log(err);
      });
      this.loading = false
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
      <q-infinite-scroll class="grid gap-3 " id="infinite-scroll" @load="onLoad" :debounce="2" :offset="10" :disable="!hasMore">
        <div class="post_map" v-if="posts.length > 0" v-for="(post, index) in posts" :id="post.id.toString" :key="post.id">
          <PostsMap :post="post" />
        </div>
        <template v-slot:loading>
          <div class="row justify-center q-my-md">
            <q-spinner-oval class="loading" size="40px" />
          </div>
        </template>
      </q-infinite-scroll>
    </div>
    <div v-if="!hasMore" class="text-center message">
      <p>{{message}}</p>
      <button class="btn btn-themed border-none text-heading px-3 py-3 rounded weight-900" @click="flushSession">Reset Session Data</button>
    </div>
  </div>
</template>

<style scoped>

/* .message {
    padding: 1rem;
} */

</style>
