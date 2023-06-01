<script lang="ts">
import {h, compile} from 'vue/dist/vue.esm-bundler.js';

export default{
    name: 'MentionLink',
    props: {
        mention: {
            type: String,
            required: true
        }
    },
   render () {
         return h(compile(this.mention))
   }
}
</script>