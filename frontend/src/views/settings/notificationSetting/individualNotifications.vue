<script lang="ts">
import { http } from '@/assets/http';
import type { Following, User } from '@/assets/interfaces';
import UserNotificationCard from '@/components/Notifications/userNotificationCard.vue';
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'individual-notif-settings',
    props: {
        scrollPosition: {
            type: Number,
            default: 0,
        },
        height: {
            type: Number,
            default: 0,
        },
    },
    data() {
        return {
            followed_users: Array<Following>(),
            loading: true,
            page: 0,
            hasMore: true,
            userTimeStamp: new Date().toISOString(),

            settings: false,
            allNotifOff: false,
            unverifiedNotifOff: false,
            verifiedNotifOff: false,
        };
    },
    methods: {
        async getFollowedUsers() {
            this.loading = true;
            await http.get(`follow/get_following_users/${this.userTimeStamp}/${this.page}/${this.$store.state.user.username}`).then((res) => {
                if (res.data.error) {
                    return;
                }
                this.followed_users = res.data.users;
            }).catch((err) => {
                console.log(err);
            });
            this.loading = false
        },
    },
    computed: {},
    created() {
        this.getFollowedUsers();
    },
    mounted() {
    },
    watch: {},
    components: { UserNotificationCard }
})

</script>

<template>
    <div>
        <div>
            <header class="sticky top-0 border-b" v-if="!$q.screen.lt.sm">
                <Item dense class="p-1">
                    <template #avatar>
                        <q-btn dense flat round @click="$router.back">
                            <q-icon name="arrow_back" />
                        </q-btn>
                    </template>
                    <template #title>
                        <span class="text-2xl weight-900 text-heading ml-5">Followed Users</span>
                    </template>
                </Item>
            </header>
        </div>
        <div>
            <div v-if="followed_users.length > 0" v-for="users in followed_users">
                <user-notification-card :user="users.followed_user"/>
            </div>
            <div v-else-if="!loading && followed_users.length == 0" class="mt-5">
                <div class="text-center">
                    <span class="text-xl weight-900 text-body">You don't follow any users</span>
                </div>
            </div>
            <div class="p-3" v-if="loading">
                <Loading />
            </div>
        </div>
    </div>
</template>


<style scoped lang="scss">

</style>