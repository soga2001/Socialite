<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent } from 'vue';
import type { User } from '../assets/interfaces';
import Mention from './Mention.vue';
import ProfileIcon from '@/icons/i-profile.vue';


export default defineComponent({
    data() {
        return {
            image: null,
            caption: "",
            submitting: false,
            users: new Array<User>(),
            capt: "",
            chars: 0,
            imgURL: '',
        };
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
                        "Content-Type": "multipart/form-data",
                    }
                }).then((res) => {
                    this.submitting = false;
                    this.image = null;
                    this.imgURL = '';
                    this.caption = "";
                    console.log(res.data);
                }).catch((err) => {
                    console.log(err);
                });
            }
        },
        getImage(e: Event) {
            const target = e.target as HTMLInputElement;
            const file: File = (target.files as FileList)[0];
            this.image = file;
            this.imgURL = URL.createObjectURL(file);
        },
        deleteImg() {
          console.log('here')
          this.image = null;
          this.imgURL = '';
        }
    },
    created() {
    },
    mounted() {
    },
    watch: {
    },
    components: { Mention, ProfileIcon }
})
</script>

<template>
  <div class="post">
    <div class="post__container">
      <q-avatar class="post__avatar" size="65px" >
          <img class="user__avatar" v-if="$store.state.user.avatar" :src="$store.state.user.avatar"/>
          <!-- <q-icon v-else size="65px" name="face" /> -->
          <profile-icon v-else size="4rem" />
      </q-avatar>
      <div class="grid gap-3">
        <form class="post__form" autocorrect="on" autocomplete="off" @submit.prevent="submit">
          <Mention @update:charsLeft="chars = $event" @update:val="caption = $event" :value="caption" input_type="text" id="caption" input_label="Caption" class="post__caption" />
          <div class="flex gap-2 col-span-2">
            <label for="file" class="pointer">
              <i-upload-img size="2rem" fill="rgb(253, 137, 137)" stroke="rbg(253,137,137)"/>
              <input @change="getImage" type="file" id="file" style="display: none" name="image" accept="image/*" data-original-title="upload photos">
            </label>
            <i-upload-vid size="2rem" fill="rgb(253, 137, 137)" stroke="rgb(253, 137, 137)" />
          </div>
          <div class="col-5 col-span-3 flex flex-row-reverse items-center gap-2 bottom-0 right-0 mr-2">
            <q-btn class="right bottom-0 right-0 mr-2 btn btn-themed text-heading rounded px-7 py-2 weight-900" flat dense :loading="submitting" type="submit" push :disable="image === null">
              <div>
                <span class="text-white text-base weight-900 text-capitalize">Spill</span>
              </div>
              <template v-slot:loading>
                <q-spinner
                  color="grey-1"
                />
              </template>
            </q-btn> 
            <circular-progress v-if="chars" :val="chars" size="30px" />
          </div>
        </form>
        <div v-if="imgURL" class="flex rounded mr-3">
          <uploaded-img class="rounded border btn" @update:delete="deleteImg" :imgUrl="imgURL"/>
        </div>
      </div>
    </div> 
  </div>
</template>

<style scoped>
.post {
  display: grid;
  background-color: var(--color-background);
  position: relative;
  width: 100%;
  max-width: 600px;
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
  /* color: var(--color-heading); */
  position: relative;
}

.post__caption:active {
  color: var(--color-heading) !important;
}

.results {
  /* background-color: var(--color-background-soft);
  text-align: center;
  position: absolute; */
  position: absolute;
  width: 100%;
  bottom: 0;
  left: 0;
  overflow-y: auto;
  max-height: 100px;
  background-color: white; /* set the background color to match your design */
  border: 1px solid #ccc; /* add a border for visual separation */
  border-top: none; /* remove top border to align with input element */
}
.results ul {
  list-style: none;
  padding: 0px 20px;
  gap: 10px;
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
