<script lang="ts">
import { defineComponent, type PropType, type CSSProperties } from 'vue';
import type {RouteLocationRaw} from 'vue-router'

export default defineComponent({
  data() {
    return {
      isAvatarOnly: false,
      style: {
        alignItems: this.alignItems,
        cursor: this.to ? 'pointer' : 'normal',
        justifyContent: this.justifyContent
      } as CSSProperties,
      titleStyle: {
        fontSize: this.titleSize,
        display: '-webkit-box',
        '-webkit-box-orient': 'vertical',
        '-webkit-line-clamp': this.titleLineClamp,
        overflow: 'hidden',
        color: "var(--color-heading)"
      } as CSSProperties,
      captionStyle: {
        fontSize: this.captionSize,
        display: '-webkit-box',
        '-webkit-box-orient': 'vertical',
        '-webkit-line-clamp': this.captionLineClamp,
        overflow: 'hidden',
        color: "var(--color-text)"
      } as CSSProperties,
      iconStyle: {
        alignItems: this.iconAlign
      } as CSSProperties,
      avatarStyle: {
        alignItems: this.avatarAlign,
        width: this.avatarSize,
        height: this.avatarSize
      } as CSSProperties
    };
  },
  props: {
    alignItems: {
      type: String,
      default: "center"
    },
    justifyContent: {
      type: String,
      default: "center"
    },
    iconAlign: {
      type: String,
      default: "center"
    },
    avatarAlign: {
      type: String,
      default: "center"
    },
    to: {
      type: [String, Object] as PropType<RouteLocationRaw>,
      default: null,
    },
    clickable: {
      type: Boolean,
      default: false
    },
    titleLineClamp: {
      type: Number,
      default: 1
    },
    captionLineClamp: {
      type: Number,
      default: 2
    },
    avatarSize: {
      type: String,
      default: "3rem"
    },
    titleSize: {
      type: String,
      default: "20px"
    },
    captionSize: {
      type: String,
      default: "16px"
    }
  },
  methods: {
    router() {
      if (this.to) {
        this.$router.push(this.to);
      }
    }
  },
  mounted() {
    this.isAvatarOnly = Boolean(
      this.$slots.avatar &&
        !this.$slots.title &&
        !this.$slots.caption &&
        !this.$slots.icon
    );
    console.log(this.$props.clickable)
  }
});
</script>
  

<template>
  <div :class="'user-card ' + (isAvatarOnly ? 'circular' : '')" :style="style" @click="router">
    <div class="avatar" :style="avatarStyle" v-if="$slots.avatar">
      <slot name="avatar" />
    </div>
    <div class="info" v-if="!isAvatarOnly">
      <div class="title" :style="titleStyle">
        <slot name="title" v-if="$slots.title" />
      </div>
      <div class="caption" :style="captionStyle">
        <slot name="caption" v-if="$slots.caption" />
      </div>
    </div>
    <div class="icon" v-if="!isAvatarOnly">
      <slot name="icon" v-if="$slots.icon" />
    </div>
  </div>
</template>

<style scoped>
  .user-card {
    display: flex;
    padding: 0.5rem .5rem;
    cursor: pointer;
    position: relative;
    line-height: normal;
    gap: 10px;
    justify-content: center;
    height: 100%;
  }
  
  .user-card.circular {
    width: fit-content;
    padding: 0;
    margin: 0;
  }

  /* .avatar,
.info,
.icon {
  line-height: 1.2;
} */

  .user-card.circular .avatar {
    width: 100%;
    display: inline-flex;
  }
  
  .avatar {
    flex: 0 0 auto;
    width: 100%;
    height: 100%;
    display: flex;
  }

  :slotted(img) {
    border-radius: 50%;
    width: 100%;
    height: 100%;
  }

  .user-card.circular .avatar :slotted(img) {
    border: 2px solid #FF7373;
  }

  
  .info {
    flex: 1 1 auto;
  }
  
  .title {
    font-weight: 900;
    font-size: 17px;
    margin-bottom: .5rem; 
  }

  .title :slotted(*) {
    font-size: inherit;
    font-weight: 900;
    color: var(--color-heading);
  }
  
  .icon {
    flex: 0 0 auto;
    width: fit-content;
  }

  .caption :slotted(p:deep(a)) {
    font-size: inherit;
    font-weight: 900;
    text-decoration: none;
    color: #FF7373;
    
  }

  :slotted(p:deep(a:hover)) {
    text-decoration: underline;
  }

  /* .post__caption:deep(a) {
    font-weight: 900;
    text-decoration: none;
    color: #FE4A4A;
    color: #FF7373;
    color: rgb(250, 89, 164); 
    color: #b16af4;
    color: rgb(37, 192, 114);
    color: rgb(0, 191, 255);
  } */
</style>
  