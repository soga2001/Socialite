<script lang="ts">
import { defineComponent, ref } from 'vue';
import type { User } from '@/assets/interfaces';

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
            timer:  ref<number | null>(),
            user: this.userProp,

        }
    },
    methods: {

        divEnter() {
            if(this.$q.screen.lt.sm) {
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
            if(this.$q.screen.lt.sm) {
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
    }
})

</script>

<template>
    <div>
        <div @click.stop="$router.push({name: 'user-profile', params: { username: user.username }})" @mouseover="divEnter"  @mouseleave="divExit" class="ellipsis">
            <slot name="text" />
        </div>

        <q-menu
            v-model="hovering"
            class="bg-theme border rounded-sm px-3 pt-1 pb-3 max-w-68"
            @mouseover="divEnter"
            @mouseleave="divExit"
            :offset="[0, 10]"
            
            >
            <div class="flex flex-col gap-3 p-2">
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
</style>