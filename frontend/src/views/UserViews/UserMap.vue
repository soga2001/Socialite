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
        <div class="user__profile__div">
            <img src="" class="user__profile" width="100" height="100" alt="User Profile"/>
        </div>
        <div class="user__profile__info">
            <h1 class="user__username">{{username}}</h1>
            <h3 class="user__name">{{first_name}} {{last_name}}</h3>
            <h4 class="user__active__status">Is Active: {{is_active}}</h4>
            <h5 class="User__last__on">Last logged in: {{last_login}}</h5>
        </div>
    </div>
</template>

<style scoped>

.user {
    position: relative;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
}

.user__profile {
    position: absolute;
    right: 0;
    margin: 5px;
    border-radius: 50px;
    background-color: var(--color-text);
}

.user__profile__info {
    padding: 0 30px;
}

    
</style>