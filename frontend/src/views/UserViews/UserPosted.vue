<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import type { Post } from '@/assets/interfaces';
import UserPostedMap from './UserPostedMap.vue';

export default defineComponent({
    name: 'User_Posted',
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
        console.log('potato')
    },
    activated() {
        console.log('activated')
    },
    deactivated() {
        // console.log((document.getElementById('main') as HTMLDivElement).scrollTop)
        // console.log(data)
    },
    components: { UserPostedMap }
})
</script>

<template>
    <div class="user__posted__main" id="main">
        <div class="user__posted row">
            <div class="col-4" v-if="user_posted.length > 0" v-for="post in user_posted" :key="post.id">
                <UserPostedMap class="post" :post="post" :user_avatar="avatar"/>
            </div>
        </div>
    </div>
</template>


<style scoped>
.user__posted__main {
    height: 100%;
    overflow: auto;
}
.post {
    padding: 10px;
}
</style>