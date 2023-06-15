<script lang="ts">
import { defineComponent, ref, getCurrentInstance } from 'vue';
import { http } from '@/assets/http';
import UserProfile from '../components/UserProfile/UserProfile.vue';
import type { User } from '@/assets/interfaces';
import Search from './Search.vue';
import UserPosted from '../components/UserProfile/UserPosted.vue';
import UserLiked from '../components/UserProfile/UserLiked.vue';
import Item from '@/components/Item.vue';
import { getParentRouterPath } from '@/assets/parentPath';

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
            docState: 'saved',
        };
    },
    methods: {
        async userInfo() {
            this.loading = true
            console.log('here')
            await http.get(`users/username/${this.$route.params.username}/${false}/`).then((res) => {
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
    watch: {
        '$route'(to, from) {
            if(to.matched[0].name === "user-profile") {
                if(to.params.username != this.username) {
                    this.username = to.params.username
                    this.user = {} as User;
                    this.userInfo();
                }
            }
        }
    },
})
</script>

<template>
    <div :class="'user__main ' + !$store.state.desktop && 'mobile'" v-if="Object.keys(user).length > 0">
        <Item class="user__name pl-2" dense :vert-icon-center="true">
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
                <div class="grid cols-2 text-base border-b bg-theme-soft gap-1 w-full text-center">
                    <RouterLink class="p-2 bg-theme bg-hover" exact-active-class="text-heading weight-900" :to="{name: 'user-posted', params: {username: username}}" exact>
                        Spills
                    </RouterLink>
                    <RouterLink class="p-2 bg-theme bg-hover" exact-active-class="text-heading weight-900" :to="{name: 'user-liked', params: {username: username}}">
                        Likes
                    </RouterLink>
                    <!-- <RouterLink class="p-2 text-lg bg-theme bg-hover" :to="{name: 'comments', params: {username: username}}">
                        Comments
                    </RouterLink> -->
                </div>


                <div class="p-2">
                    <RouterView v-slot="{ Component }">
                        <KeepAlive :max="2" :include="['user-posted', 'user-liked']">
                            <component :is="Component"/>
                        </KeepAlive>
                    </RouterView>
                </div>
            </div>
        </div>
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


a {
    text-decoration: none;
    color: var(--color-text);
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