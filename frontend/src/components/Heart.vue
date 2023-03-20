<script lang="ts">
import { defineComponent } from 'vue';


export default defineComponent({ 
    name: 'App',
    props: {
        size: {
            type: String,
            default: 'md'
        }
    },
    data() {
        return {
            liked: 0,
        }
    }
})
</script>

<template>
    <div :class="'heart ' + size">
    </div>
</template>

<style scoped>
.heart {
  width: 100px;
  height: 100px;
  /* position: absolute; */
  /* transform: translate(-50%, -50%); */
  background: url(https://cssanimation.rocks/images/posts/steps/heart.png) no-repeat;
  background-position: 0 0;
  cursor: pointer;
  /* animation: fave-heart 1s steps(28); */
}
.heart:hover {
  background-position: -2800px 0;
  transition: background 1s steps(28);
}
@keyframes fave-heart {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: -2800px 0;
  }
}

</style>