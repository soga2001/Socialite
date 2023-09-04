<script lang="ts">
import { defineComponent } from 'vue'
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
    activted() {
        console.log('activated')
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
    <div :class="{'large-screen': !$q.screen.lt.sm, 'min-h-viewport': !$q.screen.lt.sm}" class="grid w-full h-full">
        <header class="border-r h-full w-full bg-theme" v-if="($route.matched[0].name === 'settings' && ($route.matched[1] === undefined || !$q.screen.lt.sm))">
            <div v-if="!$q.screen.lt.sm">
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
                    <Item :captionLineClamp="3" clickable class="child">
                        <template #title>
                            <span class="text-xl text-heading weight-800 text-capitalize">
                                Account
                            </span>
                        </template>
                        <template #caption>
                            <span class="text-sm text-body weight-700 text-nodecor">
                                Change your password, email, username, and any other editable user data, or delete account
                            </span>
                        </template>
                        <template #icon>
                            <q-icon size="2rem" name="navigate_next" class="text-heading"/>
                        </template>
                    </Item>
                </RouterLink>
                <RouterLink :to="{name: 'notification-settings'}" active-class="active">
                    <Item :captionLineClamp="3" clickable class="child">
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
                    <Item :captionLineClamp="3" clickable class="child">
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
            </nav>
        </header>
        <div class="w-full">
            <RouterView v-slot="{Component}" >
                <KeepAlive :max="4" :include="['notification-settings', 'individual-notif-settings', 'sessions']" >
                    <component :is="Component" :key="$route.fullPath"  :height="height" :scrollPosition="scrollPosition" />
                </KeepAlive>
            </RouterView>
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

.large-screen {
    display: grid;
    grid-template-columns: 1fr 1.5fr;
}
</style>