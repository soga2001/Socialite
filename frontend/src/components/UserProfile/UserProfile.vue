<script lang="ts">
import { defineComponent } from 'vue';
import type {PropType } from 'vue';
import type { User } from '@/assets/interfaces';
import { http } from '@/assets/http';
import Timeago from '../Timeago.vue';
import { useCookies } from 'vue3-cookies';
import { Crypter } from '@/assets/crypter';

export default defineComponent({
    props: {
        user: { type: Object as PropType<User>, required: true }
    },
    setup() {
        const {cookies} = useCookies();
        return {cookies}
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
            bio: this.user.profile.bio,
            avatar: this.user.profile.avatar,
            posts: this.user.total_posted,
            followers: this.user.total_followers,
            following: this.user.total_following,
            followed: false,
            date_joined: this.user.date_joined,
        };
    },
    methods: {
        follow() {
            if (!this.$store.state.authenticated) {
                return;
            }
            http.post(`follow/follow_user/${this.id}/`, {}, {
                headers: {
                    "Authorization": "Bearer " + Crypter.decrypt(this.cookies.get("access_token")),
                }
            }).then((res) => {
                if (res.data.error) {
                    return;
                }
                this.followed = !this.followed;
                console.log(this.followed);
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
        if_followed() {
            if (!this.$store.state.authenticated) {
                return;
            }
            http.get(`follow/get_if_followed/${this.id}/`, {
                headers: {
                    "Authorization": "Bearer " +  Crypter.decrypt(this.cookies.get("access_token")),
                }
            }).then((res) => {
                // console.log("followed: ", res.data.followed);
                this.followed = res.data.followed;
            }).catch((err) => {
                this.followed = false;
                console.log("error");
            });
        }
    },
    created() {
        // console.log(this.date_joined)
        this.if_followed();
    },
    components: { Timeago }
})
</script>

<template>
    
    <div class="user row justify-center">
        <div class="user__container col-12 col-md-auto">
            <div class="user__profile__avatar">
                <!-- https://uiverse.io/igoramos77/silly-fireant-70 -->
                <q-avatar size="200px" class="avatar">
                    <img v-if="avatar" :src="avatar" />
                    <q-icon v-else size="200px" name="face" />
                </q-avatar>
                <!-- https://stackoverflow.com/questions/67104652/hover-effect-change-your-picture-with-icon-on-profile-picture -->
                <!-- <div class="profilepic">
                    <img v-if="avatar" class="profilepic__image" :src="avatar" width="150" height="150" alt="Profibild" />
                    <q-avatar v-else icon="face" class="profilepic__image" size="150px" />
                    <div class="profilepic__content">
                        <span class="profilepic__icon"><q-icon size="30px" name="photo_camera"/></span>
                        <span class="profilepic__text">Edit Profile</span>
                    </div>
                </div> -->
            </div>
            <q-item class="user__username text-center">
                <q-item-section class="username">@{{ username }}</q-item-section>
                <!-- <q-item-section avatar class="right">
                    <q-icon name="verified" />
                    <q-icon name="admin_panel_settings" />
                    <q-icon name="stars" color="" />
                </q-item-section> -->
            </q-item>
            <div class="user__profile__info">
                <div class="user__social">
                    <div class="user__following">
                        <h6>Following</h6> 
                        <p class="text-center bold">{{ followers }}</p>
                        <!-- <q-skeleton type="text" width="30px" /> -->
                    </div>
                    <div class="user__followers">
                        <h6>Followers</h6>
                        <p class="text-center bold">{{ following }}</p>
                        <!-- <q-skeleton type="text" width="30px" /> -->
                    </div>
                    <div class="user__posts">
                        <h6>Posts</h6>
                        <p class="text-center bold">{{ posts }}</p>
                    </div>
                </div>
                <div>
                    <button class="user__follow__btn bold" :hidden="$store.state.user.id == id" @click="follow" :disabled="!$store.state.authenticated">{{ followed ? 'Unfollow' : 'Follow' }}</button>
                    <button class="user__follow__btn bold" :hidden="$store.state.user.id != id" @click="" disabled>Edit Profile</button>
                </div>
                <div class="user__bio">
                    <!-- <q-icon name="calendar_month"><Timeago :date="date_joined"/></q-icon> -->
                    <!-- <h6 class="joined"><q-icon size="30px" name="calendar_month" /> <Timeago date_type="relative" :date="date_joined" /></h6> -->
                    <div>
                        <span class="joined"><q-icon class="icon" size="15px" name="calendar_month" /> Joined <Timeago class="timeago" size="15px" date_type="relative" :date="date_joined" /></span>
                    </div>
                    <h6 class="user__caption">{{bio}}</h6>
                </div>
            </div>
        </div>
  </div>
</template>

<style scoped>

.user {
    padding: 20px;
}
.user__container {
    max-width: 600px;
    width: 100%;
}


.user__profile__avatar {
    display: flex;
    justify-content: center;
    justify-items: center;
    align-items: center;
    align-content: center;
}

.avatar {
    border: 1px solid var(--color-text);
    width: 10rem;
    height: 10rem;
}
.user__username {
    font-size: 20px;
}

.right {
    position: absolute;
    display: inline-block;
    right: 0;
    top: 0;
    bottom: 0;
}

.user__profile__info {
    /* padding: 0 30px; */
    display: grid;
    
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
    width: 100%;
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
.profilepic {
  position: relative;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  background-color: var(--color-background-mute);
}

.profilepic:hover .profilepic__content {
  opacity: 1;
}

.profilepic:hover .profilepic__image {
  opacity: .3;
}

.profilepic__image {
  object-fit: cover;
  opacity: 1;
  transition: opacity .2s ease-in-out;
}

.profilepic__content {
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
}

.profilepic__icon {
  color: var(--color-heading);
  padding-bottom: 8px;
}

.fas {
  font-size: 20px;
}

.profilepic__text {
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
    
</style>