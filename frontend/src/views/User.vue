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
            user: new Array<User>(),
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
                    this.user = [res.data.users];
                    this.avatar = this.user[0].avatar || '';
                }
            }).catch((err) => {
                console.log(err);
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
    <div :class="'user__main ' + !$store.state.desktop && 'mobile'" v-if="user.length">
        <!-- <div class="user__name">
            
        </div> -->

        <Item class="user__name">
                <template #avatar>
                    <q-icon @click="$router.go(-1)" class="back" name="arrow_back" />
                </template>
                <template #title>
                    {{ user[0].first_name }} {{ user[0].last_name }}
                </template>
                <template #icon>
                        <!-- <q-icon /> -->
                        <q-btn @click.stop="" size="16px" class="less" flat dense round icon="notifications" />
                        <q-btn @click.stop="" size="16px" class="more__vert" flat dense round icon="more_vert" />
                        <!-- <q-menu class="dropdown" v-model="dropdown" transition-show="jump-down" transition-hide="jump-up" self="top middle">
                            <q-list class="more__option">
                                <q-item clickable v-close-popup @click="report = true" v-if="username !== $store.state.user.username">
                                    <q-item-section avatar>
                                        <q-icon class="danger__icon" name="flag"/>
                                    </q-item-section>
                                    <q-item-section>
                                        <q-item-label>Report Post</q-item-label>
                                    </q-item-section>
                                </q-item>
                                <q-item clickable v-close-popup @click="persistent = true" tabindex="0" v-if="username === $store.state.user.username">
                                    <q-item-section avatar>
                                        <q-icon class="danger__icon" name="delete_forever"/>
                                    </q-item-section>
                                    <q-item-section>
                                        <q-item-label>Delete</q-item-label>
                                    </q-item-section>
                                </q-item>
                                <q-item clickable v-close-popup v-if="username === $store.state.user.username">
                                    <q-item-section avatar>
                                        <q-icon class="" name="edit_note"/>
                                    </q-item-section>
                                    <q-item-section>
                                        <q-item-label>Edit</q-item-label>
                                    </q-item-section>
                                </q-item>
                            </q-list>
                        </q-menu> -->
                        <!-- Confirm Delete Model -->
                        <!-- <q-dialog v-model="persistent" persistent transition-show="scale" transition-hide="scale">
                            <q-card class="card">
                                <q-card-section class="row">
                                    <q-item>
                                        <q-item-section class="title">Are you sure you want to delete this post?</q-item-section>
                                    </q-item>
                                </q-card-section>
                                <q-card-section>
                                    <q-item>
                                        <q-item-section avatar>
                                        <q-avatar class="red" icon="warning"/>
                                        </q-item-section>
                                        <q-item-section class="red alert">This action is permanent and irreversible.</q-item-section>
                                    </q-item>
                                </q-card-section>

                                <q-card-actions align="right" class="buttons">
                                    <q-btn flat label="Cancel"  v-close-popup />
                                    <q-btn flat label="Confirm" @click="deletePost" v-close-popup />
                                </q-card-actions>
                            </q-card>
                        </q-dialog> -->
                        <!-- Report model -->
                        <!-- <q-dialog v-model="report" persistent>
                            <q-card class="card">
                                <q-card-section>
                                    <h6 class="title">Report</h6>
                                    <q-item>
                                        <q-item-section class="title">Report</q-item-section>
                                        <q-item-section avatar>
                                        <q-avatar class="red" icon="flag"/>
                                        </q-item-section>
                                    </q-item>
                                </q-card-section>
                                <q-card-section class="q-pt-none">
                                    <q-input :dark="$store.state.dark" class="report__reason" placeholder="Reason" dense v-model="reason" />
                                    <q-input
                                        v-model="reason"
                                        filled
                                        clearable
                                        type="textarea"
                                        label="Reason"
                                        :dark="$store.state.dark"                                
                                    />
                                </q-card-section>

                                <q-card-actions align="right" class="buttons">
                                    <q-btn flat label="Cancel" v-close-popup />
                                    <q-btn flat label="Report" v-close-popup @click="reportPost" />
                                </q-card-actions>
                            </q-card>
                        </q-dialog> -->
                    </template>
        </Item>
        
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