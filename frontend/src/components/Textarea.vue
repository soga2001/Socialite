<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import type { User } from '@/assets/interfaces';


export default defineComponent({
    data() {
        return {
            type: this.input_type,
            label: this.input_label,
            val: this.defaultVal ?? '',
            users: new Array<User>(),
            index: null,
            focused: false,
            textareaHeight: 0,
            labelHeight: 0,
        }
    },
    props: {
        input_type: {
            type: String,
            default: 'text'
        },
        input_label: {
            type: String,
            required: true
        },
        required: {
            type: Boolean,
            default: false,
        },
        id: {
            type: String,
            required: true,
        },
        autofocus: {
            type: Boolean,
            default: false,
        },
        defaultVal: {
            type: String,
            default: '',
        },
        showCharCounts: {
            type: Boolean,
            default: false,
        },
        charLimit: {
            type: Number,
            default: 255,
        },
        maxHeight: {
            type: [String, Number],
            default: '200px',
        },
        height: {
          type: String,
          default: 'auto',
        }
    },
    created() {
    },
    mounted() {
      const textarea = this.$refs.textarea as HTMLInputElement
      const label = this.$refs.label as HTMLLabelElement
      this.textareaHeight = textarea?.offsetHeight
      this.labelHeight = label?.offsetHeight + 25

      this.autogrow()
    },
    computed: {
      isFocused(): Boolean {
        return this.focused
      }
    },
    methods: {
      unfocus() {
        this.focused = false
      },
      inputClicked() {
        (this.$refs.textarea as HTMLTextAreaElement).focus()
      },
      autogrow() {
        const inputBox = this.$refs.inputBox as HTMLDivElement;
        inputBox.style.height = this.height
        const textarea = this.$refs.textarea as HTMLInputElement
        textarea.style.height = 'auto'
        textarea.style.height = textarea.scrollHeight + 'px'
      },
    },
    watch: {
      val: function(val: string) {
        this.autogrow()
        this.$emit('update:val', val)
      }
    }
})

</script>

<template>
  <div :style="{maxHeight: `${maxHeight}px`}" class="input-box" ref="inputBox" :class="{focused: isFocused}" @click="inputClicked">
    <textarea :style="{maxHeight: `${Number(maxHeight) - Number(labelHeight)}px`}" rows="5" :maxlength="charLimit" ref="textarea" :autofocus="autofocus" @focus="focused = true" @blur="unfocus" :required="required" :type="type" v-model="val" :class="{hasInput: val.length > 0}"  class="input resize-none text-heading"/>
    <label ref="label" :class="{focused: isFocused,  hasInput: val.length > 0}" class="label cursor-text">{{label}}</label>
    <span v-if="showCharCounts && (isFocused || val.length > 0)" @click="($refs.input as HTMLInputElement).focus()" :class="{focused: isFocused,  hasInput: val.length > 0}" class="char_count">{{ `${val.length} / ${charLimit}` }}</span>
  </div>
</template>

<style scoped lang="scss">

.input-box {
  position: relative;
  min-height: 70px;
  height: auto;
  width: 100%;
  border: 1px solid var(--color-border);
  border-radius: 10px;

  &.focused {
    border: 1px solid var(--color-theme);
  }

  .input {
    width: 100%;
    outline: none;
    border: none;
    background-color: transparent;
    margin-top: 35px;
    padding: 0 10px;
    font-size: 20px;
  }
}

* {
  transition: .3s all;
}

.label {
  position: absolute;
  top: 20px;
  left: 15px;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-body) !important;

  &.focused {
    color: var(--color-theme) !important;
    top: 10px;
    left: 10px;
    font-size: .875rem;
    font-weight: 700;
  }

  &.hasInput {
    top: 10px;
    left: 10px;
    font-size: .875rem;
    font-weight: 700;

    & ~ .input {
      padding: 1.5rem 10x .5rem 10px !important;
    }
  }

}

.char_count {
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 1.5rem;
  color: var(--color-lighter) !important;

  &.focused {
    top: 10px;
    right: 10px;
    font-size: .875rem;
  }

  &.hasInput {
    top: 10px;
    right: 10px;
    font-size: .875rem;

    & ~ .input {
      padding: 1.5rem 10x .5rem 10px !important;
    }
  }

}

</style>