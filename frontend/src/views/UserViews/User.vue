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
                    this.avatar = res.data.user[0].profile.avatar
                    console.log(this.user)
                }
            }).catch((err) => {
                console.log(err);
            });
        }
    },
    created() {
        this.userInfo();
    },
    components: { UserProfile, PostsMap, Search, UserPosted, UserLiked }
})
</script>

<template>
    <div v-for="u in user">
        <UserProfile :user="u"/>
    </div>
    <div>
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
            <!-- <div v-if="$store.state.posts_main" v-for="post in $store.state.posts_main" :key="post.id">
                <PostsMap :post="post" />
            </div> -->
            <UserPosted :user_avatar="avatar" />
          </q-tab-panel>

          <q-tab-panel name="likes" class="panel">
            <!-- <div v-if="$store.state.posts_main" v-for="post in $store.state.posts_main" :key="post.id">
                <PostsMap :post="post" />
            </div> -->
            <UserLiked :user_avatar="avatar"/>
          </q-tab-panel>
        </q-tab-panels>
    </div>
</template>


<style scoped>
.tabs {
    position: -webkit-sticky;
    position: sticky;
    top: 0;
    z-index: 999;
    background-color: var(--color-background-mute);
    display: flex;
    width: 100%;
}

.tabs .active {
    color: var(--color-heading);
    background-color: var(--color-background);
    /* background-color: black !important; */
}

.panels {
    background-color: transparent;
    display: flex;
    justify-content: center;
}
</style>