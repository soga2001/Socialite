<script lang="ts">
import { defineComponent } from 'vue';
import type {PropType } from 'vue';
import type { User } from '@/assets/interfaces';
import { http } from '@/assets/http';
import Timeago from '../Timeago.vue';
import { useCookies } from 'vue3-cookies';
import Item from '../Item.vue';

export default defineComponent({
    props: {
        user: { type: Object as PropType<User>, required: true }
    },
    data() {
        return {
            id: this.user.id,
            username: this.user.username,
            email: this.user.email,
            first_name: this.user.first_name,
            last_name: this.user.last_name,
            is_active: this.user.is_active,
            is_staff: this.user.is_staff,
            is_superuser: this.user.is_superuser,
            last_login: this.user.last_login,
            bio: this.user.bio,
            avatar: this.user.avatar,
            banner: this.user.banner,
            posts: this.user.total_posted,
            followers: this.user.total_followers,
            following: this.user.total_following,
            followed: false,
            date_joined: this.user.date_joined,
            loading: true,

            showAvatar: false,
            showBanner: false,
            editProfile: false,


            newAvatar: this.user.avatar,
            newBanner: this.user.banner,
            new_FN: this.user.first_name,
            new_LN: this.user.last_name,
            newBio: this.user.bio,
            
            avatarFile: null,
            bannerFile: null,

            fileName: null,

        };
    },
    methods: {
        async follow() {
            if (!this.$store.state.authenticated) {
                return;
            }
            await http.post(`follow/follow_user/${this.id}/`, {}, {
            }).then((res) => {
                if (res.data.error) {
                    return;
                }
                this.followed = !this.followed;
                if (!this.followed && this.following != 0) {
                    this.following -= 1;
                }
                else {
                    this.following += 1;
                }
            }).catch((err) => {
                console.log(err);
            });
        },
        async if_followed() {
            // console.log(this.$store.state.user.id != this.id && this.loading)
            if (!this.$store.state.authenticated) {
                this.loading = false
                return;
            }
            await http.get(`follow/get_if_followed/${this.id}/`, {
            }).then((res) => {
                this.followed = res.data.followed
                
            }).catch((err) => {
                this.followed = false;
            });
            this.loading = false
        },

        toggleAvatar() {
            this.$refs.avatarUpload.click();
            this.showAvatar = !this.showAvatar;
        },
        toggleBanner() {
            this.$refs.bannerUpload.click()
            this.showBanner = !this.showBanner;
        },

        updateProfile() {
            const formData = new FormData()
            if (this.avatarFile) {
                formData.append('avatar', this.avatarFile)
            }
            if (this.bannerFile) {
                formData.append('banner', this.bannerFile)
            }
            if (this.new_FN && this.first_name != this.new_FN) {
                formData.append('first_name', this.new_FN)
            }
            if (this.new_LN && this.last_name != this.new_LN) {
                formData.append('last_name', this.new_LN)
            }
            if (this.newBio && this.bio != this.newBio) {
                formData.append('bio', this.newBio)
            }

            http.post('users/update_profile/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then((res) => {
                this.editProfile = false;
                if(res.data.user) {
                    this.updateUser(res.data.user)
                }
                // this.$store.commit('setUser', res.data.user)
            }).catch((err) => {
                console.log(err)
            })

        },

        async updateUser(user: User) {
            this.first_name = user.first_name;
            this.last_name = user.last_name;
            this.bio = user.bio;
            this.avatar = user.avatar;
            this.banner = user.banner;

        },

        async launchCropper(e: Event) {
            if(!e) return;
            var file = event?.target.files[0];
            console.log(file.type)
            if(this.showBanner) {
                this.newBanner = await this.toBase64(file);
                this.$refs.bannerDialog.initCropper(file.type, file.name);

            }
            if(this.showAvatar) {
                this.newAvatar = await this.toBase64(file);
                this.$refs.avatarDialog.initCropper(file.type, file.name);

            }
        },

        async toBase64(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = () => resolve(reader.result);
                reader.onerror = (error) => reject(error);
            })
        },
    },
    created() {
        // console.log(this.date_joined)
        // console.log(this.$store.state)
        this.if_followed();
        
    },
    mounted() {
    },
    computed: {
        theme() {
            return this.$store.state.dark;
        },
    },
    watch: {
        // newAvatar(newAvatar) {
        //     console.log('here')
        // },
        // newBanner(newBanner) {
        // },
        avatarFile(avatarFile) {
            console.log(avatarFile)
        },
        bannerFile(bannerFile) {
            console.log(bannerFile)
        }
    },
    components: { Timeago }
})
</script>

<template>
    
    <div class="user">
        <div class="user__container col-12 col-md-auto">
            <div class=' grid cols-auto-fr rows-4 relative'>
                <div id="banner" class='p-0 col-start-1 col-span-full z-3 bg-theme-soft pointer'>
                    
                    <img v-if="banner" :src="banner" alt="banner"/>
                    <img v-else class="" src="https://unsplash.it/1000/1000/?random&pic=1" alt="banner"/>
                </div>
                <div class="profile-img profile-pic overflow-hidden z-3 pointer">
                    <img v-if="avatar" class="profile-pic__image" :src="avatar" alt="Profibild" />
                    <img v-else class="profile-picture" src="https://unsplash.it/300/300/?random&pic=1(14 kB)" alt="profile-picture"/>
                    <div class="profile-pic__content ">
                        <span class="profile-pic__icon"><q-icon size="30px" name="photo_camera"/></span>
                        <span class="profile-pic__text">Edit Profile</span>
                    </div>
                </div>
                <div class="edit-profile w-full h-fit flex flex-row-reverse p-2">
                    <button v-if="$store.state.user.id != id && !loading" class="border btn rounded text-heading bg-transparent weight-900" @click="follow" :disabled="!$store.state.authenticated">{{ followed ? 'Unfollow' : 'Follow' }}</button>
                    <button v-if="$store.state.authenticated && $store.state.user.id == id" class="border btn rounded text-heading bg-transparent weight-900" @click="editProfile = true">Edit Profile</button>
                    <q-btn @click.stop="" v-if="followed && !loading" size="16px" class="less" flat dense round icon="notifications" />
                    <q-btn @click.stop="" v-if="followed && !loading"  size="16px" class="more__vert" flat dense round icon="more_horiz" />
                </div>
            </div>
            <div>
                <q-dialog class="h-full" v-model="editProfile" persistent>
                    <q-card :dark="theme">
                        <q-card-section>
                            <Item>
                                <template #title>
                                    <div class="text-h6">Edit Profile</div>
                                </template>
                                <template #icon>
                                    <div class="btn" @click="editProfile = !editProfile">
                                        <i-close :vert-icon-center="true"  size="2rem"/>
                                    </div>
                                    
                                </template>
                            </Item>
                        </q-card-section>

                        <q-card-section class="q-pt-none">
                            <div class=' grid cols-auto-fr rows-4 relative'>
                                <div id="banner" class='p-0 col-start-1 col-span-full bg-theme-soft' >
                                    <img v-if="!newBanner && banner" :src="banner"/>
                                    <img v-else-if="newBanner" :src="newBanner" alt="banner"/>
                                    <img v-else class="" src="https://unsplash.it/1000/1000/?random&pic=1" alt="banner"/>
                                    <div class="centered-on-image">
                                        <button class="border-none btn rounded-lg p-3 bg-gray-op" @click="toggleBanner">
                                            <q-icon name="edit" size="2rem"/>
                                        </button>
                                        <input ref="bannerUpload" type="file" id="file" @change="launchCropper" hidden/>
                                    </div>
                                    <div class="z-100">
                                        <image-cropper ref="bannerDialog" :aspect-ratio="3/1" :filename="fileName" :chosen-img="newBanner" @close="newBanner = null" @onReset="{$refs.bannerUpload.value = null; showBanner = false}" @file="bannerFile = $event" @onCrop="(croppedImage) => {newBanner = croppedImage}"/>
                                    </div>
                                    
                                </div>
                                <div class="profile-img profile-pic relative overflow-hidden">
                                    <!-- <img v-if="!newAvatar && avatar" :src="avatar" alt="profile img"/> -->
                                    <!-- <img v-if="newAvatar" class="profile-pic__image" :src="newAvatar" alt="Profile img" /> -->
                                    <img class="profile-picture__image" src="https://unsplash.it/300/300/?random&pic=1(14 kB)" alt="profile-picture"/>
                                    <div class="centered-on-image">
                                        <button class="border-none btn rounded-lg p-3 bg-gray-op" @click="toggleAvatar">
                                            <q-icon name="edit" size="2rem"/>
                                        </button>
                                        <input ref="avatarUpload" type="file" id="file" @change="launchCropper" hidden/>
                                    </div>
                                    <div class="z-100 realtive h-full bg-theme-soft">
                                        <image-cropper ref="avatarDialog" :fileName="fileName" :chosen-img="newAvatar" @close="newAvatar = null" @onReset="{$refs.avatarUpload.value = null; showAvatar = false}" @file="avatarFile = $event" @onCrop="(croppedImage) => {newAvatar = croppedImage}"/>
                                    </div>
                                    
                                </div>
                            </div>
                            <div>
                                <q-input :dark="theme" v-model="new_FN" label="First Name" />
                                <q-input :dark="theme" v-model="new_LN" label="Last Name" />
                                <q-input :dark="theme" v-model="newBio" label="Bio" />
                            </div>
                        </q-card-section>

                        <q-card-actions align="right">
                            <q-btn flat label="Cancel" color="primary" v-close-popup />
                            <q-btn flat label="Save" color="primary" @click="updateProfile" />
                        </q-card-actions>
                    </q-card>
                </q-dialog>
            </div>
        
            <div class="user-profile__info flex py-3 mb-5">
                <div class="flex flex-col" >
                    <div class="user-name text-2xl weight-900 text-heading">{{ first_name }} {{ last_name }}</div>
                    <div class="user-username text-xl">@{{ username }}</div>
                    <div class="user-date_joined my-2  flex items-center">
                        <q-icon name="date_range" size="16px" class="q-mr-sm" />
                        <div class="flex items-center text-xl">
                            <span class="mr-2">Joined </span> <Timeago size="1.25rem" :date="date_joined" date_type="long" />
                        </div>
                    </div>
                    <div class="follows text-lg flex items-center gap-3">
                        <span><span class="text-heading weight-900">{{ followers }} </span> Followers</span> 
                        <span><span class="text-heading weight-900">{{ following }} </span> Following</span>
                    </div>
                    <div class="user-bio text-lg py-3 text-heading text-bold">{{ bio }}</div>
                </div>
            </div>
        </div>
  </div>
</template>

<style scoped>
.user__container {
    max-width: 600px;
    width: 100%;
}

.user__container:not(:first-child) {
    margin-left: 2vw;
    background-color: aliceblue;
}




.user__username {
    margin-left: 1vw;
    font-size: 20px;
}

.right {
    position: absolute;
    display: inline-block;
    right: 0;
    top: 0;
    bottom: 0;
}

.user-profile__info {
    margin-left: 2vw;
    
}
.user__social {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    max-width: 100%;
}

.user__social .user__following, .user__followers, .user__posts {
    display: grid;
    justify-content: center;
}

.user__folowers {
    border-left: 1px solid var(--color-heading) !important;
    border-right: 1px solid var(--color-heading) !important; 
}

.user__follow__btn {
    font-weight: bolder;
    padding: 10px;
    background-color: var(--color-background-mute);
    color: var(--color-text);
    border:none;
}

h6 {
    font-size: .8rem;
    font-weight: 900;
    color: var(--color-text);
    /* text-align: center; */
}

.user__bio {
    padding: 20px;
}

.user__caption {
    color: var(--color-text)
}

/* Profile Pic */
.profile-pic {
  border-radius: 50%;
  background-color: rgba(176, 176, 176);
  transition: scale 1s ease-out;
}

.profile-pic img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: all .3s ease-in-out;
}


.profile-pic:hover img {
    transform: scale(1.2);
    opacity: .3;
}



.profile-pic:hover .profile-pic__content {
    opacity: 1;
}

.profile-pic__content {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: var(--color-heading);
  font-weight: bolder;
  opacity: 0;
  transition: opacity .2s ease-in-out;
  border-radius: 50%;
}

.profile-pic__icon {
  color: var(--color-heading);
  padding-bottom: 8px;
}

.profile-pic__text {
  text-transform: uppercase;
  font-size: 12px;
  width: 50%;
  text-align: center;
}

.joined {
    display: inline-flex;
    line-height: normal;
    color: var(--color-text);
    font-size: 15px;
}

.icon {
    margin-right: 5px;
}

.timeago {
    margin-left: 5px;
}


/* Banner and profile picture */
#banner {
    grid-row: row 1 / span 3;
    min-height: 180px;
    aspect-ratio: 3/1;
}

/* #banner:hover {
    cursor: pointer;
} */

#banner img {
    object-fit: cover;
    width: 100%;
    height: 100%;
}

.profile-img {
    grid-column: 1;
    grid-row: row 3 / span 3;
    min-width: 120px;
    min-height: 120px;
    padding: 2px;
    width: 100%;
    height: 100%;
    max-height: 8vw;
    max-width: 8vw;
    margin-left: 2vw;
    background-color: var(--color-background);
}

/* .profile-img:hover {
    cursor: pointer;
} */

.profile-img img {
    border-radius: 50%;
    width: 100%;
}

.edit-profile {
    /* padding-top: 30px !important; */
    grid-column: 2;
    grid-row: row 4 / span 2;
    gap: 5px;
    /* padding: 10px; */
}

.edit-profile button {
    padding: 10px;
    /* background-color: var(--color-background-mute); */
    border: 1px solid var(--color-heading);
    color: var(--color-text);
    border:none;
}

.edit-profile button:hover {
    background-color: var(--color-background-soft);
    color: var(--color-text);
}




    
</style>