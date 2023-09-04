<script lang="ts">
import { http } from '@/assets/http';
import Input from '@/components/Input.vue';
import { defineComponent } from 'vue';

export default defineComponent({
    data() {
        return {
            token: this.$route.query.token ?? 'hell',
            password: '',
            confirm_password: '',
            disable: true,
        };
    },
    methods: {
        validPasswords() {
            if (this.password == this.confirm_password && this.password.length > 0) {
                this.disable = false;
            }
            else {
                this.disable = true;
            }
        },
        submit(e: Event) {
            e.preventDefault()
            http.put('users/reset_password/', {
                token: this.token,
                password: this.password,
                confirm_password: this.confirm_password
            }).then((res) => {
                if (res.data.success) {
                    console.log('here')
                    // this.$router.push({ name: 'login' })
                }
                console.log(res)
            }).catch((err) => {
                console.log(err);
            })
        }
    },
    created() {
        if(!this.token) {
            this.$router.push({ name: 'login' })
        }
    },
    watch: {
        password(password) {
            this.validPasswords();
        },
        confirm_password(confirm_password) {
            this.validPasswords();
        }
    },
    components: { Input }
})

</script>

<template>
    <div class="min-h-viewport max-h-viewport flex flex-col gap-5 py-5 items-center w-full">
        <span class="text-3xl weight-900 text-heading">
            Reset Password
        </span>
        <hr class="w-full"/>
        <form class="h-full py-2 w-full max-w-xs flex justify-center gap-3" @submit.preventDefault="submit">
            <Input @update:val="password = $event" input_label="Password*" id="password" class="w-full" input_type="password" required/>
            <Input @update:val="confirm_password = $event" input_label="Confirm Password*" id="c_password" class="w-full" input_type="password" required/>
            <button :disabled="disable" class="pointer hover-bg-mute bg-transparent px-5 py-2 border-brighter-3 rounded text-heading " type="submit">Reset</button>
        </form>
    </div>
</template>

<style scoped lang="scss">

</style>