<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import type { Sessions } from '@/assets/interfaces';

export default defineComponent({
    name: 'sessions',
    data() {
        return {
            loading: true,
            sessions: new Array<Sessions>(),

            mobile: ['Android','iPhone', 'Windows Phone'],
        }
    },
    created() {
        this.getAllSessions()
    },
    methods: {
        async getAllSessions() {
            this.loading = true
            await http.get('users/user_sessions/').then((res) => {
                if(res.data.success) {
                    this.sessions = res.data.sessions
                }
            }).catch((err) => {

            })
            this.loading = false
        },
        deleteAllSessions() {
            if(this.sessions.length > 1)
            http.delete('users/user_sessions/').then((res) => {
                if(res.data.success) {
                    this.sessions = this.sessions.filter((session) => {
                        return session.current_session
                    })
                }
            })
        }
    }
})

</script>

<template>
    <div class="relative">
        <div>
            <header v-if="!$q.screen.lt.sm">
                <Item >
                    <template #avatar v-if="$q.screen.lt.sm">
                        <q-btn flat round @click="$router.back">
                            <q-icon name="arrow_back" />
                        </q-btn>
                    </template>
                    <template #title>
                        <span class="text-2xl weight-900 text-heading ml-5">
                            Sessions
                        </span>
                    </template>
                </Item>
            </header>
            <div v-if="!loading">
                <div  class="py-1 flex flex-col gap-3">
                    <div class="px-3">
                        <span>
                            Sessions are the devices you are using or that have used your Socialite account. These are the sessions where your account is currently logged in. You can log out of each session.
                        </span>
                    </div>
                    <div class="flex flex-col gap-3">
                        <div class="text-heading text-lg weight-900 px-3">
                            Current active session
                        </div>
                        <div class="px-3 text-base">
                            You’re logged into this Socialite account on this device and are currently using it.
                        </div>
                        <div v-if="sessions" v-for="session in sessions">
                            <RouterLink :to="{name: 'session', params: {key: session.session_key} }" active-class="active" class="no-decor pointer bg-hover-soft">
                                <Item clickable v-if="session.current_session">
                                    <template #avatar>
                                        <div class="p-2 border">
                                            <q-icon :color="$store.state.dark ? 'white' : 'black'" v-if="['Mobile', 'Android', 'iPhone'].includes(session.device)" size="2rem" name="smartphone" />
                                            <q-icon :color="$store.state.dark ? 'white' : 'black' " v-else-if="['iPad'].includes(session.device)" size="2rem" name="tablet" />
                                            <q-icon :color="$store.state.dark ? 'white' : 'black' " v-else size="2rem" name="computer" />
                                        </div>
                                    </template>
                                    <template #title>
                                        <span class="text-heading text-lg weight-900 flex flex-row gap-3 items-center">
                                            {{ session.device }}
                                            <span class="text-xs text-heading bg-web-theme px-3 py-1 rounded">Active Now</span>
                                        </span>
                                    </template>
                                    <template #caption>
                                        <span class="text-body text-sm weight-700 flex flex-row gap-2 items-center">
                                            <div class="flex flex-row gap-2 items-center" v-if="session.location">
                                                <span class="text-sm text-heading" v-if="session.location.city">
                                                    {{ session.location.city }} {{ session.location.region && ',' }}
                                                </span>
                                                <span v-if="session.location.region">
                                                    {{ session.location.region }}
                                                </span>
                                                <span v-if="!session.location.region || !session.location.city">
                                                    {{ session.location.country_name }}
                                                </span>
                                                <span class="text-base weight-900 text-heading" v-if="session.location.city || session.location.region">
                                                    &#183;
                                                </span>
                                            </div>
                                            <Timeago spanClass="weight-900 text-heading" class="text-sm text-heading" html :date="session.last_activity" />
                                        </span>
                                    </template>
                                    <template #icon>
                                        <q-icon size="2rem" name="navigate_next" class="text-heading"/>
                                    </template>
                                </Item>
                            </RouterLink>
                        </div>
                    </div>
                </div>
                <q-separator :dark="$store.state.dark" />
                <div>
                    <div class="p-3 flex flex-col gap-3">
                        <div class="text-heading text-lg weight-900">
                            Log out of other sessions
                        </div>
                        <div>
                            <!-- These are the devices you’ve used to log into your Socalite account in the past 30 days. They’re listed by device type, such as computer or iPhone. -->
                            You’re logged into these accounts and aren’t currently using them. 
                        </div>
                        <div v-if="sessions.length > 1">
                            Logging out will end {{ sessions.length - 1 }} of your other active Socialite sessions. It won’t affect your current active session.
                        </div>
                        <div v-else>
                            You don't have any other active sessions.
                        </div>
                    </div>
                    <button @click="deleteAllSessions" class="delete-btn bg-transparent border-none text text-red weight-900 py-3 px-2 bg-hover-soft pointer w-full text-xl">
                        Log out of all other sessions
                    </button>
                    <div v-if="sessions" v-for="session in sessions">
                        <RouterLink :to="{name: 'session', params: {key: session.session_key} }" active-class="active" class="no-decor bg-hover-soft pointer">
                            <Item clickable v-if="!session.current_session">
                                <template #avatar>
                                    <div class="p-2 border">
                                        <q-icon :color="$store.state.dark ? 'white' : 'black'" v-if="mobile.includes(session.device)" size="2rem" name="smartphone" />
                                        <q-icon :color="$store.state.dark ? 'white' : 'black' " v-else-if="['iPad'].includes(session.device)" size="2rem" name="tablet" />
                                        <q-icon :color="$store.state.dark ? 'white' : 'black' " v-else size="2rem" name="computer" />
                                    </div>
                                </template>
                                <template #title>
                                    <span class="text-heading text-lg weight-900">
                                        {{ session.device ?? 'Unknown' }}
                                    </span>
                                </template>
                                <template #caption>
                                    <span class="text-body text-sm weight-700 flex flex-row gap-2 items-center">
                                        <div class="flex flex-row gap-2 items-center" v-if="session.location">
                                            <span class="text-sm text-heading" v-if="session.location.city">
                                                {{ session.location.city }} {{ session.location.region && ',' }}
                                            </span>
                                            <span v-if="session.location.region">
                                                {{ session.location.region }}
                                            </span>
                                            <span v-if="!session.location.region || !session.location.city">
                                                {{ session.location.country_name }}
                                            </span>
                                            <span class="text-base weight-900 text-heading" v-if="session.location.city || session.location.region">
                                                &#183;
                                            </span>
                                        </div>
                                        
                                       
                                        <Timeago spanClass="weight-900 text-heading" class="text-heading text-sm" html :date="session.last_activity" />
                                    </span>
                                </template>
                                <template #icon>
                                    <q-icon size="2rem" name="navigate_next" class="text-heading"/>
                                </template>
                            </Item>
                        </RouterLink>
                    </div>
                </div>
            </div>
            <div v-else>
                <Loading />
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss" >
.delete-btn {
    
    &:hover {
        background-color: rgba(255, 0, 0, 0.1) !important;
    }
}
</style>