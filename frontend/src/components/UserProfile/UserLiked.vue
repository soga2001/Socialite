<script lang="ts">
import { http } from '@/assets/http';
import type { Post } from '@/assets/interfaces';
import { defineComponent } from 'vue';
import UserPostedMap from './UserPostedMap.vue';
import Loading from '../Loading.vue';

export default defineComponent({
    name: "user-liked",
    // props: {
    // // user_avatar: {type: String, required: true}
    // },
    data() {
        return {
            // user_id: this.$route.query.id,
            username: this.$route.params.username,
            page: 0,
            user_timestap: new Date().toISOString(),
            user_liked: new Array<Post>(),
            loading: true,
            // avatar: this.user_avatar
        };
    },
    methods: {
        async getUserPosted() {
            this.loading = true
            await http.get(`like/view_liked/${this.user_timestap}/${this.page}/${(this.username)}/`).then((res) => {
                this.user_liked = [...this.user_liked, ...res.data.posts];
            }).catch((err) => {
                console.log(err);
            });
            this.loading = false
        }
    },
    created() {
        setTimeout(() => {
            this.getUserPosted();
        }, 3000);
        // this.getUserPosted();
    },
    components: { UserPostedMap, Loading }
})
</script>

<template>
    <div class="user__liked__main">
        <div class="user__liked">
            <div class="posts" v-if="user_liked.length > 0" v-for="post in user_liked" :key="post.id">
                <UserPostedMap class="post" :post="post"/>
            </div>
        </div>
        <div class="loading" v-if="loading">
            <Loading :stroke-width="5"/>
        </div>
    </div>
</template>

<style scoped>

.user__liked__main {
    width: 100%;
}
.user__liked {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 5px;
}

.loading {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>