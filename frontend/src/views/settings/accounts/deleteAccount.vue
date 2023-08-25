<script lang="ts">
// import Input from '@/components/Input.vue';
import { http } from '@/assets/http';
import { defineComponent, ref } from 'vue'
export default defineComponent({
    name: 'deactive-account',
    data() {
        return {
            password: '',
            toDelete: false,
        }
    },
    methods: {
        openModal() {
            this.toDelete = true
        },
        closeModal() {
            this.toDelete = false
        },
        async deleteAccount() {
            await http.delete('users/delete_account/', {
                params: {
                    password: this.password
                }
            }).then((res) => {
                console.log(res)
                if(res.status === 200) {
                    this.$router.push({name: 'login'})
                    this.$store.commit('authenticate', false)
                    this.$store.commit('setDefaultUser')
                    this.$notify({
                        title: 'Success!',
                        text: res.data.message,
                        type: 'success',
                        group: 'success',
                    })
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
                if(err.response.status === 401) {
                    this.$q.notify({
                        message: `<span class="text-white">${err.response.data.message}</span>`,
                        color: 'negative',
                        icon: 'report_problem',
                        iconColor: 'white',
                        position: 'top',
                        timeout: 2500,
                        html: true,
                    })
                }
                
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
                        <i-profile size="3rem" v-else />
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
                You're about to start the process of deleting your Socialite account. Your display name, @username, and public profile will no longer be viewable on {Website Link}.com.
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
            <q-btn class="w-full p-3" flat label-slot @click="openModal">
                <span class="text-red text-capitalize weight-900 text-xl">
                    Delete
                </span>
            </q-btn>
        </div>
        <q-dialog class="box-shadow" v-model="toDelete" persistent>
            <q-card class="min-w-68 w-full max-w-sm bg-theme border-brighter">
                <div>
                    <Item>
                        <template #title>
                            <span class="text-heading weight-900">Confirm Password</span>
                        </template>
                        <template #icon>
                            <q-btn flat round icon="close" v-close-popup />
                        </template>
                    </Item>
                </div>

                <q-separator :dark="$store.state.dark" />
                
                <q-card-section class="q-pt-5">
                    <!-- <input type="password" v-model="password" placeholder="Password" autofocus  class="p-2 w-full text-xl border"/> -->
                    <Input autofocus @update:val="password = $event" input_type="password" input_label="Password" id="1" />
                </q-card-section>

                <q-separator :dark="$store.state.dark" />

                <q-card-actions align="right" class="text-primary">
                    <!-- <q-btn flat @click="deleteAccount"> 
                        <span class="text-capitalize text-heading bg-web-theme px-5 py-2 rounded">Delete</span>
                    </q-btn> -->
                    <button @click="deleteAccount" class="pointer text-capitalize text-heading bg-transparent bg-hover-soft px-10 py-1 text-xl rounded border-brighter-2"> 
                        Delete
                    </button>
                </q-card-actions>
            </q-card>
        </q-dialog>
    </div>
</template>

<style scoped lang="scss">

</style>