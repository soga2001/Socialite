<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import UserProfile from '../components/UserProfile/UserProfile.vue';
// import PostsMap from '../HomeViews/PostsMap.vue';
import type { User } from '@/assets/interfaces';
import Search from './Search.vue';
import UserPosted from '../components/UserProfile/UserPosted.vue';
import UserLiked from '../components/UserProfile/UserLiked.vue';
import Item from '@/components/Item.vue';

export default defineComponent({
    name: 'user-profile',
    data() {
        return {
            // user_id: this.$route.params.id,
            username: this.$route.params.username,
            user: {} as User,
            avatar: '',
            tab: ref('User_Posted'),
            loading: true,
        };
    },
    methods: {
        async userInfo() {
            this.loading = true

            await http.get(`users/username/${this.username}/${false}/`).then((res) => {
                if (res.data.success) {
                    this.user = res.data.users;
                    this.avatar = this.user.avatar || '';
                }
            }).catch((err) => {
                // console.log(err);
            });
            
            this.loading = false
        },
    },
    created() {
        this.userInfo();

    },
    mounted() {
    },
    components: { UserProfile, Search, UserPosted, UserLiked, Item },
})
</script>

<template>
    <div :class="'user__main ' + !$store.state.desktop && 'mobile'" v-if="Object.keys(user).length > 0">
        <Item class="user__name" dense :vert-icon-center="true">
                <template #avatar>
                    <q-btn size="16px" @click="$router.go(-1)" flat dense round class="text-heading" icon="arrow_back" />
                </template>
                <template #title>
                    <h5 className="text-left">{{ user.first_name }} {{ user.last_name }}</h5>
                </template>
                <template #caption>
                    <div class="text-left">{{ user.total_posted }} Spills</div>
                </template>
        </Item>
        
        <div v-if="Object.keys(user).length > 0" >
            <UserProfile :user="user"/>
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
                <q-tab name="User_Posted" icon="grid_view" class="panel__icon text-body">
                    <q-tooltip anchor="top middle" self="bottom middle" :offset="[10, 10]">User Posted</q-tooltip>
                </q-tab>
                <q-tab name="User_Liked" icon="favorite" class="panel__icon text-body">
                    <q-tooltip anchor="top middle" self="bottom middle" :offset="[10, 10]">User Liked</q-tooltip>
                </q-tab>
                </q-tabs>

                <q-tab-panels :keep-alive="true" :keep-alive-include="['User_Posted', 'User_Liked']"  :keep-alive-max="5" v-model="tab" class="panels text-heading" swipeable>
                    <q-tab-panel name="User_Posted" class="panel" id="panel">
                        <UserPosted :uid="user.id" />
                    </q-tab-panel>
                    <q-tab-panel name="User_Liked" class="panel" id="panel">
                        <UserLiked  />
                    </q-tab-panel>
                </q-tab-panels>
            </div>
        </div>
    </div>
    <div v-if="!loading && user.length == 0" class="user__not__found">
        <div class="">
            <div class="text-h2">User not found</div>
        </div>
    </div>
    <div v-if="loading" class="loading">
        <q-spinner :thickness="10" size="100px" />
    </div>
</template>


<style scoped>

.user__main {
    height: 100%;
    padding: 0;
}

.mobile {
    margin-bottom: 70px;
}

.user__not__found, .loading {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.tabs {
    position: -webkit-sticky;
    position: sticky;
    top: 45px;
    z-index: 1;
    width: 100%;
}

.panel__icon {
    width: 100%;
    z-index: 1;
    border-bottom: 1px solid var(--color-border);
}

.tabs {
    background-color: var(--color-background);
}

.active {
    color: var(--color-heading) !important;
}

.panels {
    background-color: transparent;
    width: 100%;
}


.panel {
    padding: 10px;
    /* height: 87vh; */
}


.user__name {
    text-align: center;
    position: relative;
    font-size: 30px;
    font-weight: bolder;

    display: relative;
    position: -webkit-sticky;
    top: 0px;
    position: sticky;
    width: 100%;
    z-index: 20;
    background-color: var(--color-background);
    /* backdrop-filter: blur(50px); */

}

.back {
    position: absolute;
    left: 10px;
    top: 0;
    bottom: 0;
    margin: auto;
    cursor: pointer;
}

</style>