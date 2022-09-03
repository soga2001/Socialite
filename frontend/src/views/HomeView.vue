<script lang="ts">
import {defineComponent} from 'vue';
import  type {Post} from '@/assets/interfaces';
import { http } from '@/assets/http';
import PostsMap from './HomeViews/PostsMap.vue';
import PostView from './PostView.vue';

export default defineComponent({
    data() {
        return {
            posts: new Array<Post>()
        };
    },
    created() {
      http.get("posts/view_posts/").then((res) => {
          this.posts = res.data.posts;
      }).catch((err) => {
          console.log(err);
      });
    },
    components: { PostsMap, PostView }
})
</script>

<template>
  <div class="home">
    <div class="home__sides">
      <div class="home__sides__main">
        <h1>Stuff</h1>
      </div>
    </div>
    <div class="home__center">
      <div v-if="$store.state.authenticated">
        <PostView />
      </div>
      <div v-if="posts" v-for="post in posts" :key="post.id">
        <PostsMap :post="post" />
      </div>
    </div>
    <div class="home__sides">
      <div class="home__sides__main">
        <h1>Stuff</h1>
        <input type="search" placeholder="search"/>
      </div>
    </div>
  </div>
</template>

<style>
@media screen and (min-width: 768px){
  .home {
    display: grid;
    grid-template-columns: auto 40% auto;
    align-items: center;
  }
  .home__center {
    border-right: 2px solid var(--color-border);
    border-left: 2px solid var(--color-border);
    position: justify;  
  }

  .home__sides {
    height: 100%;
    position: sticky;
    float: right;
  }

  .home__sides__main {
    width: 100%;
    text-align: center;
  }
}


@media screen and (min-width: 400px) and (max-width: 768px){
  .home {
    display: grid;
    align-items: center;
  }
  .home__center {
    border-right: 2px solid var(--color-border);
    border-left: 2px solid var(--color-border);
    position: justify;
  }

  .home__sides {
    display: none;
  }

  .home__sides__main {
    display: none;
  }
}
</style>
