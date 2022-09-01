<script lang="ts">
import {defineComponent} from 'vue';
import  type {Post} from '@/assets/interfaces';
import { http } from '@/assets/http';
import PostsMap from './HomeViews/PostsMap.vue';

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
    components: { PostsMap }
})
</script>

<template>
  <div class="home">
    <h1>Home page</h1>
    <div v-if="posts" v-for="post in posts" :key="post.id">
      <PostsMap :post="post" />
    </div>
  </div>
</template>

<style>
.home {
  display: grid;
  align-items: center;
}
</style>
