<script lang="ts">
import {h, compile} from 'vue';



export default{
    name: 'MentionLink',
    props: {
        mention: {
            type: String,
            required: true
        }
    },
   render () {
        // return h(compile(this.mention))
        return h(compile(this.mention, {
            whitespace: 'preserve'
        }));
        
   }
}
</script>