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
            cPass: ref(''),
            errMsg: ref(''),
            error: ref(false),
            domain: ['com', 'net', 'org', 'int', 'edu', 'gov', 'mil']
        }
    },
    setup() {
        const {cookies} = useCookies()
        return {cookies}
    },
    methods: {
        checkForm() {
            return this.checkEmail() && this.checkPassword() && this.confirmPassword()
        },
        checkUsername() {
            if(this.username.length > 0) {
                return true
            }
            return false
        },
        checkPassword() {
            if(this.password.length > 0) {
                return true
            }
            return false
        },
        confirmPassword() {
            if(this.password === this.cPass && this.password.length > 0) {
                return true
            }
            return false
        },
        checkEmail() {
            let check = false
            if(this.email.length > 5) {
                const emailSplit = this.email.includes('@') ? this.email.split('@') : null
                const domainSplit = emailSplit ? emailSplit[1].split('.')[1] : null
                check = domainSplit ? this.domain.includes(domainSplit) : false 
            }
            return check
        },
        register() {
            if(!this.checkForm()) {
                this.error = true;
                this.errMsg = "Please don't leave required field empty and make sure the password matches.";
                return;
            }
            this.error = false
            http.post('users/register/', {
                first_name: this.fname,
                last_name: this.lname,
                email: this.email,
                username: this.username,
                password: this.password
            }).then((res) => {
                if(res.data.error) {
                    this.error = true
                    this.errMsg = res.data.message
                }
                else {
                    this.error = false
                    this.errMsg = ""
                    window.location.href = "/login"
                }
            }).catch((err) => {
                console.log(err)
            })
        }
    },
    created() {
    }
})
</script>

<template>
<div class="register">
    <div class="register__main">
        <h1 class="register__header">Register</h1>
        <hr/>
        <form class="register__form" v-on:submit.prevent="register">
            <!-- <input type="text" placeholder="First Name" class="fname" v-model="fname"/> -->
            <q-input
                clearable
                clear-icon="close"
                filled
                :dark="$store.state.dark"
                :color="$store.state.dark ? 'white' : 'black'"
                v-model="fname"
                label="First Name"
                class="fname"
                type="text"
            />
            <!-- <input type="text" placeholder="Last Name" class="lname" v-model="lname"/> -->
            <q-input
                clearable
                clear-icon="close"
                filled
                :dark="$store.state.dark"
                :color="$store.state.dark ? 'white' : 'black'"
                v-model="lname"
                label="Last Name"
                class="lname"
                type="text"
            />
            <!-- <input type="email" placeholder="Email*" class="email" v-model="email" required/> -->
            <q-input
                clearable
                clear-icon="close"
                filled
                :dark="$store.state.dark"
                :color="$store.state.dark ? 'white' : 'black'"
                v-model="email"
                label="Email*"
                class="email"
                type="email"
                :rules="[val => checkEmail() || 'Please enter a valid email']"
            />
            <!-- <input type="text" placeholder="Username*" class="username"  :change="checkUsername" v-model="username" required /> -->
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
                :rules="[val => checkUsername() || 'Please enter a valid email']"
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
                :rules="[val => checkPassword() || 'Please Enter a password']"
            />
            <!-- <input type="password" placeholder="Confirm Password*" class="c_password" v-model="cPass" required /> -->
            <q-input
                filled
                :dark="$store.state.dark"
                :color="$store.state.dark ? 'white' : 'black'"
                v-model="cPass"
                label="Confirm Password*"
                class="c_password"
                type="password"
                :rules="[val => confirmPassword() || 'Password does not match']"
            />
            <span v-if="error" class="errMsg">{{errMsg}}</span>
            <input type="submit" value="Register" class="submit" :disabled="!checkForm()"/>
        </form>
        
    </div>
</div>
</template>

<style scoped>
.register {
    padding: 3vh 0;
    display: flex;
    justify-content: center;
    align-content: center;
    text-align: center;
}
.fname, .lname {
    grid-column: auto / span 4;
    color: var(--color-heading) !important;
}

.email {
    grid-column: auto / span 8;
}

.username {
    grid-column: auto / span 8;
}

.password, .c_password {
    grid-column: auto / span 4;
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

.form__check {
    grid-column: 3 / span 2;
    color: var(--color-heading);
    font-size: 16px;
    text-align: left;
}


.register__main {
    min-width: fit-content;
    border: 2px solid var(--color-border);
    border-radius: 10px;
    padding: 20px;
    /* background-color: var(--color-background-soft); */
}

.register__header {
    font-size: 70px;
    color: var(--color-heading);
}

.register__form {
    display: grid;
    gap: 10px;
    grid-template-columns: repeat(8, 1fr);
    width: 100%;
    margin: auto;
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
    font-size: 20px;
    padding: 10px;
    background-color: var(--color-background);
    color: var(--color-text);
    border: var(--color-border);
    border-radius: 10px;
}


input[type="submit"]:hover {
    background-color: var(--color-button-hover);
    padding: 10px 7px;
}

::placeholder {
    color: var(--color-text);
}

.valid {
    color: green;
}

.invalid {
    color: red;
}

</style>