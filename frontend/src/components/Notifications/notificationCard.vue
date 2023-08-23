<script lang="ts">
import {defineComponent} from 'vue'
// import user interface
import type { User } from '@/assets/interfaces'
import { http } from '@/assets/http'

export default defineComponent({
    props: {
        user: {
            type: Object as () => User,
            required: true
        }
    },
    data() {
        return {
            followed: this.user.is_following,
            notification_on: this.user.notification_on,
            loading: false,
        }
    },
    created() {
        console.log(this.user.notification_on)
    },
    methods: {
        async updateNotificationSettings() {
            if (!this.$store.state.authenticated) {
                return;
            }
            this.loading = true

            await http.put(`follow/follow_user/${this.user.id}/`).then((res) => {
                if (res.data.error) {
                    this.$notify({
                      title: "Error!",
                      text: res.data.message,
                      type: 'negative',
                      group: 'error',
                    })
                    return;
                }
                if(res.data.success) {
                    this.notification_on = res.data.notification_on
                    this.$notify({
                      title: "Success!",
                      text: res.data.message,
                      type: 'success',
                      group: 'success',
                    })
                }
            }).catch((err) => {
                console.log(err);
            });

            this.loading = false
        },
    },
})
</script>

<template >
    <div>
        <Item>
            <template #avatar>
                <q-avatar>
                    <img v-if="user.avatar" :src="user.avatar">
                    <i-profile size="3rem" v-else/>
                </q-avatar>
            </template>
            <template #title>
                <Item dense align-items="start">
                    <template #title>
                        <div class="h-full min-w-full flex gap-1 items-center title">
                            <div class="ellipsis" >
                                <user-card :user-prop="user">
                                    <template #text>
                                        <span class="ellipsis text-lg pointer hover-underline text-heading weight-900" > 
                                            {{ user.first_name}}
                                            {{ user.last_name }}
                                        </span>
                                    </template>
                                </user-card>
                            </div>

                            <span class="h-full" v-if="user.verified">
                                <q-icon class="vert-align-middle "  color="blue" size="1.5rem" name="verified">
                                    <q-tooltip :delay="1000" class="bg-theme box-shadow text-sm">
                                        Verified
                                    </q-tooltip>
                                </q-icon>
                            </span>
                            <span class="h-full " v-if="user.is_admin || user.is_staff">
                                <q-icon class="vert-align-middle " color="green" size="1.5rem" name="admin_panel_settings">
                                    <q-tooltip :delay="1000" class="bg-theme box-shadow text-sm">
                                        Staff
                                    </q-tooltip>
                                </q-icon>
                            </span>
                            <span class="h-full" v-if="user.private">
                                <q-icon class="vert-align-middle "  color="green" size="1.5rem" name="admin_panel_settings">
                                    <q-tooltip :delay="1000" class="bg-theme box-shadow text-sm">
                                        Private
                                    </q-tooltip>
                                </q-icon>
                            </span>
                        </div>
                    </template>
                    <template #caption>
                        <div>
                            <div class="ellipsis">
                                <user-card :user-prop="user">
                                    <template #text>
                                        <span class="text-lg pointer hover-underline text-lighter weight-500">@{{ user.username }}</span>
                                    </template>
                                </user-card>
                            </div>
                        </div>
                    </template>
                    <template #icon>
                        <q-btn round flat dense @click="updateNotificationSettings">
                            <q-icon v-if="notification_on" name="notifications" />
                            <q-icon v-else name="notifications_off" />
                        </q-btn>
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
                                    <q-item clickable v-close-popup @click="persistent = true" tabindex="0" v-if="post.is_owner || post.user.is_admin || post.user.is_staff">
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
        </Item>
    </div>
</template>