<script lang="ts">
import { defineComponent } from 'vue';
import {useCookies} from 'vue3-cookies'
import { RouterLink, RouterView } from 'vue-router';

export default defineComponent({
    data() {
        return {

        }
    },
    setup() {
        const {cookies} = useCookies();
        return {cookies};
    },
    methods: {
        login(e: Event) {
            // console.log(e.target.elements.username.value);
        }
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
                <input type="text" name="username" defaultValue="" placeholder="Username*"/>
                <input type="password" name="password" defaultValue="" placeholder="Password*"/>
            </div>
            <div class="login__submit">
                <input type="submit" value="Login"/>
            </div>
            <div class="login__links">
                <RouterLink to="/login">Frogot Password?</RouterLink>
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
    background-color: var(--color-background-mute);
    color: var(--color-text);
    border: var(--color-border);
    border-radius: 10px;
}

input[type="submit"] {
    width: fit-content;
    font-size: 15px;
    padding: 10px;
    margin: auto;
    color: var(--color-text);
    cursor: pointer;
}

::placeholder {
    color: var(--color-text);
}

hr {
    width: 50%;
    margin: auto;
}
</style>