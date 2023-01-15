<script lang="ts">
import { defineComponent, ref, toHandlers } from 'vue';
import {useCookies} from 'vue3-cookies'
import { RouterLink, RouterView } from 'vue-router';
import { http } from '@/assets/http';
import {useStore} from '../store/store'
import { Cookies, useQuasar } from 'quasar';

export default defineComponent({
    data() {
        return {
            username: '',
            password: '',
            error: false,
            errMsg: ''
        }
    },
    setup() {
        const {cookies} = useCookies();
        return {cookies}
    },
    methods: {
        login() {
            if(this.username.length === 0 || this.password.length === 0) {
                this.error = true
                this.errMsg = "Please don't leave username or password blank!"
                return;
            }
            http.post('users/login/', {
                username: this.username,
                password: this.password
            }).then((res) => {
                if(res.data.error === true) {
                    this.error = true
                    this.errMsg = "Username or Password is incorrect."
                }
                else{
                    this.cookies.set('access_token', res.data.access_token, res.data.at_lifetime)
                    this.cookies.set('refresh_token', res.data.refresh_token, res.data.rt_lifetime)
                    this.cookies.set('loggedIn', 'true', res.data.at_lifetime)
                    this.cookies.set('user', res.data.user, res.data.at_lifetime)
                    this.$store.commit('authenticate', true)
                    this.$store.commit('setUser', res.data.user)
                    this.$router.push('/home')
                }
            }).catch((err) => {
                console.log(err)
            })
        }
    },
    created() {
        // console.log(import.meta.env)
    }
})
</script>

<template>
<div class="login">
    <div class="login__main">
        <h1 class="login__header">Login</h1>
        <hr/>
        <form class="login__form" v-on:submit.prevent="login">
            <!-- <div class="login__credentials">
                <input type="text" placeholder="Username*" v-model="username" required />
                <input type="password" placeholder="Password*" v-model="password" required />
            </div>
            <div class="login__submit">
                <input type="submit" value="Login"/>
            </div>
            <div class="login__error">
                <h3 class="login__errMsg">{{errMsg}}</h3>
            </div>
            <div class="login__links">
                <a disabled>Frogot Password?</a>
                <RouterLink to="/register">Create an Account</RouterLink>
            </div> -->
            <div class="login__credentials">
                <q-input
                    clearable
                    clear-icon="close"
                    filled
                    :dark="$store.state.dark"
                    :color="$store.state.dark ? 'white' : 'black'"
                    v-model="username"
                    label="Username*"
                    class="username"
                    type="text"
                    :rules="[val => !!val || 'Please enter a valid username']"
                />
                <!-- <input type="password" placeholder="Password*" class="password" v-model="password" required /> -->
                <q-input
                    filled
                    :dark="$store.state.dark"
                    :color="$store.state.dark ? 'white' : 'black'"
                    v-model="password"
                    label="Password*"
                    class="password"
                    type="password"
                    :rules="[val => !!val || 'Please Enter a password']"
                />
            </div>
            <div class="login__error">
                <h3 class="login__errMsg">{{errMsg}}</h3>
            </div>
            <div class="login__submit">
                <button type="submit" class="submit">
                    Login
                </button>
            </div>
            <div class="login__links">
                <a disabled>Forgot Password?</a>
                <RouterLink to="/register">Create an Account</RouterLink>
            </div>
        </form>
    </div>
</div>
</template>

<style scoped>
@import '@/assets/base.css';

.login {
    /* height: 100%; */
    display: flex;
    /* justify-content: center; */
    /* align-content: center; */
    text-align: center;
}

.login__main {
    /* min-width: 500px; */
    width: 100%;
    /* margin: auto; */
    border-radius: 10px;
}

.login__header {
    font-size: 70px;
}

.login__form {
    width: 100%;
    margin: auto;
    position: relative;
    padding: 10px;
}

.login__credentials {
    display: grid;
    padding: 20px;
}

.login__error {
    background-color: rgb(255, 0, 0, .2);
}

.login__errMsg {
    color: rgb(255, 0, 0);
    font-size: 20px;
}

.login__links {
    display: inline-flex;
}

a {
    padding: 10px;
}

input {
    margin: 10px 20px;
    font-size: 20px;
    padding: 10px;
    background-color: var(--color-background);
    color: var(--color-text);
    border: var(--color-border);
    border-radius: 10px;
}

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
}

button::after {
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

button::before {
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

button:hover::before, button:hover::after {
  transform: scale(0)
}

button:hover {
  box-shadow: inset 0px 0px 25px #1479EA;
}

::placeholder {
    color: var(--color-text);
}

hr {
    width: 50%;
    margin: auto;
}
</style>