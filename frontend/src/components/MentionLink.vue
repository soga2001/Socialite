<script lang="ts">
import {h, compile, resolveComponent} from 'vue';



export default{
    name: 'MentionLink',
    props: {
        mention: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            date: new Date().toISOString()
        }
    },
    methods: {
        cleanText() {
            // write a regex pattern for this `<RouterLink :to="{name: `user-profile`, params: {username: 'soga2001'}}" :exact="true">@soga2001</RouterLink>`
            let r = /(<[^<>]+?>)/g
            let text = this.mention.replace(r, '');
            // console.log(text)

            // const text = this.mention;
            // const regex = /<RouterLink\s+:to="{name:\s*`([^`]+)`,\s*params:\s*{username:\s*'([^']+)'}\s*}"\s*:exact="true">([^<]+)<\/RouterLink>/g;
            // const matches = text.match(regex);
            // if(matches) {
            //     const username = matches[0].split('">')[1].split('</a>')[0];
            //     return username;
            // }
            return text;
        }
    },
    mounted() {  
        console.log(this.cleanText())
    },
   render () {
        // const Timeago = resolveComponent('timeago')
        // return h('div', { class: 'my-class' }, [
            // h('h1', 'This is a heading.'),
            // h(compile(this.mention)),
            // h(Timeago, {
            //     date: this.date,
            //     date_type: 'absolute',
            //     size: '20px',
            //     class: 'text-xs',
            // } )
        // ]); 

        return h(compile(this.mention))
        
   }
}
</script>