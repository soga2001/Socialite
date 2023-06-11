<script lang="ts">
    import { defineComponent } from "vue";

  export default defineComponent({
    props: {
      type: {
        type: String,
        required: true,
      },
      title: {
        type: String,
        required: true,
      },
      message: {
        type: String,
        required: true,
      },
      duration: {
        type: Number,
        default: 5000,
      },
    },
    data() {
      return {
        show: true,
      };
    },
    mounted() {
        console.log(this.show)
        setTimeout(() => {
            this.close()
        }, this.duration);
    },
    methods: {
        close() {
            this.show = false;
            this.$emit('deleteMsg')
        },
    }
  });
  </script>

<template>
    <!-- <div v-if="show" :class="`notification notification__${type}`">
      <div :class="`notification__left`">
        <div :class="`notification__icon__${type}`"></div>
        <div class="notification__content">
          <div :class="`notification__title notification__title__${type}`">{{ title }}</div>
          <div :class="`notification__message notification__message__${type}`">{{ message }}</div>
        </div>
      </div>
      <div :class="`notification__icon__${type}`"></div>
    </div> -->
    <div>
        <Item :vert-icon-center="false" v-if="show" :class="`notification notification__${type} w-fit h-fit px-2 py-2`">
            <template #title>
                <div :class="`weight-900 text-black text-lg`">{{ title }}</div>
            </template>
            <template #caption>
                <div :class="`weight-500  text-black text-sm`">{{ message }}</div> 
            </template>
            <template #icon>
                <div :class="`notification__icon__${type}`">
                    <i-close size="2rem" class="btn" fill="black" stroke="none" @click="close" />
                </div>
            </template>

        </Item>
    </div>
</template>
  
  
  <style scoped>
.notification {
    position: fixed;
    top: 1rem;
    right: 1rem;
    z-index: 9999;
}

.notification__success {
  background: #f6fef9;
  border: 1px solid #2f9461;
  border-radius: 8px;
}

.notification__error {
  background: #edc7bd;
  border: 1px solid #e16969;
  border-radius: 8px;
}
.notification__warning {
  background: #fffcf5;
  border: 1px solid #c8811a;
  border-radius: 8px;
}
  </style>
  