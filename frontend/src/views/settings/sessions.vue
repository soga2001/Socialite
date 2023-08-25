<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import type { Sessions } from '@/assets/interfaces';

export default defineComponent({
    data() {
        return {
            loading: true,
            sessions: new Array<Sessions>(),
        }
    },
    created() {
        this.getAllSessions()
    },
    methods: {
        async getAllSessions() {
            this.loading = true
            await http.get('users/user_sessions/').then((res) => {
                console.log(res.data)
                if(res.data.success) {
                    this.sessions = res.data.sessions
                }
            }).catch((err) => {

            })
            this.loading = false
        },
        deleteSession(key: String) {
            http.delete(`users/delete_session/`, {
                params: {
                    session_id: key
                }
            }).then((res) => {
                if(res.data.success) {
                    if(res.data.current_session) {
                        this.$store.commit("authenticate", false);
                        this.$store.commit("setDefaultUser");
                    }
                    this.$q.notify( {
                        message: `<span class="text-white">${res.data.message}</span>`,
                        color: 'positive',
                        icon: 'check',
                        iconColor: 'white',
                        position: 'top',
                        timeout: 2500,
                        html: true,
                    })
                }
            })
        },
        deleteAllSessions() {
            if(this.sessions.length > 1)
            http.delete('users/user_sessions/').then((res) => {
                console.log(res.data)
                if(res.data.success) {
                    this.getAllSessions()
                }
            })
        }
    }
})

</script>

<template>
    <div>
        <div>
            <header>
                <Item>
                    <template #avatar>
                        <q-btn flat round @click="$router.back">
                            <q-icon name="arrow_back" />
                        </q-btn>
                    </template>
                    <template #title>
                        <span class="text-3xl weight-900 text-heading">
                            Sessions
                        </span>
                    </template>
                </Item>
            </header>
            <div v-if="!loading">
                <div  class="px-3 py-1 flex flex-col gap-3">
                    <div>
                        <span>
                            Sessions are the devices you are using or that have used your Socialite account. These are the sessions where your account is currently logged in. You can log out of each session.
                        </span>
                    </div>
                    <div class="flex flex-col gap-3">
                        <div class="text-heading text-lg weight-900">
                            Current active session
                        </div>
                        <div>
                            You’re logged into this Socialite account on this device and are currently using it.
                        </div>
                        <div v-if="sessions" v-for="session in sessions">
                            <Item v-if="session.current_session">
                                <template #avatar>
                                    <q-icon size="2.5rem" name="devices" />
                                </template>
                                <template #title>
                                    <span class="text-heading text-lg weight-900">
                                        Current Session
                                    </span>
                                </template>
                                <template #caption>
                                    <span class="text-body text-sm weight-700">
                                        {{ session.ip }}
                                    </span>
                                    <Timeago html :date="session.last_activity" />
                                </template>
                            </Item>
                        </div>
                    </div>
                </div>
                <q-separator :dark="$store.state.dark" />
                <div>
                    <div class="px-3 py-1 flex flex-col gap-3">
                        <div class="text-heading text-lg weight-900">
                            Log out of other sessions
                        </div>
                        <div>
                            <!-- These are the devices you’ve used to log into your Socalite account in the past 30 days. They’re listed by device type, such as computer or iPhone. -->
                            You’re logged into these accounts and aren’t currently using them. 
                        </div>
                        <div>
                            Logging out will end {{ sessions.length - 1 }} of your other active Socialite sessions. It won’t affect your current active session.
                        </div>
                    </div>
                    <button @click="deleteAllSessions" class="bg-transparent border-none text-left text-red weight-900 py-5 bg-hover-soft pointer w-full">
                        Log out of all other sessions
                    </button>
                    <div v-if="sessions" v-for="session in sessions">
                        <Item v-if="!session.current_session">
                            <template #avatar>
                                <q-avatar>
                                    <q-icon name="devices" />
                                </q-avatar>
                            </template>
                            <template #title>
                                <span v-if="session.current_session" class="text-heading text-lg weight-900">
                                    Current Session
                                </span>
                            </template>
                            <template #caption>
                                <span class="text-body text-sm weight-700">
                                    {{ session.ip }}
                                </span>
                                <Timeago html :date="session.last_activity" />
                            </template>
                            <template #icon>
                                <q-btn v-if="!session.current_session" flat round dense icon="delete" @click="deleteSession(session.session_key)">
                                    <q-tooltip :delay="500">
                                        Delete session
                                    </q-tooltip>
                                </q-btn>
                            </template>
                        </Item>
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

</style>