<script lang="ts">
import { defineComponent, toHandlers } from 'vue';
import type { User } from '@/assets/interfaces';
import { http } from '@/assets/http';

export default defineComponent({
    props: {
        user: {type: Object as () => User, required: true}
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
            avatar: this.user.profile.avatar
        }
    },
    methods: {
        maskEmail() {

        }
    },
})
</script>

<template>
    <div class="user row justify-center">
        <div class="user__container col-12 col-md-auto">
            <h2 class="user__username">@{{username}}</h2>
            <div class="user__profile__avatar">
                <q-avatar size="200px" class="avatar">
                    <img v-if="avatar" :src="avatar" />
                    <q-icon v-else size="200px" name="face" />
                </q-avatar>
            </div>
            <div class="user__profile__info">
                <div class="user__social">
                    <div class="user__following">
                        <h6>Following</h6> 
                        <q-skeleton type="text" width="30px" />
                    </div>
                    <div class="user__followers">
                        <h6>Followers</h6>
                        <q-skeleton type="text" width="30px" />
                    </div>
                    <div class="user__posts">
                        <h6>Posts</h6>
                        <q-skeleton type="text" width="30px" />
                    </div>
                </div>
                <div>
                    <button class="user__follow__btn">Follow</button>
                </div>
                <div class="user__bio">
                    <h3 class="user__name">{{first_name}} {{last_name}}</h3>
                    <h4 class="user__caption">{{bio}}</h4>
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
    font-size: 50px;
    font-weight: bolder;
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
}

.user__bio {
    padding: 20px;
}

.user__caption {
    color: var(--color-text)
}
    
</style>