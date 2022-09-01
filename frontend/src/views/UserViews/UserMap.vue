<script lang="ts">
import { defineComponent, toHandlers } from 'vue';
import type { User } from '@/assets/interfaces';

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
            last_login: this.user.last_login
        }
    },
    methods: {
        maskEmail() {

        }
    }
})
</script>

<template>
    <div class="user">
        <div class="user__profile__avatar">
            <img src="" class="user__avatar" alt="User Profile"/>
        </div>
        <div class="user__profile__info">
            <h1 class="user__username">{{username}}</h1>
            <div class="user__social">
                <div class="user__following">
                    <h5>Following</h5> 
                    <h6>10</h6>
                </div>
                <div class="user__followers">
                    <h5>Followers</h5>
                    <h6>10</h6>
                </div>
                <div class="user__posts">
                    <h5>Posts</h5>
                    <h6>10</h6>
                </div>
            </div>
            <div>
                <button class="user__follow__btn">Follow</button>
            </div>
            <div class="user__bio">
                <h3 class="user__name">{{first_name}} {{last_name}}</h3>
                <h4 class="user__caption">Bio</h4>
            </div>
        </div>
    </div>
</template>

<style scoped>

.user {
    position: relative;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    max-width: 1000px;
    min-width: 300px;
    width: 100%;
    margin: auto;
    padding: 40px;
}


/* .user__profile__avatar {
    left: 50%;
} */

.user__avatar {
    float: right;
    margin: 5px;
    border-radius: 50%;
    background-color: var(--color-text);
    max-width: 200px;
    max-height: 200px;
    width: 100%;
    height: 100%;
    min-width: 100px;
    min-width: 100px;
}

.user__profile__info {
    padding: 0 30px;
}

.user__social {
    display: flex;
}

.user__social {
    padding-right: 10px;
    padding-left: 10px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    text-align: center;
    max-width: 100%;
}

.user__social .user__following, .user__followers, .user__posts {
    display: grid;
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