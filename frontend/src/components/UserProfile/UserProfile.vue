<script lang="ts">
import { defineComponent } from 'vue';
import type {PropType } from 'vue';
import type { User, Follower, Following } from '@/assets/interfaces';
import { http } from '@/assets/http';
import Timeago from '../Timeago.vue';
import Item from '../Item.vue';
import createIntersectObserver from '@/assets/intersectionObserver'
import { parseISO, format } from "date-fns";

export default defineComponent({
    props: {
        user: { type: Object as PropType<User>, required: true }
    },
    data() {
        return {
            id: this.user.id,
            username: this.user.username,
            email: this.user.email,
            full_name: this.user.full_name,
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
            private: this.user.private,
            notification_on: this.user.notification_on,
            phone: this.user.phone ?? '',
            dob: this.user.dob ?? '',
            link: this.user.link ?? '',
            location: this.user.location ?? '',


            showAvatar: false,
            showBanner: false,
            editProfile: false,


            newAvatar: this.user.avatar as string || "",
            newBanner: this.user.banner as string || "",
            new_FN: '',
            new_LN: '',
            newBio: '',
            newPhone: '',
            newLink: '',
            newDob: '',
            newLocation: '',

            newYear: 0,
            newDay: 0,
            newMonth: 0,
            
            
            avatarFile: null,
            bannerFile: null,

            fileName: null,

            errMsg: '',
            successMsg: '',

            user_followers: new Array<Follower>(),
            user_following: new Array<Following>(),
            show_followers: false,
            show_following: false,

            loading_follow: false,
            loading_follow_request: false,

            zoomAvatar: false,
            zoomBanner: false,
            updatingNotifSettings: false,

            monthNames: [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ],

            following_page: 0,
            followers_page: 0,
            following_hasMore: true,
            followers_hasMore: true,
            userTimestamp: new Date().toISOString(),

            num: 20,
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
                
                if (!this.followed && this.following !== 0) {
                    this.followers -= 1;
                }
                else {
                    this.followers += 1;
                }
            }).catch((err) => {
            });
            this.loading_follow_request = false
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
        },

        async getFollowers() {
            if(this.user_followers.length) {
                return
            }
            this.loading_follow = true;
            await http.get(`follow/get_followers_users/${this.userTimestamp}/${this.followers_page}/${this.username}/`).then((res) => {
                if (res.data.error) {
                    return;
                }
                if(res.data.users) {
                    console.log(res.data)
                    this.user_followers = res.data.users
                    if(res.data.users.length < 20) {
                        this.followers_hasMore = false
                    }
                    else {
                        this.followers_hasMore = true
                    }
                    this.user_followers = res.data.users
                }
            }).catch((err) => {
                console.log(err);
            });
            this.loading_follow = false
            
        },

        async getFollowing() {
            if(this.user_following.length) {
                return
            }
            this.loading_follow = true;
            await http.get(`follow/get_following_users/${this.userTimestamp}/${this.followers_page}/${this.username}/`).then((res) => {
                if (res.data.error) {
                    return;
                }
                if(res.data.users) {
                    this.user_followers = res.data.users
                    if(res.data.users.length < 20) {
                        this.following_hasMore = false
                    }
                    else {
                        this.following_hasMore = true
                    }
                    this.user_following = res.data.users
                }
            }).catch((err) => {
                console.log(err);
            });

            this.loading_follow = false
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
            if (this.new_FN && this.full_name !== this.new_FN) {
                formData.append('full_name', this.new_FN)
            }
            if (this.bio !== this.newBio) {
                formData.append('bio', this.newBio)
            }
            if (this.phone !== this.newPhone) {
                formData.append('phone', this.newPhone)
            }
            if (this.link !== this.newLink) {
                formData.append('link', this.newLink)
            }
            // if (new Date(this.newDob).toUTCString() !== new Date(this.dob).toUTCString()) {
            //     formData.append('dob', this.newDob)
            // }
            if (this.location !== this.newLocation) {
                formData.append('location', this.newLocation)
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
            }).catch(err => {
                this.errMsg = err.response.data.message
            })

        },

        async updateUser(user: User) {
            this.full_name = user.full_name;
            this.bio = user.bio;
            this.avatar = user.avatar;
            this.banner = user.banner;
            this.location = user.location;
            this.dob = user.dob;
            this.link = user.link;
            this.phone = user.phone;

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
            this.new_FN = this.full_name
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
        },

        async updateNotificationSettings() {
            if (!this.$store.state.authenticated) {
                return;
            }
            this.updatingNotifSettings = true

            await http.put(`follow/follow_user/${this.user.id}/`).then((res) => {
                if (res.data.error) {
                    this.$q.notify({
                        message: `<span class="text-white">${res.data.message}</span>`,
                        color: 'negative',
                        position: 'bottom',
                        timeout: 3000,
                        html: true,
                    })
                    return;
                }
                if(res.data.success) {
                    this.notification_on = res.data.notification_on
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

            this.updatingNotifSettings = false
        },
        async onLoadFollowers(index: Number, done: CallableFunction) {
            if(this.followers_hasMore) {
                this.followers_page += 1
                await this.getFollowers()
                done()
            }
            else {
                done()
            }
        },
        async onLoadFollowing(index: Number, done: CallableFunction) {
            if(this.following_hasMore) {
                await this.getFollowing()
                this.following_page += 1
                done()
            }
            else {
                done()
            }
        },
        scrollFollowers() {
            if(this.followers_hasMore) {
                const scrollTop = (this.$refs.followers as HTMLDivElement).scrollTop;
                const scrollHeight = (this.$refs.followers as HTMLDivElement).scrollHeight;
                if(scrollTop + 500 >= scrollHeight) {
                    this.followers_page += 1
                    this.getFollowers()
                }
            }
        },
        scrollFollowing() {
            if(this.following_hasMore) {
                const scrollTop = (this.$refs.following as HTMLDivElement).scrollTop;
                const scrollHeight = (this.$refs.following as HTMLDivElement).scrollHeight;
                if(scrollTop + 500 >= scrollHeight) {
                    this.following_page += 1
                    this.getFollowing()
                }
            }
        },
    },
    created() {
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
    },
    components: { Timeago }
})
</script>

<template>
    <div class="user">
        <div class="user__container  relative">
            <div class=" w-full m-0 p-0 h-fit bg-green relative">
                <div class='banner p-0 w-full relative bg-theme-soft h-full pointer' @click="zoomBanner = true">
                    <img v-if="banner" class="hover-darker w-full" :src="banner" alt="banner"/>
                </div>
                <div class="avatar z-2 pointer overflow-hidden" @click="zoomAvatar = true">
                    <img v-if="avatar" class="profile-pic__image hover-darker w-full " :src="avatar" alt="Profibild" />
                </div>
                <zoomImg v-if="zoomAvatar && avatar" :img="avatar" :open="zoomAvatar" @update:open="zoomAvatar = $event"/>
                <zoomImg v-if="zoomBanner && avatar" :img="banner" :open="zoomBanner" @update:open="zoomBanner = $event"/>

                <div class="edit-profile absolute right-0 text-base h-fit p-2 flex gap-1">
                    <button class="border pointer bg-hover rounded-lg text-heading bg-theme weight-900" v-if="followed">
                        <q-icon :color="$store.state.dark ? 'white' : 'black'" size="1.5rem" name="more_horiz" />
                    </button>
                    <q-btn flat :loading="updatingNotifSettings" @click="updateNotificationSettings" class="border pointer bg-hover rounded-lg text-heading bg-theme weight-900" v-if="followed">
                        <q-icon :color="$store.state.dark ? 'white' : 'black'" v-if="notification_on" size="1.5rem" name="notifications" />
                        <q-icon :color="$store.state.dark ? 'white' : 'black'" v-else size="1.5rem" name="notifications_off" />
                        <template v-slot:loading>
                            <Loading />
                        </template>
                        <q-tooltip :delay="500">
                            {{ notification_on ? 'Notification' : 'Notification Off' }}
                        </q-tooltip>
                    </q-btn>
                    <button v-if="is_current_user" class="border pointer bg-hover-mute rounded-lg px-6 text-heading bg-theme weight-900" @click="editProfile = true">
                        Edit Profile
                    </button>
                    <button v-if="!is_current_user" :class="{'followed': followed}" class="border w-8 pointer bg-hover-soft rounded-lg px-6 text-heading bg-theme weight-900" @click="follow" :disabled="!$store.state.authenticated || loading_follow_request">
                        <span class="weight-900 text-heading"  v-if="!loading_follow_request">{{ followed ? 'Following' : 'Follow' }}</span>
                        <span class="p-0" v-if="loading_follow_request">
                            <Loading size="1.3rem" />
                        </span>
                    </button>
                </div>
            </div>

            <div class="h-full">
                <q-dialog class="h-full w-full p-0 m-0" v-model="editProfile" persistent :maximized="$q.screen.lt.sm ? true : false">
                    <div :class="{'max-h-md': !$q.screen.lt.sm, 'h-viewport': $q.screen.lt.sm}" class="bg-theme border fixed w-full">
                        <div class="sticky top-0 z-10 bg-theme-opacity bg-blur-half border-b">
                            <Item>
                                <template #avatar>
                                    <q-btn flat round v-close-popup >
                                        <q-icon size="2rem" name="close" :color="$store.state.dark ? 'white' : 'dark'"  />
                                    </q-btn>
                                </template>
                                <template #title>
                                    <div class="text-3xl weight-900">Edit Profile</div>
                                </template>
                                <template #icon>
                                    
                                    <button class="px-7 py-2 pointer bg-hover-mute border-brighter-2 bg-transparent rounded text-heading weight-900 text-xl" @click="updateProfile">Save</button>
                                </template>
                            </Item>
                        </div>

                        <div class="q-pt-none">
                            <div class="w-full m-0 p-0 h-fit bg-green relative">
                                <div class='banner p-0 w-full relative bg-theme-soft h-full pointer'>
                                    <img v-if="!newBanner && banner" class="w-full" :src="banner" alt="banner"/>
                                    <img v-else-if="newBanner" :src="newBanner" alt="Profile img" />
                                    <div class="centered-on-image flex gap-5">
                                        <button class="border-none pointer btn-themed-low-op rounded-lg p-3 bg-gray-op" @click="toggleBanner">
                                            <q-icon color="purple-13" name="edit" size="2rem"/>
                                        </button>
                                        <input ref="bannerUpload" type="file" id="file" @change="launchCropper" hidden/>
                                    </div>
                                    <div class=" hidden">
                                        <image-cropper ref="bannerDialog" :aspect-ratio="3/1" :fileName="fileName" :chosen-img="newBanner" @onReset="{($refs.bannerUpload as HTMLInputElement).value = ''; showBanner = false}" @file="bannerFile = $event" @onCrop="(croppedImage: string) => {newBanner = croppedImage}" />
                                    </div>
                                </div>
                                <div class="avatar z-2 profile-img profile-pic overflow-hidden">
                                    <img v-if="!newAvatar && avatar" class="profile-pic__image hover-darker w-full " :src="avatar" alt="Profibild" />
                                    <img v-else-if="newAvatar" class="profile-pic__image" :src="newAvatar" alt="Profile img" />
                                    <div class="centered-on-image">
                                        <button class="border-none pointer btn-themed-low-op rounded-lg p-3 bg-gray-op" @click="toggleAvatar">
                                            <q-icon color="purple-13" name="edit" size="2rem"/>
                                        </button>
                                        <input ref="avatarUpload" type="file" id="file" @change="launchCropper" hidden/>
                                    </div>
                                    <div class="z-100 hidden">
                                        <image-cropper circle ref="avatarDialog" :fileName="fileName" :chosen-img="newAvatar" @close="{newAvatar = ''; showAvatar = false}" @onReset="{($refs.avatarUpload as HTMLInputElement).value = ''; showAvatar = false}" @file="avatarFile = $event" @onCrop="(croppedImage: string) => {newAvatar = croppedImage}" />
                                    </div>
                                </div>
                            </div>
                            <div class="user-profile__info flex flex-col gap-3 w-full">
                                <Input showCharCounts :charLimit="30" :defaultVal="full_name" @update:val="new_FN = $event" input_type="text" input_label="First Name" id="first_name" class="w-full my-2" />
                                <Textarea showCharCounts :charLimit="160" maxHeight="176" height="200px" :defaultVal="bio" @update:val="newBio = $event" input_type="text" input_label="Bio" id="username" class="w-full my-2" />
                                <Input showCharCounts :charLimit="30" :defaultVal="location" @update:val="newLocation = $event" input_type="text" input_label="Location" id="location" class="w-full my-2" />
                                <!-- <Input :defaultVal="dob" @update:val="newDob = $event" input_type="date" input_label="Date of Birth" id="dob" class="w-full my-2" /> -->


                                <div class="grid">
                                    <Select @update:val="newMonth = $event" :defaultVal="newMonth" :pickedYear="newYear" input_type="month" input_label="Month" id="month" />
                                    <Select @update:val="newDay = $event"  :defaultVal="newDay" :pickedMonth="newMonth" :pickedYear="newYear" input_type="day" input_label="Day" id="day" />
                                    <Select @update:val="newYear = $event" :defaultVal="newYear" input_type="year" input_label="Year" id="year" />
                                </div>
                                

                                <!-- <Input showCharCounts :charLimit="30" :defaultVal="phone" @update:val="newPhone = $event" input_type="text" input_label="Phone" id="phone" class="w-full my-2" /> -->
                                <Input showCharCounts :charLimit="100" :defaultVal="link" @update:val="newLink = $event" input_type="text" input_label="Website" id="website" class="w-full my-2" />
                            </div>
                        </div>
                    </div>
                </q-dialog>
            </div>
        
            <div class="user-profile__info flex py-1 mb-5">
                <div class="flex flex-col text-left" >
                    <div class="flex gap-2 items-center">
                        <span class="user-name text-2xl weight-900 text-heading ">
                            {{ full_name }}
                        </span>
                        <span class="h-full " v-if="user.verified" >
                            <q-icon class="vert-align-middle " color="blue"  size="2rem" name="verified">
                                <q-tooltip :delay="1000" class="bg-theme text-heading box-shadow text-sm">
                                    Verified
                                </q-tooltip>
                            </q-icon>
                        </span>
                        <span class="h-full " v-if="user.is_admin || user.is_staff">
                            <q-icon class="vert-align-middle " color="purple-13" size="2rem" name="admin_panel_settings">
                                <q-tooltip :delay="1000" class="bg-theme text-heading box-shadow text-sm">
                                    Staff
                                </q-tooltip>
                            </q-icon>
                        </span>
                        <span class="h-full " v-if="user.private">
                            <q-icon class="vert-align-middle "  :color="$store.state.dark ? 'white' : 'black'" size="2rem" name="lock">
                                <q-tooltip :delay="1000" class="bg-theme text-heading box-shadow text-sm">
                                    Private
                                </q-tooltip>
                            </q-icon>
                        </span>
                    </div>
                    <div class="text-body text-base">@{{ username }}</div>

                    <div class="user-bio text-xl py-2 text-heading weight-600">{{ bio }}</div>

                    <div class="flex flex-row gap-3 mb-3">
                        <div class="user-date_joined flex items-center">
                            <Item dense  avatarSize="1.5rem">
                                <template #avatar>
                                    <q-icon :color="$store.state.dark ? 'white' : 'black'" name="date_range" size="1.5rem" />
                                </template>
                                <template #title>
                                    <div class="flex items-center text-lg">
                                        <span class="text-body mr-1">Joined</span> 
                                        <!-- <Timeago class="text-body" size="1rem" :date="date_joined" date_type="any" /> -->
                                        <span class="text-lg text-body">
                                            {{ `${monthNames[new Date(date_joined).getMonth()]} ${new Date(date_joined).getUTCDate()}, ${new Date(date_joined).getFullYear()}` }}
                                        </span>
                                    </div>
                                </template>
                            </Item>
                        </div>
                        <div v-if="link" class="user-date_joined">
                            <Item dense  avatarSize="1.5rem">
                                <template #avatar>
                                    <i-link fill="var(--color-heading)" size="1.5rem"/>
                                </template>
                                <template #title>
                                    <div class="text-lg text-body">
                                        <a target="_blank" :href="link" class="mr-1 text-body text-theme weight-900 no-decor hover-underline">{{ link }}</a>
                                    </div>
                                </template>
                            </Item>
                        </div>
                        <div class="flex gap-3">
                        <div v-if="dob"  class="user-date_joined">
                            <Item  dense avatarSize="2rem">
                                <template #avatar>
                                    <i-balloon size="2rem" fill="var(--color-heading)"/>
                                </template>
                                <template #title>
                                    <span class="text-lg text-body">
                                        {{ `${monthNames[new Date(dob).getMonth()]} ${new Date(dob).getUTCDate()}, ${new Date(dob).getFullYear()}` }}
                                    </span>
                                </template>
                            </Item>
                        </div>
                        <div v-if="location" class="user-date_joined">
                            <Item dense avatarSize="2rem">
                                <template #avatar>
                                    <q-icon :color="$store.state.dark ? 'white' : 'black'" name="place" size="2rem" class="primary" />
                                </template>
                                <template #title>
                                    <div class="text-lg text-body">
                                        {{ location }}
                                    </div>
                                </template>
                            </Item>
                        </div>
                    </div>
                    </div>
                    
                    
                    <div class="follows text-lg flex items-center gap-3">
                        <span class="text-body pointer hover-underline" @click="{show_followers = true; getFollowers()}"><span class="text-heading weight-900">{{ followers }} </span> Followers</span> 
                        <span class="text-body pointer hover-underline" @click="{show_following = true; getFollowing()}"><span class="text-heading weight-900">{{ following }} </span> Following</span>
                    </div>

                    <div class="relative w-full">
                        <q-dialog class="w-full" v-model="show_followers" :maximized="$q.screen.lt.sm ? true : false">
                            <!-- <div ref="followers" :class="{'max-h-sm max-w-xs': !$q.screen.lt.sm, 'h-viewport': $q.screen.lt.sm}" class="bg-theme border w-full h-full">
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
                                    <Item clickable :to="{ name: 'user-profile', params: { username: user.following_user.username } }">
                                        <template #avatar>
                                            <img :src="user.following_user.avatar" alt="user profile pic"/>
                                        </template>
                                        <template #title>
                                            <div class="text-heading weight-900">
                                                {{ user.following_user.full_name }}
                                                <q-icon v-if="user.following_user.private" name="lock" />
                                            </div>
                                        </template>
                                        <template #caption>
                                            <div class="text-body">{{ user.following_user.username }}</div>
                                        </template>
                                        <template #icon>
                                            <button @click.stop="" v-if="!user.following_user.is_following && !user.following_user.is_current_user" class="pointer bg-web-theme bg-web-theme-hover border-none text-heading weight-900 rounded px-5 py-2">
                                                Follow
                                            </button>
                                            <button v-else-if="!user.following_user.is_current_user" class="pointer bg-web-theme border-none text-heading weight-900 rounded px-5 py-2">
                                                Following
                                            </button>
                                        </template>
                                    </Item>
                                </div>
                            </div> -->
                            <div @scroll="scrollFollowers" ref="followers" :class="{'max-h-sm max-w-xs': !$q.screen.lt.sm, 'h-viewport': $q.screen.lt.sm}" class="bg-theme border w-full h-full">
                                <div class="p-1 w-full sticky top-0 z-10 bg-theme-opacity bg-blur-half border-b h-fit">
                                    <Item>
                                        <template #title>
                                            <div class="text-2xl weight-900">Followers</div>
                                        </template>
                                        <template #icon>
                                            <div class="pointer" @click="show_followers = !show_followers">
                                                <i-close :vert-icon-center="true" fill="var(--color-heading)" stroke="none"  size="2rem"/>
                                            </div>
                                        </template>
                                    </Item>
                                </div>
                                <div v-if="loading_follow" class="p-5 flex justify-center items-center">
                                    <Loading/>
                                </div>
                                <div v-else-if="!loading_follow && user_followers" class="h-fit w-full">
                                    <div v-for="user in user_followers" :key="user.id" class="caption">
                                        <Item clickable :to="{ name: 'user-profile', params: { username: user.following_user.username } }">
                                            <template #avatar>
                                                <img :src="user.following_user.avatar" alt="user profile pic"/>
                                            </template>
                                            <template #title>
                                                <div class="text-heading weight-900">
                                                    {{ user.following_user.full_name }}
                                                    <q-icon v-if="user.following_user.private" name="lock" />
                                                </div>
                                            </template>
                                            <template #caption>
                                                <div class="text-body">@{{ user.following_user.username }}</div>
                                            </template>
                                            <template #icon>
                                                <button @click.stop="" v-if="!user.following_user.is_following && !user.following_user.is_current_user" class="pointer bg-web-theme bg-web-theme-hover border-none text-heading weight-900 rounded px-5 py-2">
                                                    Follow
                                                </button>
                                                <button v-else-if="!user.following_user.is_current_user" class="pointer bg-web-theme border-none text-heading weight-900 rounded px-5 py-2">
                                                    Following
                                                </button>
                                            </template>
                                        </Item>
                                    </div>
                                </div>
                                <!-- <q-infinite-scroll @load="onLoadFollowers" :offset="250" class="w-full h-full">
                                    <div v-for="user in user_followers" :key="user.id" class="caption">
                                        <Item clickable :to="{ name: 'user-profile', params: { username: user.following_user.username } }">
                                            <template #avatar>
                                                <img :src="user.following_user.avatar" alt="user profile pic"/>
                                            </template>
                                            <template #title>
                                                <div class="text-heading weight-900">
                                                    {{ user.following_user.full_name }}
                                                    <q-icon v-if="user.following_user.private" name="lock" />
                                                </div>
                                            </template>
                                            <template #caption>
                                                <div class="text-body">{{ user.following_user.username }}</div>
                                            </template>
                                            <template #icon>
                                                <button @click.stop="" v-if="!user.following_user.is_following && !user.following_user.is_current_user" class="pointer bg-web-theme bg-web-theme-hover border-none text-heading weight-900 rounded px-5 py-2">
                                                    Follow
                                                </button>
                                                <button v-else-if="!user.following_user.is_current_user" class="pointer bg-web-theme border-none text-heading weight-900 rounded px-5 py-2">
                                                    Following
                                                </button>
                                            </template>
                                        </Item>
                                    </div>
                                    <template v-slot:loading>
                                        <div class="row justify-center q-my-md">
                                            <Loading />
                                        </div>
                                    </template>
                                </q-infinite-scroll> -->
                            </div>
                            
                        </q-dialog>

                        <q-dialog class="w-full" v-model="show_following" :maximized="$q.screen.lt.sm ? true : false">
                            <div @scroll="scrollFollowing" ref="following" class="bg-theme border w-full max-w-xs h-full max-h-sm">
                                <div class="p-1 w-full sticky top-0 z-10 bg-theme-opacity bg-blur-half border-b h-fit">
                                    <Item>
                                        <template #title>
                                            <div class="text-2xl weight-900">Following</div>
                                        </template>
                                        <template #icon>
                                            <div class="pointer" @click="show_following = !show_following">
                                                <i-close :vert-icon-center="true" fill="var(--color-heading)" stroke="none"  size="2rem"/>
                                            </div>
                                        </template>
                                    </Item>
                                </div>
                                <div v-if="loading_follow" class="p-5 flex justify-center items-center">
                                    <Loading/>
                                </div>
                                <!-- <div class="results-even" v-else-if="!loading_follow && user_following" v-for="user in user_following">
                                    <Item clickable :to="{ name: 'user-profile', params: { username: user.followed_user.username } }">
                                        <template #avatar>
                                            <img :src="user.followed_user.avatar" alt="user profile pic"/>
                                        </template>
                                        <template #title>
                                            <div class="text-heading weight-900">{{ user.followed_user.full_name }}</div>
                                        </template>
                                        <template #subtitle>
                                            <div class="text-heading text-base">@{{ user.followed_user.username }}</div>
                                        </template>
                                        <template v-if="user.followed_user.is_following" #caption>
                                            <div class="text-body text-sm">Follows you</div>
                                        </template>
                                    </Item>
                                </div> -->
                                <div class="h-fit w-full">
                                    <div v-if="!loading_follow && user_following" v-for="user in user_following" :key="user.id" class="caption">
                                        <Item clickable :to="{ name: 'user-profile', params: { username: user.followed_user.username } }">
                                            <template #avatar>
                                                <img :src="user.followed_user.avatar" alt="user profile pic"/>
                                            </template>
                                            <template #title>
                                                <div class="text-heading weight-900">
                                                    {{ user.followed_user.full_name }}
                                                    <q-icon v-if="user.followed_user.private" name="lock" />
                                                </div>
                                            </template>
                                            <template #caption>
                                                <div class="text-body">@{{ user.followed_user.username }}</div>
                                            </template>
                                            <template #icon>
                                                <button @click.stop="" v-if="!user.followed_user.is_following && !user.followed_user.is_current_user" class="pointer bg-web-theme bg-web-theme-hover border-none text-heading weight-900 rounded px-5 py-2">
                                                    Follow
                                                </button>
                                                <button v-else-if="!user.followed_user.is_current_user" class="pointer bg-web-theme border-none text-heading weight-900 rounded px-5 py-2">
                                                    Following
                                                </button>
                                            </template>
                                        </Item>
                                    </div>
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
    width: 100% !important;
    aspect-ratio: 3/1 !important;
}

.banner {
    img {
        width: 100%;
        background-color: var(--color-background-soft);
        aspect-ratio: 3/1;
        object-fit: cover;
    }
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

.grid {
    display: grid;
    grid-template-columns: 2fr repeat(2, 1fr);
    gap: 10px;
}

    
</style>