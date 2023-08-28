<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import type { User } from '@/assets/interfaces';
import { format, sub } from 'date-fns';


export default defineComponent({
    data() {
        return {
            type: this.input_type,
            label: this.input_label,
            val: this.defaultVal ?? '' as String | Date,
            users: new Array<User>(),
            index: null,
            focused: false,

            min: this.minDate ?? '',
            max: this.maxDate ?? '',

            currentDate: new Date(),
            monthNames: [
              'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December'
            ]
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
            type: [String, Number, Date],
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
        minDate: {
            type: String,
            default: ``,
        },
        maxDate: {
            type: String,
            default: ``,
        },
    },
    created() {
      if(this.input_type === 'date') {
        this.max = format(this.currentDate, 'yyyy-MM-dd')
        this.min = format(sub(this.currentDate, {
          years: 120,
        }), 'yyyy-MM-dd')
        try {
          const date = new Date(this.defaultVal).toUTCString()
          const fullYear = new Date(date).getFullYear()
          const month = new Date(date).getUTCMonth() < 10 ? '0' + (new Date(date).getUTCMonth() + 1) : new Date(date).getUTCMonth()
          const day = new Date(date).getUTCDate() < 10 ? '0' + new Date(date).getUTCDate() : new Date(date).getUTCDate()
          this.val = `${fullYear}-${month}-${day}`
        }
        catch (e) {

        }
      }
      
    },
    mounted() {
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
        (this.$refs.input as HTMLInputElement).focus()
      }
    },
    watch: {
      val: function(val: string) {
        this.$emit('update:val', val)
      },
    }
})

</script>

<template>
  <div class="input-box" :class="{focused: isFocused}" @click="inputClicked">
    <input v-if="type === 'date'" :min="min" :max="max" ref="input" :autofocus="autofocus" @focus="focused = true" @blur="unfocus" :required="required" :type="type" v-model="val" :class="{hasInput: (val as string).length > 0}"  class="input text-heading">
    <input v-else-if="type === 'tel'" pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}" ref="input" :autofocus="autofocus" @focus="focused = true" @blur="unfocus" :required="required" :type="type" v-model="val" :class="{hasInput: (val as string).length > 0}"  class="input text-heading">
    <input v-else :maxlength="charLimit" ref="input" :autofocus="autofocus" @focus="focused = true" @blur="unfocus" :required="required" :type="type" v-model="val" :class="{hasInput: (val as string).length > 0}"  class="input text-heading">
    <label :class="{focused: isFocused,  hasInput: (val as string).length > 0 || type === 'date'}" class="label cursor-text">{{label}}</label>
    <span v-if="showCharCounts && (isFocused || (val as string).length > 0)" @click="($refs.input as HTMLInputElement).focus()" :class="{focused: isFocused,  hasInput: (val as string).length > 0}" class="char_count">{{ `${(val as string).length} / ${charLimit}` }}</span>
  </div>

</template>

<style scoped lang="scss">
.input-box {
  position: relative;
  height: 60px;
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
    margin-top: 25px;
    padding: 0 10px;
    font-size: 20px;
    line-height: 1rem;
  }

  .input::-moz-placeholder {
    opacity: 0;
  }
}

* {
  transition: .3s all;
}

.label {
  position: absolute;
  top: 50%;
  left: 15px;
  transform: translate(0, -50%);
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-body) !important;

  &.focused {
    color: var(--color-theme) !important;
    top: 15px;
    left: 10px;
    font-size: .875rem;
    font-weight: 700;
  }

  &.hasInput {
    top: 15px;
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
  top: 50%;
  right: 20px;
  transform: translate(0, -50%);
  font-size: 1.5rem;
  // font-weight: 900;
  color: var(--color-lighter) !important;

  &.focused {
    top: 15px;
    right: 10px;
    font-size: .875rem;
  }

  &.hasInput {
    top: 15px;
    right: 10px;
    font-size: .875rem;

    & ~ .input {
      padding: 1.5rem 10x .5rem 10px !important;
    }
  }

}

</style>