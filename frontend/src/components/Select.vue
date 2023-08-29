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
            val: ref<number | string | Date>(this.defaultVal),

            min: this.minVal ?? '',
            max: this.maxVal ?? '',
            focused: false,
            monthNames: [
              'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December'
            ],

            years: [],
            day: '',

        }
    },
    props: {
        input_type: {
            type: String,
            default: 'year'
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
        minVal: {
            type: Number,
            default: 0,
        },
        maxVal: {
            type: Number,
            default: 0,
        },
    },
    created() {
    //   if(this.input_type === 'year') {
    //     this.min = sub(new Date(), {years: 120}).getFullYear()
    //     this.max = new Date().getFullYear()
    //   }
    //   if(this.input_type === 'day') {
    //     this.min = 1
    //     this.max = new Date().getDate();
    //   }

        if(this.input_type === 'year'){
            console.log('here')
            this.range(new Date().getFullYear(), sub(new Date(), {years: 120}).getFullYear()) 
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
        (this.$refs.input as HTMLInputElement).focus();
        (this.$refs.input as HTMLInputElement).click();
      },
      range: (start: number, end: number) =>{ 
        const result = [];
        for (let i = start; i <= end; i++) {
            result.push(i);
        }
        return result;
    },
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
    <select ref="input" :autofocus="autofocus" @focus="focused = true" @blur="unfocus" :required="required" v-if="input_type==='month'" v-model="val" class="input text-heading ">
        <option disabled value=""></option>
        <option class="text-sm" v-for="month in monthNames">{{ month }}</option>
    </select>

    <select ref="input" :autofocus="autofocus" @focus="focused = true" @blur="unfocus" :required="required" v-if="input_type==='year'" v-model="val" class="input text-heading ">
        <option disabled value=""></option>
        <option class="text-sm" v-for="year in years">{{ years }}</option>
    </select>

    <select ref="input" :autofocus="autofocus" @focus="focused = true" @blur="unfocus" :required="required" v-if="input_type==='day'" v-model="val" class="input text-heading ">
        <option disabled value=""></option>
        <option class="text-sm" v-for="month in monthNames">{{ month }}</option>
    </select>



    <label :class="{focused: isFocused,  hasInput: (val as string).length > 0 || type === 'date' || type === 'select' || type === 'number'}" class="label cursor-text">{{label}}</label>
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
    
    // -webkit-appearance: none;
    // -moz-appearance:    none;
    // appearance:         none;
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

.grid {
  display: grid;
  grid-template-columns: 1.5fr repeat(2, 1fr);
  gap: 10px;
  padding: 0 10px;
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