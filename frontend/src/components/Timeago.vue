<script lang="ts">
import { defineComponent } from 'vue';
import format from 'date-fns/format';
import formatDistance from 'date-fns/formatDistance';
import differenceInCalendarDays  from 'date-fns/differenceInCalendarDays'
import formatRelative from 'date-fns/formatRelative';
import addDays from 'date-fns/addDays'
import formatDistanceToNow from 'date-fns/formatDistanceToNow'
import { addHours, addMilliseconds, addMinutes, differenceInHours, differenceInMilliseconds, differenceInMinutes } from 'date-fns';
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
        }
    },
    data() {
        return {
            // timeago: '',
            date_posted: this.timeago(),
        };
    },
    methods: {
        timeago() {
            var timestamp = new Date();
            const posted_date = new Date(this.date); 
            const days = differenceInCalendarDays(posted_date, timestamp);
            const miliseconds = differenceInMilliseconds(posted_date, timestamp);

            if(this.date_type == 'absolute') {
                if(Math.abs(days) < 7) {
                    const date = new Date();
                    return formatRelative(addMilliseconds(date, miliseconds), date);
                    // return formatDistance(posted_date, timestamp, { addSuffix: true, locale: navigator.language });
                }
                const date = format(posted_date, 'MMM dd, yyyy - hh:mm a');
                const splt = date.split(' - ');
                return splt[0] + ' at ' + splt[1];
            }
            else {
                const date = format(posted_date, 'MMM dd, yyyy');
                return date;
            }
            

            
        }
    },
    created() {
        // this.timeago();
        // console.log(navigator.language)
    }

})

</script>

<template>
    <p role="span" :class="class" :style="'font-size: ' + size">{{ date_posted }}</p>
</template>


<style scoped>
p {
    padding: 0;
    margin: 0;
}
p::first-letter {
    text-transform: uppercase !important;
}
</style>