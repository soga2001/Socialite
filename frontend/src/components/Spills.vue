<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent } from 'vue';
import type { User } from '../assets/interfaces';
import Mention from './Mention.vue';
import ProfileIcon from '@/icons/i-profile.vue';


export default defineComponent({
    data() {
        return {
            image: null as File | null,
            caption: "",
            submitting: false,
            users: new Array<User>(),
            capt: "",
            chars: 0,
            imgURL: '',
            disabled: true,
        };
    },
    props: {
      placeholder: {
        type: String,
        default: "Spill your guts here",
      },
      btnString: {
        type: String,
        default: "Spill",
      },
      isComment: {
        type: Boolean,
        default: false,
      },
      spillId: {
        type: Number,
        default: 0,
      },
    },
    computed: {
      
    },
    methods: {
        submit() {
            this.submitting = true;
            const formData = new FormData();
            if (this.image && !this.isComment) {
              formData.append("caption", this.caption);
              formData.append("image", this.image);
              http.post("posts/post_content/", formData, {
                  headers: {
                      "Content-Type": "multipart/form-data",
                  }
              }).then((res) => {
                  this.submitting = false;
                  this.image = null;
                  this.imgURL = '';
                  this.caption = "";
              }).catch((err) => {
                  console.log(err);
              });
            }
            else {
              if(!this.isComment) {
                return
              }
              formData.append("comment", this.caption);
              http.post(`comments/comment/${this.spillId}/`, formData, {
                  headers: {
                      "Content-Type": "multipart/form-data",
                  }
              }).then((res) => {
                  this.submitting = false;
                  this.caption = "";
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
      chars(chars) {
        if(chars > 0 && chars <= 255) {
          this.disabled = false;
        }
        else {
          this.disabled = true;
        }
      }
    },
    components: { Mention, ProfileIcon }
})
</script>

<template>
  <div class="post bg-transparent">
    <div class="post__container">
      <q-avatar class="post__avatar" size="65px" >
          <img class="user__avatar" v-if="$store.state.user.avatar" :src="$store.state.user.avatar"/>
          <!-- <q-icon v-else size="65px" name="face" /> -->
          <profile-icon v-else size="4rem" />
      </q-avatar>
      <div class="grid gap-3">
        <form class="relative cols-5 grid gap-2 p-2" autocorrect="on" autocomplete="off" @submit.prevent="submit">
          <Mention @update:charsLeft="chars = $event" @update:val="caption = $event" :value="caption" input_type="text" id="caption" :placeholder="placeholder" class="post__caption h-full" />
          <div class="flex w-full gap-2 col-span-2">
            <label :hidden="isComment" for="file" class="pointer btn-transition btn-hover pt-2 px-2 rounded">
              <i-upload-img  size="1.5rem" fill="rgb(253, 137, 137)" stroke="rbg(253,137,137)"/>
              <input @change="getImage" type="file" id="file" style="display: none" name="image" accept="image/*" data-original-title="upload photos"/>
            </label>
            <label :hidden="isComment" for="file" class="pointer btn-transition btn-hover pt-2 px-2 rounded">
              <i-upload-vid size="1.5rem" fill="rgb(253, 137, 137)" stroke="rgb(253, 137, 137)" />
              <input @change="getImage" type="file" id="file" style="display: none" name="image" accept="image/*" data-original-title="upload photos"/>
            </label>
          </div>
          <div class="col-5 col-span-3 flex flex-row-reverse items-center gap-2 bottom-0 right-0 mr-2">
            <q-btn class="right bottom-0 right-0 mr-2 btn btn-themed text-heading rounded px-7 py-2 weight-900" flat dense :loading="submitting" type="submit" push :disable="disabled">
              <div>
                <span class="text-white text-base weight-900 text-capitalize">{{ btnString }}</span>
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
  font-size: 15px;
  margin-top: 20px;
  grid-column: auto / span 5;
  position: relative;
}

.post__caption:active {
  color: var(--color-heading) !important;
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
