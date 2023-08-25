<script lang="ts">
import { defineComponent } from 'vue'
import { routerKey } from 'vue-router'
export default defineComponent({
    name: 'settings',
    props:{
        scrollPosition: {
            type: Number,
            default: 0,
        },
        height: {
            type: Number,
            default: 0,
        }
    },
    data() {
        return {
            hide: false,
            val: ''
        }
    },
    methods: {
    },
    beforeRouteEnter: (to, from) => {
        if(window.innerWidth > 768 && to.name === 'settings') {
            return {name: 'account'}
        }
    },
    beforeMount() {
        // const route =  this.$route.name ?? ''
        // console.log(route)
        // if (route !== 'settings' && this.$q.screen.lt.sm) {
        //     this.hide = true
        // }
        // else if(route === 'settings') {
        //     this.hide = false
        // }
    },
    mounted() {
    },
    watch: {
        '$route': function(to, from) {
            const route =  this.$route.name ?? ''
            if (route !== 'settings') {
                this.hide = true
            }
            else {
                this.hide = false
            }
            if(window.innerWidth > 768 && route === 'settings') {
                this.$router.push({name: 'account'})
            }
        },
    },
})
</script>

<template>
    <div :class="{'cols-2': !$q.screen.lt.sm}" class="grid w-full h-full h-viewport p-0">
        <header class="border-r h-full w-full bg-theme" v-if="($route.matched[0].name === 'settings' && ($route.matched[1] === undefined || !$q.screen.lt.sm))">
            <div>
                <Item>
                    <template #title>
                        <span class="text-3xl weight-900 text-heading">
                            Settings
                        </span>
                    </template>
                </Item>
            </div>
            
            <nav class="w-full">
                <RouterLink :to="{name: 'account'}" active-class="active">
                    <Item clickable class="child">
                        <template #title>
                            <span class="text-xl text-heading weight-800 text-capitalize">
                                Account
                            </span>
                        </template>
                        <template #caption>
                            <span class="text-sm text-body weight-700 text-nodecor">
                                Change your password, email, username, or deactive account
                            </span>
                        </template>
                        <template #icon>
                            <q-icon size="2rem" name="navigate_next" class="text-heading"/>
                        </template>
                    </Item>
                </RouterLink>
                <RouterLink :to="{name: 'notification-settings'}" active-class="active">
                    <Item clickable class="child">
                        <template #title>
                            <span class="text-xl text-heading weight-800 text-capitalize">
                                Notifications
                            </span>
                        </template>
                        <template #caption>
                            <span class="text-sm text-body weight-700 text-nodecor">
                                Turn off notifications from users you follow
                            </span>
                        </template>
                        <template #icon>
                            <q-icon size="2rem" name="navigate_next" class="text-heading"/>
                        </template>
                    </Item>
                </RouterLink>
                <RouterLink :to="{name: 'sessions'}" active-class="active">
                    <Item clickable class="child">
                        <template #title>
                            <span class="text-xl text-heading weight-800 text-capitalize">
                                User Sessions
                            </span>
                        </template>
                        <template #caption>
                            <span class="text-sm text-body weight-700 text-nodecor">
                                Check all the sessions you currently have active
                            </span>
                        </template>
                        <template #icon>
                            <q-icon size="2rem" name="navigate_next" class="text-heading"/>
                        </template>
                    </Item>
                </RouterLink>
                <RouterLink :to="{name: 'privacy-settings'}" active-class="active">
                    <Item clickable class="child">
                        <template #title>
                            <span class="text-xl text-heading weight-800 text-capitalize">
                                Privacy and Safety
                            </span>
                        </template>
                        <template #caption>
                            <span class="text-sm text-body weight-700 text-nodecor">
                                Make Account Private
                            </span>
                        </template>
                        <template #icon>
                            <q-icon size="2rem" name="navigate_next" class="text-heading"/>
                        </template>
                    </Item>
                </RouterLink>
            </nav>
        </header>
        <div class="w-full">
            <RouterView class="w-full" />
        </div>
    </div>
</template>


<style scoped lang="scss">
* {
    text-decoration: none;
}

.active {
    
    .child {
        background-color: var(--color-background-mute);
    }
}
</style>