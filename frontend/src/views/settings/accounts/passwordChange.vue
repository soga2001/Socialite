<script lang="ts">
// import Input from '@/components/Input.vue';
import { http } from '@/assets/http';
import { defineComponent } from 'vue'
export default defineComponent({
    name: 'account',
    data() {
        return {
            currentPassword: '',
            newPassword: '',
            confirmPassword: '',
            disable: true,
        };
    },
    methods: {
        async submit() {
            if(!this.isValid()) {
                let message = '';
                if(this.currentPassword.length === 0 || this.newPassword.length === 0 || this.newPassword !== this.confirmPassword) {
                    message = "Please don't leave any input blank"
                }
                else if(this.newPassword !== this.confirmPassword) {
                    message = 'New password and confirm password does not match'
                }
                this.$notify({
                    title: 'Error!',
                    text: message,
                    type: 'error',
                    group: 'error',
                })
                return
            }
            await http.put('users/change_password/', {
                current_password: this.currentPassword,
                new_password: this.newPassword,
                confirm_password: this.confirmPassword,
            }).then((res) => {
                if(res.data.success) {
                    this.$notify({
                        title: 'Success!',
                        text: res.data.message,
                        type: 'success',
                        group: 'success',
                    })
                    this.$router.push({name: 'account'})
                }
            }).catch((err) => {
                console.log(err)
            })
        },
        isValid() {
            const isNewPasswordValid = this.newPassword === this.confirmPassword;
            const isConfirmPasswordNotEmpty = this.confirmPassword.length > 0;
            const isCurrentPasswordNotEmpty = this.currentPassword.length > 0;

            if (isNewPasswordValid && isConfirmPasswordNotEmpty && isCurrentPasswordNotEmpty) {
                this.disable = false;
                return true
            } else {
                this.disable = true;
                return false
            }
        }
    },
    mounted() {
    },
    computed: {
    },
    watch: {
        newPassword(newPassword) {
            this.isValid()
        },
        confirmPassword(confirmPassword) {
            this.isValid()
        },
    },
    components: {
        
    }
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
                    <span class="text-left text-2xl text-heading weight-900">Change your password</span>
                </template>
            </Item>
        </header>
        <div class="w-full flex flex-row justify-center">
            <form class="w-full flex flex-col gap-1" @submit.prevent="submit">
                <div class="border-b p-2 flex flex-col gap-1">
                    <q-input color="teal" type="password" outlined v-model="currentPassword" label-slot clearable>
                        <template v-slot:label>
                            <div class="text-heading weight-500 text-xl">
                                Current Password
                            </div>
                        </template>
                    </q-input>
                    <span class="px-3">
                        <RouterLink to="/" class=" w-fit hover-underline no-decor weight-800 text-theme text-base">
                            Forgot Password?
                        </RouterLink>
                    </span>
                    
                </div>
                <div class="p-2 border-b flex flex-col gap-4">
                    <q-input type="password" outlined v-model="newPassword" label-slot clearable>
                        <template v-slot:label>
                            <div class="text-heading weight-500 text-xl">
                                New Password
                            </div>
                        </template>
                    </q-input>
                    <q-input type="password" outlined v-model="confirmPassword" label-slot clearable>
                        <template v-slot:label>
                            <div class="text-heading weight-500 text-xl">
                                Confirm Password
                            </div>
                        </template>
                    </q-input>
                </div>
                
                <div class="flex w-full">
                    <!-- :disabled="disable"  -->
                    <input type="submit" value="Save" class="pointer mr-2 my-2 ml-auto w-fit rounded text-xl text-heading weight-900 px-10 py-1 bg-web-theme border-none" />
                </div>
            </form>
        </div>
    </div>
</template>

<style scoped lang="scss">

</style>