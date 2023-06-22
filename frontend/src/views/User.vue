<script lang="ts">
import { defineComponent, ref, getCurrentInstance } from 'vue';
import { http } from '@/assets/http';
import UserProfile from '../components/UserProfile/UserProfile.vue';
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
            docState: 'saved',
            websocket: new WebSocket(`wss://localhost:8000/ws/user_consumer/${this.$route.params.username}/`),
            headerHeight: '',
        };
    },
    methods: {
        async userInfo() {
            this.loading = true
            console.log('here')
            await http.get(`users/username/${this.$route.params.username}/${false}/`).then(async (res) => {
                if (res.data.success) {
                    this.user = res.data.users;
                    this.avatar = this.user.avatar || '';
                }
            }).catch((err) => {
                // console.log(err);
            });
            await this.getHeightOfHeader()
            console.log(this.headerHeight)
            this.loading = false
        },
        async websocketOpen() {
            this.websocket = new WebSocket(`wss://localhost:8000/ws/user_consumer/${this.$route.params.username}/`)
        },
        async websocketClose() {
            this.websocket.close()

            this.websocket.onclose = (e) => {
                console.log('Websocket closed')
            }
        },
        getHeightOfHeader() {
            if (this.$refs.header) {
                const headerElement: HTMLDivElement = this.$refs.header as HTMLDivElement;
                const headerHeight = headerElement.offsetHeight;
                this.headerHeight = headerHeight + 'px'
            }
        },
    },
    created() {
        this.userInfo();
    },
    computed: {
    },
    components: { UserProfile, Search, UserPosted, UserLiked, Item },
    watch: {
        '$route'(to, from) {
            if(to.matched[0].name === "user-profile") {
                if(to.params.username != this.username) {
                    this.username = to.params.username
                    this.user = {} as User;
                    this.websocketClose()
                    this.userInfo();
                    this.websocketOpen()
                }
            }
        }
    },
})
</script>

<template>
    <div :class="'user__main ' + !$store.state.desktop && 'mobile'" v-if="Object.keys(user).length > 0">
        <header ref="header" class="user__name">
            <Item class="pl-2" dense :vert-icon-center="true">
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
        </header>
        

        <div v-if="Object.keys(user).length > 0" >
            <UserProfile :user="user"/>
        </div>
        <div class="">
            <div class="">                
                <div :style="{top: headerHeight}" class="sticky z-5 grid cols-2 text-xl bg-theme w-full text-center relative">
                    <RouterLink class="h-full p-2 bg-theme bg-hover relative" exact-active-class="text-heading weight-900 link" :to="{name: 'user-posted', params: {username: username}}" exact>
                        Spills
                    </RouterLink>
                    <RouterLink class="h-full p-2 bg-theme bg-hover relative" exact-active-class="text-heading weight-900 link" :to="{name: 'user-liked', params: {username: username}}">
                        Likes
                    </RouterLink>
                </div>
                <div class="p-2 w-full overflow-hidden">
                    <RouterView v-slot="{ Component }">
                        <KeepAlive :max="2" :include="['user-posted', 'user-liked']">
                            <component :is="Component" :websocket="websocket"/>
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


.link:after {
    content: '';
    display: flex;
    width: 100px;
    margin: 0 auto;
    border: 2px solid rgb(253, 137, 137);
    bottom: 0;
}

</style>