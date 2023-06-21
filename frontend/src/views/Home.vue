<script lang="ts">
import {defineComponent, ref} from 'vue';
import  type {Post} from '@/assets/interfaces';
import { http } from '@/assets/http';
import PostsMap from '../components/PostsMap.vue';
import Spills from '../components/Spills.vue';
import Search from './Search.vue';
import { useStore } from '@/store/store';

export default defineComponent({
  title: 'Home',
  data() {
      return {
        posts: new Array<Post>(),
        input: ref(''),
        user_timestap: new Date().toISOString(),
        page: ref(0),
        hasMore: false,
        loading: true,
      };
  },
  name: 'home',
  props: {
    scrollPosition: {
      type: Number,
      required: true,
    },
    height: {
      type: Number,
      required: true,
    }
  },
  setup() {
    const store = useStore()
  },
  created() {
    this.getData();
    console.log(this.height)
  },
  
  mounted() {
    const element = (document.getElementById("infinite-scroll") as HTMLDivElement)
    element.addEventListener("scroll", function() {
      console.log('x')
    })
  },
  methods: {
    async getData() {
      this.loading = true
      http.get(`posts/posts_by_followed_users/${this.user_timestap}/${this.page}/`).then((res) => {
        if(res.data.posts.length === 5) {
          this.hasMore = true
        }
        else {
          this.hasMore = false
        }
        if((res.data.posts).length > 0){
          this.posts = [...this.posts, ...res.data.posts]
        }

        this.loading = false
      }).catch((err) => {
          console.log(err);
          this.loading = false
      });
    },
    async search() {
      this.input = ""
    },
    onLoad(index: any, done: any) {
      if(this.hasMore) {
        this.page = this.page + 1
        this.getData()
      }
      done()
    },
    scroll() {
      const div = (document.getElementById("infinite-scroll") as HTMLDivElement)
      if(this.scrollPosition >= div.scrollHeight - 1000 && this.hasMore) {
        this.page += 1
        this.getData()
      }
    },
  },
  components: { PostsMap, Spills, Search },
})
</script>

<template>
  <div class="home" id="home">
    <div class="home__center">
      <div class="">
        <header class="border-b" v-if="$store.state.desktop">
          Home
        </header>
        <div v-if="$store.state.authenticated && $store.state.desktop" class="border-b">
          <Spills :rows="1" />
        </div>
        <q-infinite-scroll class="grid gap-3 " id="infinite-scroll" @load="onLoad" :debounce="2" :offset="10" :disable="!hasMore">
          <div class="" v-if="posts.length > 0" v-for="(post, index) in posts" :id="post.id.toString" :key="post.id">
            <PostsMap :post="post" />
          </div>
          <template v-slot:loading>
            <div class="row justify-center q-my-md">
              <q-spinner-oval class="loading" size="40px" />
            </div>
          </template>
        </q-infinite-scroll>
        <div class="w-full flex flex-center flex-col" v-if="posts.length == 0 && !loading">
            <div>
                <i-folder :fill="'black'" stroke="black"/>
            </div>
            <div class="text-xl weight-900">
                Follow more users to see their posts here.
            </div>
        </div>
      </div>
    </div>
    
  </div>
</template>

<style scoped>

header {
  display: relative;
  position: -webkit-sticky;
	position: sticky;
  
  width: 100%;
	top: 0;
  z-index: 10;
  padding: 0 10px;

  font-size: 25px;
  font-weight: 900;
  backdrop-filter: blur(10px);
  color: var(--color-heading);

  text-shadow: -1px 1px 0 var(--color-background),
                          1px 1px 0 var(--color-background),
                         1px -1px 0 var(--color-background),
                        -1px -1px 0 var(--color-background);
}

/* #infinite-scroll {
  height: 100vh;
  overflow-y: scroll;
} */

.home {
  width: 100%;
}

/* .posts:not(:first-child) {
  margin: 20px 0;
} */
</style>
