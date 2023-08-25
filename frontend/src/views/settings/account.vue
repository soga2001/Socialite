<script lang="ts">
// import Input from '@/components/Input.vue';
import { defineComponent } from 'vue'
export default defineComponent({
    name: 'account',
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
    <div class="w-full min-h-viewport">
        <header class="h-full w-full bg-theme">
            <div>
                <Item>
                    <template #avatar v-if="$q.screen.lt.sm">
                        <q-avatar>
                            <q-btn round flat icon="arrow_back" @click="$router.go(-1)"/>
                        </q-avatar>
                    </template>
                    <template #title>
                        <span class="text-3xl weight-900 text-heading">
                            Your Account
                        </span>
                    </template>
                </Item>
            </div>
            <nav class="w-full">
                <RouterLink to="account-information" active-class="active">
                    <Item clickable class="child" :captionLineClamp="2">
                        <template #avatar>
                            <i-profile size="10px" fill="var(--color-heading)"/>
                        </template>
                        <template #title>
                            <span class="text-xl text-heading weight-800 text-capitalize">
                                Account Information
                            </span>
                        </template>
                        <template #caption>
                            <span class="text-sm text-body weight-700 text-nodecor">
                                View your account information such as phone number and email address.
                            </span>
                        </template>
                        <template #icon>
                            <q-icon size="2rem" name="navigate_next" class="text-heading"/>
                        </template>
                    </Item>
                </RouterLink>
                <RouterLink to="change-password" active-class="active">
                    <Item clickable class="child" :captionLineClamp="2">
                        <template #avatar>
                            <q-icon size="3rem" name="lock" class="text-heading"/>
                        </template>
                        <template #title>
                            <span class="text-xl text-heading weight-800 text-capitalize">
                                Change Password
                            </span>
                        </template>
                        <template #caption>
                            <span class="text-sm text-body weight-700 text-nodecor">
                                Change your password (requires current password)
                            </span>
                        </template>
                        <template #icon>
                            <q-icon size="2rem" name="navigate_next" class="text-heading"/>
                        </template>
                    </Item>
                </RouterLink>
                <RouterLink to="deactive-account" active-class="active">
                    <Item clickable class="child" :captionLineClamp="2">
                        <template #avatar>
                            <!-- <q-icon size="2rem" name="heart_break" class="text-heading"/> -->
                            <!-- <i-user-close fill="var(--color-heading)"/> -->
                            <i-ghost fill="var(--color-heading)"/>
                        </template>
                        <template #title>
                            <span class="text-xl text-heading weight-800 text-capitalize">
                                Deactive your account
                            </span>
                        </template>
                        <template #caption>
                            <span class="text-sm text-body weight-700 text-nodecor">
                                Deactive your account but you can reactive it at a later time.
                            </span>
                        </template>
                        <template #icon>
                            <q-icon size="2rem" name="navigate_next" class="text-heading"/>
                        </template>
                    </Item>
                </RouterLink>
                <RouterLink to="delete-account" active-class="active">
                    <Item clickable class="child" :captionLineClamp="2">
                        <template #avatar>
                            <q-icon size="3rem" name="heart_broken" class="text-heading"/>
                        </template>
                        <template #title>
                            <span class="text-xl text-heading weight-800 text-capitalize">
                                Delete your account
                            </span>
                        </template>
                        <template #caption>
                            <span class="text-sm text-body weight-700 text-nodecor">
                                Delete your account permantely.
                            </span>
                        </template>
                        <template #icon>
                            <q-icon size="2rem" name="navigate_next" class="text-heading"/>
                        </template>
                    </Item>
                </RouterLink>
            </nav>
        </header>
    </div>
</template>

<style scoped lang="scss">
* {
    text-decoration: none;
}

.active {
    
    .child {
        background-color: #f5f5f5;
    }
}
</style>