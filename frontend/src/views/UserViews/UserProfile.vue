<script lang="ts">
import { defineComponent, toHandlers } from 'vue';
import type { User } from '@/assets/interfaces';
import { http } from '@/assets/http';
import UserLiked from './UserLiked.vue';
import { Cookies, useQuasar } from 'quasar';

export default defineComponent({
    props: {
        user: {type: Object as () => User, required: true}
    },
    setup() {
        // const {cookies} = useCookies();
        // return {cookies}
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
        }
    },
    
    methods: {
        follow() {
            // console.log(Cookies.get("access_token"))
            http.post(`follow/follow_user/${this.id}/`, {}, {
                headers: {
                    "Authorization": `Bearer ${Cookies.get("access_token")}`,
                }}
            ).then((res) => {
                if(res.data.error) {
                    return
                }
                this.followed = !this.followed
                console.log(this.followed)
                if(!this.followed && this.following != 0) {
                    this.following -= 1
                } else {
                    this.following += 1
                }
            }).catch((err) => {
                console.log(err)
            })
        },
        if_followed() {
            http.get(`follow/get_if_followed/${this.id}/`, {
                headers: {
                    "Authorization": `Bearer ${Cookies.get("access_token")}`,
                }
            }).then((res) => {
                console.log("followed: ", res.data.followed)
                this.followed = res.data.followed
            }).catch((err) => {
                this.followed = false
            })
        }
    },
    created() {
        this.if_followed()
    },
})
</script>

<template>
    <div class="user row justify-center">
        <div class="user__container col-12 col-md-auto">
            <div class="user__profile__avatar">
                <q-avatar size="200px" class="avatar">
                    <img v-if="avatar" :src="avatar" />
                    <q-icon v-else size="200px" name="face" />
                </q-avatar>
            </div>
            <!-- <h3 class="text-center">
                <span class="user__username">@{{username}}</span>
                <span> <q-icon name="verified" /></span>
            </h3> -->
            <q-item class="user__username">
                <q-item-section class="">@{{ username }}</q-item-section>
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
                    <h6 class="user__name">{{first_name}} {{last_name}}</h6>
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
}

.avatar {
    border: 1px solid var(--color-text);
    /* border-radius: 50%; */
    width: 200px;
    height: 200px;
    overflow: hidden;
    margin: 15px 0;
}

.user__username {
    text-align: center;
    position: relative;
    font-size: 40px;
    font-weight: bolder;
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
    padding-right: 10px;
    padding-left: 10px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    max-width: 100%;
}

.user__social .user__following, .user__followers, .user__posts {
    display: grid;
    justify-content: center;
}

.user__follow__btn {
    width: 100%;
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
    
</style>