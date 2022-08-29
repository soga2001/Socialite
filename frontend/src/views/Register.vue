<script lang="ts">
import {useCookies} from 'vue3-cookies'
import { defineComponent } from 'vue';
import { http } from '@/assets/http';

export default defineComponent({
    data() {
        return {
        }
    },
    setup() {
        const {cookies} = useCookies()
        return {cookies}
    },
    methods: {
        register(e: Event) {
            http.post('users/register/', {
                data: {

                }
            })
        }
    },
    created() {
        // this.cookies.set("myCookies", 'cookies')  
        this.cookies.set('token', 'cookies')
    }
})
</script>

<template>
<div class="register">
    <div class="register__main">
        <h1 class="register__header">Register</h1>
        <hr/>
        <form class="register__form" v-on:submit.prevent="register">
            <div class="register__info">
                <input type="text" name="fname" placeholder="First Name"/>
                <input type="text" name="lname" placeholder="Last Name"/>
            </div>
            <div class="register__contact">
                <input type="email" name="email" defaultValue="" required placeholder="Email*"/>
            </div>
            <div class="register__credentials">
                <input type="text" name="username" defaultValue=""  required placeholder="Username*"/>
                <input type="password" name="password" defaultValue="" required placeholder="Password*"/>
            </div>
            
            <input type="submit" value="Register"/>
        </form>
    </div>
</div>
</template>

<style scoped>
@import '@/assets/base.css';

.register {
    padding: 12vh 0;
    text-align: center;
}

.register__main {
    width: 40vw;
    min-width: fit-content;
    margin: auto;
    border: 2px solid var(--color-border);
    border-radius: 10px;
    padding: 20px;
    /* background-color: var(--color-background-soft); */
}

.register__header {
    font-size: 70px;
}

.register__form {
    display: grid;
    grid-template-columns: 1fr;
    width: 100%;
    margin: auto;
    position: relative;
    padding: 10px;
}

.register__info {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
}

.register__contact {
    display: grid;
    grid-template-columns: 1fr;
}

.register__credentials {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
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