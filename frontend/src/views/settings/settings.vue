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
        console.log(this.$route.matched[1] == undefined)
    },
    watch: {
        '$route': function() {
            const route =  this.$route.name ?? ''
            if (route !== 'settings') {
                this.hide = true
            }
            else {
                this.hide = false
            }
        },
    },
})
</script>

<template>
    <div :class="{'cols-2': !$q.screen.lt.sm}" class="grid w-full min-h-viewport">
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
                <RouterLink :to="{name: 'notifications'}" active-class="active">
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