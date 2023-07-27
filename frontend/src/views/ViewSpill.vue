<script lang="ts">
import { http } from '@/assets/http';
import type { Post, Comment, User } from '@/assets/interfaces';
import PostsMap from '@/components/PostsMap.vue';
import { defineComponent, ref } from 'vue';
import { AbbreviateNumber } from '@/assets/abbreviate';
import convertTime from '@/assets/convertTime';

export default defineComponent({
    name: "view-spill",
    data() {
        return {
            spill: {} as Post,
            user: {} as User,
            comments: new Array<Comment>(),
            loading_post: true,
            liked: false,
            total_likes: 0,
            total_comments: 0,

            loading_comments: true,
            date: new Date(),
            date_posted: '',
            page: 0,
            // websocket: new WebSocket(`wss://localhost:8000/ws/spill/${this.$route.params.post_id}/`),
            dropdown: false,
            persistent: false,
            report: false,
            reason: '',

            imgZoom: false,

            hovering: false,

            delayEnter: ref<number | null>(),
            delayExit: ref<number | null>(),
            toolTip_date: '',
        };
    },
    created() {
        this.getSpill();
        this.getComments();
    },
    methods: {
        async getSpill() {
            this.loading_post = true;
            await http.get(`posts/post_by_id/${this.$route.params.post_id}/`).then((res) => {
                this.spill = res.data.spill;
                this.user = this.spill.user;
                this.date_posted = convertTime(this.spill.date_posted, 'short')
                this.toolTip_date = convertTime(this.spill.date_posted, 'absolute')
                this.total_likes = this.spill.total_likes;
                this.liked = this.spill.user_has_liked
                // this.checkLiked();
            }).catch((err) => {
            });
            this.loading_post = false;
        },
        async getComments() {
            this.loading_comments = true;
            await http.get(`comments/comments_by_post/${this.date.toISOString()}/${this.page}/${this.$route.params.post_id}/`).then((res) => {
                if(res.data.comments) {
                    this.comments = [...res.data.comments, ...this.comments]
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
                    // console.log(res.data)
                }
            }).catch((err) => {
                console.log(err)
            })
        },
        // async websocketOpen() {
        //     this.websocket = new WebSocket(`wss://localhost:8000/ws/spill/${this.$route.params.post_id}/`)
        //     this.websocket.onopen = (e) => {
        //         console.log('Websocket opened')
        //     }
        // },
        // async websocketMessage() {
        //     this.websocket.onmessage = async (e) => {
        //         const data = JSON.parse(e.data)
        //         if(data.type == "comment") {
        //             const newComment = JSON.parse(data.message) as Comment

        //             if(this.comments.length !== 0) {
        //                 this.comments = [newComment, ...this.comments];
        //                 this.total_comments = this.comments.length
        //             }
        //             else {
        //                 this.comments.push(newComment)
        //             }
        //         }
        //     }
        // },
        // async websocketClose() {
        //     this.websocket.close()

        //     this.websocket.onclose = (e) => {
        //         console.log('Websocket closed')
        //     }
        // },
        deleteComment(index: number) {
            this.comments.splice(index, 1)
        },
        reportPost() {

        },
        deletePost() {

        },
        divEnter() {
            if(this.$q.screen.lt.sm) {
                return;
            }
            if (this.delayExit) {
                clearTimeout(this.delayExit);
            }
            if (!this.hovering) { // Check if the menu is not already open
                this.delayEnter = window.setTimeout(() => {
                    this.hovering = true;
                    this.delayEnter = null;
                }, 700); // Add a delay before opening the menu (adjust this value as needed)
            }
        },

        divExit() {
            if(this.$q.screen.lt.sm) {
                return;
            }
            if (this.delayEnter) {
                clearTimeout(this.delayEnter);
            }
            if (this.hovering) { // Check if the menu is currently open
                this.delayExit = window.setTimeout(() => {
                    this.hovering = false;
                    this.delayExit = null;
                }, 500); // Add a delay before closing the menu (adjust this value as needed)
            }
        },
    },
    mounted() {
        // this.websocketOpen()
        // this.websocketMessage()
    },
    unmounted() {
        // this.websocketClose()
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
       '$route'() {
            this.divExit()
       },
        comments(comments) {
            this.total_comments = comments.length;
        }
    }
})
</script>

<template>
    <div class="grid">
        <div>
            <header class="sticky top-0 bg-theme-opacity bg-blur-1 z-1">
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
                    <Item align-items="start" avatar-size="3.5rem">
                        <template #avatar>
                            <div class="hover-darker pointer" @click.stop="$router.push({name: 'user-profile', params: { username: spill.user.username }})">
                                <img v-if="spill.user.avatar" :src="spill.user.avatar" alt="User Avatar" class="rounded-full" />
                                <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" />
                            </div>
                        </template>
                        <template #title>
                        <div class="h-full min-w-full flex gap-1 items-center title">
                            <div class="ellipsis" >
                                <user-card :user-prop="user">
                                    <template #text>
                                        <span @mouseover="divEnter"  @mouseleave="divExit"  class="text-lg pointer hover-underline text-heading weight-900" @click.stop="$router.push({name: 'user-profile', params: { username: spill.user.username }})">{{spill.user.first_name}} 
                                            {{ spill.user.last_name }}
                                        </span>
                                    </template>
                                </user-card>
                            </div>
                        </div>

                        </template>

                        <template #caption>
                            <!-- <div class="ellipsis">
                                <span class="text-lg text-lighter weight-500 hover-underline">{{ date_posted }}</span>
                                <q-tooltip class="bg-theme box-shadow">
                                    <span class="text-sm " v-html="toolTip_date"></span>
                                </q-tooltip>
                            </div> -->

                            <div>
                                <div class="ellipsis">
                                    <span class="text-lg pointer hover-underline text-lighter weight-500" @click.stop="$router.push({name: 'user-profile', params: { username: spill.user.username }})">@{{ spill.user.username }} </span>
                                </div>
                            </div>
                        </template>
                        <template #icon>
                            <div>
                                <q-btn @click.stop="dropdown = !dropdown" size="13px" class="more__vert" flat round icon="more_horiz" />
                                <q-menu class="dropdown bg-theme border" v-model="dropdown" transition-show="jump-down" transition-hide="jump-up" cover anchor="top right">
                                    <q-list class="more__option">
                                        <q-item clickable v-close-popup @click="report = true" v-if="!spill.is_owner">
                                            <q-item-section avatar>
                                                <q-icon class="danger__icon" name="flag"/>
                                            </q-item-section>
                                            <q-item-section>
                                                <q-item-label>Report Post</q-item-label>
                                            </q-item-section>
                                        </q-item>
                                        <q-item clickable v-close-popup @click="persistent = true" tabindex="0" v-if="spill.is_owner">
                                            <q-item-section avatar>
                                                <q-icon class="danger__icon" name="delete_forever"/>
                                            </q-item-section>
                                            <q-item-section>
                                                <q-item-label>Delete</q-item-label>
                                            </q-item-section>
                                        </q-item>
                                        <q-item clickable v-close-popup v-if="spill.is_owner">
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
                            
                        </template>
                    </Item>
                </div>
                <div class="text-base no-decor w-fit px-2">
                    <Item dense>
                        <template #caption>
                            <span class="text-base">
                                <MentionLink  :mention="spill.caption"/>
                            </span>
                        </template>
                    </Item>
                </div>
                <div class="w-full p-2">
                    <q-img @click="imgZoom = true" class="w-full rounded border hover-darker  cursor-zoom" :src="spill.img_url" />
                    <zoomImg v-if="imgZoom" :img="spill.img_url" :open="imgZoom" @update:open="imgZoom = $event"/>
                </div>
                <!-- <div class="q-pa-md q-gutter-sm relative" style="height: 80px">
                    <q-avatar
                        v-for="(user, index) in spill.all_liked_users"
                        :key="user.id"
                        size="40px"
                        class="absolute"
                        :style="`left: ${Number(index) * 25}px`"
                        >
                        <img :src="user.avatar">
                    </q-avatar>
                    <div v-for="user in spill.all_liked_users">
                        {{ user.avatar }}
                        <q-tooltip :offset="[0,0]">
                            <span class="text-sm">{{ user.first_name }} {{ user.last_name }}</span>
                        </q-tooltip>
                    </div>
                </div> -->
                <hr class="m-2"/>
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
                        <span><span class="text-heading weight-900">{{ total_comments }}</span> Comments</span>
                    </div>
                </div>
                <hr class="m-2"/>
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
                                Comment
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
                <hr class="m-2"/>
                <div class="px-2 border-b" v-if="$store.state.authenticated">
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

<style scoped lang="scss">

* {
    transition: all .3s;
}

.followed {
  &:hover {
    span {
      display: none;
    }

    border: 1px solid red !important;
    background-color: rgba(255, 0, 0, 0.1) !important;

    &::before {
      content: 'Unfollow';
      // font-size: 20px;
      color: red;
      font-weight: 900;
      transition: opacity 0.3s ease-in-out;
    }
  }
}

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