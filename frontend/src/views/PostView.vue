<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent } from 'vue';
import { useCookies } from 'vue3-cookies';
import type { User } from '../assets/interfaces';

export default defineComponent({
  data() {
    return {
      image: null,
      caption: "",
    }
  },
  setup() {
    const {cookies} = useCookies();
    return {cookies}
  },
  methods: {
    uploadFile(e: any) {
      this.image = e.target.files[0] || null
    },
    submit() {
      const formData = new FormData()
      if(this.image) {
        formData.append('image', this.image)
        formData.append('caption', this.caption)
        http.post("posts/post_content/", formData, {
          headers: {
            "Authorization": `Bearer ${this.cookies.get("access_token")}`,
            "Content-Type": "multipart/form-data"
          }
        }).then((res) => {
          console.log(res.data)
        }).catch((err) => {
          console.log(err)
        })
      }

    }
  },
  created() {
  },
  mounted() {
  }
})
</script>

<template>
  <div class="post">
    <div class="post__container">
      <q-avatar size="65px">
        <img :src="$store.state.user.profile.avatar" >
      </q-avatar>
      <form class="post__input" v-on:submit.prevent="submit">
        <input multiple type="file" accept="image/*" @change="uploadFile" ref="file" class="post__file" />
        <input type="text" placeholder="caption" v-model="caption" class="post__caption"/>
        <input type="submit" value="Post" class="post__submit__btn" :disabled="image === null" />
      </form>
    </div>
  </div>
</template>

<style scoped>
.post {
  margin: 0px auto;
  display: grid;
  background-color: var(--color-background-soft);
  position: relative;
  min-width: 500px;
  max-width: 600px;
}
.post__container {
  padding: 20px;
  display: grid;
  gap: 10px;
  grid-template-columns: 70px 1fr;
  position: relative;
  border: .5px solid var(--color-heading);
  min-width: 500px;
  max-width: 600px;
}

/* textarea {
  
} */

.post__avatar {
  width: 50px;
  height: 50px;
  background-color: var(--color-heading);
  border-radius: 50%;
  border: 0;
}

.post__input {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
}

.post__file {
  width: fit-content;
  cursor: pointer;
  grid-column: auto / span 5;
}

.post__caption {
  border-bottom: 2px solid var(--color-border);
  font-size: 30px;
  margin-top: 20px;
  grid-column: auto / span 5;
}

.post__submit {
  padding: 10px;
  
}

.post__submit__btn {
  grid-column: 4 / span 2;
  background-color: var(--color-border);
  padding: 10px 20px;
  font-size: 15px;
}

.post__submit__btn:enabled {
  cursor: pointer;
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
