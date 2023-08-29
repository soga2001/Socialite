<script lang="ts">
import { defineComponent, ref, toHandlers } from 'vue';
import {useCookies} from 'vue3-cookies'
import { RouterLink, RouterView } from 'vue-router';
import { http } from '@/assets/http';
import {useStore} from '../store/store'
import Input from '@/components/Input.vue';
import type { User } from '@/assets/interfaces';
// import { AES } from 'crypto-ts';
// import { get_user_from_cookie } from '@/assets/userFromCookie';

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
            http.post("users/login/", {
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
        },
        updateDisableState(username: string, password:string) {
            this.disable = !(username.length >= 1 && password.length >= 1);
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
    components: { Input },
    watch: {
        username(username) {
            this.updateDisableState(username, this.password);
        },
        password(password) {
            this.updateDisableState(this.username, password);
        }
    },
    computed: {

    },
})
</script>

<template>

<div class="form-container text-heading w-full">
	<h1 class="text-5xl weight-900 text-heading">Login</h1>
  <hr/>
	<form class="form" autocomplete="off" v-on:submit.prevent="login">
        <Input @update:val="username = $event" input_type="text" input_label="Username" id="username" class="w-full my-2" />
        <Input @update:val="password = $event" input_type="password" input_label="Password" id="1" />
        <div class="forgot my-4">
            <span class="text-base weight-900 pointer no-decor hover-underline text-theme" @click="forgotPass = true">Forgot Password?</span>
        </div>
		<button type="submit" :disabled="disable" class="w-full rounded text-xl py-2 bg-transparent border-brighter-2 bg-hover-soft pointer">Sign in</button>
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
    font-size: 0.75rem;
    line-height: 1rem;
    color: rgba(156, 163, 175, 1);
  }
}


</style>

<!-- <style scoped lang="scss">


@import '@/assets/base.css';

.login {
  height: 100%;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-content: center;
  text-align: center;
  
  &__main {
    min-width: fit-content;
    border-radius: 10px;
  }
  
  &__header {
    font-size: 70px;
    color: var(--color-heading);
  }
  
  &__form {
    display: grid;
    gap: 10px;
    grid-template-columns: repeat(8, 1fr);
    width: 100%;
    margin: auto;
    padding: 10px;
    
    .username, .password {
      grid-column: auto / span 8;
    }
  
    .errMsg {
      background-color: rgba(255, 0, 0, 0.566);
      grid-column: auto / span 8;
      padding: 10px;
      border-radius: 10px;
      color: var(--color-heading);
    }
  
    .submit {
      grid-column: 4 / span 2;
    }
  }
  
  &__links {
    grid-column: 2 / span 6;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    
    a {
      text-decoration: none;
      padding: 10px;
      border: 1px solid var(--color-text);
      color: var(--color-text);
      
      &:hover {
        background-color: var(--color-text);
        color: var(--color-background);
      }
    }
  }
}

a {
  padding: 10px;
}

/* input {
  margin: 10px 20px;
  font-size: 20px;
  padding: 10px;
  background-color: var(--color-background);
  color: var(--color-text);
  border: var(--color-border);
  border-radius: 10px;
} */

button {
  width: 10em;
  position: relative;
  height: 3.5em;
  border: 3px ridge #149CEA;
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
    box-shadow: inset 0px 0px 25px #1479EA;
  }
}

::placeholder {
  color: var(--color-text);
}

hr {
  width: 50%;
  margin: auto;
}



</style> -->