<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import type { User } from '@/assets/interfaces';
import Item from './Item.vue';
import getCaretCoordinates from '@/assets/caretCoord'


export default defineComponent({
    data() {
        return {
            type: this.input_type,
            label: this.input_label,
            val: ref(""),
            users: new Array<User>(),
            index: ref<number>(-1),
            charsLeft: 0,
            savedUsers: new Map<string, Array<User>>(),

            caretPosition: {top: 0, height: 0},
        }
    },
    props: {
        input_type: {
            type: String,
            default: 'text'
        },
        // input_label: {
        //     type: String,
        //     required: true
        // },
        required: {
            type: Boolean,
            default: false,
        },
        maxChars: {
          type: Number,
          default: 255,
        },
        textarea: {
          type: Boolean,
          default: true,
        },
        placeholder: {
          type: String,
          default: "Spill your guts here",
        },
        rows: {
          type: Number,
          default: 1,
        }
    },
    components: {Item},
    created() {
      console.log(this.rows)
    },
    mounted() {
    },
    methods: {
      getCoordinates() {
        const textarea = this.$refs.textarea as HTMLInputElement;
        if (!textarea) return;

        const selectionEnd = textarea.selectionEnd || 0;

        const caret = getCaretCoordinates(textarea, selectionEnd);
        this.caretPosition = {
          top: caret.top,
          height: caret.height,
        };
      },
      reset() {
        this.val = ""
        this.charsLeft = 0
        this.savedUsers.clear()
        this.index = -1
        this.users = new Array<User>();
      },
      emitData() {
        this.$emit('update:val', this.val)
        this.$emit('update:charsLeft', this.charsLeft)
      },
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
        this.emitData()
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
          this.charsLeft = 0
          this.savedUsers.clear()
          this.index = -1
          this.users = new Array<User>();
        }
        else {
          // const promise = await this.updateRows()
          const sub = this.val.substring(0, e.target.selectionStart)
          const at = sub.lastIndexOf('@')
          const space = sub.lastIndexOf(" ")
          const enter = sub.lastIndexOf("\n")
          if(at > space) {
            this.index = at
          }

          if(at < enter) {
            this.index = -1;
          }

          // if user spaces or the @ is removed
          if(e.key == ' ' || at == -1 || this.val.charAt(e.target.selectionStart-1) == " " || at < enter) {
            this.savedUsers.set(this.val.substring(this.index + 1, space), this.users)
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
      async checkSavedUsers(e: any) {
        if(this.val.length == 0) {
          this.emitData()
        }
        this.getCoordinates()

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
      autogrow() {
        const textarea = this.$refs.textarea as HTMLInputElement;
        textarea.style.height = "auto"
        textarea.style.height = textarea.scrollHeight + 'px'
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
        this.autogrow()
        if(val.length == 0) {
          this.savedUsers.clear()
          this.index = -1
          this.users = new Array<User>();
        }
        this.charsLeft = (val.trimStart(" ")).length
        this.emitData()
      },
    }
})

</script>

<template>
  <div class="main">
    <div class="wave-group">
        <textarea ref="textarea" :rows="rows" :placeholder="placeholder" :required="required"  autocomplete="off" @input="mention" @mouseup="checkSavedUsers" :maxlength="maxChars"  @keyup="checkSavedUsers" v-model="val"  :type="type" id="input" class="input"/>
        <div :style="{ top: `${caretPosition.top + caretPosition.height}px` }" class="results rounded-sm" v-if="users.length">
          <div @click="replaceMention(user.username)" class="result__map pointer" v-for="user in users" :key="user.id">
            <Item avatarSize="3.5rem">
                <template #avatar>
                    <!-- <img src="https://avatarairlines.com/wp-content/uploads/2020/05/Male-placeholder.jpeg" alt="John Doe" class="rounded-full" /> -->
                    <img v-if="user.avatar" :src="user.avatar" alt="John Doe" class="rounded-full" />
                    <q-icon size="50px" v-else name="account_circle" class="rounded-full" />
                </template>
                <template #title>
                  <span class="text-xl text-heading weight-900">{{user.first_name + ' ' + user.last_name}}</span> 
                </template>
                <template #caption>@{{ user.username }}</template>
            </Item>
          </div>
      </div>
    </div>
  </div>
</template>

<style scoped>


textarea {
  font-size: 20px;
  padding: 10px 10px 10px 5px;
  display: block;
  width: 100%;
  border: none;
  background: transparent;

  color: var(--color-heading);
  position: relative;
  resize: none;
  border: 0;
  outline: none;
  overflow: scroll;
  overflow-y: scroll;
  max-height: 10rem;
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
  /* border: 2px solid black; */
  background-color: var(--color-background);
  z-index: 999;
  -webkit-box-shadow: 0 0 10px var(--color-heading);
  box-shadow: 0 0 10px var(--color-heading);
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 999;
  max-height: 300px;
  overflow-y: auto;
  width: 100%;
}

/* .result__map:nth-child(odd) {
  background-color: var(--color-background-mute);
} */

::placeholder {
  color: var(--color-heading);
}

</style>