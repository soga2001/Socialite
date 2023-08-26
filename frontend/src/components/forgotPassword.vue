<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent, ref } from 'vue';

export default defineComponent({
    data() {
        return {
            email: '',
            disable: true,
        }
    },
    methods: {
        disabled() {
            this.disable = this.email.match(/^\S+@\S+\.\S+$/) == null
        },
        async sendEmail() {
            if (this.disable) {
                this.$q.notify({
                    message: "Please don't leave the email field empty",
                    type: 'negative',
                    group: 'negative',
                })
                return;
            }
            await http.post('users/send_reset_password_email/', {
                email: this.email
            }).then((res) => {
                if(res.data.success) {
                this.$emit('update:forgotpass', false)
                this.email = '';
                this.$notify({
                    text: 'Intruction to reset your password has been sent to your email.',
                    type: 'success',
                    group: 'success',
                })
                }
            }).catch((err) => {
                console.log(err)
            })
        },
        onClose() {
            this.$emit('update:forgotpass', false)
        },
    },
    watch: {
        email() {
            this.disabled()
        }
    }

})
</script>

<template>
    <div :class="{'min-w-viewport': $q.screen.lt.sm}" class="w-full p-0 m-0">
        <q-card class="bg-theme w-full box-shadow">
            <div class="px-2">
                <Item>
                    <template #title>
                        <div class="text-2xl weight-900">
                            Forgot Password
                        </div>
                    </template>
                    <template #icon>
                        <q-btn @click="onClose" round flat icon="close" size="1rem" />
                    </template>
                </Item>
            </div>

            <q-separator :dark="$store.state.dark" />

            <q-card-section class="flex flex-col gap-2">
            <p class="text-heading weight-700 text-base">Please Enter Your Email.</p>
            <p class="caption text-sm">We'll send you an email to reset your password.</p>
            <Input @update:val="email = $event" input_label="Email*" id="email" class="email" input_type="email" required/>
            <q-item class="mt-10">
                <q-item-section avatar>
                <q-icon name="warning" color="red-5" />
                </q-item-section>
                <q-item-section>
                <div class="text-red-5 weight-900 text-xs">
                    This link will expire in 10 minutes. Even if you are able to open the link, you will not be able to change your password after that until you request a new link.
                </div>
                </q-item-section>
            </q-item>
            </q-card-section>

            <q-separator :dark="$store.state.dark" />

            <q-card-actions align="right">
                <q-btn flat v-close-popup>
                    <div class="text-capitalize text-heading">
                    Cancel
                    </div>
                </q-btn>
                <q-btn :disable="disable" class="border-brighter-2 rounded px-8 py-1 bg-hover-mute" flat @click="sendEmail">
                    <div class="text-capitalize text-heading">
                        Submit
                    </div>
                </q-btn>
            </q-card-actions>
        </q-card>
    </div>
    
</template>


<style scoped lang="scss">
</style>