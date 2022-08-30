<script lang="ts">
import {useCookies} from 'vue3-cookies'
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';

export default defineComponent({
    data() {
        return {
            fname: ref(''),
            lname: ref(''),
            email: ref(''),
            username: ref(''),
            password: ref(''),
            error: ref(false),
            errMsg: ref('')
        }
    },
    setup() {
        const {cookies} = useCookies()
        return {cookies}
    },
    methods: {
        register() {
            if(this.username.length === 0 || this.password.length === 0) {
                this.error = true
                this.errMsg = "Please don't leave username or password blank!"
                console.log(this.errMsg)
                return;
            }
            if(!this.email.includes("@")) {
                this.error = true
                this.errMsg = "Please enter a valid email!"
                return;
            }
            this.error = false
            this.errMsg = ""
            http.post('users/register/', {
                first_name: this.fname,
                last_name: this.lname,
                email: this.email,
                username: this.username,
                password: this.password
            }).then((res) => {
                console.log(res.data)
            }).catch((err) => {
                console.log(err)
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
                <input type="text" placeholder="First Name" v-model="fname"/>
                <input type="text" placeholder="Last Name" v-model="lname"/>
            </div>
            <div class="register__contact">
                <input type="email" placeholder="Email*" v-model="email" required/>
            </div>
            <div class="register__credentials">
                <input type="text" placeholder="Username*" v-model="username" required />
                <input type="password" placeholder="Password*" v-model="password" required />
            </div>
            <input type="submit" value="Register"/>
        </form>
        <span v-if="error">{{errMsg}}</span>
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
    color: var(--color-button);
    background-color: var(--color-button-background);
}

::placeholder {
    color: var(--color-text);
}

hr {
    width: 50%;
    margin: auto;
}
</style>