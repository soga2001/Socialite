<script lang="ts">
import { defineComponent, ref, toHandlers } from 'vue';
import {useCookies} from 'vue3-cookies'
import { RouterLink, RouterView } from 'vue-router';
import { http } from '@/assets/http';
import {useStore} from '../store/store'

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
        const store = useStore()
        const {cookies} = useCookies();
        return {cookies};
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
                if(res.data.loggedIn === false) {
                    this.error = true
                    this.errMsg = "Username or Password is incorrect."
                    return;
                }
                this.cookies.set('access_token', res.data.access_token,res.data.at_lifetime);
                this.cookies.set('refresh_token', res.data.refresh_token, res.data.rt_lifetime);
                this.cookies.set('loggedIn', 'true', res.data.lifetime);
                this.cookies.set('user', res.data.user)
                this.$store.commit('authenticate', true)
                this.$store.commit('setUser', res.data.user)
                this.$router.push('/')
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
            <div class="login__credentials">
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
            </div>
        </form>
    </div>
</div>
</template>

<style scoped>
@import '@/assets/base.css';

.login {
    padding: 12vh 0;
    text-align: center;
    position: relative;
}

.login__main {
    width: 30vw;
    min-width: fit-content;
    margin: auto;
    border: 2px solid var(--color-border);
    border-radius: 10px;
    /* background-color: var(--color-background-soft); */
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
    color: rgb(255, 0, 0)
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

input[type="submit"] {
    width: fit-content;
    font-size: 15px;
    padding: 10px;
    margin: auto;
    color: var(--color-button);
    cursor: pointer;
    transform: transition 1s;
    border-radius: 0px !important;
    border-left: 2px solid var(--vt-c-divider-dark-1);
    border-right: 2px solid var(--vt-c-divider-dark-1);
}

input[type="submit"]:hover {
    background-color: var(--color-button-hover);
    padding: 10px 7px;
}

::placeholder {
    color: var(--color-text);
}

hr {
    width: 50%;
    margin: auto;
}
</style>