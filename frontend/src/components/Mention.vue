<script lang="ts">
import { defineComponent, ref, type CSSProperties } from 'vue';
import { http } from '@/assets/http';
import type { User } from '@/assets/interfaces';
import Item from './Item.vue';
import getCaretCoordinates from '@/assets/caretCoord'
import createIntersectionObserver from '@/assets/intersectionObserver';


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
            hasResults: false,
            resultsBelow: true,
            loading: false,

            resultPositionTop: 0,
            resultPositionBottom: 0,
            divHeight: 0,
            textareaWidth: 0,
        }
    },
    props: {
        input_type: {
            type: String,
            default: 'text'
        },
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
      resetData() {
      },
      reset() {
        this.val = ""
        this.charsLeft = 0
        this.savedUsers.clear()
        this.index = -1
        this.users = new Array<User>();
      },
      emitData() {
        this.$emit('update:val', this.val.trim())
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
        const input = this.$refs.textarea as HTMLInputElement;
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

          // console.log((space < this.index && (sub.charAt(this.index-1) == '' || sub.charAt(this.index-1) == ' ' || sub.charAt(this.index-1) == '\n')))

          if(this.index != -1 && (space < this.index && (sub.charAt(this.index-1) == '' || sub.charAt(this.index-1) == ' ' || sub.charAt(this.index-1) == '\n'))) {
            this.loading = true
            const user = this.val.substring(this.index, space < this.index ? this.val.length : space).match(/@\w+/g);
            if(user) {
              user.forEach(async (match) => {
                const username = match.replace("@", "");
                const u = this.savedUsers.get(username)
                if(u) { 
                  this.users = u
                  
                } else {
                  const tempUsers = await this.getUsers(username)
                  if( tempUsers) {
                    this.users = tempUsers
                    this.hasResults = true
                  }
                  else {
                    this.users = new Array<User>()
                    this.hasResults = false
                  }
                }
              });
            }
          } 
          else {
            this.users = new Array<User>()
          }
        }
      },
      async checkSavedUsers(e: any) {
          
          if(e.code === 'Space') {
            this.savedUsers.set(this.val.substring(this.index + 1, this.val.length), this.users)
            this.index = -1
            this.users = new Array<User>();
            return;
          }


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
        // console.log(end)
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
      handleKeyUp(e: any) {
        const arrowKeys = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'];
        if (arrowKeys.includes(e.key)) {
          this.checkSavedUsers(e)
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
            if (res.data.users) {
                tempUsers = res.data.users
            }
          }).catch((err) => {
            this.hasResults = false
        });
        return tempUsers
      },
      isElementAtTopOrBottom() {
        const mentionDiv = this.$refs.mentionDiv as HTMLDivElement;
        const results = this.$refs.results as HTMLDivElement;
        const div = this.$refs.div as HTMLElement;
        const area = this.$refs.textarea as HTMLElement
        if(results) {
          const height = results?.offsetHeight || 400
          const rect = mentionDiv.getBoundingClientRect();
          this.textareaWidth = area.getBoundingClientRect().width;
          this.divHeight = rect.height
          const isAtTop = rect.top >= 0 && rect.top <= height;
          const isAtBottom = rect.bottom >= 0 && (rect.bottom >= (window.innerHeight - height) || this.caretPosition.top >= (window.innerHeight - height)) ;
          this.resultPositionBottom = window.innerHeight - rect.bottom;
          this.resultPositionTop = rect.top 
          console.log(isAtTop, isAtBottom, this.resultPositionBottom, this.resultPositionTop, rect)
          if(isAtBottom && this.resultsBelow ) {
            this.resultsBelow = false;
          }
          else if(isAtTop && !this.resultsBelow && isAtTop !== isAtBottom) {
            this.resultsBelow = true;
          }
        }
      }
      
    },
    computed: {
      resultStyle(): CSSProperties {
        return {
          top: this.resultsBelow ? ((this.caretPosition.top + this.caretPosition.height <= (this.$refs.textarea as HTMLInputElement).offsetHeight) ? `${this.resultPositionTop  + this.caretPosition.top + this.caretPosition.height + 20}px` : ( this.resultPositionTop + ( this.$refs.textarea as HTMLInputElement).offsetHeight + 20) + 'px') : `auto`, 
          bottom: !this.resultsBelow ? `${ this.resultPositionBottom  + this.caretPosition.height + 20}px` : 'auto', 
          maxWidth: `${this.textareaWidth}px`,
          width: this.$q.screen.lt.sm ? '100%' : `${this.textareaWidth * .8}px`,
        }
      }
    },
    watch: {
      val(val) { 
        this.autogrow()
    
        if(val.length == 0) {
          this.hasResults = false
          this.savedUsers.clear()
          this.index = -1
          this.users = new Array<User>();
        }
        this.charsLeft = val.trim().length
        this.emitData()

      },
      caretPosition () {
        this.isElementAtTopOrBottom()
      },
    }
})

</script>

<template>
  <div class="main " ref="mentionDiv">
    <div class="relative w-full" ref="div">
        <textarea ref="textarea" :rows="rows" :placeholder="placeholder" :required="required"  autocomplete="off" @input="mention" @mouseup="checkSavedUsers" :maxlength="maxChars" @keyup="checkSavedUsers" v-model="val"  :type="type" id="input" class="input textl-xl"/>
        <!-- <div v-if="caretPosition.top" :style="{bottom: !resultsBelow ? `${300 + caretPosition.height + 20}px` : 'auto', top: resultsBelow ? ((caretPosition.top + caretPosition.height <= ($refs.textarea as HTMLInputElement).offsetHeight) ? `${caretPosition.top + caretPosition.height + 20}px` : (($refs.textarea as HTMLInputElement).offsetHeight + 20) + 'px') : 'auto', backgroundColor: !resultsBelow ? 'red' : 'transparent'}"  ref="results"  class="results absolute left-0 bg-theme box-shadow-soft flex flex-col shrink rounded-sm" >
          <div >
            <div v-if="users.length >0"  @click="replaceMention(user.username)" class=" pointer w-full" v-for="user in users" :key="user.id">
              <Item class="bg-hover-mute" avatarSize="3.5rem">
                  <template #avatar>
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
          </div> -->
          <div v-if="caretPosition.top" :style="resultStyle"  ref="results" class="results fixed bg-theme box-shadow-soft flex flex-col shrink rounded-sm">
            <div >
              <div v-if="users.length > 0" @click="replaceMention(user.username)" class=" pointer w-full" v-for="user in users" :key="user.id">
                <Item de class="bg-hover-mute" avatarSize="3.5rem">
                    <template #avatar>
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
  </div>
</template>

<style scoped>


textarea {
  padding: 10px 10px 0px 10px;
  height: fit-content;
  width: 100%;
  border: none;
  background: transparent;

  color: var(--color-heading);
  font-size: 25px;
  position: relative;
  resize: none;
  border: 0;
  outline: none;
  height: 100%;
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
  z-index: 999;
  max-height: 360px;
  overflow-y: auto;
  /* max-width: 70% !important; */
}

@media only screen and (max-width: 600px) {
  .results {
    width: 70%;
  }
}

::placeholder {
  color: var(--color-heading);
}

</style>