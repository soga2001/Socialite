<script lang="ts">
import { http } from '@/assets/http';
import type { User } from '@/assets/interfaces';
import { defineComponent } from 'vue';
import notificationCard from '@/components/Notifications/notificationCard.vue';

export default defineComponent({
    name: 'notification-settings',
    data() {
        return {
            followed_users: Array<User>(),
            loading: true,
            page: 0,
            hasMore: true,
            settings: false,
            allNotifOff: false,
        }
    },
    methods: {
        getFollowedUsers() {
            if(!this.hasMore) {
                return
            }
            this.loading = true;
            http.get(`follow/get_following_users/${this.$store.state.user.username}/`).then((res) => {
                if(res.data.error) {
                    return
                }
                this.loading = false
                this.followed_users = res.data.users
            }).catch((err) => {
                console.log(err)
            })
        },
    },
    computed: {
    },
    created() {
        this.getFollowedUsers()
    },
    mounted() {
    },
    watch: {
    },
    components: {notificationCard}
})

</script>

<template>
    <div>
        <div>
            <header class="sticky top-0 border-b">
                <Item>
                    <template #avatar>
                        <q-btn flat round>
                            <q-icon name="arrow_back" />
                        </q-btn>
                    </template>
                    <template #title>
                        <span class="text-3xl weight-900 text-heading">Notification Settings</span>
                    </template>
                    <template #icon>
                        <q-btn flat round @click="settings = true">
                            <q-icon size="2rem" name="settings" />
                            <q-dialog v-model="settings">
                                <div class="w-full bg-theme box-shadow">
                                    <Item>
                                        <template #title>
                                            <span class="text-3xl weight-900 text-heading">Notification Settings</span>
                                        </template>
                                        <template #icon>
                                            <q-btn flat round @click="settings = false">
                                                <q-icon name="close" />
                                            </q-btn>
                                        </template>
                                    </Item>
                                    <q-separator :dark="$store.state.dark" />
                                    <div>
                                        <Item>
                                            <template #avatar>
                                                <q-toggle v-model="allNotifOff" />
                                            </template>
                                            <template #title>
                                                <span>Turn off all notifications from followed users</span>
                                            </template>
                                        </Item>
                                        <Item>
                                            <template #avatar>
                                                <q-toggle v-model="allNotifOff" />
                                            </template>
                                            <template #title>
                                                <span>Turn off notifications from unverified users</span>
                                            </template>
                                        </Item>
                                        <Item>
                                            <template #avatar>
                                                <q-toggle v-model="allNotifOff" />
                                            </template>
                                            <template #title>
                                                <span>Turn off notifications from verified users</span>
                                            </template>
                                        </Item>
                                    </div>
                                    <q-separator :dark="$store.state.dark" />
                                    <div class="flex w-full p-2">
                                        <button class="border-none ml-auto bg-web-theme weight-900 text-lg rounded px-10 py-2">Save</button>
                                    </div>
                                </div>
                            </q-dialog>
                        </q-btn>
                    </template>
                </Item>
            </header>
            <div class="flex flex-col">
                <div v-for="user in followed_users">
                    <notification-card :user="user" />
                </div>
            </div>
        </div>
    </div>
</template>


<style scoped lang="scss">

</style>