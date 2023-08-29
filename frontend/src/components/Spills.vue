<script lang="ts">
import { http } from '@/assets/http';
import { defineComponent, type ComponentPublicInstance, type Ref } from 'vue';
import type { User } from '../assets/interfaces';
import Mention from './Mention.vue';
import ProfileIcon from '@/icons/i-profile.vue';
import uploadedImg from './uploadedImg.vue';


export default defineComponent({
    data() {
        return {
            image: null as File | null,
            caption: "",
            submitting: false,
            users: new Array<User>(),
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
        type: String,
        default: "",
      },
      rows: {
        type: Number,
        default: 1,
      }
    },
    computed: {
      lessThan20() {
        console.log('here')
        return (255 - this.chars) <= 20;
      },
    },
    methods: {
        submit() {
            this.submitting = true;
            const formData = new FormData();
            const mention = this.$refs.input as {
                  reset: () => void;
            };
            if (this.image) {
              formData.append("caption", this.caption.trim());
              formData.append("image", this.image);
              http.post("posts/post_content/", formData, {
                  headers: {
                      "Content-Type": "multipart/form-data",
                  }
              }).then((res) => {
                if(res.data.error) {
                  this.$q.notify({
                      message: `<span class="text-white">${res.data.message}</span>`,
                      color: 'negative',
                      textColor: 'white',
                      position: 'bottom',
                      timeout: 3000,
                      html: true,
                  })
                }
                this.submitting = false;
                this.deleteImg()
                mention.reset()
                if(res.data.success) {
                  this.$q.notify({
                      message: `<span class="text-white">${res.data.message}</span>`,
                      color: 'positive',
                      textColor: 'white',
                      position: 'bottom',
                      timeout: 3000,
                      html: true,
                  })
                }
              }).catch((err) => {
                  console.log(err);
              });
            }
            else {
              if(!this.isComment) {
                this.submitting = false;
                return
              }
              formData.append("comment", this.caption.trim());
              http.post(`comments/comment/${this.spillId}/`, formData, {
                  headers: {
                      "Content-Type": "multipart/form-data",
                  }
              }).then((res) => {
                  this.submitting = false;
                  mention.reset();
              }).catch((err) => {
                  console.log(err);
              });
            }
        },
        async getImage(e: Event) {
            const target = e.target as HTMLInputElement;
            const file = target.files?.[0];
            if(file){
              this.image = file;
              this.imgURL = await this.toBase64(file);
            }
        },
        async toBase64(file: File): Promise<string> {
            return new Promise<string>((resolve, reject) => {
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = () => resolve(reader.result as string);
                reader.onerror = (error) => reject(error);
            })
        },
        deleteImg() {
          this.image = null;
          this.imgURL = '';
        },
        disablePost() {
          if(this.isComment) {
            if(this.chars > 255) {
              this.disabled = true;
            }
            else {
              this.disabled = false;
            }
            return
          }
          if(this.image === null || this.chars > 255) {
            this.disabled = true;
          }
          else {
            this.disabled = false;
          }
        },
    },
    created() {
    },
    mounted() {
    },
    watch: {
      chars(chars) {
        this.disablePost()
      },
      image(image) {
        this.disablePost()
      },

    },
    components: { Mention, ProfileIcon, uploadedImg }
})
</script>

<template>
  <div class="post bg-transparent relative">
    <div class="post__container ">
      <q-avatar class="post__avatar " size="70px" >
          <img class="user__avatar" v-if="$store.state.user.avatar" :src="$store.state.user.avatar"/>
          <profile-icon v-else size="4rem" />
      </q-avatar>
      <div class="grid gap-3">
        <form class="relative w-full cols-5 grid gap-2 px-2" autocorrect="on" autocomplete="off" @submit.prevent="submit">
          <div class="flex col-span-5 flex-rows caption-div">
            <Mention ref="input" @update:charsLeft="chars = $event" :rows="rows" @update:val="caption = $event" :value="caption" input_type="text" id="caption" :placeholder="placeholder" class="post__caption w-full" />
            <div v-if="imgURL" class="mr-3">
              <uploadedImg :img-url="imgURL" @update:delete="deleteImg()"/>
            </div>
          </div>
          <div class="flex col-span-5 bg-theme sticky bottom-0 ">
            <div class="flex gap-2 flex-start">
              <q-btn v-if="!isComment" rounded dense flat class="px-2" @click="($refs.file as HTMLInputElement).click()">
                <i-upload-img  size="1.5rem" fill="rgb(253, 137, 137)" stroke="rbg(253,137,137)"/>
                <input ref="file" @change="getImage" type="file" id="file" style="display: none" name="image" accept="image/*" data-original-title="upload photos"/>
              </q-btn>
              <!-- <label :hidden="isComment" class="pointer btn-transition btn-hover-ligher pt-2 px-2 rounded">
                <i-upload-vid size="1.5rem" fill="rgb(253, 137, 137)" stroke="rgb(253, 137, 137)" />
                <input @change="getImage" type="file" id="file" style="display: none" name="image" accept="image/*" data-original-title="upload photos"/>
              </label> -->
            </div>
            <div class="sticky bottom-0 justify-end flex flex-row-reverse items-center gap-2 mr-2 end">
              <q-btn class="right bottom-0 right-0 mr-2 btn btn-themed bg-web-theme-hover text-heading rounded px-7 py-2 weight-900" flat dense :loading="submitting" type="submit" push :disable="disabled">
                <div>
                  <span class="text-white text-base weight-900 text-capitalize">{{ btnString }}</span>
                </div>
                <template v-slot:loading>
                  <q-spinner />
                </template>
              </q-btn> 
              <circular-progress v-if="chars" :val="chars" size="30px" :showVal="true" />
            </div>
          </div>
        </form>
      </div>
    </div> 
  </div>
</template>

<style scoped>
.post {
  display: grid;
  background-color: red;
  position: relative;
  width: 100%;
  max-width: 600px;
  /* max-height: calc(100vh - 110px); */
  max-height: calc(100vh - 60px);
  /* max-height: 100vh; */
  position: relative;
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

.caption-div {
  max-height: calc(100vh - 120px);
  overflow: auto;
  overflow-y: scroll;
}

.post__caption {
  font-size: 15px;
  margin-top: 20px;
  grid-column: auto / span 5;
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

.container {
  position: relative;
  text-align: center;
  color: black;
}

.top-right {
  position: absolute;
  top: 8px;
  right: 16px;
}

.end {
  margin-left: auto;
}
</style>
