<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import type { User } from '@/assets/interfaces';


export default defineComponent({
    data() {
        return {
            type: this.input_type,
            label: this.input_label,
            val: ref(""),
            users: new Array<User>(),
            index: ref<number>(-1),
            rows: 1,
            charsLeft: this.maxChars,
            savedUsers: new Map<string, Array<User>>(),
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
        },
        numRows: {
          type: Number,
          default: 3
        },
        maxChars: {
          type: Number,
          default: 255,
        }
    },
    created() {
      
    },
    mounted() {
    },
    methods: {
      async replaceMention(username: string) {
        const at = this.index
        const space = this.val.indexOf(" ", this.index)
        const length = this.val.length
        const u = this.val.substring(at, space < at ? length : space)
        const beginning  = this.val.substring(0, at)
        const endIndex = this.index + u.length
        const ending = this.val.substring(endIndex)
        this.val = beginning + this.val.substring(at, space < at ? length : space).replace(u, '@' + username + ' ') + ending
        const input = document.getElementById('input') as HTMLInputElement;
        this.$emit('update:val', this.val);
        const data = await this.getUsers(username)
        await this.savedUsers.set(username, data)
        this.users = new Array<User>()
        this.$nextTick(() => {
          input.setSelectionRange(at + username.length + 2, at + username.length + 2);
        });
        input.focus();
        this.index = -1
      },
      async mention(e: any) {
        // if input is empty
        if(this.val.length == 0) {
          this.charsLeft = this.maxChars
          this.savedUsers.clear()
          this.index = -1
          this.users = new Array<User>();
        }
        else {
          const promise = await this.updateRows()
          const sub = this.val.substring(0, e.target.selectionStart)
          const at = sub.lastIndexOf('@')
          const space = sub.lastIndexOf(" ")
          if(at > space) {
            this.index = at
          }

          // if user spaces or the @ is removed
          if(e.key == ' ' || at == -1 || this.val.charAt(e.target.selectionStart-1) == " " || this.val.charAt(e.target.selectionStart-1) == '\n') {
            this.savedUsers.set(this.val.substring(this.index, space), this.users)
            this.index = -1
            this.users = new Array<User>();
          }

          if(this.index != -1 && (space < this.index && (sub.charAt(this.index-1) == '' || sub.charAt(this.index-1) == ' ' || sub.charAt(this.index-1) == '\n'))) {
            const user = this.val.substring(this.index, space < this.index ? this.val.length : space).match(/@\w+/g);
            if(user) {
              user.forEach(async (match) => {
                const username = match.replace("@", "");
                const u = this.savedUsers.get(username)
                if(u) { 
                  this.users = u
                  
                } else {
                  const tempUsers = await this.getUsers(username)
                  if( tempUsers)
                    this.users = tempUsers
                  // this.getUsers(username)
                }
              });
            }
          } 
        }
      },
      checkSavedUsers(e: any) {
        if(this.savedUsers.size == 0) {
          return
        }

        const sub = this.val.substring(0, e.target.selectionStart)
        const start = sub.lastIndexOf('@')
        this.index = start
        let end = this.val.indexOf(" ", start)
        if(end < e.target.selectionStart && start < end) {
          this.users = new Array<User>();
          return
        }
        if(end == -1 || start > end) {
          end = this.val.length
        }
        const username = this.val.substring(start + 1, end)
        const u = this.savedUsers.get(username.trim())
        if(u) {
          this.users = u
        }
      },
      updateRows() {
        this.rows = Math.min(this.val.split("\n").length, this.numRows);
        this.charsLeft = this.maxChars - this.val.length
        this.$emit('update:val', this.val)
        this.$emit('update:charsLeft', this.charsLeft)
      },
      async getUsers(username: String) {
        let tempUsers = new Array<User>()
        await http.get(`users/username/${username}/`).then((res) => {
            if (res.data.success) {
                tempUsers = res.data.users
            }
          }).catch((err) => {
              console.log(err);
        });
        return tempUsers
      }
      
    },
    watch: {
      val(val) { 
        if(val.length == 0) {
          this.charsLeft = this.maxChars
          this.savedUsers.clear()
          this.index = -1
          this.users = new Array<User>();
          this.$emit('update:charsLeft', this.charsLeft)
        }
      }

    }
})

</script>

<template>
  <div class="main">
    <div class="wave-group">
        <!-- <input :required="required" @mouseup="mention" @keyup="mention" v-model="val"  :type="type" id="input" class="input" /> -->
        <textarea :rows="rows" :required="required" :maxlength="maxChars" autocomplete="off" @input="mention" @mouseup="checkSavedUsers"  @keyup="checkSavedUsers" v-model="val"  :type="type" id="input" class="input"></textarea>
        <label class="label">
            <span class="label-char" v-for="(char, index) in label" :key="index" :style="{'--index': index }">{{ char == ' ' ? '&nbsp' : char }}</span>
        </label>
    </div>
    <div class="results" v-if="users.length">
        <div @click="replaceMention(user.username)" class="result__map" v-for="user in users" :key="user.id">
          <q-item>
            <q-item-section avatar>
              <img class="avatar" v-if="user.avatar" :src="user.avatar"/>
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
  min-height: 50px;
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

textarea {
  color: var(--color-heading);
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
  /* border: none;  */
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 999;
  max-height: 200px;
  overflow-y: auto;
  width: 100%;
}

.result__map:nth-child(odd) {
  background-color: var(--color-background-mute);
}

::placeholder {
  color: var(--color-heading);
}

</style>