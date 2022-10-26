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
        };
    },
    setup() {
      const store = useStore()
    },
    created() {
      // if(Object.keys(this.$store.state.posts_main).length === 0) {
      //   this.getData();
      // }
      this.getData();
      console.log('created')
    },
    methods: {
      async getData() {
        http.get(`posts/view_posts/${this.user_timestap}/`).then((res) => {
          // this.$store.commit('setMainPosts', res.data.posts)
          this.posts = [...this.posts, ...res.data.posts]
        }).catch((err) => {
            console.log(err);
        });
      },
      async search() {
        
        this.input = ""
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
      <div v-if="posts.length > 0" v-for="post in posts" :key="post.id">
        <PostsMap :post="post" />
      </div>
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
</style>
