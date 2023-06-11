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
        console.log('here')
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
                    <q-btn size="16px" @click="$router.back" flat dense round class="text-heading" icon="arrow_back" />
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
                <div class="grid cols-2 w-full text-center border">
                    <RouterLink class="border-r p-2" exact-active-class="text-heading weight-900 bg-theme-mute" :to="{name: 'user-posted', params: {username: username}}" exact replace>
                        Spills
                    </RouterLink>
                    <RouterLink class=" p-2" exact-active-class="text-heading weight-900 bg-theme-mute" :to="{name: 'user-liked', params: {username: username}}" exact replace>
                        Likes
                    </RouterLink>
                </div>


                <div class="p-2">
                    <RouterView v-slot="{ Component }">
                        <KeepAlive :max="2" :include="['user-posted', 'user-liked']">
                            <component :is="Component" :key="$route.fullPath" />
                        </KeepAlive>
                    </RouterView>
                </div>
                

                <!-- <q-tab-panels :keep-alive="true" :keep-alive-include="['User_Posted', 'User_Liked']"  :keep-alive-max="5" v-model="tab" class="panels text-heading" swipeable>
                    <q-tab-panel name="User_Posted" class="panel" id="panel">
                        <UserPosted :uid="user.id" />
                    </q-tab-panel>
                    <q-tab-panel name="User_Liked" class="panel" id="panel">
                        <UserLiked  />
                    </q-tab-panel>
                </q-tab-panels> -->
            </div>
        </div>
    </div>
    <!-- <div v-if="!loading && user.length == 0" class="user__not__found">
        <div class="">
            <div class="text-h2">User not found</div>
        </div>
    </div>
    <div v-if="loading" class="loading">
        <q-spinner :thickness="10" size="100px" />
    </div> -->
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


a {
    text-decoration: none;
    color: var(--color-text);
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