<script lang="ts">
import { http } from '@/assets/http';
import type { Post } from '@/assets/interfaces';
import { defineComponent } from 'vue';
import UserPostedMap from './UserPostedMap.vue';
import Loading from '../Loading.vue';
import type { PropType } from 'vue';

export default defineComponent({
    name: "user-liked",
    props: {
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
            required: false,
            default: 'User Liked',
        }
    },
    data() {
        return {
            // user_id: this.$route.query.id,
            username: this.$route.params.username,

            page: 0,
            user_timestap: new Date().toISOString(),
            user_liked: new Array<Post>(),
            loading: true,
            hasMore: true,
            // avatar: this.user_avatar

            errMsg: '',
        };
    },
    methods: {
        async getUserLiked() {
            this.loading = true
            await http.get(`like/view_liked/${this.user_timestap}/${this.page}/${(this.username)}/`).then((res) => {
                if(res.data.posts) {
                    if(res.data.posts.length == 0) {
                        this.hasMore = false
                    }
                    else{
                        this.hasMore = true
                    }
                    this.user_liked = [...this.user_liked, ...res.data.posts];
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
        //         if(data.type == "liked") {
        //             this.user_liked.unshift(JSON.parse(data.message))
        //         }
        //     }
        // },
        dislikeSpill(index: number) {
            this.user_liked.splice(index, 1)
        }
        
    },
    created() {
        this.getUserLiked()
        document.title = this.name
    },
    activated() {
        document.title = this.name
    },
    components: { UserPostedMap, Loading },
    watch: {
        scrollPosition(scrollPosition) {
            if(scrollPosition >= this.height - 500 && this.hasMore && !this.loading) {
                this.page += 1
                this.loading = true
                this.getUserLiked()
            }
        }
    }
})
</script>

<template>
    <div class="user__liked__main pb-2">
        <!-- <TransitionGroup name="slide" mode="out-in" tag="div">
                
        </TransitionGroup> -->
        <!-- <div class="grid gap-1 cols-3">
            <UserPostedMap class="post"  v-if="user_liked" v-for="(user, index) in user_liked" :key="user.id" :post="user" @disliked="dislikeSpill(index)"/>
        </div> -->
        <div class="grid">
            <div class="post_map border-b" v-if="user_liked.length > 0" v-for="(post, index) in user_liked" :id="post.id" :key="post.id">
                <PostsMap :post="post" />
            </div>
            <!-- <div class="w-full flex justify-center p-5" v-if="loading">
                <Loading />
            </div> -->
        </div>
        <div class="w-full flex flex-center flex-col" v-if="user_liked.length == 0 && !loading">
            <div>
                <i-folder :fill="'black'" stroke="black"/>

            </div>
            <div v-if="!errMsg" class="text-3xl weight-900 text-center">
                User hasn't liked any spills.
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