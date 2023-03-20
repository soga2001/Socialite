<script lang="ts">

import { defineComponent } from 'vue'
export default defineComponent({
    name: 'Item',
    // props: {
    //     // avatar: {
    //     //     type: String,
    //     //     default: ''
    //     // },
    //     // title: {
    //     //     type: String,
    //     //     required: true,
    //     // },
    //     // subtitle: {
    //     //     type: String,
    //     //     default: ''
    //     // },
    //     // icon: {
    //     //     type: String,
    //     //     default: ''
    //     // }
    // },
    data() {
        return {
            // show: false
        }
    },
    methods: {
    }
})

</script>

<template>
    <div class="item">
        <div class="avatar">
            <slot name="avatar">
            </slot>
        </div>
        <div class="title">
            <slot name="title">
            </slot>
        </div>
        <div class="subtitle">
            <slot name="subtitle">
            </slot>
        </div>
        <div class="actions">
            <slot name="actions">
            </slot>
        </div>
    </div>
</template>

<style scoped>
.item {
    display: grid;
    grid-template-columns: 40px auto 30px;
    grid-template-rows: repeat(auto-fill, 20px);
    text-align: center;
    /* gap: 5px; */
    max-width: 200px;
}

.avatar :slotted(img) {
    width: 40px;
    height: 40px;
}
.title :slotted(h1) {
  font-size: 20px;
  font-weight: bold;
}

.avatar {
    grid-column: auto span 1;
    grid-row: auto / span 2;
    display: flex;
    align-items: center;
    text-align: center;
}

.img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
}

.title {
    grid-column: 2 / 3;
    grid-row: auto / auto;
    height: 100%;

}

.subtitle {
    grid-column: 2 / 3;
    grid-row: auto / auto;
    height: 100%;
}

.actions {
    grid-column: 3 / 3;
    grid-row: 1 / 3;
    display: flex;
    justify-content: center;
    align-items: center;
    justify-items: center;
}

#title {
    font-size: 1rem;
    font-weight: 500;
    color: var(--color-heading);
}

#subtitle {
    font-size: .8rem;
    font-weight: 400;
    color: var(--color-text);
}

</style>