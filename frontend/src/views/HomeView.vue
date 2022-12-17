<script lang="ts">
import {defineComponent, ref} from 'vue';
import  type {Post} from '@/assets/interfaces';
import { http } from '@/assets/http';
import PostsMap from './HomeViews/PostsMap.vue';
import PostView from './PostView.vue';
import Search from './Search/Search.vue';
import { useStore } from '@/store/store';

export default defineComponent({
  data() {
      return {
        posts: new Array<Post>(),
        input: ref(''),
        user_timestap: new Date().toISOString(),
        page: ref(0),
        hasMore: false,
      };
  },
  name: 'Home',
  setup() {
    const store = useStore()
  },
  created() {
    // if(Object.keys(this.$store.state.posts_main).length === 0) {
    //   this.getData();
    // }
    this.getData();
  },
  methods: {
    async getData() {
      http.get(`posts/view_posts/${this.user_timestap}/${this.page}/`).then((res) => {
        this.$store.commit('setMainPosts', res.data.posts)
        if(res.data.posts.length === 5) {
          this.hasMore = true
        }
        else {
          this.hasMore = false
        }
        this.posts = [...this.posts, ...res.data.posts]
        // console.log(this.page)x
      }).catch((err) => {
          console.log(err);
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
    }
  },
  components: { PostsMap, PostView, Search }
})
</script>

<template>
  <div class="home">
    <div class="home__sides left">
      
    </div>
    <div class="home__center">
      <div v-if="$store.state.authenticated">
        <PostView />
      </div>
      <!-- <div v-if="$store.state.posts_main" v-for="post in $store.state.posts_main" :key="post.id">
        <PostsMap :post="post" />
      </div> -->
      <q-infinite-scroll @load="onLoad" :debounce="2" :offset="10" :disable="!hasMore">
        <div v-if="posts.length > 0" v-for="(post, index) in posts" :key="post.id">
          <PostsMap :post="post" />
        </div>
        <template v-slot:loading>
          <div class="row justify-center q-my-md">
            <q-spinner-oval class="loading" size="40px" />
          </div>
        </template>
      </q-infinite-scroll>
    </div>
    <div class="home__sides right">
      
    </div>
  </div>
</template>

<style>
@media screen and (min-width: 1220px){
  .home {
    display: grid;
    grid-template-columns: auto minmax(500px, 600px) auto;
    align-items: center;
  }

  .home__sides {
    height: 100%;
    position: sticky;
  }
}


@media screen and (min-width: 860px) and (max-width: 1220px){
  .home {
    display: grid;
    grid-template-columns: minmax(500px, 600px) auto;
    justify-content: center;
  }

  .home__sides.left {
    display: none;
  }

}

@media screen and (min-width: 400px) and (max-width: 859px){
  .home {
    display: grid;
    grid-template-columns: minmax(500px, 600px) auto;
    justify-content: center;
  }

  .home__sides {
    display: none;
  }

}

.loading {
  color: var(--color-heading);
}
</style>
