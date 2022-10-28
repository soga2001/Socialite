<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import type { Post } from '@/assets/interfaces';
import UserPostedMap from './UserPostedMap.vue';

export default defineComponent({
    name: 'UserPosted',
    props: {
        user_avatar: {type: String, required: true}
    },
    data() {
        return {
            user_id: this.$route.query.id,
            user_timestap: new Date().toISOString(),
            user_posted: new Array<Post>(),
            avatar: this.user_avatar
        };
    },
    methods: {
        getUserPosted() {
            http.get(`posts/user_posted/${this.user_timestap}/${(this.user_id)}/`).then((res) => {
               this.user_posted = [...this.user_posted, ...res.data.posts]
            }).catch((err) => {
                console.log(err);
            });
        }
    },
    created() {
        this.getUserPosted();
        // $(window).scrollTop(0);
    },
    components: { UserPostedMap }
})
</script>

<template>
    <div class="user__posted__main">
        <div class="user__posted row justify-center">
            <div class="col-12 col-md-auto" v-if="user_posted.length > 0" v-for="post in user_posted" :key="post.id">
                <UserPostedMap class="post" :post="post" :user_avatar="avatar"/>
            </div>
        </div>
    </div>
</template>


<style scoped>

.post {
    padding: 10px;
}
</style>