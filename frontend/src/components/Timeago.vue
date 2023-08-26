<script lang="ts">
import { defineComponent } from 'vue';
import format from 'date-fns/format';
import formatDistance from 'date-fns/formatDistance';
import differenceInCalendarDays  from 'date-fns/differenceInCalendarDays'
import formatRelative from 'date-fns/formatRelative';
import addDays from 'date-fns/addDays'
import formatDistanceToNow from 'date-fns/formatDistanceToNow'
import { addHours, addMilliseconds, addMinutes, differenceInHours, differenceInMilliseconds, differenceInMinutes } from 'date-fns';
import convertTime from '@/assets/convertTime';
// import { format, formatDistance, formatRelative, subDays } from 'date-fns'


export default defineComponent({
    props: {
        date: {type: String, required: true},
        date_type: {
            type: String,
            default: 'absolute',
        },
        size: {
            type: String,
            default: '20px',
        },
        class: {
            type: String,
            default: 'text-xs',
        },
        html: {
            type: Boolean,
            default: false,
        },
        spanClass: {
            type: String,
            default: '',
        }
    },
    data() {
        return {
            date_posted: this.timeAgo(),
        };
    },
    methods: {
        timeAgo() {
            let date = convertTime(this.date, this.date_type)
            let val = null
            if(date.includes("&#183;")) {
                val = date.split('&#183;');
                console.log(val[0], val[1])
                console.log(`<span class="flex flex-row gap-1 items-center ${this.class}"> ${val[0]} <span class="${this.spanClass}">&#183;</span> ${val[1]} </span>`)

                return `<span :class="${this.class}" class="flex flex-row gap-1 items-center"> ${val[0]} <span class="${this.spanClass}">&#183;</span> ${val[1]} </span>`
            }
            return date
        }
    },
    created() {
    },

})

</script>

<template>
    <span v-if="!html" role="span" :class="class">{{ date_posted }}</span>
    <span ref="val"  v-html="date_posted" v-else></span>
</template>


<style scoped>
p {
    padding: 0;
    margin: 0;

    /* display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;  
    overflow: hidden; */

    text-overflow: ellipsis;

    /* Needed to make it work */
    overflow: hidden;
    white-space: nowrap;
}
p::first-letter {
    text-transform: uppercase !important;
}
</style>