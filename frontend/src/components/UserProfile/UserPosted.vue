<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import type { Post } from '@/assets/interfaces';
import UserPostedMap from './UserPostedMap.vue';
import $j from 'jquery';


export default defineComponent({
    name: 'user-posted',
    props: {
        // user_avatar: {type: String, required: true},
        uid: {type: Number, required: true},
    },
    data() {
        return {
            // user_id: this.$route.params.id,
            user_id: this.uid,
            user_timestap: new Date().toISOString(),
            user_posted: new Array<Post>(),
            // avatar: this.user_avatar,
            scrollY: 0,
        };
    },
    setup() {
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
    },
    mounted() {
    },
    activated() {
    },
    deactivated() {
    },
    components: { UserPostedMap }
})
</script>

<template>
    <div class="user__posted__main" id="main">
        <div class="user__posted row">
            <div class="col-4" v-if="user_posted.length > 0" v-for="post in user_posted" :key="post.id">
                <!-- <UserPostedMap class="post" :post="post" :user_avatar="avatar"/> -->
                <UserPostedMap class="post" :post="post"/>

            </div>
            <div class="col-12" v-else>
                <h1 class="text-center">No Posts</h1>
            </div>
        </div>
    </div>
</template>


<style scoped>
.user__posted__main {
    height: 100%;
    overflow: visible;
}
.post {
    padding: 10px;
}
</style>