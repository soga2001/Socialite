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
import { AbbreviateNumber } from '@/assets/abbreviate';
import createIntersectObserver from '@/assets/intersectionObserver'

import SpillCard from './Cards/SpillCard.vue';
import Favorite from './Buttons/Favorite.vue';



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
            total_comments: this.post.total_comments,
            total_likes: this.post.total_likes,
            total_views: 0,
            comments: [],
            img_loading: true,
            avatar_loading: true,
            deleted: false,
            persistent: ref(false),
            report: ref(false),
            reason: ref(""),
            moment: moment,
            showComments: false,

            abbreviateLikes: AbbreviateNumber(this.post.total_likes) as Number,
            abbreviateComments: AbbreviateNumber(this.post.total_comments) as Number,
            abbreviateViews: AbbreviateNumber(0) as Number,

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
        },
        captionChange() {

        },
        viewed() {
            console.log(this.id)
            setTimeout(() => {
                // http.post('posts/viewed/', {
                //     post_id: this.id
                // }, {
                // }).then((res) => {
                //     this.abbreviateViews = AbbreviateNumber(res.data.views);
                // }).catch((err) => {
                //     console.log(err)
                // })
                this.total_views += 1;
            }, 1000);
        }
        
    },
    created() {
    },
    async mounted() {
        await this.$nextTick()
        const observer = createIntersectObserver(this.$el, this.viewed, {threshold: .75})
    },
    
    watch: {
        '$store.state.authenticated': function () {
            if(this.$store.state.authenticated) {
                this.checkLiked()
            } else {
                this.liked = false;
            }
        },
        total_likes(total_likes) {
            this.abbreviateLikes = AbbreviateNumber(total_likes) as Number;
        },
        total_comments(total_comments) {
            this.abbreviateComments = AbbreviateNumber(total_comments) as Number;
        },
        total_views(total_views) {
            this.abbreviateViews = AbbreviateNumber(total_views) as Number;
        }
    },
    components: { Timeago, Heart, Item, MentionLink, ToolTips, HeartIcon, SpillCard, Favorite }
})
</script>

<template>
    <div class="grid rounded-none bg-theme bg-hover-mute pointer" @click="$router.push({name: 'view-spill', params: { user: username, post_id: id}})" v-if="!deleted">
        <SpillCard class="w-full h-full relative">
            <template #avatar>
                <q-avatar class="hover-darker relative pointer" @click.stop="$router.push({name: 'user-profile', params: { username: username }})">
                    <img v-if="avatar" :src="avatar" alt="John Doe" class="rounded-full" />
                    <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" />
                </q-avatar>
            </template>
            <template #title>
                <Item dense align-items="start">
                    <template #title><span class="text-lg pointer hover-underline text-heading weight-900" @click.stop="$router.push({name: 'user-profile', params: { username: username }})">@{{ username }}</span></template>
                    <template #caption>
                        <span><Timeago size="12px" :date="date_posted"/></span>
                    </template>
                    <template #icon>
                        <div>
                            <q-btn @click.stop="dropdown = !dropdown" size="13px" class="more__vert" flat round icon="more_horiz" />
                            <q-menu class="dropdown bg-theme-soft" v-model="dropdown" transition-show="jump-down" transition-hide="jump-up" self="top middle">
                                <q-list class="more__option box-shadow" >
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
                    </template>
                </Item>

            </template>
            <template #subtitle>
                <div class="text-base w-fit" >
                    <MentionLink @click.stop="" :mention="caption"/>
                </div>
            </template>
            <template #body>
                <div class="w-full relative h-full">
                    <img class="w-full relative" :src="img_url" alt="Spill image" loading="lazy"/>
                </div>
            </template>
            <template #actions>
                    <div>
                        <div class="flex justify-center items-center gap-3">
                            <div>
                                <q-btn flat round :class="'action like__btn ' + (liked ? 'liked' : '')"  @click.stop="like">
                                    <q-tooltip v-if="!$q.screen.lt.sm" :offset="[0,0]">
                                        Like
                                    </q-tooltip>
                                    <i-heart size="1.4rem" :fill="liked ? 'red' : 'var(--color-text)'"  stroke="red" />
                                </q-btn>
                            </div>
                            <div>
                                <!-- <span :style="{color: liked ? 'red' : 'inherit'}">{{ abbreviateLikes}}</span> -->
                                <transition name="fade" mode="out-in">
                                    <span :style="{color: liked ? 'red' : 'inherit'}" class="weight-900" v-if="total_likes % 2 == 0">{{ abbreviateLikes}}</span>
                                    <span :style="{color: liked ? 'red' : 'inherit'}" class="weight-900" v-else>{{ abbreviateLikes}}</span>
                                </transition>
                            </div>
                        </div>
                    </div>
                    <div>
                        <div class="flex justify-center items-center gap-2">
                            <div>
                                <q-btn flat round class="action comment" @click.stop="commentToggle">
                                    <q-tooltip v-if="!$q.screen.lt.sm" :offset="[0,0]">
                                        Comment
                                    </q-tooltip>
                                    <i-comment fill="var(--color-text)" />
                                </q-btn>
                            </div>
                            <transition name="fade" mode="out-in">
                                <span class="text-heading weight-900" v-if="total_comments % 2 == 0">{{ abbreviateComments }}</span>
                                <span class="text-heading weight-900" v-else>{{ abbreviateComments }}</span>
                            </transition>
                        </div>

                        <q-dialog class="min-h-sm" v-model="showComments" persistent>
                            <div class="bg-theme box-shadow box-theme-soft w-full min-h-fit max-w-sm h-fit overflow-visible" >
                                <div class="p-2">
                                    <Item dense :vert-icon-center="true">
                                        <template #title>
                                            <div class="text-2xl weight-900">Comment</div>
                                        </template>
                                        <template #icon>
                                            <i-close size="2rem" class="pointer" @click="showComments = false"/>
                                        </template>
                                    </Item>
                                </div>
                                <hr class="border"/>
                                <div class="">
                                    <Spills  placeholder="Reply to the spill" btnString="Reply" isComment :spillId="id" :rows="4"/>
                                </div>
                            </div>
                        </q-dialog>
                    </div>

                    <div>
                        <div class="flex justify-center items-center gap-1">
                            <div>
                                <q-btn round flat @click.stop="">
                                    <q-tooltip :offset="[0,0]" v-if="!$q.screen.lt.sm">
                                        Views
                                    </q-tooltip>
                                    <q-icon class="text-body" name="visibility"/>
                                </q-btn>
                            </div>
                            <transition name="fade" mode="out-in">
                                <span class="text-heading weight-900" v-if="total_views % 2 == 0">{{ abbreviateViews }}</span>
                                <span class="text-heading weight-900" v-else>{{ abbreviateViews }}</span>
                            </transition>
                        </div>
                    </div>

                    <q-btn round flat>
                        <q-tooltip v-if="!$q.screen.lt.sm" :delay="500" :offset="[0,0]">
                            Copy Link
                        </q-tooltip>
                        <i-share fill="var(--color-text)" />
                    </q-btn>
            </template>
        </SpillCard>
    </div>
</template>

<!-- <template>
    <q-card ref="spill" id="spill"  class="grid rounded-none bg-theme bg-hover-mute pointer" @click="$router.push({name: 'view-spill', params: { user: username, post_id: id}})" v-if="!deleted">
        <div  class="post__main">
            <Item>
                <template #avatar>
                    <div class="hover-darker" @click.stop="$router.push({name: 'user-profile', params: { username: username }})">
                        <img v-if="avatar" :src="avatar" alt="John Doe" class="rounded-full" />
                        <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" />
                    </div>
                </template>
                <template #title><span class="text-xl pointer hover-underline text-heading weight-900" @click.stop="$router.push({name: 'user-profile', params: { username: username }})">@{{ username }}</span></template>
                <template #caption>
                    <span><Timeago size="12px" :date="date_posted"/></span>
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
        <q-img :src="img_url" @click.stop=""/>
        <Item title-size="16px" caption-size="13px">
            <template #caption>
                <div class="text-base w-fit" @click.stop="" >
                    <MentionLink   :mention="caption"/>
                </div>
            </template>
        </Item>

        <q-separator :dark="$store.state.dark"/>
        <q-card-actions class="p-0 m-0 flex gap-2 justify-center z-2">
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
                        <span :style="{color: liked ? 'red' : 'none'}">{{abbreviateLikes}}</span>
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
                        <label>{{abbreviateComments}}</label>
                    </div>
                </div>

                <q-dialog class="min-h-sm" v-model="showComments" persistent>
                    <div class="bg-theme box-theme-soft w-full min-h-fit max-w-sm h-fit overflow-visible" >
                        <div class="p-2">
                            <Item dense :vert-icon-center="true">
                                <template #title>
                                    <div class="text-2xl weight-900">Comment</div>
                                </template>
                                <template #icon>
                                    <i-close size="2rem" class="pointer" @click="showComments = false"/>
                                </template>
                            </Item>
                        </div>
                        <hr class="border"/>
                        <div class="">
                            <Spills  placeholder="Reply to the spill" btnString="Reply" isComment :spillId="id" :rows="4"/>
                        </div>
                    </div>
                </q-dialog>
            </div>

            <div>
                <div class="flex justify-center items-center gap-1">
                    <div>
                        <q-btn round flat @click.stop="">
                            <q-tooltip :offset="[0,0]">
                                Views
                            </q-tooltip>
                            <q-icon class="text-body" name="visibility"/>
                        </q-btn>
                    </div>
                    <transition name="fade" mode="out-in">
                        <span class="text-heading" v-if="total_views % 2 == 0">{{ abbreviateViews }}</span>
                        <span class="text-heading" v-else>{{ abbreviateViews }}</span>
                    </transition>
                </div>
            </div>

            <q-btn round flat>
                <q-tooltip :offset="[0,0]">
                    Copy Link
                </q-tooltip>
                <i-share fill="var(--color-text)" />
            </q-btn>  
        </q-card-actions>
    </q-card>
    <q-card class="deleted" v-else>
        <span class="deleted__msg">This post has been deleted.</span>
    </q-card>
</template> -->

