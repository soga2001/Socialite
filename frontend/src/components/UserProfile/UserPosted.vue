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
        // websocket: {
        //     type: Object as PropType<WebSocket>,
        //     required: true,
        // },
        scrollPosition: {
            type: Number,
            default: 0,
        },
        height: {
            type: Number,
            default: 0,
        },
        name: {
            type: String,
            default: 'User Posted',
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
            hasMore: true,

            deleted: false,
            deletedMsg: '',

            errMsg: '',
        };
    },
    setup() {
    },
    methods: {
        async getUserPosted() {
            this.loading = true
            await http.get(`posts/user_posted/${this.user_timestap}/${this.page}/${(this.username)}/`).then((res) => {
                if(res.data.posts) {
                    if(res.data.posts.length == 0) {
                        this.hasMore = false
                    }
                    else{
                        this.hasMore = true
                    }
                    this.user_posted = [...this.user_posted, ...res.data.posts];
                }
                if(res.data.error) {
                    this.errMsg = res.data.message
                    this.hasMore = false
                }
            }).catch((err) => {
                console.log(err);
            });

            this.loading = false
        },
        // async websocketMessage() {
        //     this.websocket.onmessage = (e) => {
        //         const data = JSON.parse(e.data)
        //         if(data.type == "posted") {
        //             this.user_posted.unshift(JSON.parse(data.message))
        //         }
        //     }
        // },
        deleteSpill(index: number) {
            this.user_posted.splice(index, 1)
        }
    },

    created() {
        this.getUserPosted()
        document.title = this.name
        // this.websocketMessage()
    },
    mounted() {
    },
    activated() {
        // this.websocketMessage()
        document.title = this.name
    },
    deactivated() {
    },
    components: { UserPostedMap, Loading},
    watch: {
        scrollPosition(scrollPosition) {
            if(scrollPosition >= this.height - 500 && this.hasMore && !this.loading) {
                this.page += 1
                this.loading = true
                this.getUserPosted()
            }
        },
    }
})
</script>

<template>
    <div class="user__posted__main pb-2" id="main">
        <!-- <TransitionGroup name="slide" mode="out-in" tag="div">
                
        </TransitionGroup> -->
        <!-- <div class="grid gap-1 cols-3">
            <UserPostedMap class="post" :post="user" v-if="user_posted" v-for="(user, index) in user_posted" :key="user.id" @deleted="deleteSpill(index)"/>
        </div> -->
        <div class="grid">
            <div class="post_map border-b" v-if="user_posted.length > 0" v-for="(post, index) in user_posted" :id="post.id" :key="post.id">
                <PostsMap :post="post" />
            </div>
            <!-- <div class="w-full flex justify-center p-5" v-if="loading">
                <Loading />
            </div> -->
        </div>
        
        <div class="w-full flex flex-center flex-col" v-if="user_posted.length == 0 && !loading">
            <div>
                <i-folder :fill="'black'" stroke="black"/>
            </div>
            <div v-if="!errMsg" class="text-3xl weight-900 text-center">
                User hasn't spilled any tea.
            </div>
            <div v-else class="text-3xl weight-900 text-center">
                {{errMsg}}
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