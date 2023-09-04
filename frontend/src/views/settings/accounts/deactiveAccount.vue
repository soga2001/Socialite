<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
    name: 'deactive-account',
    data() {
        return {
            verified: false,
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
        <header class="sticky top-0 pb-2 " v-if="!$q.screen.lt.sm">
            <Item>
                <template #avatar>
                    <q-btn flat icon="arrow_back" @click="$router.back"/>
                </template>
                <template #title>
                    <span class="text-left text-2xl text-heading weight-900">Deactive Account</span>
                </template>
            </Item>
        </header>
        <div>
            <Item clickable :to="{name: 'user-profile', params: {username: $store.state.user.username}}">
                <template #avatar>
                    <q-avatar>
                        <q-img v-if="$store.state.user.avatar" :src="$store.state.user.avatar"/>
                        <i-profile size="3rem" v-else />
                    </q-avatar>
                </template>
                <template #title>
                    <span class="text-left text-xl text-heading weight-900">{{ $store.state.user.full_name }}</span>
                </template>
                <template #caption>
                    <span class="text-sm text-body weight-700 text-nodecor">
                        @{{ $store.state.user.username }}
                    </span>
                </template>
            </Item>
        </div>
        <div class="p-2 flex flex-col gap-2">
            <div class="text-2xl weight-900 text-heading"> This will deactivate your account</div>
            <div>
                You’re about to start the process of deactivating your Socialite account. Your display name, @username, and public profile will no longer be viewable on {Website Link}.com.
            </div>
            <div class="text-2xl weight-900 text-heading">
                What else you should know
            </div>
            <div>
                You can restore your X account if it was accidentally or wrongfully deactivated for up to 30 days after deactivation.
            </div>
        </div>
        <hr/>
        <div class="p-2 flex- flex-col gap-2">
            <div>
                If you just want to change your @username, you don’t need to deactivate your account — edit it in your <RouterLink to='account-information' class="text-theme no-decor hover-underline weight-800">settings</RouterLink>.
            </div>
        </div>
        <hr/>
        <div class="w-full">
            <button class="w-full p-3 text-red border-none weight-900 bg-transparent text-xl danger-btn pointer"  @click="">
                Deactivate
            </button>
        </div>
    </div>
</template>

<style scoped lang="scss">

</style>