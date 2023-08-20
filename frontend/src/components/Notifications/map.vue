<script lang="ts">
import { defineComponent } from 'vue';
import type { Notifications, NotificationDataAsset } from '@/assets/interfaces';
import convertTime from '@/assets/convertTime';
import MentionLinkVue from '../MentionLink.vue';
// import createIntersectionObserver
import createIntersectionObserver from '@/assets/intersectionObserver';
import { http } from '@/assets/http';

export default defineComponent({
    props: {
        notification: {
            type: Object as () => Notifications,
            required: true
        }
    },
    data() {
        return {
            date_posted: convertTime(this.notification.timestamp, 'short'),
            toolTipDate: convertTime(this.notification.timestamp, 'absolute'),
            unread: this.notification.unread,
        };
    },
    computed: {
    },
    methods: {
        alert() {
        },
        mark_read() {
            // if(this.unread) {
            //     http.put('notifications/mark_as_read/', {
            //         id: this.notification.id
            //     }).then((res) => {
                    
            //     })
            // }
            setTimeout(() => {
                this.unread = false
            }, 1000)
        }
    },
    async mounted() {
        const observer = createIntersectionObserver(this.$el, this.mark_read, {threshold: 1})
    },
    watch: {
    },
    components: { MentionLinkVue }
})
</script>

<template>
    <Item class="max-w-viewport w-full pointer item" :class="{'bg-theme-mute': unread}" clickable :to="notification.data.url"  align-items="start"  avatarSize="3.5rem">
        <template #avatar>
            <user-card :user-prop="notification.actor">
                <template #text>
                    <q-avatar>
                        <img :style="{width: '3rem', height: '3rem'}" v-if="notification.actor.avatar" :src="notification.actor.avatar" alt="user's avatar"/>
                        <i-profile v-else size="3rem" />
                        <q-badge class="absolute bottom-0 right-0 bg-theme" style="border-radius: 50%; width: 25px; height: 25px">
                        <q-badge class="absolute-center bg-web-theme" style="border-radius: 50%; width: 20px; height: 20px">
                            <i-mention fill="white" :style="{transform: 'scale(1.7)'}" v-if="notification.verb == 'mention'"/>
                            <i-profile stroke="none" fill="white" :style="{transform: 'scale(1.7)'}" v-if="notification.verb == 'follow'" />
                            <i-comment fill="white" stroke="none" :style="{transform: 'scale(1.5)'}" v-if="notification.verb == 'commented'" />
                        </q-badge>
                        </q-badge>
                    </q-avatar>
                </template>
            </user-card>
        </template>
        <template #title>
            <Item dense align-items="start">
                <template #title>
                    <div class="h-full min-w-full flex gap-1 items-center title">
                        <div class="ellipsis" >
                            <user-card :user-prop="notification.actor">
                                <template #text>
                                    <span class="ellipsis text-lg pointer hover-underline text-heading weight-900" > 
                                        {{notification.actor.first_name}}
                                        {{ notification.actor.last_name }}
                                    </span>
                                </template>
                            </user-card>
                        </div>

                        <span class="text-lighter weight-900">&#183;</span>

                        <div>
                            <div class="ellipsis">
                                <user-card :user-prop="notification.actor">
                                    <template #text>
                                        <span class="text-lg pointer hover-underline text-lighter weight-500">@{{ notification.actor.username }}</span>
                                    </template>
                                </user-card>
                            </div>
                        </div>

                        <span class="text-lighter weight-900">&#183;</span>

                        <div class="ellipsis ">
                            <span class="text-lg text-lighter weight-500 hover-dotted">{{ date_posted }}</span>
                            <q-tooltip class="bg-theme box-shadow">
                                <span class="text-sm " v-html="toolTipDate"></span>
                            </q-tooltip>
                        </div>
                        
                    </div>

                </template>
                <!-- <template #icon>
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
                </template> -->
            </Item>
        </template>
        <template #subTitle>
            <span class="text-lighter">{{ notification.description }}</span>
        </template>
        <template v-if="notification.data.text" #caption>
            <span class="text-heading weight-600" >
                <MentionLinkVue class="text-sm" :mention="notification.data.text" />
            </span>
        </template>
        <template #icon>
            <q-btn @click.stop="alert" size="12px" flat dense round icon="more_horiz" />
        </template>
    </Item>
</template>

<style lang="scss" scoped>

</style>