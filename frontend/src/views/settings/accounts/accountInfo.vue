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

            forgotPass: false,

            monthNames: [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]
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
    },
    components: { Input }
})
</script>

<template>
    <div>
        <div>
            <header class="">
                <Item v-if="!$q.screen.lt.sm">
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
                    <div class="text-sm text-body weight-500 text-nodecor">
                        Please enter your password to continue
                    </div>
                </div>
            </header>
            <div class="w-full flex flex-row justify-center px-2" v-if="!verified">
                <form class="w-full flex flex-col gap-1" @submit.prevent="submit">
                    <Input @update:val="password = $event" input_type="password" input_label="Password" id="1" />
                    <span @click="forgotPass = true" class=" w-fit pointer hover-underline no-decor weight-800 text-theme text-base">
                        Forgot Password?
                    </span>
                    <q-dialog v-model="forgotPass">
                        <forgot-password @update:forgotpass="forgotPass = $event" />
                    </q-dialog>
                    <div class="flex w-full">
                        <input :disable="password.length == 0" type="submit" value="Confirm" class="pointer ml-auto w-fit rounded text-base text-heading weight-900 px-10 py-2 bg-web-theme border-none" />
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
                        <span v-if="!editName" class="text-left text-xl text-heading weight-500">{{ user.full_name }}</span>
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
                        <span class="text-left text-xl text-heading weight-500">{{ user.email }}</span>
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
                        <span class="text-left text-xl text-heading weight-500">{{ user.username }}</span>
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
                            <q-icon name="smartphone" :color="$store.state.dark ? 'white' : 'black'"/>
                        </q-avatar>
                    </template>
                    <template #title>
                        <span v-if="user.phone" class="text-left text-xl text-heading weight-500">{{ user.phone}}</span>
                        <span v-else class="text-left text-xl text-heading weight-500">No Phone Number</span>
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
                            <q-icon name="calendar_today" :color="$store.state.dark ? 'white' : 'black'"/>
                        </q-avatar>
                    </template>
                    <template #title>
                        <span v-if="user.dob" class="text-left text-xl text-heading weight-500">
                            {{ `${monthNames[new Date(user.dob).getMonth()]} ${new Date(user.dob).getUTCDate()}, ${new Date(user.dob).getFullYear()}` }}
                        </span>
                        <span v-else class="text-left text-xl text-heading weight-500">Date of Birth not set</span>
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
                            <q-icon size="2rem" name="person" :color="$store.state.dark ? 'white' : 'black'"/>
                        </q-avatar>
                    </template>
                    <template #title>
                        <span v-if="user.bio" class="text-left text-xl text-heading weight-500">{{ user.bio}}</span>
                        <span v-else class="text-left text-xl text-heading weight-500">No Bio</span>
                    </template>
                    <template #icon>
                        <q-btn flat round name="edit">
                            <q-icon name="edit" :color="$store.state.dark ? 'white' : 'black'"/>
                        </q-btn>
                    </template>
                </Item>
                <Item :align-items="user.avatar ? 'start' : 'center'">
                    <template #avatar>
                        <q-avatar>
                            <!-- <q-icon name="banner" :color="$store.state.dark ? 'white' : 'black'"/> -->
                            <i-banner size="2rem" fill="var(--color-heading)"/>
                        </q-avatar>
                    </template>
                    <template #title>
                        <!-- <span class="text-left text-xl text-heading weight-500">{{ user.bio ?? 'N/A' }}</span> -->
                        <q-img class="w-full" v-if="user.banner" :src="user.banner" />
                        <div class="text-left text-xl text-heading weight-500" v-else>No banner</div>
                    </template>
                    <template #icon>
                        <q-btn flat round name="edit">
                            <q-icon name="edit" :color="$store.state.dark ? 'white' : 'black'"/>
                        </q-btn>
                    </template>
                </Item>
                <Item :align-items="user.avatar ? 'start' : 'center'">
                    <template #avatar>
                        <q-avatar>
                            <q-icon size="2rem" name="account_circle" :color="$store.state.dark ? 'white' : 'black'"/>
                        </q-avatar>
                    </template>
                    <template #title>
                        <q-img class="aspect-ratio-1-1" v-if="user.avatar" :src="user.avatar" />
                        <div class="text-left text-xl text-heading weight-500" v-else>No avatar</div>
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
                            <q-icon size="2rem" name="lock" :color="$store.state.dark ? 'white' : 'black'"/>
                        </q-avatar>
                    </template>
                    <template #title>
                        <div v-if="user.private" class="text-left text-xl text-heading weight-500">Private</div>
                        <div v-else class="text-left text-xl text-heading weight-500">Public</div>
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