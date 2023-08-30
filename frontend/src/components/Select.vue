<script lang="ts">
import { defineComponent, ref } from 'vue';
import { http } from '@/assets/http';
import type { User } from '@/assets/interfaces';
import { format, sub } from 'date-fns';

interface Years {
    year: number
}


export default defineComponent({
    data() {
        return {
            val: ref<number | string | Date>(this.defaultVal),

            min: this.minVal ?? '',
            max: this.maxVal ?? '',
            focused: false,
            monthNames: [
              'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December'
            ],

            years: ref<number[]>(),
            totalDays: ref<number>(0),

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
        pickedMonth: {
            type: [String, Number],
            default: '',
        },
        pickedYear: {
            type: [String, Number],
            default: '',
        },
    },
    created() {

        if(this.input_type === 'year'){
            const endYear = new Date()
            const startYear = sub(endYear, {years: 120}).getFullYear()

            this.years = this.range(startYear, endYear.getFullYear())
        }

        if(this.input_type === 'day' && !this.pickedYear && this.pickedMonth) {
            this.totalDays = new Date(new Date().getFullYear() as number, this.pickedMonth as number, 0).getDate() || 31
        }

        else if(this.input_type === 'day' && this.pickedYear && !this.pickedMonth) {
            this.totalDays = 31
        }

        else if(this.input_type === 'day' && !this.pickedYear && !this.pickedMonth) {
            this.totalDays = 31
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
        range: (start: number, end: number) => { 
            return Array(end - start + 1).fill(0).map((_, idx) => end - idx)
        },

    },
    watch: {
        val: function(val: string) {
            this.$emit('update:val', val)
        },
        pickedMonth: function(val: any) {
            console.log(this.pickedYear)
            const year = (this.pickedYear as number ) || new Date().getFullYear() as number
            console.log(year)
            this.totalDays = new Date(year, (this.monthNames.indexOf(val) + 1), 0).getDate() || 31
            if(this.input_type === 'day' && this.totalDays < (this.defaultVal as number)) {
                this.val = ''
            }
        },
        pickedYear: function(val: any) {
            
            this.totalDays = new Date(val as number, ((this.monthNames.indexOf(this.pickedMonth as string) + 1) as number) || (new Date().getMonth() + 1), 0).getDate() || 31
            if(this.input_type === 'day' && this.totalDays < (this.defaultVal as number)) {
                this.val = ''
            }
        },
    }
})

</script>

<template>
  <div class="input-box" :class="{focused: isFocused}" @click="inputClicked">
    <select ref="input" :autofocus="autofocus" @focus="focused = true" @blur="unfocus" :required="required" v-if="input_type==='month'" v-model="val" class="input text-heading ">
        <option value=""></option>
        <option class="text-sm" v-for="month in monthNames">{{ month }}</option>
    </select>

    <select ref="input" :autofocus="autofocus" @focus="focused = true" @blur="unfocus" :required="required" v-if="input_type==='year' && years && years.length > 0" v-model.number="val" class="input text-heading ">
        <option value=""></option>
        <option class="text-sm" v-for="year in years">{{ year }}</option>
    </select>

    <select ref="input" :autofocus="autofocus" @focus="focused = true" @blur="unfocus" :required="required" v-if="input_type==='day'" v-model.number="val" class="input text-heading ">
        <option value=""></option>
        <option class="text-sm" v-for="day in totalDays">{{ day }}</option>
    </select>



    <label :class="{focused: isFocused}" class="label cursor-text">{{input_label}}</label>
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
    width: 95%;
    outline: none;
    border: none;
    background-color: transparent;
    margin-top: 25px;
    padding-left: 5px;
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
    top: 2px;
    left: 10px;
    font-size: 1rem;
    font-weight: 700;
    color: var(--color-body) !important;

  &.focused {
    color: var(--color-theme) !important;
  }

//   &.hasInput {
//     top: 15px;
//     left: 10px;
//     font-size: .875rem;
//     font-weight: 700;

//     & ~ .input {
//       padding: 1.5rem 10x .5rem 10px !important;
//     }
//   }

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