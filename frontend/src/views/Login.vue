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
            errMsg: ""
        };
    },
    setup() {
        const { cookies } = useCookies();
        return { cookies };
    },
    methods: {
        async login() {
            if (this.username.length === 0 || this.password.length === 0) {
                this.error = true;
                this.errMsg = "Please don't leave username or password blank!";
                return;
            }

            // Crypter.decryption(dis)
            // const u = Crypter.encrypter(this.username);
            // const p = Crypter.encrypter(this.password);
            // console.log(Crypter.decrypter(u), Crypter.decrypter(p));
            // console.log()
            http.post("users/login/", {
                // username: Crypter.encrypt(this.username),
                // password: Crypter.encrypt(this.password)
                username: this.username,
                password: this.password,
            }, {
            }).then(async (res) => {
                if (res.data.error === true) {
                    this.error = true;
                    this.errMsg = "Username or Password is incorrect.";
                }
                else {
                    
                    await get_user_from_cookie()
                    this.$store.commit("authenticate", true);
                    // this.cookies.set("loggedIn", "true", res.data.at_lifetime);
                    this.$router.push("/home");
                    // get_csrf_token();
                }
            }).catch((err) => {
                console.log(err);
            });
        },
    },
    created() {
        // console.log(import.meta.env)
    },
    components: { Input },
})
</script>

<template>
<div class="login">
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
</div>
</template>

<style scoped>
@import '@/assets/base.css';

.login {
    padding: 20px;
    display: flex;
    justify-content: center;
    align-content: center;
    text-align: center;
}

.login__main {
    min-width: fit-content;
    border-radius: 10px;
}

.login__header {
    font-size: 70px;
    color: var(--color-heading);
}

.login__form {
    display: grid;
    gap: 10px;
    grid-template-columns: repeat(8, 1fr);
    width: 100%;
    margin: auto;
    padding: 10px;
}

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

.login__links {
    grid-column: 2 / span 6;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
}

.login__links a {
    text-decoration: none;
    padding: 10px;
    border: 1px solid var(--color-text);
    color: var(--color-text);
}

.login__links a:hover {
    background-color: var(--color-text);
    color: var(--color-background);
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