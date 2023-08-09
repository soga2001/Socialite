<script lang="ts">
import { defineComponent, ref, toHandlers } from 'vue';
import {useCookies} from 'vue3-cookies'
import { RouterLink, RouterView } from 'vue-router';
import { http } from '@/assets/http';
import {useStore} from '../store/store'
import Input from '@/components/Input.vue';
// import { AES } from 'crypto-ts';
import { get_user_from_cookie } from '@/assets/userFromCookie';

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
                this.error = true;
                this.errMsg = "Please don't leave username or password blank!";
                return;
            }
            http.post("users/login/", {
                username: this.username,
                password: this.password,
            }, {
            }).then(async (res) => {
                if (res.data.error === true) {
                    console.log(res.data)
                    this.error = true;
                    this.errMsg = res.data.message;
                }
                else {
                    await get_user_from_cookie()
                    this.$store.commit("authenticate", true);
                    this.$router.push("/home");
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
            console.log(res.data)
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
<!-- <div class="login">
    <div class="login__main">
        <h1 class="login__header">Login</h1>
        <hr/>
        <form class="login__form" autocomplete="off" v-on:submit.prevent="login">
            <Input @update:val="username = $event" required input_type="text" input_label="Username*" id="username" class="username" />
            <Input @update:val="password = $event" required input_type="password" input_label="Password*" id="password" class="password" />
            <span v-if="error" class="errMsg">{{errMsg}}</span>
            <button type="submit" class="submit" :disabled="username.length < 1 && password.length < 1" >
                Login
            </button>
            <div class="login__links">
                <a disabled>Forgot Password?</a>
                <RouterLink to="/register" class="link">Create an Account</RouterLink>
            </div>
        </form>
    </div>
</div> -->

<div class="form-container text-heading w-full">
	<p class="title">Login</p>
	<form class="form" autocomplete="off" v-on:submit.prevent="login">
		<!-- <div class="input-group">
			<label for="username">Username</label>
			<input type="text" name="username" id="username" placeholder="">
		</div> -->
        <Input @update:val="username = $event" input_type="text" input_label="Username*" id="username" class="w-full my-2" />
        <Input @update:val="password = $event" input_type="password" input_label="Password*" id="password" class="w-full my-2" />
        <span v-if="error" class="flex justify-center m-3 p-3 text-xl bg-red-2 text-red-13 w-full text-center">{{errMsg}}</span>
        <div class="forgot mb-2">
            <RouterLink class="hover-text-heading weight-bold" to="" @click="forgotPass = true">Forgot Password?</RouterLink>
        </div>
		<button type="submit" :disabled="disable" class="w-full border-none rounded text-xl py-3 bg-theme-mute pointer">Sign in</button>
	</form>

  <q-dialog v-model="forgotPass">
      <q-card class="bg-theme min-w-52 w-full border">
        <q-card-section>
          <div class="text-heading weight-900 text-2xl">Forgot Password</div>
        </q-card-section>

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
          <q-btn flat @click="sendEmail">
            <div class="text-capitalize text-heading">
              Submit
            </div>
          </q-btn>
          
        </q-card-actions>
      </q-card>
    </q-dialog>

	<!-- <div class="social-message">
		<div class="line"></div>
		<p class="message">Login with social accounts</p>
		<div class="line"></div>
	</div> -->
	<!-- <div class="social-icons">
		<button aria-label="Log in with Google" class="icon">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" class="w-5 h-5 fill-current">
				<path d="M16.318 13.714v5.484h9.078c-0.37 2.354-2.745 6.901-9.078 6.901-5.458 0-9.917-4.521-9.917-10.099s4.458-10.099 9.917-10.099c3.109 0 5.193 1.318 6.38 2.464l4.339-4.182c-2.786-2.599-6.396-4.182-10.719-4.182-8.844 0-16 7.151-16 16s7.156 16 16 16c9.234 0 15.365-6.49 15.365-15.635 0-1.052-0.115-1.854-0.255-2.651z"></path>
			</svg>
		</button>
		<button aria-label="Log in with Twitter" class="icon">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" class="w-5 h-5 fill-current">
				<path d="M31.937 6.093c-1.177 0.516-2.437 0.871-3.765 1.032 1.355-0.813 2.391-2.099 2.885-3.631-1.271 0.74-2.677 1.276-4.172 1.579-1.192-1.276-2.896-2.079-4.787-2.079-3.625 0-6.563 2.937-6.563 6.557 0 0.521 0.063 1.021 0.172 1.495-5.453-0.255-10.287-2.875-13.52-6.833-0.568 0.964-0.891 2.084-0.891 3.303 0 2.281 1.161 4.281 2.916 5.457-1.073-0.031-2.083-0.328-2.968-0.817v0.079c0 3.181 2.26 5.833 5.26 6.437-0.547 0.145-1.131 0.229-1.724 0.229-0.421 0-0.823-0.041-1.224-0.115 0.844 2.604 3.26 4.5 6.14 4.557-2.239 1.755-5.077 2.801-8.135 2.801-0.521 0-1.041-0.025-1.563-0.088 2.917 1.86 6.36 2.948 10.079 2.948 12.067 0 18.661-9.995 18.661-18.651 0-0.276 0-0.557-0.021-0.839 1.287-0.917 2.401-2.079 3.281-3.396z"></path>
			</svg>
		</button>
		<button aria-label="Log in with GitHub" class="icon">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" class="w-5 h-5 fill-current">
				<path d="M16 0.396c-8.839 0-16 7.167-16 16 0 7.073 4.584 13.068 10.937 15.183 0.803 0.151 1.093-0.344 1.093-0.772 0-0.38-0.009-1.385-0.015-2.719-4.453 0.964-5.391-2.151-5.391-2.151-0.729-1.844-1.781-2.339-1.781-2.339-1.448-0.989 0.115-0.968 0.115-0.968 1.604 0.109 2.448 1.645 2.448 1.645 1.427 2.448 3.744 1.74 4.661 1.328 0.14-1.031 0.557-1.74 1.011-2.135-3.552-0.401-7.287-1.776-7.287-7.907 0-1.751 0.62-3.177 1.645-4.297-0.177-0.401-0.719-2.031 0.141-4.235 0 0 1.339-0.427 4.4 1.641 1.281-0.355 2.641-0.532 4-0.541 1.36 0.009 2.719 0.187 4 0.541 3.043-2.068 4.381-1.641 4.381-1.641 0.859 2.204 0.317 3.833 0.161 4.235 1.015 1.12 1.635 2.547 1.635 4.297 0 6.145-3.74 7.5-7.296 7.891 0.556 0.479 1.077 1.464 1.077 2.959 0 2.14-0.020 3.864-0.020 4.385 0 0.416 0.28 0.916 1.104 0.755 6.4-2.093 10.979-8.093 10.979-15.156 0-8.833-7.161-16-16-16z"></path>
			</svg>
		</button>
	</div> -->
	<p class="signup mt-5">Don't have an account?
		<RouterLink to="/register" class="hover-text-heading weight-bold">Sign up</RouterLink>
	</p>
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