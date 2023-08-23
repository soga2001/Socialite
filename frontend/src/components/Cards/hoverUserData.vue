<script lang="ts">
import { defineComponent, ref } from 'vue';
import type { User } from '@/assets/interfaces';

import UserProfile from '../UserProfile/UserProfile.vue';
import { http } from '@/assets/http';
export default defineComponent({
    props: {
        userProp: {
            type: Object as () => User,
            required: true,
        }
    },
    data() {
        return {
            hovering: false,
            timer: ref<number | null>(),
            user: this.userProp,
            loading_follow_request: false,
            followed: this.userProp.is_following,
            followers: this.userProp.total_followers,
            following: this.userProp.total_following,
        };
    },
    methods: {
        async follow() {
            if (!this.$store.state.authenticated) {
                return;
            }
            this.loading_follow_request = true

            await http.post(`follow/follow_user/${this.user.id}/`).then((res) => {
                if (res.data.error) {
                    return;
                }
                this.followed = !this.followed;
                this.loading_follow_request = false;
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
        divEnter() {
            if (this.$q.screen.lt.sm) {
                return;
            }
            if (this.timer) {
                clearTimeout(this.timer);
            }
            if (!this.hovering) {
                this.timer = setTimeout(() => {
                    this.hovering = true;
                    this.timer = null;
                }, 500);
            }
        },
        divExit() {
            if (this.$q.screen.lt.sm) {
                return;
            }
            if (this.timer) {
                clearTimeout(this.timer);
            }
            if (this.hovering) {
                this.timer = setTimeout(() => {
                    this.hovering = false;
                    this.timer = null;
                }, 300);
            }
        },
        dontCloseMenu() {
            setTimeout(() => {
                if (this.timer) {
                    clearTimeout(this.timer);
                }
                this.hovering = true;
                this.timer = null;
            }, 200)
            
        }
    },
    components: { UserProfile }
})

</script>

<template>
    <div>
        <div @click.stop="$router.push({name: 'user-profile', params: { username: user.username }})" @mouseover="divEnter"  @mouseleave="divExit" class="ellipsis">
            <slot name="text" />
        </div>

        <q-menu
            v-model="hovering"
            no-focus
            class="bg-transparent border-brighter-2 menu"
            @mouseover="divEnter"
            @mouseleave="divExit"
            :offset="[0, 10]"
            
            >
            <!-- <div class="flex flex-col gap-3 p-2">
                <Item dense class="p-0 m-0" avatar-size="5rem" align-items="start">
                    <template #avatar >
                        <q-avatar size="5rem" class="hover-darker pointer" @click.stop="$router.push({name: 'user-profile', params: { username: user.username }})">
                            <img :src="user.avatar" alt="User Avatar" />   
                        </q-avatar>
                    </template>


                    <template #icon>
                        <button v-if="$store.state.user.id != user.id" :class="{'followed': user.is_following}" class="border w-8 pointer bg-hover-mute rounded-lg px-4 py-2 text-heading text-lg bg-theme weight-900" @click="" :disabled="!$store.state.authenticated">
                            <span v-if="user.is_following" class=" weight-900">Following</span>
                            <span v-else class=" weight-900">Follow</span>
                        </button>
                    </template>
                </Item>
                <div>
                    <Item dense>
                        <template #title>
                            <div class="text-2xl weight-900 hover-underline pointer" @click.stop="$router.push({name: 'user-profile', params: { username: user.username }})">{{ user.first_name }} {{ user.last_name }}</div>
                        </template>
                        <template #caption>
                            <div class="text-base weight-700 w-fit text-lighter wrap" >
                                @{{user.username}}
                            </div>
                        </template>
                    </Item>
                </div>
                <div>
                    <div :style="{wordWrap: 'break-word'}" class="text-base weight-900 no-wrap">{{ user.bio }}</div>
                </div>
                <div>
                    <Item dense>
                        <template #title>
                            <div class="text-base weight-900 flex gap-2 w-full">
                                <div>
                                    <span class="text-base weight-900">
                                        {{ user.total_followers  }}
                                    </span>
                                    <span class="text-lighter">
                                        Followers
                                    </span>
                                </div>

                                <div>
                                    <span class="text-base weight-900">
                                        {{ user.total_following  }}
                                    </span>
                                    <span class="text-lighter">
                                        Following
                                    </span>
                                </div>
                            </div>
                        </template>
                    </Item>
                </div>
            </div> -->
            <!-- <div class="profile-card">
                <UserProfile @click="dontCloseMenu" :user="user" />
            </div> -->



            <div class="card bg-theme">
                <div class="cover-photo"  :style="{backgroundImage: `url(${user.banner})`, backgroundColor: 'var(--color-background-mute)'}">
                    <img v-if="user.avatar" :src="user.avatar" class="profile">
                    <span v-else class="profile"></span>
                    <button v-if="!user.is_current_user" :class="{'followed': followed}" class="border w-8 pointer btn-following bg-hover-mute rounded-lg px-4 py-2 text-heading text-sm bg-theme weight-900" @click="follow" :disabled="!$store.state.authenticated">
                        <span v-if="followed" class=" weight-900">Following</span>
                        <span v-else class="weight-900">Follow</span>
                    </button>
                </div>
                <div class="user-info flex flex-col gap-3">
                    <div >
                        <Item dense >
                            <template #title>
                                <div class="text-2xl weight-900 w-fit" >
                                    <span class="hover-underline pointer" @click.stop="$router.push({name: 'user-profile', params: { username: user.username }})">{{ user.first_name }} {{ user.last_name }}</span>
                                </div>
                            </template>
                            <template #caption>
                                <div class="text-base weight-700 w-fit  wrap" >
                                    <span class="text-lighter hover-underline pointer" @click.stop="$router.push({name: 'user-profile', params: { username: user.username }})">
                                        @{{user.username}}
                                    </span>
                                </div>
                            </template>
                        </Item>
                    </div>
                    <div>
                        <div :style="{wordWrap: 'break-word'}" class="text-base text-heading weight-700 no-wrap">{{ user.bio }}</div>
                    </div>
                    <div>
                        <Item dense>
                            <template #title>
                                <div class="text-base weight-500 flex gap-2 w-full">
                                    <div>
                                        <span class="text-base weight-900">
                                            {{ followers  }}
                                        </span>
                                        <span class="text-body">
                                            Followers
                                        </span>
                                    </div>

                                    <div>
                                        <span class="text-base weight-900">
                                            {{ following  }}
                                        </span>
                                        <span class="text-body">
                                            Following
                                        </span>
                                    </div>
                                </div>
                            </template>
                        </Item>
                    </div>
                </div>
                
            </div>
        </q-menu>
    </div>
</template>

<style scoped lang="scss">

.followed {
  &:hover {
    span {
      display: none;
    }

    border: 1px solid red !important;
    background-color: rgba(255, 0, 0, 0.1) !important;

    &::before {
      content: 'Unfollow';
      // font-size: 20px;
      color: red;
      font-weight: 900;
      transition: opacity 0.3s ease-in-out;
    }
  }
}

@import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@300;700&display=swap");



.menu {
    // width: 300px;
    height: fit-content;
}


.card {
    width: 300px;
}

.cover-photo {
    position: relative;
    background-size: cover;
    width: 100%;
    aspect-ratio: 3/1;
}

.profile {
    position: absolute;
    width: 110px !important;
    aspect-ratio: 1/1 !important;
    height: auto;
    bottom: -55px;
    left: 15px;
    border-radius: 50%;
    border: 4px solid var(--color-background);
    background: var(--color-background-mute);
}

.btn-following {
    position: absolute;
    bottom: -45px;
    right: 10px;
}

.user-info {
    margin-top: 50px;
    padding: 10px 10px 20px 15px;
}

.btn {
    margin: 30px 15px;
    background: #7ce3ff;
    padding: 10px 25px;
    border-radius: 3px;
    border: 1px solid #7ce3ff;
    font-weight: bold;
    font-family: Montserrat;
    cursor: pointer;
    color: #222;
    transition: 0.2s;
}

.btn:last-of-type {
    background: transparent;
    border-color: #7ce3ff;
    color: #7ce3ff;
}

.btn:hover {
    background: #7ce3ff;
    color: #222;
}

// .icons {
//     width: 180px;
//     margin: 0 auto 10px;
//     display: flex;
//     justify-content: space-between;
//     gap: 15px;
// }

// .icons i {
//     cursor: pointer;
//     padding: 5px;
//     font-size: 18px;
//     transition: 0.2s;
// }

// .icons i:hover {
//     color: #7ce3ff;
// }

</style>