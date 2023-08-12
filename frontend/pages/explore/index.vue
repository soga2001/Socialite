<script lang="ts">
// import usefetch
// import ref
import { ref } from 'vue';
import { useFetch, useAsyncData } from 'nuxt/app';
import type { Post } from '../../assets/interfaces';
import {backend_baseURL} from '../../composables/backendURL';

export default {
    data() {
        return {
            posts: Array<Post>(),
            tempPosts: Array<Post>(),
            input: '',
            user_timestamp: new Date().toISOString(),
            page: ref(0),
            hasMore: false,
            message: '',
            offset: 0,
            searchModal: false,
            loading: true,
        }
    },
    methods: {
        async fetchData() {
            // const { pending, data: posts}  = await useFetch(`${backend_baseURL}/posts/explore/${this.user_timestamp}/${this.page}/`,);

            // const dat = await $fetch(`${backend_baseURL}/posts/explore/${this.user_timestamp}/${this.page}/`).then((res) => {
            //     console.log(res)
            // }).catch((error) => error.data)
            // console.log(dat)

            // if(posts.value) {
            //     this.posts = [...this.posts, ...(posts.value as { posts: Post[] }).posts]
            // }

            const { data: posts } = await useFetch(`${backend_baseURL}/posts/explore/${this.user_timestamp}/${this.page}/`)

            if(posts.value) {
                this.posts = [...this.posts, ...(posts.value as { posts: Post[] }).posts]
            }
            // if(posts.value) {
            //     console.log(posts.value.posts)
            // }

        }
    },
    mounted() {
        this.fetchData()
    }
}
</script>

<template>
    <!-- <div v-if="">
        <div v-if="posts.length > 0" v-for="post in posts" :key="post.id">
            <p>{{ post.id }}</p>
        </div>
    </div> -->
</template>