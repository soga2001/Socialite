<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent } from 'vue';
import { useCookies } from 'vue3-cookies';

export default defineComponent({
  data() {
    return {
      image: null,
      caption: ""
    }
  },
  setup() {
    const {cookies} = useCookies();
    return cookies
  },
  methods: {
    uploadFile(e: any) {
      this.image = e.target.files[0]
    },
    submit() {
      const formData = new FormData()
      console.log(this.image)
      if(this.image) {
        formData.append('image', this.image)
        formData.append('caption', this.caption)
        http.post("posts/post_content/", formData, {
          headers: {
            // "Authorization": `Bearer ${cookies.get("access_token")}`
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

  }
})
</script>

<template>
  <div class="post">
    <img src="" class="post__avatar" />
    <form class="post__input" v-on:submit.prevent="submit">
      <input type="file" accept="image/*" @change="uploadFile" ref="file" class="post__file" />
      <input type="text" placeholder="caption" v-model="caption" class="post__caption"/>
      <div class="post__submit">
        <input type="submit" value="Post" class="post__submit__btn" />
      </div>
    </form>
    <!-- <img v-if="image" :src="image"/> -->
  </div>
</template>

<style scoped>
.post {
  padding: 20px;
  display: grid;
  grid-template-columns: 60px 1fr;
  position: relative;
  border-bottom: 2px solid var(--color-border);
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
}

.post__file {
  width: fit-content;
  cursor: pointer;
}

.post__caption {
  border-bottom: 2px solid var(--color-border);
  font-size: 30px;
  margin-top: 20px;
}

.post__submit {
  padding: 10px;
}

.post__submit__btn {
  width: fit-content;
  float: right;
  background-color: var(--color-border);
  padding: 10px 20px;
  font-size: 15px;
  cursor: pointer;
}

input {
  background-color: transparent;
  border: 0;
  color: var(--color-heading);
  width: 100%;
}

input:focus {
  border-bottom: 2px solid var(--color-border);
  outline: none;
}

input:active {
  border: none;
  border-bottom: 2px solid var(--color-border);
}

::placeholder {
  color: var(--color-heading);
}
</style>
