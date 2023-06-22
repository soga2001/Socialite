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

            deleted: false,
            deletedMsg: '',
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
        async websocketMessage() {
            this.websocket.onmessage = (e) => {
                const data = JSON.parse(e.data)
                if(data.type == "posted") {
                    this.user_posted.unshift(JSON.parse(data.message))
                }
            }
        },
        deleteSpill(index: number) {
            this.user_posted.splice(index, 1)
        }
    },

    created() {
        this.getUserPosted()
        this.websocketMessage()
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
        <TransitionGroup name="slide" mode="out-in" tag="div">
                <UserPostedMap class="post m-2" :post="user" v-if="user_posted" v-for="(user, index) in user_posted" :key="user.id" @deleted="deleteSpill(index)"/>
        </TransitionGroup>
        <div class="w-full flex flex-center flex-col" v-if="user_posted.length == 0 && !loading">
            <div>
                <i-folder :fill="'black'" stroke="black"/>
            </div>
            <div class="text-3xl weight-900">
                User hasn't liked anything.
            </div>
        </div>
        <div class="loading" v-if="loading">
            <Loading :stroke-width="5"/>
        </div>
    </div>
</template>


<style scoped>
#main {
    height: 100%;
}

.loading {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>