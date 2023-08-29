<script lang="ts">
import { http } from '@/assets/http';
import type { Following, User } from '@/assets/interfaces';
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'notification-settings',
    data() {
        return {
            followed_users: Array<Following>(),
            loading: true,
            page: 0,
            hasMore: true,
            settings: false,
            allNotifOff: false,
            unverifiedNotifOff: false,
            verifiedNotifOff: false,
            likesNotif: false,
            commentsNotif: false,
        }
    },
    methods: {
    },
    computed: {
    },
    created() {
    },
    mounted() {
    },
    watch: {
    },
})

</script>

<template>
    <div>
        <div>
            <header class="sticky top-0 border-b bg-theme-opacity bg-blur-half z-10" v-if="!$q.screen.lt.sm">
                <Item>
                    <template v-if="$q.screen.lt.sm" #avatar>
                        <q-btn flat round  @click="$router.back">
                            <q-icon name="arrow_back" />
                        </q-btn>
                    </template>
                    <template #title>
                        <span class="text-2xl weight-900 text-heading ml-5">Notification Settings</span>
                    </template>
                </Item>
            </header>
            <div>
                <div class="w-full">
                    <div>
                        <Item :titleLineClamp="2">
                            <template #avatar>
                                <q-toggle size="2.5rem" :icon-color="$store.state.dark ? 'black' : 'white'" :dark="$store.state.dark" checked-icon="notifications_off" unchecked-icon="notifications" v-model="allNotifOff" />
                            </template>
                            <template #title>
                                <span class="text-heading weight-700 text-lg">Disable notifications from followed users</span>
                            </template>
                        </Item>
                        <Item :titleLineClamp="2">
                            <template #avatar>
                                <q-toggle size="2.5rem" :icon-color="$store.state.dark ? 'black' : 'white'" :dark="$store.state.dark" checked-icon="notifications_off" unchecked-icon="notifications" v-model="unverifiedNotifOff" />
                            </template>
                            <template #title>
                                <span class="text-heading weight-700 text-lg">Disable notifications from unverified users</span>
                            </template>
                        </Item>
                        <Item :titleLineClamp="2">
                            <template #avatar>
                                <q-toggle size="2.5rem" :icon-color="$store.state.dark ? 'black' : 'white'" :dark="$store.state.dark" checked-icon="notifications_off" unchecked-icon="notifications" v-model="verifiedNotifOff" />
                            </template>
                            <template #title>
                                <span class="text-heading weight-700 text-lg">Disable notifications from verified users</span>
                            </template>
                        </Item>
                        <Item :titleLineClamp="2">
                            <template #avatar>
                                <q-toggle size="2.5rem" :icon-color="$store.state.dark ? 'black' : 'white'" :dark="$store.state.dark" checked-icon="notifications_off" unchecked-icon="notifications" v-model="likesNotif" />
                            </template>
                            <template #title>
                                <span class="text-heading weight-700 text-lg">Disable notifications for likes on your spills</span>
                            </template>
                        </Item>
                        <Item :titleLineClamp="2">
                            <template #avatar>
                                <q-toggle size="2.5rem" :icon-color="$store.state.dark ? 'black' : 'white'" :dark="$store.state.dark" checked-icon="notifications_off" unchecked-icon="notifications" v-model="commentsNotif" />
                            </template>
                            <template #title>
                                <span class="text-heading weight-700 text-lg">Disable notifications for comments on your spills</span>
                            </template>
                        </Item>
                    </div>
                    <div class="flex w-full p-2">
                        <button class="border-brighter-2 ml-auto bg-transparent bg-hover-mute text-heading pointer weight-900 text-lg rounded px-12 py-1">Coming Soon</button>
                    </div>
                    <q-separator :dark="$store.state.dark"/>
                    <div class="flex flex-col gap-2 w-full p-2">
                        <div class="text-heading weight-900 text-base">
                            Notificaitons Users aren't able to turn off
                        </div>
                        <ul>
                            <li>Notifications from Socialite</li>
                            <li>Notifications from user follow requests</li>
                            <li>Notifications from user mentions</li>
                        </ul>
                    </div>
                    <q-separator :dark="$store.state.dark"/>
                    
                </div>
            </div>
        </div>
        <div>
            <RouterLink :to="{name: 'individual-notif-settings'}" active-class="active" class="no-decor">
                <Item clickable class="child" :captionLineClamp="2">
                    <template #avatar>
                        <q-icon size="2rem" name="notifications_off" />
                    </template>
                    <template #title>
                        <span class="text-xl text-heading weight-800 text-capitalize">
                            Specific User Notifications
                        </span>
                    </template>
                    <template #caption>
                        <span class="text-sm text-body weight-700 text-nodecor">
                            Turn off notifications from specific users you follow
                        </span>
                    </template>
                    <template #icon>
                        <q-icon size="2rem" name="navigate_next" class="text-heading"/>
                    </template>
                </Item>
            </RouterLink>
        </div>
    </div>
</template>


<style scoped lang="scss">

</style>