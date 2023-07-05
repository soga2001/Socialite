<script lang="ts">
import {useCookies} from 'vue3-cookies'
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import Input from '@/components/Input.vue';

export default defineComponent({
    data() {
        return {
            fname: ref(""),
            lname: ref(""),
            email: ref(""),
            username: ref(""),
            password: ref(""),
            cPass: ref(""),
            errMsg: ref(""),
            error: ref(false),
            domain: ["com", "net", "org", "int", "edu", "gov", "mil"]
        };
    },
    setup() {
        const { cookies } = useCookies();
        return { cookies };
    },
    methods: {
        checkForm() {
            return this.checkEmail() && this.checkPassword() && this.confirmPassword() && this.lname.length > 0 && this.fname.length > 0 && this.checkUsername();
        },
        checkUsername() {
            if (this.username.length > 0) {
                return true;
            }
            return false;
        },
        checkPassword() {
            if (this.password.length > 0) {
                return true;
            }
            return false;
        },
        confirmPassword() {
            if (this.password === this.cPass && this.password.length > 0) {
                return true;
            }
            return false;
        },
        checkEmail() {
            let check = false;
            if (this.email.length > 5) {
                const emailSplit = this.email.includes("@") ? this.email.split("@") : null;
                const domainSplit = emailSplit ? emailSplit[1].split(".")[1] : null;
                check = domainSplit ? this.domain.includes(domainSplit) : false;
            }
            return check;
        },
        register() {
            if (!this.checkForm()) {
                this.error = true;
                this.errMsg = "Please don't leave required field empty and make sure the password matches.";
                return;
            }
            this.error = false;
            this.errMsg = "";
            http.post("users/register/", {
                first_name: this.fname,
                last_name: this.lname,
                email: this.email,
                username: this.username,
                password: this.password,
                confirm_password: this.cPass
            }).then((res) => {
                if (res.data.error) {
                    this.error = true;
                    this.errMsg = res.data.message;
                }
                else {
                    this.error = false;
                    this.errMsg = "";
                    window.location.href = "/login";
                }
            }).catch((err) => {
                console.log(err);
            });
        }
    },
    created() {
    },
    components: { Input }
})
</script>

<template>
<div class="register">
    <div class="register__main">
        <h1 class="register__header">Register</h1>
        <hr/>
        <form class="register__form" autocomplete="off" v-on:submit.prevent="register">
            <Input
                @update:val="fname = $event"
                input_label="First Name*"
                class="fname"
                input_type="text" required
                id="fname"
                />
            <Input @update:val="lname = $event" input_label="Last Name*" id="lname" class="lname" input_type="text" required/>
            <Input @update:val="email = $event" input_label="Email*" id="email" class="email" input_type="email" required/>
            <Input @update:val="username = $event" input_label="Username*" id="username" class="username" input_type="text" required/>
            <Input @update:val="password = $event" input_label="Password*" id="password" class="password" input_type="password" required/>
            <Input @update:val="cPass = $event" input_label="Confirm Password*" id="c_password" class="c_password" input_type="password" required/>
            <span v-if="error" class="errMsg">{{errMsg}}</span>
            <button type="submit" class="submit" :disabled="!checkForm()">
                Register
            </button>
        </form>
        
    </div>
</div>
</template>

<style scoped lang="scss">
.register {
  padding: 20px;
  display: flex;
  justify-content: center;
  align-content: center;
  text-align: center;
  
  &__main {
    min-width: fit-content;
    border-radius: 10px;
    // background-color: var(--color-background-soft);
  }
  
  &__header {
    font-size: 70px;
    color: var(--color-heading);
  }
  
  &__form {
    display: grid;
    gap: 20px;
    grid-template-columns: repeat(8, 1fr);
    width: 100%;
    margin: auto;
    padding: 10px;
    
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
  }
  
  &__info {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
  
  &__contact {
    display: grid;
    grid-template-columns: 1fr;
  }
  
  &__credentials {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
}

/* input {
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

.valid {
  color: green;
}

.invalid {
  color: red;
}



</style>