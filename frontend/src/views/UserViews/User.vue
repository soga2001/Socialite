<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import UserProfile from './UserProfile.vue';
import PostsMap from '../HomeViews/PostsMap.vue';
import type { User } from '@/assets/interfaces';
import Search from '../Search/Search.vue';
import UserPosted from './UserPosted.vue';
import UserLiked from './UserLiked.vue';

export default defineComponent({
    name: 'User',
    data() {
        return {
            user_id: this.$route.query.id,
            user: new Array<User>(),
            avatar: '',
            tab: ref('posts')
        };
    },
    methods: {
        userInfo() {
            http.get(`users/user/${(this.user_id)}/`).then((res) => {
                if (res.data.success) {
                    this.user = res.data.user;
                    this.avatar = res.data.user[0].profile.avatar || '';
                }
            }).catch((err) => {
                console.log(err);
            });
        },
    },
    created() {
        this.userInfo();
    },
    components: { UserProfile, PostsMap, Search, UserPosted, UserLiked },
})
</script>

<template>
    <div class="user__main">
        <div v-for="u in user">
            <UserProfile :user="u"/>
        </div>
        <div class="row">
            <div class="col-12 col-md-3">

            </div>
            <div class="col-12 col-md-6">
                <q-tabs
                v-model="tab"
                inline-label
                outside-arrows
                mobile-arrows
                class="tabs"
                active-class="active"
                >
                <q-tab name="posts" icon="grid_view" class="panel__icon">
                    <q-tooltip anchor="top middle" self="bottom middle" :offset="[10, 10]">User Posted</q-tooltip>
                </q-tab>
                <q-tab name="likes" icon="favorite" class="panel__icon">
                    <q-tooltip anchor="top middle" self="bottom middle" :offset="[10, 10]">User Liked</q-tooltip>
                </q-tab>
                </q-tabs>

                <q-tab-panels keep-alive :keep-alive-max="2" v-model="tab" animated class="panels" swipeable>
                    <q-tab-panel name="posts" class="panel">
                        <UserPosted :user_avatar="avatar" />
                    </q-tab-panel>

                    <q-tab-panel name="likes" class="panel">
                        <UserLiked :user_avatar="avatar"/>
                    </q-tab-panel>
                </q-tab-panels>
            </div>
            <div class="col-12 col-md-3">

            </div>
        </div>
    </div>
</template>


<style scoped>
.tabs {
    position: -webkit-sticky;
    position: sticky;
    top: 51px;
    z-index: 999;
    width: 100%;
}

.panel__icon {
    width: 100%;
    z-index: 999;
}

.tabs .active {
    color: var(--color-heading);
    background-color: var(--color-background-soft);
}

.panels {
    background-color: transparent;
    /* min-height: 87vh; */
    height: 100%;
}

</style>