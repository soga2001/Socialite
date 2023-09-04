<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';

import { useToast } from "vue-toastification";

export default defineComponent({
    data() {
        return {
            full_name: ref(""),
            email: ref(""),
            username: ref(""),
            password: ref(""),
            cPass: ref(""),
            registering: false,
            domain: ["com", "net", "org", "int", "edu", "gov", "mil"],
            disable: false,
        };
    },
    setup() {
      const toast = useToast()
      return { toast}
    },
    methods: {
        checkEmail() {
          let check = false;
          if (this.email.length > 5) {
              const emailSplit = this.email.includes("@") ? this.email.split("@") : null;
              const domainSplit = emailSplit ? emailSplit[1].split(".")[1] : null;
              check = domainSplit ? this.domain.includes(domainSplit) : false;
          }
          return check;
        },
        async register() {
          this.updateDisableState
          if (!this.disable) {
            this.$notify({
              title: "Error!",
              text: "Please don't leave required field empty and make sure the password matches.",
              type: 'error',
              group: 'error',
            })
            return;
          }
          this.registering = true,
          await http.post("users/register/", {
            full_name: this.full_name,
            email: this.email,
            username: this.username,
            password: this.password,
            confirm_password: this.cPass
          }).then((res) => {
            if(res.data.success) {
              this.$notify({
                title: 'Registration Successful!',
                text: res.data.message,
                type: 'success',
                group: 'success',
              })
            }
            if (res.data.error) {
              this.$notify({
                title: 'Registration Unsuccessfull!',
                text: res.data.message,
                type: 'error',
                group: 'error',
              })
            }
          }).catch((err) => {
              console.log(err);
          });
          this.registering = false
        },
        async updateDisableState() {
          let disableBtn = this.username.length >= 1 && this.password.length >= 1;
          disableBtn = disableBtn && this.password == this.cPass;
          disableBtn = disableBtn && await this.checkEmail()
          disableBtn = disableBtn && this.full_name.length > 0 
          this.disable = disableBtn;
        },
        toastTesting() {
          
        }
    },
    created() {
    },
    watch: {
      full_name() {
        this.updateDisableState()
      },
      email: function() {
        this.updateDisableState()
      },
      username: function() {
        this.updateDisableState()
      },
      password: function() {
        this.updateDisableState()
      },
      cPass: function() {
        this.updateDisableState()
      }
    }
})
</script>

<template>
<div class="register grid">
    <div class="register__main">
        <h1 class="text-5xl weight-900 text-heading">Register</h1>
        <hr/>
        <form class="register__form" autocomplete="off" v-on:submit.prevent="register">
            <Input @update:val="full_name = $event" input_label="Full Name" id="fullname" class="fullname" input_type="text" required/>
            <Input @update:val="email = $event" input_label="Email" id="email" class="email" input_type="email" required/>
            <Input @update:val="username = $event" input_label="Username" id="username" class="username" input_type="text" required/>
            <Input @update:val="password = $event" input_label="Password" id="password" class="password" input_type="password" required/>
            <Input @update:val="cPass = $event" input_label="Confirm Password" id="c_password" class="c_password" input_type="password" required/>
            <div class="col-span-8">
              <p class="w-full">By Registering to use Socialite, you agree Sociliate using cookies to persist your data.</p>
            </div>
              <q-btn
                :loading="registering"
                dark-percentage
                unelevated
                class="submit"
                type="submit"
                :disable="!disable"
              >
                <div class="text-capitalize text-xl weight-900 text-heading">
                  Register
                </div>
                <template v-slot:loading>
                  <Loading />
                </template>
              </q-btn>
            <div class="submit">
              <span>Already have an account? <RouterLink to="/login" class="text-theme no-decor hover-underline weight-900">Sign in</RouterLink></span>
            </div>
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
    
    .fullname {
      grid-column: auto / span 8;
      // color: var(--color-heading) !important;
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
      grid-column: auto / span 8;
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
  // width: 10em;
  width: 100%;
  position: relative;
  height: 3.5rem;
  border: 3px ridge #ff00ff;
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
    box-shadow: inset 0px 0px 25px rgba(255, 0, 255, 1);
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