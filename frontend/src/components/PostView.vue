<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent } from 'vue';
import { useCookies } from 'vue3-cookies';
import type { User } from '../assets/interfaces';
import {Cookies} from 'quasar';

export default defineComponent({
  data() {
    return {
      image: null,
      caption: "",
      submitting: false,
      users: new Array<User>(),
    }
  },
  setup() {
    const {cookies} = useCookies();
    return {cookies}
  },
  methods: {
    submit() {
      this.submitting = true
      const formData = new FormData()
      if(this.image) {
        formData.append('image', this.image)
        formData.append('caption', this.caption)
        http.post("posts/post_content/", formData, {
          headers: {
            "Authorization": `Bearer ${Cookies.get("access_token")}`,
            "Content-Type": "multipart/form-data"
          }
        }).then((res) => {
          this.submitting = false
          console.log(res.data)
        }).catch((err) => {
          console.log(err)
        })
      }
    },
    mention() {
      console.log("mention")
      if (this.caption) {
        const regex = /@([a-zA-Z0-9_]+)/g;
        const matches = this.caption.match(regex);
        console.log(matches)
        if (matches !== null) {
          matches.forEach((match) => {
            const username = match.replace("@", "")
            http.get(`users/username/${username}`).then((res) => {
              if (res.data.success) {
                console.log(res.data.users)
                const user = res.data.users
                // this.caption = this.caption.replace(match, `<a href="/user/${user.username}">${match}</a>`)
              }
            }).catch((err) => {
              console.log(err)
            })
          })
        }
      }
    }
  },
  created() {
  },
  mounted() {
  },
  watch: {
    caption() {
      this.mention()
    }
  }
})
</script>

<template>
  <div class="post">
    <div class="post__container">
      <q-avatar class="post__avatar" size="65px" >
          <img class="user__avatar" v-if="$store.state.user.profile.avatar" :src="$store.state.user.profile.avatar"/>
          <q-icon v-else size="65px" name="face" />
      </q-avatar>
      <form class="post__input" @submit.prevent="submit">
        <q-file v-model="image" clearable class="post__file" label="Upload an image" :dark="$store.state.dark" :color="$store.state.dark ? 'white': 'black'">
          <template v-slot:prepend>
            <q-icon name="cloud_upload" />
          </template>
        </q-file>
        <q-input
          clearable
          :dark="$store.state.dark"
          clear-icon="close"
          :color="$store.state.dark ? 'white' : 'black'"
          class="post__caption"
          v-model="caption"
          label="Caption"
          @change="mention"
        />
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
  min-width: 500px;
  max-width: 600px;
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

.post__input {
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
  border-bottom: 2px solid var(--color-border);
  font-size: 15px;
  margin-top: 20px;
  grid-column: auto / span 5;
  color: var(--color-heading);
}

.post__caption:active {
  color: var(--color-heading) !important;
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
