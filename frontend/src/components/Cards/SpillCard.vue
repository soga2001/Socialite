<script lang="ts">
import { defineComponent, type CSSProperties } from 'vue';

export default defineComponent({
    name: 'SpillCard',
    props: {
        avatarSize: {
            type: String,
            default: "3rem"
        },
    },
    data() {
        return {
            avatarStyle: {
                width: this.avatarSize,
                height: this.avatarSize
            } as CSSProperties,
        }
    },
    methods: {

    },

});

</script>

<template>
    <div class="grid cols-auto-fr gap-2 w-full">
        <div class="avatar col-1" :style="avatarStyle" v-if="$slots.avatar">
            <slot name="avatar" />
        </div>
        <div class="col-2 flex gap-1 flex-cols">
            <div class="w-full">
                <slot name="title"/>
            </div>
            <div class="w-full sub">
                <slot name="subtitle"/>
            </div>
            <div class="w-full body">
                <slot name="body"/>
            </div>
            <div class="w-full action">
                <slot name="actions"/>
            </div>
        </div>
    </div>
</template>

<style scoped>

.avatar {
    /* width: 100%;
    height: 100%; */
    display: flex;
    place-items: center;
}

.avatar img {
    border-radius: 50%;
    width: 100%;
    height: 100%;
}

.avatar :slotted(*) {
    border-radius: 50%;
    width: 3rem;
    height: 3rem;
}

.body :slotted(img) {
    border-radius: 50%;
}

:slotted(*:deep(a)) {
    font-size: inherit;
    font-weight: 900;
    text-decoration: none;
    color: #FF7373;
    
  }

:slotted(*:deep(a:hover)) {
    text-decoration: underline;
  }

.action {
    display: flex;
    /* justify-content: space-evenly; */
    /* align-items: center;
    margin-top:.2em!important ; */
}

.action :slotted(*) {
    margin: 0 .2em!important;
}

/* 
::slotted(img) {
    border-radius: 50%;
    width: 5rem !important;
    height: 3rem !important;
} */
</style>