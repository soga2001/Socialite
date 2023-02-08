<script lang="ts">
import { http } from '@/assets/http';
import type { Post } from '@/assets/interfaces';
import { defineComponent } from 'vue';
import UserPostedMap from './UserPostedMap.vue';

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
            // avatar: this.user_avatar
        };
    },
    methods: {
        async getUserPosted() {
            await http.get(`like/view_liked/${this.user_timestap}/${this.page}/${(this.username)}/`).then((res) => {
                this.user_liked = [...this.user_liked, ...res.data.posts];
            }).catch((err) => {
                console.log(err);
            });
            console.log(this.user_liked)
        }
    },
    created() {
        this.getUserPosted();
    },
    components: { UserPostedMap }
})
</script>

<template>
    <div class="user__liked__main">
        <div class="user__liked row">
            <div class="col-4" v-if="user_liked.length > 0" v-for="post in user_liked" :key="post.id">
                <UserPostedMap class="post" :post="post"/>
            </div>
            <!-- <q-icon size="100px" name="las la-folder-open" />
            <h4>User has liked no Posts</h4> -->
        </div>
    </div>
</template>

<style scoped>
/* .user__liked__main {
    text-align: center;
    display: flex;
    justify-content: center;
    justify-self: center;
    align-items: center;
    align-self: center;
    height: 100%;
} */
.user__liked__main {
    height: 100%;
    overflow: visible;
}
.post {
    padding: 10px;
}
</style>