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
            headerHeight: '' || 0,
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
                this.headerHeight = headerHeight
            }
        },
    },
    created() {
        this.userInfo();
    },
    computed: {
    },
    activated() {
        if(this.$route.params.username != this.username) {
            this.username = this.$route.params.username
            this.user = {} as User;
            this.websocketClose()
            this.userInfo();
            this.websocketOpen()
        }
    },
    components: { UserProfile, Search, UserPosted, UserLiked, Item },
    watch: {
        // '$route'(to, from) {
        //     if(to.matched[0].name === "user-profile") {
                // if(to.params.username != this.username) {
                //     this.username = to.params.username
                //     this.user = {} as User;
                //     this.websocketClose()
                //     this.userInfo();
                //     this.websocketOpen()
                // }
        //     }
        // }
        // '$route.params.username':function() {
        //     this.username = this.$route.params.username
        //     this.user = {} as User;
        //     this.websocketClose()
        //     this.userInfo();
        //     this.websocketOpen()
        // }
    },
    // beforeRouteUpdate(to, from, next) {
    //     if(to.matched[0].name === "user-profile") {
    //         if(to.params.username != this.username) {
    //             this.username = to.params.username
    //             this.user = {} as User;
    //             this.websocketClose()
    //             this.userInfo();
    //             this.websocketOpen()
    //         }
    //     }
    //     next()
    // },
})
</script>

<template>
    <div :class="'user__main '" v-if="Object.keys(user).length > 0">
        <header ref="header" class="user__name z-5 w-full bg-theme-opacity bg-blur-2">
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
        

        <div ref="profile" >
            <UserProfile :user="user"/>
        </div>

        <div>
            <div>
                <nav :style="{top: `${headerHeight - .4}px`}" class="w-full sticky z-5 m-0 bg-theme-opacity bg-blur-2">
                    <q-tabs
                        class="bg-transparent w-full text-lg text-capitalize border-b"
                        active-class="text-heading"
                    >
                        <q-route-tab class="text-capitalize bg-transparent" active-class="active" :to="{name: 'user-posted', params: {username: username}}" exact replace>
                            <span>Spills</span>
                        </q-route-tab>
                        <q-route-tab class="text-capitalize bg-transparent" active-class="active"  :to="{name: 'user-liked', params: {username: username}}" exact replace>
                            <span>Likes</span>
                        </q-route-tab>
                    </q-tabs>
                </nav>
                <div class="w-full overflow-hidden">
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


<style scoped lang="scss">


.active {
    span {
        color: var(--color-heading);
        font-weight: 900;
    }
}

span {
    color: var(--color-text);
    font-weight: 900;
}


.user__main {
  height: 100%;

  .user__not__found,
  .loading {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
}

a {
  text-decoration: none;
  color: var(--color-text);
}

.user__name {
  font-size: 30px;
  font-weight: bolder;

  display: relative;
  position: -webkit-sticky;
  top: 0px;
  position: sticky;
  width: 100%;
  z-index: 20;
  background-color: var(--color-background);

  .back {
    position: absolute;
    left: 10px;
    top: 0;
    bottom: 0;
    margin: auto;
    cursor: pointer;
  }
}


</style>