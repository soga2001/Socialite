<script lang="ts">
import { defineComponent, type PropType, type CSSProperties } from 'vue';
import type {RouteLocationRaw} from 'vue-router'

export default defineComponent({
  data() {
    return {
      isAvatarOnly: false,
      style: {
        alignItems: this.alignItems,
        cursor: this.clickable ? 'pointer' : 'normal',
        justifyContent: this.justifyContent,
        padding: this.dense ? "0" : ".5rem"
      } as CSSProperties,
      infoStyle: {
        padding: this.infoMargin
      } as CSSProperties,
      titleStyle: {
        fontSize: this.titleSize,
        display: '-webkit-box',
        '-webkit-box-orient': 'vertical',
        '-webkit-line-clamp': this.titleLineClamp,
        // 'line-clamp': this.titleLineClamp,
        overflow: 'hidden',
        color: "var(--color-heading)",
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
    hover: {
      type: Boolean,
      default: false
    },
    dense: {
      type: Boolean,
      default: false,
    },
    infoMargin: {
      type: String,
      default: "0 0 0 0"
    },
    titleLineClamp: {
      type: [Number, String],
      default: 1
    },
    captionLineClamp: {
      type: [Number, String],
      default: 1
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
    },
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
  }
});
</script>
  

<template>
  <div ref="item" class="user-card" :class="{'circular': isAvatarOnly, 'bg-hover-soft': clickable}" :style="style" @click="router">
    <div class="avatar" :style="avatarStyle" v-if="$slots.avatar" @click="router">
      <slot name="avatar" />
    </div>
    <div class="info" :style="infoStyle" v-if="!isAvatarOnly">
      <div class="title" :style="titleStyle">
        <slot name="title" v-if="$slots.title" />
      </div>
      <div class="subtitle">
        <slot name="subtitle" v-if="$slots.subtitle" />
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
    position: relative;
    line-height: normal;
    gap: 10px;
    justify-content: center;
    align-items: center;
    height: 100%;
  }
  
  .user-card.circular {
    width: fit-content;
    padding: 0;
    margin: 0;
  }

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

  .avatar :slotted(*) {
    border-radius: 50%;
    width: 100%;
    height: 100%;
  }

  .user-card.circular .avatar :slotted(img) {
    border: 2px solid #FF7373;
  }

  
  .info {
    flex: 1;
    /* display: flex; */
    justify-content: center;
  }
  
  .title {
    font-weight: inherit;
    font-size: inherit;
    /* margin-bottom: .5rem;  */
  }

  .title :slotted(*) {
    font-size: inherit;
    font-weight: inherit;
    color: var(--color-heading);
  }
  
  .icon {
    display: flex;
    justify-content: flex-end;
    flex: 0 0 auto;
    width: fit-content;
  }


  .caption :slotted(*) {
    font-size: inherit;
    font-weight: 400;
    color: var(--color-heading);
  }
  .caption :slotted(*:deep(a)) {
    font-size: inherit;
    font-weight: 900;
    text-decoration: none;
    color: #FF7373;
    
  }

  :slotted(*:deep(a:hover)) {
    text-decoration: underline;
  }
</style>
  