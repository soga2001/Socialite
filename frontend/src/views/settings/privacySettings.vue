<script lang="ts">
// import Input from '@/components/Input.vue';
import { http } from '@/assets/http';
import type { User } from '@/assets/interfaces';
import { defineComponent } from 'vue'
export default defineComponent({
    name: 'privacy-settings',
    data() {
        return {
            verified: false,
            password: '',
            user: {} as User,
        };
    },
    methods: {
        async submit() {
            await http.get('users/get_user_info/', {
                params: {
                    password: this.password,
                }
            }).then((res) => {
                if(res.data.success) {
                    this.verified = true
                    this.user = res.data.user
                }
                else {
                    this.$notify({
                        title: 'Error!',
                        text: res.data.message,
                        type: 'error',
                        group: 'error',
                    })
                }
            }).catch((err) => {
            })
        }
    },
    mounted() {
    },
    watch: {},
    components: {  }
})
</script>

<template>
    <div class="w-full min-h-viewport">
        <header class="h-full w-full bg-theme border-b pb-3">
            <div>
                <Item>
                    <template #avatar v-if="$q.screen.lt.sm">
                        <q-avatar>
                            <q-btn round flat icon="arrow_back" @click="$router.go(-1)"/>
                        </q-avatar>
                    </template>
                    <template #title>
                        <span class="text-3xl weight-900 text-heading">
                            Security and Privacy
                        </span>
                    </template>
                </Item>
                <div class="ml-2" v-if="!verified">
                    <div class="text-xl text-heading weight-900">
                        Confirm your password
                    </div>
                    <div class="text-sm text-body weight-700 text-nodecor">
                        Please enter your password to continue
                    </div>
                </div>
            </div>
        </header>
        <div class="w-full flex flex-row justify-center px-2 py-2" v-if="!verified">
            <form class="w-full flex flex-col gap-1" @submit.prevent="submit">
                <Input @update:val="password = $event" input_type="password" input_label="Password" id="1" />
                <RouterLink to="/" class=" w-fit hover-underline no-decor weight-800 text-theme text-base">
                    Forgot Password?
                </RouterLink>
                <div class="flex w-full">
                    <input :disable="password.length == 0" type="submit" value="Confirm" class="pointer ml-auto w-fit rounded text-base text-heading weight-900 px-10 py-2 bg-web-theme border-none" />
                </div>
            </form>
        </div>
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