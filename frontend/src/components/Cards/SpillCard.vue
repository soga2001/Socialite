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
    <div class="grid main gap-1 pr-2 pt-2 w-full relative">
        <div class="avatar col-1" :style="avatarStyle" v-if="$slots.avatar">
            <slot name="avatar" />
        </div>
        <div class="col-2 grid">
            <div class="w-full">
                <slot name="title"/>
            </div>
            <div class="w-full sub">
                <slot name="subtitle"/>
            </div>
            <div class="w-full body py-2">
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
    grid-template-columns: 65px 1fr;
}

@media only screen and (max-width: 599px) {
    .main {
        grid-template-columns: 3rem 1fr;
    }

    .avatar {
        display: flex;
        place-items: center;
        width: 2.8rem;
        height: 2.8rem;
    }

    .avatar :slotted(*) {
        border-radius: 50%;
        width: 2.8rem;
        height: 2.8rem;
    }
}

.avatar {
    display: flex;
    place-items: center;
    width: 60px;
    height: 60px;
}

.avatar :slotted(*) {
    border-radius: 50%;
    width: 60px;
    height: 60px;
}

.sub, .body :slotted(*) {
    white-space: pre-line;
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
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(50px, 1fr));
    position: relative;
}

.action :slotted(*) {
  width: fit-content;
}
</style>