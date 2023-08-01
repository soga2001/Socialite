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

import convertTime from '@/assets/convertTime';



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
            user: this.post.user,
            // user_id: this.post.user,
            img_url: this.post.img_url,
            caption: this.post.caption,
            date_posted: convertTime(this.post.date_posted, 'short'),
            toolTip_date: convertTime(this.post.date_posted, 'absolute'),
            date_updated: this.post.date_posted,
            dropdown: false,
            liked: this.post.user_has_liked,
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

            is_following: this.post.user.is_following,

            abbreviateLikes: AbbreviateNumber(this.post.total_likes) as Number,
            abbreviateComments: AbbreviateNumber(this.post.total_comments) as Number,
            abbreviateViews: AbbreviateNumber(0) as Number,

            imgZoom: false,

            hovering: false,

            delayEnter: ref<number | null>(),
            delayExit: ref<number | null>(),


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
                this.total_views += 1;
            }, 1000);
        },
        focused() {
            this.date_posted = convertTime(this.post.date_posted, 'short')
        },

        // divEnter() {
        //     if(this.delayExit) {
        //         clearTimeout(this.delayExit as number)
        //     }
        //     this.delayEnter = setTimeout(() => {
        //         this.hovering = true;
        //         this.delayEnter = null
        //     }, 1000);

        // },

        // divExit() {
        //     if(this.delayEnter ) {
        //         clearTimeout(this.delayEnter as number)
        //     }
        //     this.delayExit = setTimeout(() => {
        //         this.hovering = false;
        //         this.delayExit = null
        //     }, 500);

        // },

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

        closeMenu() {
            // clearTimeout(this.delayTimeoutId as number)
        }
        
    },
    created() {
        console.log(this.is_following)
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
        },
        '$route'() {
            this.divExit()
        },
    },
    components: { Timeago, Heart, Item, MentionLink, ToolTips, HeartIcon, SpillCard, Favorite }
})
</script>

<template>
    <div @mousedown="focused" class="grid p-2 rounded-none bg-theme bg-hover-mute pointer" @click="$router.push({name: 'view-spill', params: { user: user.username, post_id: id}})" v-if="!deleted">
        <SpillCard class="w-full h-full relative">
            <template #avatar>
                <user-card :user-prop="user">
                    <template #text>
                        <q-avatar :size="$q.screen.lt.sm ? '2.8rem' : '3.5rem'" class="hover-darker relative pointer" @click.stop="$router.push({name: 'user-profile', params: { username: user.username }})">
                            <img v-if="user.avatar" :src="user.avatar" alt="John Doe" class="rounded-full" />
                            <img v-else src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" />
                        </q-avatar>
                    </template>
                </user-card>
            </template>
            <template #title>
                <Item dense align-items="start">
                    <template #title>
                        <div class="h-full min-w-full flex gap-1 items-center title">
                            <div class="ellipsis" >
                                <user-card :user-prop="user">
                                    <template #text>
                                        <span class="ellipsis text-lg pointer hover-underline text-heading weight-900" > 
                                            {{user.first_name}}
                                            {{ post.user.last_name }}
                                        </span>
                                    </template>
                                </user-card>
                            </div>

                            <span class="text-lighter weight-900">&#183;</span>

                            <div>
                                <div class="ellipsis">
                                    <user-card :user-prop="user">
                                        <template #text>
                                            <span class="text-lg pointer hover-underline text-lighter weight-500">@{{ user.username }}</span>
                                        </template>
                                    </user-card>
                                </div>
                            </div>

                            <span class="text-lighter weight-900">&#183;</span>

                            <div class="ellipsis ">
                                <span class="text-lg text-lighter weight-500 hover-dotted">{{ date_posted }}</span>
                                <q-tooltip class="bg-theme box-shadow">
                                    <span class="text-sm " v-html="toolTip_date"></span>
                                </q-tooltip>
                            </div>
                            
                        </div>

                    </template>
                    <template #icon>
                        <div>
                            <q-btn @click.stop="dropdown = !dropdown" size="10px" class="more__vert" flat round icon="more_horiz" />
                            <q-menu class=" bg-theme rounded-xs border-brighter" v-model="dropdown" transition-show="jump-down" transition-hide="jump-up" cover anchor="top right">
                                <q-list class="more__option box-shadow" >
                                    <q-item clickable v-close-popup @click="report = true" v-if="!post.is_owner">
                                        <q-item-section avatar>
                                            <q-icon class="danger__icon" name="flag"/>
                                        </q-item-section>
                                        <q-item-section>
                                            <q-item-label>Report Post</q-item-label>
                                        </q-item-section>
                                    </q-item>
                                    <q-item clickable v-close-popup @click="persistent = true" tabindex="0" v-if="post.is_owner">
                                        <q-item-section avatar>
                                            <q-icon class="danger__icon" name="delete_forever"/>
                                        </q-item-section>
                                        <q-item-section>
                                            <q-item-label>Delete</q-item-label>
                                        </q-item-section>
                                    </q-item>
                                    <q-item clickable v-close-popup v-if="post.is_owner">
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
                                <q-card class="bg-theme min-w-68 w-full">
                                    <q-card-section>
                                        <q-item>
                                            <q-item-section class="text-2xl text-heading weight-900">Report</q-item-section>
                                            <q-item-section avatar class="pointer" @click="report=false">
                                                <i-close stroke="none" fill="var(--color-heading)" size="2.3rem"/>
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

                                    <q-card-section>
                                        <q-item>
                                            <q-item-section avatar>
                                                <q-icon class="text-red-6" name="warning"/>
                                            </q-item-section>
                                            <q-item-section class="text-red-6 alert weight-700">If you submit a false report, you can be subjected to a ban!</q-item-section>
                                        </q-item>
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

                <!-- <div class="grid">
                    <div class="h-full flex gap-1 items-center">
                        <span class="text-xl pointer hover-underline text-heading weight-900" @click.stop="$router.push({name: 'user-profile', params: { username: username }})">Suyogya Poudel</span>
                        <span class="text-lighter weight-900">&#183</span>
                        <span class="text-base pointer hover-underline text-lighter weight-500" @click.stop="$router.push({name: 'user-profile', params: { username: username }})">@{{ username }}</span>
                        <span class="text-lighter weight-500">&#183</span>
                        <span class="text-base text-lighter weight-500">{{ date_posted }}</span>
                    </div>
                </div> -->
            </template>
            <template #subtitle>
                <div class="text-base w-fit "  >
                    <MentionLink  :mention="caption"/>
                </div>
            </template>
            <template #body>
                <div class="w-full relative h-full">
                    <q-img @click.stop="imgZoom = true" class="rounded-sm cursor-zoom hover-darker img" :src="img_url"/>
                    <zoomImg v-if="imgZoom" :img="img_url" :open="imgZoom" @update:open="imgZoom = $event" />
                </div>
            </template>
            <template #actions>
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

<style scoped lang="scss">



.title  {

    min-width: 100%;

    > :first-child {
        max-width: 40%;
    }


    :nth-child(3) {
        max-width: 30%;
    }

    > :last-child {
        max-width: 20%;
    }
}

.img {
    max-height: 600px;
    height: 100%;
    object-fit:contain;

}


.symbol {
    font-size: 1.5rem;
    font-weight: 900;
    color: var(--color-text);
}



</style>

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

