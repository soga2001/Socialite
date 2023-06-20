<script lang="ts">
import { defineComponent, ref } from 'vue';
import type { Post } from '@/assets/interfaces';
import { http } from '@/assets/http';
import moment from 'moment'
import Timeago from './Timeago.vue';
import { useCookies } from 'vue3-cookies';
import Heart from './Heart.vue';
import Item from './Item.vue';
import MentionLink from './MentionLink.vue';
import ToolTips from './ToolTips.vue';
import HeartIcon from '@/icons/i-heart.vue';


export default defineComponent({
    props: {
        post: { type: Object as () => Post, required: true }
    },
    setup() {
        const {cookies} = useCookies();
        return {cookies}
    },
    data() {
        return {
            id: this.post.id,
            username: this.post.username,
            user_id: this.post.user,
            img_url: this.post.img_url,
            caption: this.post.caption,
            date_posted: this.post.date_posted,
            date_updated: this.post.date_posted,
            avatar: this.post.user_avatar,
            dropdown: false,
            liked: this.checkLiked(),
            total_comments: 0,
            total_likes: this.post.total_likes || 0,
            comments: [],
            img_loading: true,
            avatar_loading: true,
            deleted: false,
            persistent: ref(false),
            report: ref(false),
            reason: ref(""),
            moment: moment,
            showComments: false,
        };
    },
    methods: {
        reportPost() {
            console.log(this.reason);
        },
        checkLiked() {
            if(!this.$store.state.authenticated) {
                return false;
            }
            http.get(`like/check_liked/${this.post.id}/`).then((res) => {
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
                post_id: this.id
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
        setDelete() {
            this.deleted = true;
        },
        deletePost() {
            http.delete("posts/delete_post/", {
                data: {
                    id: this.id
                },
            }).then((res) => {
                this.deleted = true
            }).catch((err) => {
                console.log(err);
            });
        },
        onImgLoad() {
            this.img_loading = false;
        },
        onAvatarLoaded() {
            this.avatar_loading = false;
        },
        commentToggle() {
            this.showComments = !this.showComments;
            alert("clicked")
        },
        captionChange() {

        },
        
    },
    created() {
    },
    mounted() {
    },
    watch: {
        '$store.state.authenticated': function () {
            if(this.$store.state.authenticated) {
                this.checkLiked()
            } else {
                this.liked = false;
            }
        }
    },
    components: { Timeago, Heart, Item, MentionLink, ToolTips, HeartIcon }
})
</script>

<template>
    <q-card class="grid border-t border-b bg-theme bg-hover-mute pointer" @click="$router.push({name: 'view-spill', params: { user: username, post_id: id}})" v-if="!deleted">
        <div class="post__main">
            <Item>
                <template #avatar>
                    <div class="hover-darker" @click.stop="$router.push({name: 'user-profile', params: { username: username }})">
                        <img v-if="avatar" :src="avatar" alt="John Doe" class="rounded-full" />
                        <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" />
                    </div>
                </template>
                <template #title><span class="text-xl pointer hover-underline text-heading weight-900" @click.stop="$router.push({name: 'user-profile', params: { username: username }})">@{{ username }}</span></template>
                <template #caption>
                    <Timeago size="12px" :date="date_posted"/>
                </template>
                <template #icon>
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
                        <!-- Confirm Delete Model -->
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
                        <!-- Report model -->
                        <q-dialog v-model="report" persistent>
                            <q-card class="card">
                                <q-card-section>
                                    <!-- <h6 class="title">Report</h6> -->
                                    <q-item>
                                        <q-item-section class="title">Report</q-item-section>
                                        <q-item-section avatar>
                                        <q-avatar class="red" icon="flag"/>
                                        </q-item-section>
                                    </q-item>
                                </q-card-section>
                                <q-card-section class="q-pt-none">
                                    <!-- <q-input :dark="$store.state.dark" class="report__reason" placeholder="Reason" dense v-model="reason" /> -->
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
        <q-img :src="img_url" @click.stop=""/>
        <Item title-size="16px" caption-size="13px">
            <!-- <template #title class="caption__username">
                {{ username }}
            </template> -->
            <template #caption>
                <div class="text-base w-fit" @click.stop="" >
                    <MentionLink   :mention="caption"/>
                </div>
            </template>
        </Item>

        <q-separator :dark="$store.state.dark"/>
        <q-card-actions class="p-0 m-0 flex gap-2 justify-center z-index-2">
            <div>
                <div class="flex justify-center items-center gap-1">
                    <div>
                        <q-btn flat round :class="'action like__btn ' + (liked ? 'liked' : '')"  @click.stop="like">
                            <q-tooltip :offset="[0,0]">
                                Like
                            </q-tooltip>
                            <i-heart size="1.5rem" :fill="liked ? 'red' : 'var(--color-text)'"  stroke="red" />
                        </q-btn>
                    </div>
                    <div>
                        <label>{{total_likes}}</label>
                    </div>
                </div>
            </div>
            <div>
                <div class="flex justify-center items-center gap-2">
                    <div>
                        <q-btn flat round class="action comment" @click.stop="commentToggle">
                            <q-tooltip :offset="[0,0]">
                                Comment
                            </q-tooltip>
                            <i-comment fill="var(--color-text)" />
                        </q-btn>
                    </div>
                    <div>
                        <label>{{total_comments}}</label>
                    </div>
                </div>
            </div>
            
            <!-- <q-btn :icon="total_comments == 0 ? 'sym_o_chat_bubble' : 'sym_o_chat'" round flat>
                <q-tooltip :offset="[0,0]">
                    Comment
                </q-tooltip>
            </q-btn> -->

            <q-btn round flat>
                <q-tooltip :offset="[0,0]">
                    Copy Link
                </q-tooltip>
                <i-share fill="var(--color-text)" />
            </q-btn> 
        </q-card-actions>
        <!-- <q-separator :dark="$store.state.dark"/>
        <div class="comments">
            <p>Comments</p>
            <q-item v-if="caption">
                <q-item-section avatar>
                <q-avatar>
                    <img :src="avatar">
                </q-avatar>
                </q-item-section>

                <q-item-section>
                <q-item-label><span class="caption__username">{{ username }}</span> <span></span></q-item-label>
                <q-item-label caption class="post__caption">{{caption}}</q-item-label>
                <q-item-label caption class="post__caption">Some comment</q-item-label>

                </q-item-section>
            </q-item>
        </div> -->
    </q-card>
    <q-card class="deleted" v-else>
        <span class="deleted__msg">This post has been deleted.</span>
    </q-card>
</template>

<style scoped>

.z-index-2 {
    z-index: 2;
}

.post__info {
    padding: 5px 10px;
    background-color: transparent !important;
}
.username {
    font-size: 20px;
    color: var(--color-heading);
    font-weight: bold;
}

.date__posted {
    font-size: 12px;
    color: var(--color-text);
}

.dropdown-btn {
    background-color: transparent;
    border: none;
    padding: 10px;
    cursor: pointer;
}

.dropdown-btn:hover {
    /* background-color: red; */
    border-radius: 50%;
}

.more__option {
    background-color: var(--color-background-mute);
    color: var(--color-heading);
    
}

.danger__icon {
    color: rgb(244, 106, 106);
}

.post__img {
    width: 100%;
}


.footer {
    padding: 15px 20px;
}
.post__interact {
    display: flex;
}


.like__btn {
    color: red;
}

.like__chip {
    background-color: transparent;
    color: var(--color-heading);
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
}

.like__btn.liked {
    animation: heartButton .5s;
}

@keyframes heartButton {
 0% {
  transform: scale(1);
 }

 50% {
  transform: scale(2);
 }

 100% {
  transform: scale(1);
 }
}


.actions {
    display: inline-flex;
    gap: 20px;
}
.action {
    padding: 0px 10px;
    cursor: pointer;
}

.skeleton {
    color: var(--color-text);
}


.post__interact h3 {
    padding: 10px;
}

.card {
    background-color: var(--color-background);
    box-shadow:0 4px 20px 0 var(--color-border);
    width: 100%;
    max-width: 500px;
}

.title {
    color: var(--color-heading) !important;
    font-weight: 900;
    font-size: 20px;
}

.confirm__divider {
    background-color: var(--color-border);
}

.confirm__text {
    color: var(--color-heading);
}

.buttons {
    color: var(--color-heading);
}


.alert {
    font-size: 15px;
}

.report__reason {
    background-color: var(--color-background);
    color: var(--color-heading) !important;
}

::placeholder {
    /* color: var(--color-heading) !important; */
    color: red !important;
}


.caption {
    padding: 15px 15px !important;
}

.caption__username {
    font-weight: bolder;
    color: var(--color-heading);
}


.post__caption {
    color: var(--color-text);
    line-height: 1.5;
    z-index: 3;
}

.comments {
    padding: 5px 15px;
    color: var(--color-heading);
}

.deleted {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100px;
}
.deleted__msg {
    font-weight: 900;
    font-size: 20px;
}
</style>