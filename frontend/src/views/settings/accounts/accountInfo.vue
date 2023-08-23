<script lang="ts">
// import Input from '@/components/Input.vue';
import { http } from '@/assets/http';
import type { User } from '@/assets/interfaces';
import Input from '@/components/Input.vue';
import { defineComponent } from 'vue'
export default defineComponent({
    name: 'change-password',
    data() {
        return {
            verified: false,
            password: '',
            user: {} as User,
            input: '',
            editName: false,
            editEmail: false,
            editUsername: false,
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
    watch: {
        password() {
            if(this.password.length > 0) {
                this.verified = false
            }
            console.log('here')
        }
    },
    components: { Input }
})
</script>

<template>
    <div>
        <div>
            <header class="sticky top-0 border-b pb-2">
                <Item>
                    <template #avatar>
                        <q-btn flat icon="arrow_back" @click="$router.back"/>
                    </template>
                    <template #title>
                        <span class="text-left text-2xl text-heading weight-900">Account Information</span>
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
            </header>
            <div class="w-full flex flex-row justify-center px-2 py-2" v-if="!verified">
                <form class="w-full flex flex-col gap-1" @submit.prevent="submit">
                    <Input @update:val="password = $event" input_type="password" input_label="Password" id="1" />
                    <RouterLink to="/" class=" w-fit hover-underline no-decor weight-800 text-theme text-base">
                        Forgot Password?
                    </RouterLink>
                    <div class="flex w-full">
                        <input :disable="password.length == 0" type="submit" value="Confirm" class="pointer ml-auto w-fit rounded text-xl text-heading weight-900 px-10 py-2 bg-web-theme border-none" />
                    </div>
                </form>
            </div>
        </div>
        <div v-if="verified">
            <div>
                <Item>
                    <template #avatar>
                        <q-avatar>
                            <!-- <i-profile size="2rem" fill="var(--color-heading)"/> -->
                            <q-icon name="badge" :color="$store.state.dark ? 'white' : 'black'"/>
                        </q-avatar>
                    </template>
                    <template #title>
                        <span v-if="!editName" class="text-left text-xl text-heading weight-700">{{ user.first_name }} {{ user.last_name }}</span>
                    </template>
                    <template #icon>
                        <q-btn flat round name="edit">
                            <q-icon name="edit" :color="$store.state.dark ? 'white' : 'black'"/>
                        </q-btn>
                    </template>
                </Item>
                <Item>
                    <template #avatar>
                        <q-avatar>
                            <q-icon name="email" :color="$store.state.dark ? 'white' : 'black'"/>
                        </q-avatar>
                    </template>
                    <template #title>
                        <span class="text-left text-xl text-heading weight-700">{{ user.email }}</span>
                    </template>
                    <template #icon>
                        <q-btn flat round name="edit">
                            <q-icon name="edit" :color="$store.state.dark ? 'white' : 'black'"/>
                        </q-btn>
                    </template>
                </Item>
                <Item>
                    <template #avatar>
                        <q-avatar>
                            <q-icon name="alternate_email" :color="$store.state.dark ? 'white' : 'black'"/>
                        </q-avatar>
                    </template>
                    <template #title>
                        <span class="text-left text-xl text-heading weight-700">{{ user.username }}</span>
                    </template>
                    <template #icon>
                        <q-btn flat round name="edit">
                            <q-icon name="edit" :color="$store.state.dark ? 'white' : 'black'"/>
                        </q-btn>
                    </template>
                </Item>
                <Item>
                    <template #avatar>
                        <q-avatar>
                            <q-icon name="phone" :color="$store.state.dark ? 'white' : 'black'"/>
                        </q-avatar>
                    </template>
                    <template #title>
                        <span class="text-left text-xl text-heading weight-700">{{  }}</span>
                    </template>
                    <template #icon>
                        <q-btn flat round name="edit">
                            <q-icon name="edit" :color="$store.state.dark ? 'white' : 'black'"/>
                        </q-btn>
                    </template>
                </Item>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
.input {

    &:focus {
        outline-color: green !important;
    }
}
</style>