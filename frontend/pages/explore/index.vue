<script lang="ts">
// import usefetch
// import ref
import type { Post } from '../../assets/interfaces';
import {backend_baseURL} from '../../composables/backendURL';

export default {
    data() {
        return {
            posts: Array<Post>(),
            input: '',
            user_timestamp: new Date().toISOString(),
            page: 0,
            hasMore: false,
            message: '',
            offset: 0,
            searchModal: false,
            loading: true,
        }
    },
    methods: {
        async fetchData() {
            this.loading = true;
            await http.get(`${backend_baseURL}/posts/explore/${this.user_timestamp}/${this.page}/`).then((res) => {
                if(res.data.posts) {
                    this.posts = res.data.posts
                    if((res.data.posts).length < 10) {
                        this.hasMore = false
                    } else {
                        this.hasMore = true
                    }
                } else {
                    this.message = res.data.message
                }
            }).catch((err) => {
                console.log(err)
            })
            this.loading = false

        }
    },
    created() {
        if(process.client) {
            this.fetchData()
        }
    }
}
</script>

<template>
    <div class="bg-red h-full w-full">
        <div v-if="posts.length == 0 && !loading">
            <p class="text-lg text-heading">No posts to show</p>
        </div>
        <div v-else>
            <div v-for="post in posts" :key="post.id">
                <!-- <p class="text-lg text-heading">{{ post.id }}</p> -->
                <spillcard :post="post" />
            </div>
        </div>
        <div>
            <p v-if="message">{{ message }}</p>
        </div>
        <div class="flex justify-center w-full p-2" v-if="loading">
            <q-spinner size="2rem" />
        </div>
        <div v-else>
            Here
        </div>
    </div>
    
</template>