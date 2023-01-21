<script lang="ts">
import {defineComponent, ref} from 'vue';
import  type {Post} from '@/assets/interfaces';
import { http } from '@/assets/http';
import PostsMap from '../components/PostsMap.vue';
import PostView from '../components/PostView.vue';
import Search from './Search.vue';
import { useStore } from '@/store/store';
import Navbar from '../components/Navbar.vue';

export default defineComponent({
  title: 'Home',
  data() {
      return {
        posts: new Array<Post>(),
        input: ref(''),
        user_timestap: new Date().toISOString(),
        page: ref(0),
        hasMore: false,
        scrollY: 0
      };
  },
  name: 'home',
  setup() {
    const store = useStore()
  },
  created() {
    document.addEventListener('scroll' , () => {
      this.scrollY = window.scrollY
    })
    this.getData();
  },
  
  mounted() {
    
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
  components: { PostsMap, PostView, Search, Navbar }
})
</script>

<template>
  <div class="home">
    <div class="home__center col-6">
      <header>
        Home
      </header>
      <div v-if="$store.state.authenticated">
        <PostView />
      </div>
      <q-infinite-scroll @load="onLoad" :debounce="2" :offset="10" :disable="!hasMore">
        <div class="posts" v-if="posts.length > 0" v-for="(post, index) in posts" :key="post.id">
          <PostsMap :post="post" />
        </div>
        <template v-slot:loading>
          <div class="row justify-center q-my-md">
            <q-spinner-oval class="loading" size="40px" />
          </div>
        </template>
      </q-infinite-scroll>
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
  z-index: 999;
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

.posts:not(:first-child) {
  margin: 20px 0;
}

/* @media screen and (min-width: 1220px){
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

  .home__sides {
    display: none;
  }

}

@media screen and (min-width: 400px) and (max-width: 859px){
  .home {
    display: grid;
    grid-template-columns: minmax(500px, 600px) auto;
    justify-content: center;
  }

  .home__sides.right {
    display: none;
  }

}

.loading {
  color: var(--color-heading);
} */
</style>