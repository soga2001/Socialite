<script lang="ts">
import { defineComponent} from 'vue';
import { RouterLink } from 'vue-router';
import { http } from '@/assets/http';
import type { User } from '@/assets/interfaces';

export default defineComponent({
    data() {
        return {
            username: "",
            password: "",
            error: false,
            errMsg: "",
            loading:false,
            disable: true,
            forgotPass: false,
            email: '',
        };
    },
    methods: {
        async login() {
            if (this.username.length === 0 || this.password.length === 0) {
                this.$notify({
                  title: 'Error!',
                  text: "Please don't leave username or password blank!",
                  type: 'error',
                  group: 'error',
                })
                return;
            }
            this.loading = true
            await http.post("users/login/", {
                username: this.username,
                password: this.password,
            }, {
            }).then(async (res) => {
                if (res.data.error === true) {
                    this.$q.notify({
                      message: `<span class="text-white weight-900">${res.data.message}</span>`,
                      position: 'top-right',
                      type: 'negative',
                      iconColor: 'white',
                      timeout: 2000,
                      // classes: 'bg-web-theme',
                      html: true,
                    })
                }
                else {
                    await this.$store.commit("setUser", res.data.user as User);
                    // await this.$router.go(0);
                    this.$store.commit("authenticate", true);
                    // this.$notify({
                    //   title: "Success!",
                    //   text: "Login Successful!",
                    //   type: 'success',
                    //   group: 'success',
                    // })
                    this.$q.notify({
                      message: `<span class="text-white weight-900">Log in successful</span>`,
                      position: 'top-right',
                      timeout: 2000,
                      classes: 'bg-web-theme',
                      html: true,
                    })
                }
            }).catch((err) => {
                console.log(err);
            });
            this.loading = false
        },
        async updateDisableState() {
          let disableBtn = !(this.username.length >= 1 && this.password.length >= 1);
          this.disable = disableBtn;
        },
        async sendEmail() {
          await http.post('users/send_reset_password_email/', {
            email: this.email
          }).then((res) => {
            if(res.data.success) {
              this.forgotPass = false;
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
        }
    },
    created() {
    },
    watch: {
        username(username) {
            this.updateDisableState();
        },
        password(password) {
            this.updateDisableState();
        }
    },
    computed: {

    },
})
</script>

<template>

<div class="form-container text-heading w-full">
	<h1 class="text-5xl weight-900 text-heading text-center">Login</h1>
  <hr/>
	<form class="form" autocomplete="off" v-on:submit.prevent="login">
        <Input @update:val="username = $event" input_type="text" input_label="Username" id="username" class="w-full my-2" />
        <Input @update:val="password = $event" input_type="password" input_label="Password" id="1" />
        <div class="forgot my-4">
            <span class="text-base weight-900 pointer no-decor hover-underline text-theme" @click="forgotPass = true">Forgot Password?</span>
        </div>
		    <q-btn
          :loading="loading"
          dark-percentage
          unelevated
          class="submit"
          type="submit"
          :disable="disable"
        >
          <div class="text-capitalize text-xl weight-900 text-heading">
            Sign in
          </div>
          <template v-slot:loading>
            <Loading size="2rem" />
          </template>
        </q-btn>
	</form>

  <q-dialog v-model="forgotPass">
    <forgot-password @update:forgotpass="forgotPass = $event" />
  </q-dialog>

  <div class="signup mt-5">
      <span>Don't have an account? <RouterLink to="/register" class="text-theme no-decor hover-underline weight-900">Sign up</RouterLink></span>
    </div>
</div>
</template>

<style scoped lang="scss">

.form-container {
  border-radius: 0.75rem;
  padding: 2rem;
  color: rgba(243, 244, 246, 1);
  
  .title {
    text-align: center;
    font-size: 1.5rem;
    line-height: 2rem;
    font-weight: 700;
  }
  
  .form {
    margin-top: 1.5rem;
    
  }
  
  .forgot {
    display: flex;
    justify-content: flex-end;
    font-size: 0.75rem;
    line-height: 1rem;
  }
  
  .sign {
    display: block;
    width: 100%;
    background-color: rgba(167, 139, 250, 1);
    padding: 0.75rem;
    text-align: center;
    color: rgba(17, 24, 39, 1);
    border: none;
    border-radius: 0.375rem;
    font-weight: 600;
  }
  
  .social-message {
    display: flex;
    align-items: center;
    padding-top: 1rem;
    
    .line {
      height: 1px;
      flex: 1 1 0%;
      background-color: rgba(55, 65, 81, 1);
    }
    
    .message {
      padding-left: 0.75rem;
      padding-right: 0.75rem;
      font-size: 0.875rem;
      line-height: 1.25rem;
      color: rgba(156, 163, 175, 1);
    }
  }
  
  .social-icons {
    display: flex;
    justify-content: center;
    
    .icon {
      border-radius: 0.125rem;
      padding: 0.75rem;
      border: none;
      background-color: transparent;
      margin-left: 8px;
      
      svg {
        height: 1.25rem;
        width: 1.25rem;
        fill: #fff;
      }
    }
  }
  
  .signup {
    text-align: center;
    line-height: 1rem;
    color: rgba(156, 163, 175, 1);
  }
}

button {
  // width: 10em;
  width: 100%;
  position: relative;
  height: 3.5rem;
  border: 3px ridge #ff00ff;
  outline: none;
  background-color: transparent;
  color: var(--color-text);
  transition: 1s;
  border-radius: 0.3em;
  font-size: 16px;
  font-weight: bold;

  &::after {
    content: "";
    position: absolute;
    top: -10px;
    left: 3%;
    width: 95%;
    height: 40%;
    background-color: var(--color-background);
    transition: 0.5s;
    transform-origin: center;
  }

  &::before {
    content: "";
    transform-origin: center;
    position: absolute;
    top: 80%;
    left: 3%;
    width: 95%;
    height: 40%;
    background-color: var(--color-background);
    transition: 0.5s;
  }

  &:hover::before, &:hover::after {
    transform: scale(0);
  }

  &:hover {
    box-shadow: inset 0px 0px 25px rgba(255, 0, 255, 1);
  }
}


</style>