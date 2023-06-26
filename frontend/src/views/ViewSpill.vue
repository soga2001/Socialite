<script lang="ts">
import { http } from '@/assets/http';
import type { Post, Comment } from '@/assets/interfaces';
import PostsMap from '@/components/PostsMap.vue';
import { defineComponent } from 'vue';

export default defineComponent({
    name: "view-spill",
    props: {
        propSpill: {
            type: Object as () => Post,
        },
    },
    data() {
        return {
            spill: {} as Post,
            comments: new Array<Comment>(),
            loading_post: true,
            liked: false,
            total_likes: 0,
            total_comments: 0,

            loading_comments: true,
            date: new Date(),
            page: 0,
            websocket: new WebSocket(`wss://localhost:8000/ws/spill/${this.$route.params.post_id}/`),
        };
    },
    created() {
        this.getSpill();
        this.getComments();
        // console.log(this.$route.fullPath)
    },
    methods: {
        async getSpill() {
            this.loading_post = true;
            await http.get(`posts/post_by_id/${this.$route.params.post_id}/`).then((res) => {
                this.spill = res.data.spill;
                this.total_likes = this.spill.total_likes;
                this.checkLiked();
            }).catch((err) => {
                // console.log(err);
            });
            this.loading_post = false;
        },
        async getComments() {
            this.loading_comments = true;
            await http.get(`comments/comments_by_post/${this.date.toISOString()}/${this.page}/${this.$route.params.post_id}/`).then((res) => {
                if(res.data.comments) {
                    if(this.comments) {
                        this.comments.unshift(...res.data.comments)
                    }
                    else {
                        this.comments = res.data.comments;
                    }
                }
                    
            }).catch((err) => {
                console.log(err);
            });
            this.loading_comments = false;
        },
        checkLiked() {
            if(!this.$store.state.authenticated) {
                return false;
            }
            console.log('here')
            http.get(`like/check_liked/${this.spill.id}/`).then((res) => {
                if(res.data.liked) {
                    this.liked = res.data.liked;
                }
                else {
                    this.liked = false;
                }
            }).catch((err) => {
                console.log(err)
            })
            // this.liked = true
        },
        like() {
            if (!this.$store.state.authenticated) {
                this.$q.notify({
                    message: "You must be logged in to like a post!",
                    color: "negative",
                    position: "top-right",
                    timeout: 1000
                })
                return;
            }
            this.liked = !this.liked;
            http.post('like/like_post/', {
                post_id: this.spill.id
            }, {
            }).then((res) => {
                if(res.data.liked) {
                    this.total_likes += 1;
                }
                else if(!res.data.liked) {
                    this.total_likes -= 1;
                }
                else {
                    console.log(res.data)
                }
            }).catch((err) => {
                console.log(err)
            })
        },
        async websocketOpen() {
            this.websocket = new WebSocket(`wss://localhost:8000/ws/spill/${this.$route.params.post_id}/`)
            this.websocket.onopen = (e) => {
                console.log('Websocket opened')
            }
        },
        async websocketMessage() {
            this.websocket.onmessage = (e) => {
                const data = JSON.parse(e.data)
                if(data.type == "comment") {
                    const newComment = JSON.parse(data.message) as Comment
                    console.log(newComment)
                    if(this.comments.length !== 0) {
                        this.comments.unshift(newComment)
                    }
                    else {
                        this.comments.push(newComment)
                    }
                }
            }
        },
        async websocketClose() {
            this.websocket.close()

            this.websocket.onclose = (e) => {
                console.log('Websocket closed')
            }
        },
        deleteComment(index: number) {
            this.comments.splice(index, 1)
        }
    },
    mounted() {
        this.websocketOpen()
        this.websocketMessage()
    },
    unmounted() {
        this.websocketClose()
    },
    // activated() {
    //     this.websocketOpen();
    //     this.websocketMessage()
    // },
    // deactivated() {
    //     this.websocketClose();
    // },
    components: { },
    watch: {
    }
})
</script>

<template>
    <div class="grid">
        <div>
            <header class="sticky top-0 border-b bg-theme z-1">
                <Item dense>
                    <template #avatar>
                        <q-btn size="16px" @click="$router.back" flat dense round class="text-heading" icon="arrow_back" />
                    </template>
                    <template #title>
                        <span class="text-2xl text-heading weight-900">Spill</span>
                    </template>
                </Item>
            </header>
            <div v-if="!loading_post" class="">
                <div>
                    <Item>
                        <template #avatar>
                            <div class="hover-darker pointer" @click.stop="$router.push({name: 'user-profile', params: { username: spill.username }})">
                                <img v-if="spill.user_avatar" :src="spill.user_avatar" alt="John Doe" class="rounded-full" />
                                <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" />
                            </div>
                        </template>
                        <template #title><span class="text-xl pointer hover-underline text-heading weight-900" @click.stop="$router.push({name: 'user-profile', params: { username: spill.username }})">@{{ spill.username }}</span></template>
                        <template #caption>
                            <Timeago size="12px" :date="spill.date_posted"/>
                        </template>
                        <!-- <template #icon>
                            <div>
                                <q-btn @click.stop="dropdown = !dropdown" size="13px" class="more__vert" flat round icon="more_horiz" />
                                <q-menu class="dropdown" v-model="dropdown" transition-show="jump-down" transition-hide="jump-up" self="top middle">
                                    <q-list class="more__option">
                                        <q-item clickable v-close-popup @click="report = true" v-if="username !== $store.state.user.username">
                                            <q-item-section avatar>
                                                <q-icon class="danger__icon" name="flag"/>
                                            </q-item-section>
                                            <q-item-section>
                                                <q-item-label>Report Post</q-item-label>
                                            </q-item-section>
                                        </q-item>
                                        <q-item clickable v-close-popup @click="persistent = true" tabindex="0" v-if="username === $store.state.user.username">
                                            <q-item-section avatar>
                                                <q-icon class="danger__icon" name="delete_forever"/>
                                            </q-item-section>
                                            <q-item-section>
                                                <q-item-label>Delete</q-item-label>
                                            </q-item-section>
                                        </q-item>
                                        <q-item clickable v-close-popup v-if="username === $store.state.user.username">
                                            <q-item-section avatar>
                                                <q-icon class="" name="edit_note"/>
                                            </q-item-section>
                                            <q-item-section>
                                                <q-item-label>Edit</q-item-label>
                                            </q-item-section>
                                        </q-item>
                                    </q-list>
                                </q-menu>


                                <q-dialog v-model="persistent" persistent transition-show="scale" transition-hide="scale">
                                    <q-card class="card">
                                        <q-card-section class="row">
                                            <q-item>
                                                <q-item-section class="title">Are you sure you want to delete this post?</q-item-section>
                                            </q-item>
                                        </q-card-section>
                                        <q-card-section>
                                            <q-item>
                                                <q-item-section avatar>
                                                <q-avatar class="red" icon="warning"/>
                                                </q-item-section>
                                                <q-item-section class="red alert">This action is permanent and irreversible.</q-item-section>
                                            </q-item>
                                        </q-card-section>

                                        <q-card-actions align="right" class="buttons">
                                            <q-btn flat label="Cancel"  v-close-popup />
                                            <q-btn flat label="Confirm" @click="deletePost" v-close-popup />
                                        </q-card-actions>
                                    </q-card>
                                </q-dialog>


                                <q-dialog v-model="report" persistent>
                                    <q-card class="card">
                                        <q-card-section>
                                            <q-item>
                                                <q-item-section class="title">Report</q-item-section>
                                                <q-item-section avatar>
                                                <q-avatar class="red" icon="flag"/>
                                                </q-item-section>
                                            </q-item>
                                        </q-card-section>
                                        <q-card-section class="q-pt-none">
                                            <q-input
                                                v-model="reason"
                                                filled
                                                clearable
                                                type="textarea"
                                                label="Reason"
                                                :dark="$store.state.dark"                                
                                            />
                                        </q-card-section>

                                        <q-card-actions align="right" class="buttons">
                                            <q-btn flat label="Cancel" v-close-popup />
                                            <q-btn flat label="Report" v-close-popup @click="reportPost" />
                                        </q-card-actions>
                                    </q-card>
                                </q-dialog>
                            </div>
                            
                        </template> -->
                    </Item>
                </div>
                <div class="w-full">
                    <img class="w-full" :src="spill.img_url" alt="Spill Picture"/>
                </div>
                <div class="text-base no-decor w-fit">
                    <Item>
                        <template #caption>
                            <span class="text-base">
                                <MentionLink  :mention="spill.caption"/>
                            </span>
                        </template>
                    </Item>
                </div>
                <hr/>
                <div class="flex flex-row p-3 gap-5 text-base">
                    <div>
                        <span >
                            <span>
                            <transition name="fade" mode="out-in">
                                <span class="text-heading weight-900" v-if="total_likes % 2 == 0">{{ total_likes }}</span>
                                <span class="text-heading weight-900" v-else>{{ total_likes }}</span>
                            </transition>
                            </span>
                            Likes
                        </span>
                        
                    </div>
                    <div>
                        <!-- <span><span class="text-heading weight-900"> {{ spill.total_likes }}</span> Comments</span> -->
                        <span><span class="text-heading weight-900"> 0</span> Comments</span>
                    </div>
                </div>
                <hr/>
                <div class="flex flex-row gap-10 py-2 px-5">
                    <div>
                        <q-btn flat round :class="(liked ? 'liked' : '')"  @click.stop="like">
                            <q-tooltip :offset="[0,0]">
                                Like
                            </q-tooltip>
                            <i-heart size="1.5rem" :fill="liked ? 'red' : 'var(--color-text)'"  stroke="red" />
                        </q-btn>
                    </div>
                    <div>
                        <q-btn flat round :class="(liked ? 'liked' : '')"  @click.stop="">
                            <q-tooltip :offset="[0,0]">
                                Like
                            </q-tooltip>
                            <i-comment size="1.5rem" fill="var(--color-text)" stroke="var(--color-heading)" />
                        </q-btn>
                    </div>
                    <div>
                        <q-btn flat round :class="(liked ? 'liked' : '')"  @click.stop="">
                            <q-tooltip :offset="[0,0]">
                                Like
                            </q-tooltip>
                            <i-share size="1.5rem" fill="var(--color-text)" stroke="var(--color-heading)" />
                        </q-btn>
                    </div>
                </div>
                <hr/>
                <div class="border-b" v-if="$store.state.authenticated">
                    <Spills placeholder="Reply to the spill" btnString="Reply" isComment :spillId="spill.id"/>
                </div>
                <div class="grid overflow-hidden w-100">
                    <TransitionGroup name="slide" mode="out-in" tag="div">
                        <div v-if="comments" v-for="(comment, index) in comments" :key="comment.id">
                            <CommentMap :comment="comment" @deleted="deleteComment(index)"/>
                        </div>
                    </TransitionGroup>
                </div>
            </div>
            <div v-else="loading_post" class="">
                <Loading/>
            </div>
        </div>
    </div>
</template>

<style scoped>

/* #app {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.app span {
    position: relative;
} */





</style>