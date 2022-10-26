<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import UserMap from './UserMap.vue';
import PostsMap from '../HomeViews/PostsMap.vue';
import type { User } from '@/assets/interfaces';

export default defineComponent({
    data() {
        return {
            user_id: this.$route.params.id,
            user: new Array<User>(),
            tab: ref('posts')
        };
    },
    methods: {
        userInfo() {
            http.get(`users/user/${(this.user_id)}/`).then((res) => {
                if (res.data.success) {
                    this.user = res.data.user;
                }
            }).catch((err) => {
                console.log(err);
            });
        }
    },
    created() {
        this.userInfo();
    },
    components: { UserMap, PostsMap }
})
</script>

<template>
    <div v-for="u in user">
        <UserMap :user="u"/>
    </div>
    <div>
        <q-tabs
        v-model="tab"
        inline-label
        outside-arrows
        mobile-arrows
        class="tabs"
      >
        <q-tab name="posts" icon="grid_view" class="panel__icon">
            <q-tooltip anchor="top middle" self="bottom middle" :offset="[10, 10]">User Posted</q-tooltip>
        </q-tab>
        <q-tab name="alarms" icon="favorite" class="panel__icon">
            <q-tooltip anchor="top middle" self="bottom middle" :offset="[10, 10]">User Liked</q-tooltip>
        </q-tab>
      </q-tabs>

      <q-tab-panels keep-alive :keep-alive-max="2" v-model="tab" animated class="panels" swipeable>
          <q-tab-panel name="posts" class="panel">
            <div v-if="$store.state.posts_main" v-for="post in $store.state.posts_main" :key="post.id">
                <PostsMap :post="post" />
            </div>
          </q-tab-panel>

          <q-tab-panel name="alarms" class="panel">
            <div v-if="$store.state.posts_main" v-for="post in $store.state.posts_main" :key="post.id">
                <PostsMap :post="post" />
            </div>
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
}

.panels {
    background-color: transparent;
}
</style>