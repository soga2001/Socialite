<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import type { User } from '@/assets/interfaces';


export default defineComponent({
    data() {
        return {
            type: this.input_type,
            label: this.input_label,
            val: ref(''),
            users: new Array<User>(),
            index: null,
            // required: this.required,
        }
    },
    props: {
        input_type: {
            type: String,
            default: 'text'
        },
        input_label: {
            type: String,
            required: true
        },
        required: {
            type: Boolean,
            default: false,
        }
    },
    created() {
      
    },
    mounted() {
    },
    methods: {
      handleChange(e: any) {
        // this.$emit('update:input', e.target.value)
        console.log(e.target.selectionStart)
      },
      mention() {
        // console.log(this.val.trim())
        if (this.val) {
          if(this.val.substring(this.val.length - 1) == ' ') {
            this.users = new Array<User>();
            return
          }
          const at = this.val.lastIndexOf('@')
          const space = this.val.lastIndexOf(' ')
          const user = this.val.substring(at, space < at ? this.val.length : space).match(/@\w+/g);
          const u = this.val.substring(at + 1, space < at ? this.val.length : space)
          if (user) {
              user.forEach((match) => {
                  const username = match.replace("@", "");
                  http.get(`users/username/${username}`).then((res) => {
                      if (res.data.success) {
                          // console.log(res.data.users);
                          this.users = res.data.users;
                      }
                  }).catch((err) => {
                      console.log(err);
                  });
              });
          }
        //   if(u) {
        //     http.get(`users/username/${u}`).then((res) => {
        //         if (res.data.success) {
        //             // console.log(res.data.users);
        //             this.users = res.data.users;
        //         }
        //     }).catch((err) => {
        //         console.log(err);
        //     });
        //   }
        }
        else {
            this.users = new Array<User>();
        }
      },
      replaceMention(username: string) {
        const at = this.val.lastIndexOf('@')
        const space = this.val.lastIndexOf(' ')
        const length = this.val.length
        const u = this.val.substring(at, space < at ? length : space)
        this.val = this.val.substring(0, at) + this.val.substring(at, space < at ? length : space).replace(u, '@' + username + ' ')
        this.users = new Array<User>();
        console.log(this.users)
        document.getElementById('input')?.focus()
        this.index = null
      },
      keyup(e: any) {
        // this.mention();
        console.log(e.target.selectionStart)
      }
    },
    watch: {
      val: function(val: any) {
        if(val.substring(val.length - 1) == '@' || val.substring(val.length - 2) == ' ') {
          this.index = val.lastIndexOf('@')
        }
        if(val.substring(val.length - 1) == ' ') {
          this.index = null
          this.users = new Array<User>();
        }
        if(this.index != null) {
          // console.log(this.index)
          this.mention()
        }
        this.$emit('update:input', val)
        
      }
    }
})

</script>

<template>
  <div class="main">
    <div class="wave-group">
        <input :required="required" @keyup="keyup" v-model="val" @input="(e: any) => $emit('update:val', e.target.value)" :type="type" id="input" class="input" />
        <label class="label">
            <span class="label-char" v-for="(char, index) in label" :key="index" :style="{'--index': index }">{{ char == ' ' ? '&nbsp' : char }}</span>
        </label>
    </div>
    <div class="results" v-if="users.length">
        <div @click="replaceMention(user.username)" class="result__map" v-for="user in users" :key="user.id">
          <q-item>
            <q-item-section avatar>
              <img class="avatar" v-if="user.profile.avatar" :src="user.profile.avatar"/>
              <q-icon size="50px" v-else name="o_person" class="avatar__icon" />
            </q-item-section>

            <q-item-section>
              <q-item-label>{{ user.first_name + ' ' + user.last_name }}</q-item-label>
              <q-item-label caption class="username">@{{ user.username }}</q-item-label>
            </q-item-section>
          </q-item>
        </div>
    </div>
  </div>
</template>

<style scoped>

.main {
  overflow: visible;
  height: 50px;
  display: grid;
  grid-template-columns: 1fr;
}
.wave-group {
  position: relative;
  width: 100%;
}

.wave-group .input {
  font-size: 16px;
  padding: 10px 10px 10px 5px;
  display: block;
  width: 100%;
  border: none;
  border-bottom: 1px solid #515151;
  background: transparent;
}

.wave-group .input:focus {
  outline: none;
}

.wave-group .label {
  color: var(--color-text);
  font-size: 18px;
  font-weight: normal;
  position: absolute;
  pointer-events: none;
  left: 5px;
  top: 10px;
  display: flex;
}


.wave-group .label-char {
  transition: 0.2s ease all;
  transition-delay: calc(var(--index) * .05s);
}

.wave-group .input:focus ~ label .label-char,
.wave-group .input:valid ~ label .label-char {
  transform: translateY(-20px);
  font-size: 14px;
  /* color: #5264AE; */
  color: var(--color-heading);
}

.wave-group .bar {
  position: relative;
  display: block;
  width: 100%;
}

.wave-group .bar:before,.wave-group .bar:after {
  content: '';
  height: 2px;
  width: 0;
  bottom: 1px;
  position: absolute;
  background: #5264AE;
  transition: 0.2s ease all;
  -moz-transition: 0.2s ease all;
  -webkit-transition: 0.2s ease all;
}

.wave-group .bar:before {
  left: 50%;
}

.wave-group .bar:after {
  right: 50%;
}

.wave-group .input:focus ~ .bar:before,
.wave-group .input:focus ~ .bar:after {
  width: 50%;
}

input {
  color: var(--color-heading);
  position: relative;
}

span {
  white-space: pre-line;
}


.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.username {
  color: var(--color-text);
}

.results {
  background-color: var(--color-background-soft);
  z-index: 999;
  border: none;
}

.result__map:nth-child(odd) {
  background-color: var(--color-background-mute);
}

</style>