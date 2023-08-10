<script lang="ts">
import { defineComponent } from 'vue';
import type {PropType } from 'vue';
import type { User } from '@/assets/interfaces';
import { http } from '@/assets/http';
import Timeago from '../Timeago.vue';
import { useCookies } from 'vue3-cookies';
import Item from '../Item.vue';
import createIntersectObserver from '@/assets/intersectionObserver'

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
            followed: this.user.is_following,
            date_joined: this.user.date_joined,
            is_current_user: this.user.is_current_user,

            showAvatar: false,
            showBanner: false,
            editProfile: false,


            newAvatar: this.user.avatar as string || "",
            newBanner: this.user.banner as string || "",
            new_FN: this.user.first_name,
            new_LN: this.user.last_name,
            newBio: this.user.bio,
            
            avatarFile: null,
            bannerFile: null,

            fileName: null,

            errMsg: '',
            successMsg: '',

            user_followers: new Array<User>(),
            user_following: new Array<User>(),
            show_followers: false,
            show_following: false,

            loading_follow: false,
            loading_follow_request: false,

            zoomAvatar: false,
            zoomBanner: false,
        };
    },
    methods: {
        async follow() {
            if (!this.$store.state.authenticated) {
                return;
            }
            this.loading_follow_request = true
            await http.post(`follow/follow_user/${this.id}/`).then((res) => {
                if (res.data.error) {
                    return;
                }
                this.followed = !this.followed;
                this.loading_follow_request = false;
                // setTimeout(() => {
                //     this.loading_follow_request = false
                // }, 4000)
                if (!this.followed && this.following != 0) {
                    this.followers -= 1;
                }
                else {
                    this.followers += 1;
                }
            }).catch((err) => {
                console.log(err);
            });
        },
        async if_followed() {
            if (!this.$store.state.authenticated) {
                // this.loading = false
                return;
            }
            await http.get(`follow/get_if_followed/${this.id}/`, {
            }).then((res) => {
                this.followed = res.data.followed
                
            }).catch((err) => {
                this.followed = false;
            });
            // this.loading = false
        },

        getFollowers() {
            if(this.user_followers.length) {
                return
            }
            this.loading_follow = true;
            http.get(`follow/get_followers_users/${this.username}`).then((res) => {
                if(res.data.error) {
                    return
                }
                this.loading_follow = false
                // setTimeout(() => {
                //     this.loading_follow = false
                // }, 3000)
                this.user_followers = res.data.users
            }).catch((err) => {
                console.log(err)
            })
        },

        getFollowing() {
            if(this.user_following.length) {
                return
            }
            this.loading_follow = true;
            http.get(`follow/get_following_users/${this.username}/`).then((res) => {
                if(res.data.error) {
                    return
                }
                // this.loading_follow = false
                setTimeout(() => {
                    this.loading_follow = false
                }, 3000)
                this.user_following = res.data.users
            }).catch((err) => {
                console.log(err)
            })
        },

        toggleAvatar() {
            if (this.$refs.avatarUpload instanceof HTMLElement) {
                (this.$refs.avatarUpload as HTMLElement).click();
                this.showAvatar = !this.showAvatar;
            }
        },
        toggleBanner() {
            if (this.$refs.bannerUpload instanceof HTMLElement) {
                (this.$refs.bannerUpload as HTMLElement).click();
                this.showBanner = !this.showBanner;
            }
            
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
                if(res.data.message) {
                    this.successMsg = res.data.message
                }
                // this.$store.commit('setUser', res.data.user)
            }).catch(err => {
                // console.error(err.response.data.message)
                this.errMsg = err.response.data.message
            })

        },

        async updateUser(user: User) {
            this.first_name = user.first_name;
            this.last_name = user.last_name;
            this.bio = user.bio;
            this.avatar = user.avatar;
            this.banner = user.banner;

            this.$store.commit('setUser', user);

        },

        async launchCropper(e: Event) {
            if(!e) return;
            const inputElement = e.target as HTMLInputElement;
            const file = inputElement.files?.[0];
            if(this.showBanner && file) {
                this.newBanner = await this.toBase64(file);
                const bannerDialogRef = this.$refs.bannerDialog as {
                    initCropper: (type: string | undefined, name: string | undefined) => void;
                };
                // this.newBanner = await this.toBase64(file);
                bannerDialogRef.initCropper(file?.type, file?.name);

            }
            if(this.showAvatar && file) {
                this.newAvatar = await this.toBase64(file);
                const avatarDialogRef = this.$refs.avatarDialog as {
                    initCropper: (type: string | undefined, name: string | undefined) => void;
                };
                // this.newBanner = await this.toBase64(file);
                avatarDialogRef.initCropper(file?.type, file?.name);

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

        async onCancel() {
            this.showAvatar = false;
            this.showBanner = false;
            this.newAvatar = this.avatar;
            this.newBanner = this.banner;
            this.new_FN = this.first_name;
            this.new_LN = this.last_name;
            this.newBio = this.bio;
            this.avatarFile = null;
            this.bannerFile = null;
            this.editProfile = false

        },

        async notIntersecting(e: IntersectionObserverEntry) {
            // emit that it isn't intersecting
            if(e.isIntersecting) {
                this.$emit('update:intersecting', true)
            }
            else {
                this.$emit('update:intersecting', false)
            }
        }
    },
    created() {
        // this.if_followed();
        
    },
    async mounted() {
        await this.$nextTick()
        const observer = createIntersectObserver(this.$el, this.notIntersecting, {threshold: .66}, false)
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
        // avatarFile(avatarFile) {
        //     console.log(avatarFile)
        // },
        // bannerFile(bannerFile) {
        //     console.log(bannerFile)
        // }
    },
    components: { Timeago }
})
</script>

<template>
    <div class="user">
        <div class="user__container  relative">
            <!-- <div class=' grid cols-auto-fr rows-4 relative overflow-hidden'>
                <div id="banner" class='p-0 col-start-1 col-span-full z-2 bg-theme-soft h-full pointer' @click="zoomBanner = true">
                    <img v-if="banner" class="hover-darker" :src="banner" alt="banner"/>
                    <img v-else class="hover-darker" src="https://unsplash.it/1000/1000/?random&pic=1" alt="banner"/>
                </div>
                <div class="profile-img profile-pic z-2 pointer overflow-hidden" @click="zoomAvatar = true">
                    <img v-if="avatar" class="profile-pic__image hover-darker" :src="avatar" alt="Profibild" />
                    <img v-else class="profile-picture hover-darker" src="https://unsplash.it/300/300/?random&pic=1(14 kB)" alt="profile-picture"/>
                </div>
                
                <zoomImg v-if="zoomAvatar" :img="avatar" :open="zoomAvatar" @update:open="zoomAvatar = $event"/>
                <zoomImg v-if="zoomBanner" :img="banner" :open="zoomBanner" @update:open="zoomBanner = $event"/>

                <div class="edit-profile text-base w-full h-fit flex justify-end p-2">
                    <button class="border pointer bg-hover rounded-lg text-heading bg-theme weight-900" v-if="followed">
                        <q-icon size="1.5rem" name="more_horiz" />
                    </button>
                    <button class="border pointer bg-hover rounded-lg text-heading bg-theme weight-900" v-if="followed">
                        <q-icon size="1.5rem" name="notifications" />
                    </button>
                    <button flat v-if="is_current_user" class="border pointer bg-hover-mute rounded-lg px-6 text-heading bg-theme weight-900" @click="editProfile = true">
                        Edit Profile
                    </button>
                    <button v-if="!is_current_user" :class="{'followed': followed}" class="border w-8 pointer bg-hover-soft rounded-lg px-6 text-heading bg-theme weight-900" @click="follow" :disabled="!$store.state.authenticated || loading_follow_request">
                        <span class="weight-900"  v-if="!loading_follow_request">{{ followed ? 'Following' : 'Follow' }}</span>
                        <span class="p-0" v-if="loading_follow_request">
                            <Loading size="1.3rem" />
                        </span>
                    </button>
                    
                    
                    
                </div>
            </div> -->

            <div class=" w-full m-0 p-0 h-fit bg-green relative">
                <div class='banner p-0 w-full relative bg-theme-soft h-full pointer' @click="zoomBanner = true">
                    <img v-if="banner" class="hover-darker w-full" :src="banner" alt="banner"/>
                    <img v-else class="hover-darker w-full" src="https://unsplash.it/1000/1000/?random&pic=1" alt="banner"/>
                </div>
                <div class="avatar z-2 pointer overflow-hidden" @click="zoomAvatar = true">
                    <img v-if="avatar" class="profile-pic__image hover-darker w-full " :src="avatar" alt="Profibild" />
                    <img v-else class="profile-picture hover-darker w-full" src="https://unsplash.it/300/300/?random&pic=1(14 kB)" alt="profile-picture"/>
                </div>
                <zoomImg v-if="zoomAvatar" :img="avatar" :open="zoomAvatar" @update:open="zoomAvatar = $event"/>
                <zoomImg v-if="zoomBanner" :img="banner" :open="zoomBanner" @update:open="zoomBanner = $event"/>

                <div class="edit-profile absolute right-0 text-base h-fit p-2">
                    <button class="border pointer bg-hover rounded-lg text-heading bg-theme weight-900" v-if="followed">
                        <q-icon size="1.5rem" name="more_horiz" />
                    </button>
                    <button class="border pointer bg-hover rounded-lg text-heading bg-theme weight-900" v-if="followed">
                        <q-icon size="1.5rem" name="notifications" />
                    </button>
                    <button flat v-if="is_current_user" class="border pointer bg-hover-mute rounded-lg px-6 text-heading bg-theme weight-900" @click="editProfile = true">
                        Edit Profile
                    </button>
                    <button v-if="!is_current_user" :class="{'followed': followed}" class="border w-8 pointer bg-hover-soft rounded-lg px-6 text-heading bg-theme weight-900" @click="follow" :disabled="!$store.state.authenticated || loading_follow_request">
                        <span class="weight-900"  v-if="!loading_follow_request">{{ followed ? 'Following' : 'Follow' }}</span>
                        <span class="p-0" v-if="loading_follow_request">
                            <Loading size="1.3rem" />
                        </span>
                    </button>
                </div>
            </div>

            <div class="h-full">
                <q-dialog class="h-full w-full" v-model="editProfile" persistent :maximized="$q.screen.lt.sm ? true : false">
                    <q-card class="h-fit bg-theme border">
                        <q-card-section>
                            <Item>
                                <template #title>
                                    <div class="text-h6">Edit Profile</div>
                                </template>
                                <template #icon>
                                    <div class="pointer" @click="editProfile = !editProfile">
                                        <i-close :vert-icon-center="true" fill="var(--color-heading)" stroke="none"  size="2rem"/>
                                    </div>
                                    
                                </template>
                            </Item>
                        </q-card-section>

                        <q-card-section class="q-pt-none">
                            <div class=' grid cols-auto-fr rows-4 relative'>
                                <div id="banner" class='col-start-1 col-span-full bg-theme-soft h-fit' >
                                    <img v-if="!newBanner && banner" :src="banner"/>
                                    <img v-else-if="newBanner" :src="newBanner" alt="banner"/>
                                    <img v-else class="" src="https://unsplash.it/1000/1000/?random&pic=1" alt="banner"/>
                                    <div class="centered-on-image">
                                        <button class="border-none btn-themed-low-op pointer rounded-lg p-3" @click="toggleBanner">
                                            <q-icon color="white" name="edit" size="2rem"/>
                                        </button>
                                        <input ref="bannerUpload" type="file" id="file" @change="launchCropper" hidden/>
                                    </div>
                                    <div class=" hidden">
                                        <!-- <image-cropper ref="bannerDialog" :aspect-ratio="3/1" :filename="fileName" :chosen-img="newBanner" @close="newBanner = null" @onReset="{$refs.bannerUpload.value = null; showBanner = false}" @file="bannerFile = $event" @onCrop="(croppedImage) => {newBanner = croppedImage}"/> -->
                                            <image-cropper ref="bannerDialog" :aspect-ratio="3/1" :fileName="fileName" :chosen-img="newBanner" @onReset="{($refs.bannerUpload as HTMLInputElement).value = ''; showBanner = false}" @file="bannerFile = $event" @onCrop="(croppedImage: string) => {newBanner = croppedImage}" />
                                    </div>
                                    
                                </div>
                                <div class="profile-img profile-pic relative overflow-hidden">
                                    <img v-if="!newAvatar && avatar" :src="avatar" alt="profile img"/>
                                    <img v-else-if="newAvatar" class="profile-pic__image" :src="newAvatar" alt="Profile img" />
                                    <img v-else class="profile-picture__image" src="https://unsplash.it/300/300/?random&pic=1(14 kB)" alt="profile-picture"/>
                                    <div class="centered-on-image">
                                        <button class="border-none pointer btn-themed-low-op rounded-lg p-3 bg-gray-op" @click="toggleAvatar">
                                            <q-icon color="white" name="edit" size="2rem"/>
                                        </button>
                                        <input ref="avatarUpload" type="file" id="file" @change="launchCropper" hidden/>
                                    </div>
                                    <div class="z-100 hidden">
                                        <!-- <image-cropper ref="avatarDialog" :fileName="fileName" :chosen-img="newAvatar" @close="newAvatar = null" @onReset="{$refs.avatarUpload.value = null; showAvatar = false}" @file="avatarFile = $event" @onCrop="(croppedImage) => {newAvatar = croppedImage}"/> -->
                                            <image-cropper circle ref="avatarDialog" :fileName="fileName" :chosen-img="newAvatar" @close="{newAvatar = ''; showAvatar = false}" @onReset="{($refs.avatarUpload as HTMLInputElement).value = ''; showAvatar = false}" @file="avatarFile = $event" @onCrop="(croppedImage: string) => {newAvatar = croppedImage}" />
                                    </div>
                                    
                                </div>
                            </div>
                            <div>
                                <q-input class="text-lg" :dark="theme" v-model="new_FN" label="Last Name"> 
                                </q-input>
                                <q-input class="text-lg" :dark="theme" v-model="new_LN" label="Last Name" />
                                <q-input class="text-lg" :dark="theme" v-model="newBio" type="textarea" label="Bio" />
                            </div>
                        </q-card-section>

                        <q-card-actions align="right">
                            <q-btn flat label="Cancel" color="primary" @click="onCancel" />
                            <q-btn flat @click="updateProfile">
                                <div class="capitalize">
                                    Save
                                </div>
                            </q-btn>
                        </q-card-actions>
                    </q-card>
                </q-dialog>
            </div>
        
            <div class="user-profile__info flex py-1 mb-5">
                <div class="flex flex-col text-left" >
                    <div class="user-name text-2xl weight-900 text-heading">{{ first_name }} {{ last_name }}</div>
                    <div class="text-body text-base">@{{ username }}</div>

                    <div class="user-bio text-xl py-2 text-heading weight-600">{{ bio }}</div>

                    <div class="user-date_joined mb-2 flex items-center">
                        <q-icon name="date_range" size="16px" class="mr-1 text-body" />
                        <div class="flex items-center text-base">
                            <span class="mr-1 text-body">Joined </span> <Timeago class="text-body" size="1rem" :date="date_joined" date_type="long" />
                        </div>
                    </div>
                    <div class="follows text-lg flex items-center gap-3">
                        <span class="text-body pointer hover-underline" @click="{show_followers = true; getFollowers()}"><span class="text-heading weight-900">{{ followers }} </span> Followers</span> 
                        <span class="text-body pointer hover-underline" @click="{show_following = true; getFollowing()}"><span class="text-heading weight-900">{{ following }} </span> Following</span>
                    </div>

                    <div class="relative w-full">
                        <q-dialog class="w-full" v-model="show_followers" :maximized="$q.screen.lt.sm ? true : false">
                            <div class="bg-theme border w-full max-w-xs h-full max-h-sm">
                                <div class="p-1">
                                    <Item>
                                        <template #title>
                                            <div class="text-h6">Followers</div>
                                        </template>
                                        <template #icon>
                                            <div class="btn" @click="show_followers = !show_followers">
                                                <i-close :vert-icon-center="true" fill="var(--color-heading)" stroke="none"  size="2rem"/>
                                            </div>
                                        </template>
                                    </Item>
                                </div>

                                <div>
                                    <hr/>
                                </div>

                                <div v-if="loading_follow" class="max-h-xs h-full flex justify-center items-center">
                                    <Loading/>
                                </div>

                                <div class="results-even" v-else-if="!loading_follow && user_followers" v-for="user in user_followers">
                                    <Item clickable :to="{ name: 'user-profile', params: { username: user.username } }">
                                        <template #avatar>
                                            <img :src="user.avatar" alt="user profile pic"/>
                                        </template>
                                        <template #title>
                                            <div class="text-heading weight-900">{{ user.first_name }} {{ user.last_name }}</div>
                                        </template>
                                        <template #caption>
                                            <div class="text-body">{{ user.username }}</div>
                                        </template>
                                    </Item>
                                </div>
                            </div>
                        </q-dialog>

                        <q-dialog class="w-full" v-model="show_following" :maximized="$q.screen.lt.sm ? true : false">
                            <div class="bg-theme border w-full max-w-xs h-full max-h-sm">
                                <div class="p-1">
                                    <Item>
                                        <template #title>
                                            <div class="text-h6">Following</div>
                                        </template>
                                        <template #icon>
                                            <div class="btn" @click="show_following = !show_following">
                                                <i-close :vert-icon-center="true" fill="var(--color-heading)" stroke="none"  size="2rem"/>
                                            </div>
                                        </template>
                                    </Item>
                                </div>

                                <div>
                                    <hr/>
                                </div>

                                <div v-if="loading_follow" class="max-h-xs h-full flex justify-center items-center">
                                    <Loading />
                                </div>
                                <div class="results-even" v-else-if="!loading_follow && user_following" v-for="user in user_following">
                                    <Item clickable :to="{ name: 'user-profile', params: { username: user.username } }">
                                        <template #avatar>
                                            <img :src="user.avatar" alt="user profile pic"/>
                                        </template>
                                        <template #title>
                                            <div class="text-heading weight-900">{{ user.first_name }} {{ user.last_name }}</div>
                                        </template>
                                        <template #caption>
                                            <div class="text-body">{{ user.username }}</div>
                                        </template>
                                    </Item>
                                </div>
                            </div>
                        </q-dialog>
                    </div>

                    
                </div>
            </div>

        </div>

        <div v-if="errMsg">
            <!-- <Notify :message="errMsg" type="error" @deleteMsg="errMsg=''" title="Error Message"/> -->
        </div>
        <div v-if="successMsg">
            <!-- <Notify :message="successMsg" type="success" @deleteMsg="successMsg=''" title="Success Message"/> -->
        </div>
  </div>
</template>

<style scoped lang="scss">

.user__container {
    max-width: 600px;
    width: 100%;
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
    position: relative;
    grid-row: row 1 / span 3;
    aspect-ratio: 3/1;
    /* min-height: 180px; */
    /* aspect-ratio: 3/1; */
}

/* #banner:hover {
    cursor: pointer;
} */

#banner img {
    object-fit: cover;
    width: 100%;
    /* height: 100%; */
    aspect-ratio: 3/1;
}

.profile-img {
    grid-column: 1;
    grid-row: row 3 / span 2;
    min-width: 120px;
    min-height: 120px;
    height: 100%;
    max-height: 10vw;
    max-width: 10vw;
    padding: 2px;
    width: 100%;
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

.user-profile__info {
    margin-top: 70px; 
    padding: max(10px, 1vw);
}


.followed {
    transition: 0.1s ease-in;

    &:hover span {
        display: none;
    }

    &:hover {
        border: 1px solid red !important;
        background-color: rgba(255, 0, 0, 0.1) !important;

        &::before {
            content: 'Unfollow';
            color: red;
            font-weight: 900;
            transition: opacity 0.3s ease-in-out;
        }
    }
}

.edit-profile {

    button {
        padding: 10px;
        border: 1px solid var(--color-heading);
        color: var(--color-text);
        border: none;

        &:hover {
            background-color: var(--color-background-soft);
            color: var(--color-heading);
        }
    }
}


.banner {
    background: var(--color-background-mute);
    border: none;
    border-radius: 0;
    width: 100%;
    aspect-ratio: 3/1;
}

.avatar {
    background: var(--color-background-soft);
    width: 150px;
    aspect-ratio: 1;
    border-radius: 50%;
    margin-left: max(10px, 0.8vw);
    position: absolute;
    bottom: -70px;
    border: 4px solid var(--color-background);
}

    
</style>