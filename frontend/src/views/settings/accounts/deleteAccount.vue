<script lang="ts">
// import Input from '@/components/Input.vue';
import { defineComponent } from 'vue'
export default defineComponent({
    name: 'deactive-account',
    data() {
        return {
            password: '',
        };
    },
    methods: {},
    mounted() {
    },
    watch: {},
    components: {  }
})
</script>

<template>
    <div>
        <header class="sticky top-0 pb-2">
            <Item>
                <template #avatar>
                    <q-btn flat icon="arrow_back" @click="$router.back"/>
                </template>
                <template #title>
                    <span class="text-left text-2xl text-heading weight-900">Delete Account</span>
                </template>
            </Item>
        </header>
        <div>
            <Item clickable :to="{name: 'user-profile', params: {username: $store.state.user.username}}">
                <template #avatar>
                    <q-avatar>
                        <q-img v-if="$store.state.user.avatar" :src="$store.state.user.avatar"/>
                        <i-profile v-else />
                    </q-avatar>
                </template>
                <template #title>
                    <span class="text-left text-xl text-heading weight-900">{{ $store.state.user.first_name }} {{ $store.state.user.last_name }}</span>
                </template>
                <template #caption>
                    <span class="text-sm text-body weight-700 text-nodecor">
                        @{{ $store.state.user.username }}
                    </span>
                </template>
            </Item>
        </div>
        <div class="p-2 flex flex-col gap-2">
            <div class="text-2xl weight-900 text-heading"> This will permantely delete your account</div>
            <div>
                You’re about to start the process of deleting your Socialite account. Your display name, @username, and public profile will no longer be viewable on {Website Link}.com.
            </div>
            <div class="text-2xl weight-900 text-heading">
                What else you should know
            </div>
            <div>
                Unlike where you can recover your account within 30 days after deactivating your account. You will forever lose your account after deleting your account.
            </div>
        </div>
        <hr/>
        <div class="p-2 flex- flex-col gap-2">
            <div>
                Once you delete your account, others will be able to change their username to your current username.
            </div>
        </div>
        <hr/>
        <div class="w-full">
            <q-btn class="w-full p-3" flat label-slot>
                <span class="text-red text-capitalize weight-900 text-xl">
                    Delete
                </span>
            </q-btn>
        </div>
    </div>
</template>

<style scoped lang="scss">

</style>