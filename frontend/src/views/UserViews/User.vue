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
            tab: ref('User_Posted')
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
        <div class="">
            <div class="">
                <q-tabs
                v-model="tab"
                inline-label
                outside-arrows
                mobile-arrows
                class="tabs"
                active-class="active"
                >
                <q-tab name="User_Posted" icon="grid_view" class="panel__icon">
                    <q-tooltip anchor="top middle" self="bottom middle" :offset="[10, 10]">User Posted</q-tooltip>
                </q-tab>
                <q-tab name="User_Liked" icon="favorite" class="panel__icon">
                    <q-tooltip anchor="top middle" self="bottom middle" :offset="[10, 10]">User Liked</q-tooltip>
                </q-tab>
                </q-tabs>

                <q-tab-panels :keep-alive="true" :keep-alive-include="['User_Posted', 'User_Liked']"  :keep-alive-max="5" v-model="tab" class="panels" swipeable>
                    <q-tab-panel name="User_Posted" class="panel">
                        <UserPosted :user_avatar="avatar" />
                    </q-tab-panel>
                    <q-tab-panel name="User_Liked" class="panel">
                        <UserLiked :user_avatar="avatar"/>
                    </q-tab-panel>
                </q-tab-panels>
            </div>
        </div>
    </div>
</template>


<style scoped>

.user__main {
    height: 100%;
}
.tabs {
    position: -webkit-sticky;
    position: sticky;
    top: 0;
    z-index: 999;
    width: 100%;
}

.panel__icon {
    width: 100%;
    z-index: 999;
    border-bottom: 1px solid var(--color-border);
}

.tabs {
    background-color: var(--color-background);
}

.active {
    color: var(--color-heading);
}

.panels {
    background-color: transparent;
}


.panel {
    padding: 10px;
    height: 95vh;
    /* height: 100%; */
}
</style>