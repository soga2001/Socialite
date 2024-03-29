<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent } from 'vue';


export default defineComponent({
    name: 'VerifyEmail',
    data() {
        return {
            token: this.$route.query.token,
            loading: true,
            success: false,
            message: '',
        }
    },
    methods: {
        async verifyEmail() {
            await http.post(`users/verify_email/`, {
                token: this.token
            }).then((res) => {
                if(res.data.success) {
                    this.success = true
                    this.$router.push({ name: 'Login' })
                }
                else {
                    this.message = res.data.message
                }
            }).catch((err) => {
                console.log(err)
            })
            this.loading = false
        }
    },
    mounted() {
        this.verifyEmail()
    }
})
</script>

<template>
    <div class="h-full p-10 flex justify-center h-full text-center">
        <div v-if="loading" class="">
            <Loading />
        </div>
        <div v-else-if="!loading && success" class="flex flex-col items-center justify-center h-full text-lg weight-900 gap-2">
            <span class="text-3xl weight-900 text-heading">
                Verification Successful!
            </span>
            <svg class="checkmark success" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                <circle class="checkmark__circle success" cx="26" cy="26" r="25" fill="none"/>
                <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
            </svg>
            <span class="text-heading weight-700">
                Your email has been verified. You can login now and continue using Socialite.
            </span>
            <div class="text-xl mt-5 text-heading">
              <RouterLink to="/login" class="no-decor text-heading hover-underline hover-text-theme">Login</RouterLink>
               to have access to Socialite.
            </div>
            
        </div>
        <div v-else-if="!loading && !success" class="flex flex-col items-center justify-center h-full text-lg weight-900">
            <span class="text-3xl weight-900 text-heading">
                Verification Unsuccessful!
            </span>
            <svg class="checkmark failure" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                <circle class="checkmark__circle failure" cx="26" cy="26" r="25" fill="none"/>
                <path class="checkmark__check" fill="none" d="M16 16 36 36 M36 16 16 36"/>
            </svg>
            <span class="text-heading weight-700">
                Your email could not be verified because <span class="text-heading weight-700 text-lowercase">{{ message }}</span>. Please try again later.
            </span>
            
        </div>
    </div>
</template>

<style scoped lang="scss">
.checkmark__circle.success {
  stroke-dasharray: 166;
  stroke-dashoffset: 166;
  stroke-width: 2;
  stroke-miterlimit: 10;
  stroke: #7ac142;
  fill: none;
  animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}

.checkmark__circle.failure {
  stroke-dasharray: 166;
  stroke-dashoffset: 166;
  stroke-width: 2;
  stroke-miterlimit: 10;
  stroke: #ff0000;
  fill: none;
  animation: stroke 0.6s cubic-bezier(0.65, 0, 0.45, 1) forwards;
}

.checkmark.success {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: block;
  stroke-width: 2;
  stroke: #fff;
  stroke-miterlimit: 10;
  margin: 10% auto;
  box-shadow: inset 0px 0px 0px #7ac142;
  animation: fill-success .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;
}

.checkmark.failure {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: block;
  stroke-width: 2;
  stroke: #fff;
  stroke-miterlimit: 10;
  margin: 10% auto;
  box-shadow: inset 0px 0px 0px #ff0000;
  animation: fill-failure .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;
}

.checkmark__check {
  transform-origin: 50% 50%;
  stroke-dasharray: 48;
  stroke-dashoffset: 48;
  animation: stroke 0.3s cubic-bezier(0.65, 0, 0.45, 1) 0.8s forwards;
}

@keyframes stroke {
  100% {
    stroke-dashoffset: 0;
  }
}
@keyframes scale {
  0%, 100% {
    transform: none;
  }
  50% {
    transform: scale3d(1.1, 1.1, 1);
  }
}
@keyframes fill-success {
  100% {
    box-shadow: inset 0px 0px 0px 30px #7ac142;
  }
}

@keyframes fill-failure {
  100% {
    box-shadow: inset 0px 0px 0px 30px #ff0000;
  }
}
</style>