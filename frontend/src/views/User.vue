<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import UserProfile from '../components/UserProfile/UserProfile.vue';
// import PostsMap from '../HomeViews/PostsMap.vue';
import type { User } from '@/assets/interfaces';
import Search from './Search.vue';
import UserPosted from '../components/UserProfile/UserPosted.vue';
import UserLiked from '../components/UserProfile/UserLiked.vue';
import $j from 'jquery';

export default defineComponent({
    name: 'user-profile',
    data() {
        return {
            // user_id: this.$route.params.id,
            username: this.$route.params.username,
            user: new Array<User>(),
            avatar: '',
            tab: ref('User_Posted'),
            loading: true,
        };
    },
    methods: {
        async userInfo() {
            this.loading = true
            // await http.get(`users/user/${(this.user_id)}/`).then((res) => {
            //     if (res.data.success) {
            //         this.user = res.data.user;
            //         // console.log(res.data.user)

            //         this.avatar = res.data.user[0].profile.avatar || '';
            //     }
            // }).catch((err) => {
            //     console.log(err);
            // });
            // await http.get(`users/username/${(this.username)}/`).then((res) => {
            //     if (res.data.success) {
            //         this.user = res.data.user;
            //         // console.log(res.data.user)

            //         this.avatar = res.data.user[0].profile.avatar || '';
            //     }
            // }).catch((err) => {
            //     console.log(err);
            // });

            await http.get(`users/username/${this.username}/`).then((res) => {
                if (res.data.success) {
                    this.user = res.data.users;
                    this.avatar = this.user[0].profile.avatar || '';
                }
            }).catch((err) => {
                console.log(err);
            });
            
            this.loading = false
        },
    },
    created() {
        // setTimeout(
        //     () => {
        //         this.userInfo();
        //     }, 3000,
        // )
        this.userInfo();

    },
    mounted() {
        // console.log('mounted')
        // this.userInfo();
        $j("#panel").on('scroll', function() {
            console.log('here')
        });
    },
    components: { UserProfile, Search, UserPosted, UserLiked },
})
</script>

<template>
    <div class="user__main" v-if="user.length">
        <div class="user__name">
        <q-icon @click="$router.go(-1)" class="back" name="arrow_back" />
        <span class="name">{{ user[0].first_name + " " + user[0].last_name }}</span>
        </div>
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
                    <q-tab-panel name="User_Posted" class="panel" id="panel">
                        <UserPosted :uid="user[0].id" />
                    </q-tab-panel>
                    <q-tab-panel name="User_Liked" class="panel" id="panel">
                        <UserLiked  />
                    </q-tab-panel>
                </q-tab-panels>
                <!-- <div class="tabs">
                    <RouterLink class="nav__link" :to="{ name: 'user-posted'}">
                        <q-icon size="30px" name="grid_view" class="panel__icon" />
                    </RouterLink>
                    <RouterLink class="nav__link" :to="{ name: 'user-liked'}">
                        <q-icon size="30px" name="favorite" class="panel__icon" />
                    </RouterLink>
                </div>
               
                <RouterView /> -->
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
}

.user__not__found, .loading {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.tabs {
    position: -webkit-sticky;
    position: sticky;
    top: 45px;
    z-index: 900;
    width: 100%;
}

.panel__icon {
    width: 100%;
    z-index: 900;
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
    /* height: 87vh; */
}


.user__name {
    text-align: center;
    position: relative;
    font-size: 30px;
    font-weight: bolder;

    display: relative;
    position: -webkit-sticky;
    position: sticky;
    width: 100%;
    top: 0;
    z-index: 999;
    background-color: var(--color-background);

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