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
                    this.$q.notify({
                        message: `<span class="text-white">${res.data.message}</span>`,
                        color: 'negative',
                        position: 'bottom',
                        timeout: 3000,
                        html: true,
                    })
                    return;
                }
                if(res.data.success) {
                    this.notification_on = res.data.notification_on
                    this.$q.notify({
                        message: `<span class="text-white">${res.data.message}</span>`,
                        color: 'positive',
                        textColor: 'white',
                        position: 'bottom',
                        timeout: 3000,
                        html: true,
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
        <Item clickable :to="{name: 'user-profile', params: { username: user.username } }">
            <template #avatar>
                <q-avatar>
                    <img v-if="user.avatar" :src="user.avatar">
                    <i-profile size="3rem" v-else/>
                </q-avatar>
            </template>
            <template #title>
                <div class="h-full min-w-full flex gap-1 items-center title">
                    <div class="ellipsis" >
                        <span class="ellipsis text-lg text-heading weight-900" > 
                            {{ user.full_name}}
                        </span>
                    </div>

                    <span class="h-full" v-if="user.verified">
                        <q-icon class="vert-align-middle "  color="blue" size="1.5rem" name="verified">
                            <q-tooltip :delay="1000" class="bg-theme text-heading box-shadow text-sm">
                                Verified
                            </q-tooltip>
                        </q-icon>
                    </span>
                    <span class="h-full " v-if="user.is_admin || user.is_staff">
                        <q-icon class="vert-align-middle " color="green" size="1.5rem" name="admin_panel_settings">
                            <q-tooltip :delay="1000" class="bg-theme text-heading box-shadow text-sm">
                                Staff
                            </q-tooltip>
                        </q-icon>
                    </span>
                    <span class="h-full" v-if="user.private">
                        <q-icon class="vert-align-middle "  :color="$store.state.dark ? 'white' : 'black'" size="1.5rem" name="lock">
                            <q-tooltip :delay="1000" class="bg-theme text-heading box-shadow text-sm">
                                Private
                            </q-tooltip>
                        </q-icon>
                    </span>
                </div>
            </template>
            <template #caption>
                <div>
                    <span class="text-lg text-lighter weight-500">@{{ user.username }}</span>
                </div>
            </template>
            <template #icon>
                <q-btn size="1rem" round flat dense @click.stop="updateNotificationSettings">
                    <q-icon v-if="notification_on" name="notifications" />
                    <q-icon v-else name="notifications_off" />
                </q-btn>
            </template>
        </Item>
    </div>
</template>