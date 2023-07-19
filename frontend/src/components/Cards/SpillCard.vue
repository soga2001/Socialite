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
    <div class="grid main gap-1 p-2 w-full relative">
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
            <div class="w-full body ">
                <slot name="body"/>
            </div>
            <div class="w-full action">
                <slot name="actions"/>
            </div>
        </div>
    </div>
</template>

<style scoped>

.main {
    display: grid;
    grid-template-columns: 70px 1fr;
}

.avatar {
    display: flex;
    place-items: center;
    width: 70px;
    height: 70px;
}

.avatar :slotted(*) {
    border-radius: 50%;
    width: 60px;
    height: 60px;
}

.body :slotted(img) {
    padding: 0 !important;
    margin: 0 !important;
    border-radius: 10px;
    border: 1px solid var(--color-heading)
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
    justify-content: space-evenly;
    align-items: stretch;
    position: relative;
}

.action :slotted(*) {
  width: fit-content;
}
</style>