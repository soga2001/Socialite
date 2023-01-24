<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent } from 'vue';
import { useCookies } from 'vue3-cookies';
import type { User } from '../assets/interfaces';
import {Cookies} from 'quasar';
import Input from './Input.vue';


export default defineComponent({
    data() {
        return {
            image: null,
            caption: "",
            submitting: false,
            users: new Array<User>(),
            capt: ""
        };
    },
    setup() {
        const { cookies } = useCookies();
        return { cookies };
    },
    methods: {
        submit() {
            this.submitting = true;
            const formData = new FormData();
            if (this.image) {
                formData.append("image", this.image);
                formData.append("caption", this.caption);
                http.post("posts/post_content/", formData, {
                    headers: {
                        "Authorization": `Bearer ${Cookies.get("access_token")}`,
                        "Content-Type": "multipart/form-data"
                    }
                }).then((res) => {
                    this.submitting = false;
                    console.log(res.data);
                }).catch((err) => {
                    console.log(err);
                });
            }
        },
        mention() {
            if (this.caption) {
                const user = this.caption.match(/@\w+/g);
                const tag = this.caption.match(/#\w+/g);
                if (user) {
                    user.forEach((match) => {
                        const username = match.replace("@", "");
                        http.get(`users/username/${username}`).then((res) => {
                            if (res.data.success) {
                                console.log(res.data.users);
                                this.users = res.data.users;
                                // this.capt = this.caption.replace(match, `<a href="profile/user/${this.users[0].id}/">${match}</a>`)
                            }
                        }).catch((err) => {
                            console.log(err);
                        });
                    });
                }
            }
            else {
                this.users = new Array<User>();
            }
            // if (this.caption) {
            //   const matches = this.caption.match(/@\w+/g);
            //   if (matches !== null) {
            //     console.log('matches')
            //     matches.forEach((match) => {
            //       const username = match.replace("@", "")
            //       http.get(`users/username/${username}`).then((res) => {
            //         if (res.data.success) {
            //           console.log(res.data.users)
            //           this.users = res.data.users
            //           // this.caption = this.caption.replace(match, `<a href="/user/${user.id}">${match}</a>`)
            //         }
            //       }).catch((err) => {
            //         console.log(err)
            //       })
            //     })
            //   }
            //   else{
            //     this.users = new Array<User>()
            //   }
            // }
            // else {
            //   this.users = new Array<User>()
            // }
        }
    },
    created() {
    },
    mounted() {
    },
    watch: {
        caption() {
            this.mention();
        }
    },
    components: { Input }
})
</script>

<template>
  <div class="post">
    <div class="post__container">
      <q-avatar class="post__avatar" size="65px" >
          <img class="user__avatar" v-if="$store.state.user.profile.avatar" :src="$store.state.user.profile.avatar"/>
          <q-icon v-else size="65px" name="face" />
      </q-avatar>
      <form class="post__form" @submit.prevent="submit">
        <q-file v-model="image" clearable class="post__file" label="Upload an image" :dark="$store.state.dark" :color="$store.state.dark ? 'white': 'black'">
          <template v-slot:prepend>
            <q-icon name="cloud_upload" />
          </template>
        </q-file>
        <!-- <q-input
          clearable
          :dark="$store.state.dark"
          clear-icon="close"
          :color="$store.state.dark ? 'white' : 'black'"
          class="post__caption"
          v-model="caption"
          label="Caption"
          @change="mention"
          v-html="caption"
        >
        </q-input> -->
        <!-- <Input input_type="text" class="post__caption" @update:val="caption = $event" input_label="Caption"/> -->
        <Input @update:val="caption = $event" required input_type="text" input_label="Caption" class="post__caption" />
        <div v-if="users.length > 0" class="results" >
          <ul v-for="u in users">
            <li>{{ u.username }}</li>
          </ul>
        </div>
        <q-btn class="post__submit__btn" :loading="submitting" type="submit"  icon-right="send" push label="Post" :disable="image === null">
          <template v-slot:loading>
            <q-spinner-puff
              class="loading"
            />
          </template>
        </q-btn> 
      </form>
    </div>
  </div>
</template>

<style scoped>
.post {
  display: grid;
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  position: relative;
  width: 100%;
}
.post__container {
  padding: 10px 0px;
  display: grid;
  gap: 10px;
  grid-template-columns: 70px 1fr;
  position: relative;
  /* border: .5px solid var(--color-heading); */
  width: 100%;
}

/* textarea {
  
} */

.post__avatar {
  margin: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  justify-items: center;

}

.user__avatar {
  width: 65px;
  height: 65px;
  background-color: var(--color-heading);
  border-radius: 50%;
  border: 0;
}

.post__form {
  position: relative;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
  padding: 0 10px;
}

.post__file {
  width: fit-content;
  cursor: pointer;
  grid-column: auto / span 5;
  max-width: 100%;
}

.post__caption {
  /* border-bottom: 2px solid var(--color-border); */
  font-size: 15px;
  margin-top: 20px;
  grid-column: auto / span 5;
  color: var(--color-heading);
  position: relative;
}

.post__caption:active {
  color: var(--color-heading) !important;
}

.results {
  background-color: var(--color-background-soft);
  text-align: center;
}
.results ul {
  list-style: none;
  padding: 0px 20px;
  gap: 10px;
}


.post__submit__btn {
  grid-column: 4 / span 2;
  background-color: var(--color-border);
  /* padding: 10px 20px; */
  font-size: 15px;
}

.post__submit__btn:enabled {
  cursor: pointer;
}

.loading {
  color: var(--color-heading);
}

input {
  background-color: transparent;
  border: 0;
  color: var(--color-heading);
  width: 100%;
}

input[type="text"]:focus {
  border-bottom: 2px solid var(--color-border);
  outline: none;
}

::placeholder {
  color: var(--color-heading);
}
</style>
