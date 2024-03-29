<script lang="ts">

import { defineComponent } from 'vue';
import type { Sessions } from '@/assets/interfaces';
import { http } from '@/assets/http';
import Timeago from '@/components/Timeago.vue';

export default defineComponent({
    data() {
        return {
            session_key: this.$route.params.key,
            session: {} as Sessions,
            loading: true,
            hasData: false,
        };
    },
    created() {
        this.getSession();
    },
    methods: {
        async getSession() {
            this.loading = true
            await await http.get(`users/session/`, {
                params: {
                    session_key: this.session_key
                }
            }).then((res) => {
                if (res.data.error) {
                    return;
                }
                if(res.data.session) {
                    this.session = res.data.session;
                    console.log(this.session)
                    this.hasData = true;
                }
            }).catch((err) => {
                console.log(err);
            });
            this.loading = false
        },
        async deleteSession() {
            await http.delete(`users/session/`, {
                params: {
                    session_key: this.session_key
                }
            }).then((res) => {
                if (res.data.error) {
                    this.$q.notify({
                        message: `<span class="text-white weight-900">${res.data.message}</span>`,
                        classes: 'bg-web-theme text-white',
                        html: true,
                    })
                }
                if(res.data.success) {
                    this.$q.notify({
                        message: `<span class="text-heading weight-900">${res.data.message}</span>`,
                        classes: 'bg-web-theme text-white',
                        html: true,
                    })
                }
            }).catch((err) => {
                console.log(err);
            });
            this.$router.back();
        }
    },
    components: { Timeago }
})
</script>

<template>
    <div>
        <div v-if="hasData && !loading">
            <header v-if="!$q.screen.lt.sm">
                <Item>
                    <template #avatar>
                        <q-btn flat round @click="$router.back">
                            <q-icon name="arrow_back" />
                        </q-btn>
                    </template>
                    <template #title>
                        <div class="text-2xl weight-900 ml-5">{{ session.device ?? 'Unknown' }}</div>
                    </template>
                </Item>
            </header>
            <div class="pb-3">
                <Item>
                    <template #avatar>
                        <div class="p-2 border">
                            <q-icon :color="$store.state.dark ? 'white' : 'black'" v-if="['Android','iPhone', 'Windows Phone'].includes(session.device)" size="2rem" name="smartphone" />
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
                        <span class="text-caption">
                            {{ session.browser }}
                        </span>
                    </template>
                </Item>
            </div>
            <q-separator :dark="$store.state.dark" />
            <div class="p-2">
                <Item>
                    <template #title>
                        <span class="text-heading text-2xl weight-900">
                            Date and time
                        </span>
                    </template>
                    <template #caption>
                        <div class="mt-5">
                            <span class="text-body" v-if="session.current_session">
                                Active Now
                            </span>
                            <span v-else class="text-caption">
                                <Timeago spanClass="weight-900 text-heading" html :date="session.last_activity" />
                            </span>
                        </div>
                    
                    </template>
                </Item>
            </div>
            <q-separator :dark="$store.state.dark" />
            <div class="p-2">
                <Item>
                    <template #title>
                        <span class="text-heading text-2xl weight-900">
                            Location
                        </span>
                    </template>
                    <template #caption>
                        <div class="flex flex-row gap-2 items-center mt-5" v-if="session.location">
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
                        <div v-else class="mt-5 text-sm text-heading">
                            Unknown
                        </div>
                    
                    </template>
                </Item>
            </div>
            <div v-if="!session.current_session" class="border-t border-b">
                <button @click="deleteSession" class="danger-btn bg-transparent text-xl text-red weight-900 border-none pointer w-full py-5">
                    Logout of this device
                </button>
            </div>
        </div>
        <div  v-if="!hasData && !loading">
            <div class="text-center">
                <q-icon name="error" size="10rem" color="red" />
                <div class="text-heading text-2xl weight-900">
                    Session not found
                </div>
            </div>
        </div>
        <div v-if="loading">
            <Loading />
        </div>
    </div>
    
</template>

<style scoped lang="scss">


.danger-btn {
    
    &:hover {
        background-color: rgba(255, 0, 0, 0.1) !important;
    }
}
</style>