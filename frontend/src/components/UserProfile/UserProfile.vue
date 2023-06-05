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
            posts: this.user.total_posted,
            followers: this.user.total_followers,
            following: this.user.total_following,
            followed: false,
            date_joined: this.user.date_joined,
            loading: true,
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
        }
    },
    created() {
        // console.log(this.date_joined)
        this.if_followed();
        
    },
    mounted() {
    },
    components: { Timeago, Item }
})
</script>

<template>
    
    <div class="user row justify-center">
        <div class="user__container col-12 col-md-auto">
            <div class=' grid cols-auto-fr rows-4 relative h-fit'>
                <div id="banner" class='p-0 col-start-1 col-span-full z-1 bg-theme-soft'>
                    <img class="" src="https://unsplash.it/1000/1000/?random&pic=1" id="header-background-id" alt="background-img"/>
                </div>
                <div class="profile-img profile-pic relative overflow-hidden z-3">
                    <img v-if="avatar" class="profile-pic__image" :src="avatar" width="150" height="150" alt="Profibild" />
                    <img v-else class="profile-picture" src="https://unsplash.it/300/300/?random&pic=1(14 kB)" alt="profile-picture"/>
                    <div class="profile-pic__content">
                        <span class="profile-pic__icon"><q-icon size="30px" name="photo_camera"/></span>
                        <span class="profile-pic__text">Edit Profile</span>
                    </div>
                </div>
                <div class="edit-profile w-full h-fit flex flex-row-reverse p-2">
                    <button v-if="$store.state.user.id != id && !loading" class="border btn rounded text-heading bg-transparent weight-900" @click="follow" :disabled="!$store.state.authenticated">{{ followed ? 'Unfollow' : 'Follow' }}</button>
                    <button v-if="$store.state.authenticated && $store.state.user.id == id" class="border btn rounded text-heading bg-transparent weight-900" @click="">Edit Profile</button>
                    <q-btn @click.stop="" v-if="followed && !loading" size="16px" class="less" flat dense round icon="notifications" />
                    <q-btn @click.stop="" v-if="followed && !loading"  size="16px" class="more__vert" flat dense round icon="more_horiz" />
                </div>
            </div>
            <div>
                
            </div>
        
            <div class="user__profile__info">
                <Item title-size="30px">
                    <template #title>
                        <span class="joined"> {{first_name }} {{last_name }}</span>
                    </template>
                    <template #caption>
                        <span class="joined">@{{ username }}</span>
                    </template>
                </Item>
                <div class="user__bio">
                    <h6><span class="joined"> Joined <Timeago class="timeago" size="15px" date_type="relative" :date="date_joined" /></span> </h6>
                    <h6 class="user__caption">{{bio}}</h6>
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




.avatar {
    border: 1px solid var(--color-text);
    width: 10rem;
    height: 10rem;
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

.user__profile__info {
    /* padding: 0 30px; */
    margin-left: 2vw;
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
    aspect-ratio: 3/1;
}

#banner:hover {
    cursor: pointer;
}

#banner img {
    object-fit: cover;
    width: 100%;
    height: 100%;
}

.profile-img {
    grid-column: 1;
    grid-row: row 3 / span 3;
    min-width: 90px;
    min-height: 90px;
    padding: 2px;
    width: 8vw;
    height: 8vw;
    margin-left: 2vw;
    z-index: 2;
    background-color: var(--color-background);
}

.profile-img:hover {
    cursor: pointer;
}

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