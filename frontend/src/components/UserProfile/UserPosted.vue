<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import type { Post } from '@/assets/interfaces';
import UserPostedMap from './UserPostedMap.vue';
import Loading from '../Loading.vue';
import type { PropType } from 'vue';



export default defineComponent({
    name: 'user-posted',
    props: {
        // user_avatar: {type: String, required: true},
        websocket: {
            type: Object as PropType<WebSocket>,
            required: true,
        }
    },
    data() {
        return {
            // user_id: this.$route.params.id,
            user_id: this.uid,
            username: this.$route.params.username,
            user_timestap: new Date().toISOString(),
            user_posted: new Array<Post>(),
            // avatar: this.user_avatar,
            scrollY: 0,
            isLoggedUser: false,
            page: 0,
            loading: true,
        };
    },
    setup() {
    },
    methods: {
        getUserPosted() {
            http.get(`posts/user_posted/${this.user_timestap}/${this.page}/${(this.username)}/`).then((res) => {
               this.user_posted = [...this.user_posted, ...res.data.posts]
               this.loading = false
            }).catch((err) => {
                console.log(err);
            });
        },
    },

    created() {
        setTimeout(() => {
            this.getUserPosted();
        }, 2000);
    },
    mounted() {
    },
    activated() {
    },
    deactivated() {
    },
    components: { UserPostedMap, Loading}
})
</script>

<template>
    <div class="user__posted__main" id="main">
        <div class="">
            <!-- <div class="posts" v-if="user_posted.length > 0" v-for="post in user_posted" :key="post.id">
                <UserPostedMap class="post" :post="post"/>
            </div> -->
            <TransitionGroup name="slide" mode="out-in" tag="div">
                <div class="user__posted" v-if="user_posted" v-for="user in user_posted" :key="user.id">
                    <UserPostedMap class="post" :post="user"/>
                </div>
            </TransitionGroup>
        </div>
        <div class="col-12" v-if="user_posted.length == 0 && !loading">
            <h3 class="text-center">User hasn't made any post.</h3>
        </div>
        <div class="loading" v-if="loading">
            <!-- <q-spinner-oval class="spinner"/> -->
            <Loading :stroke-width="5"/>
        </div>
    </div>
</template>


<style scoped>
#main {
    height: 100%;
}
.user__posted {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 5px;
    width: 100%;
}

/* .user__posted__main {

} */

.loading {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>