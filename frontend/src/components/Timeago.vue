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
        }
    },
    data() {
        return {
            // timeago: '',
            date_posted: this.timeAgo(),
        };
    },
    methods: {
        timeAgo() {
            return convertTime(this.date, this.date_type)
        }
    },
    created() {
        // this.timeago();
        // console.log(navigator.language)
    }

})

</script>

<template>
    <span v-if="!html" role="span" :class="class">{{ date_posted }}</span>
    <span :class="class" v-else v-html="date_posted"></span>
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