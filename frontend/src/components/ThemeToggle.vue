<script lang="ts">
import { defineComponent } from 'vue'
import Item from './Item.vue';
export default defineComponent({
  data() {
      return {
          theme: false,
      };
  },
  computed: {
  },
  methods: {
      switchTheme(e: any) {
          if (this.theme) {
              this.$q.cookies.set("theme", "light");
              document.documentElement.setAttribute("data-theme", "light");
          }
          else {
              this.$q.cookies.set("theme", "dark");
              document.documentElement.setAttribute("data-theme", "dark");
          }
          this.$store.commit("setTheme", !this.$store.state.dark);
      },
  },
  created() {
      this.theme = this.$q.cookies.get("theme") === "dark";
      this.$store.commit("setTheme", this.theme);
      document.documentElement.setAttribute("data-theme", this.theme ? "dark" : "light");
  },
  mounted() {
  },
  watch: {
    '$store.state.dark': function() {
      this.theme = this.$store.state.dark
    }
  },
  components: { Item }
})
</script>


<template>
    <div>
        <div class="toggleWrapper">
            <input type="checkbox" v-model="theme" @click="switchTheme" class="dn" id="dn">
            <label for="dn" class="toggle">
                <span class="toggle__handler">
                    <span class="crater crater--1"></span>
                    <span class="crater crater--2"></span>
                    <span class="crater crater--3"></span>
                </span>
                <span class="star star--1"></span>
                <span class="star star--2"></span>
                <span class="star star--3"></span>
                <span class="star star--4"></span>
                <span class="star star--5"></span>
                <span class="star star--6"></span>
            </label>
        </div>
    </div>
</template>

<style scoped>
.toggleWrapper input {
  position: absolute;
  left: -99em;
  zoom: 1%;
}

.toggle {
  cursor: pointer;
  display: inline-block;
  position: relative;
  width: 45px;
  height: 25px;
  background-color: #83d8ff;
  border-radius: 84px;
  transition: background-color 200ms cubic-bezier(0.445, 0.05, 0.55, 0.95);
}

.toggle__handler {
  display: inline-block;
  position: relative;
  z-index: 1;
  top: 1.7px;
  left: 3px;
  width: 21px;
  height: 21px;
  background-color: #f5d418;
  border-radius: 50px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, .3);
  transition: all 400ms cubic-bezier(0.68, -0.55, 0.265, 1.55);
  transform: rotate(-45deg);
}

.toggle__handler .crater {
  position: absolute;
  background-color: #e8cda5;
  opacity: 0;
  transition: opacity 200ms ease-in-out;
  border-radius: 100%;
}

.toggle__handler .crater--1 {
  top: 9px;
  left: 5px;
  width: 2px;
  height: 2px;
}

.toggle__handler .crater--2 {
  top: 14px;
  left: 11px;
  width: 3px;
  height: 3px;
}

.toggle__handler .crater--3 {
  top: 5px;
  left: 12.5px;
  width: 4px;
  height: 4px;
}

.star {
  position: absolute;
  background-color: rgb(255, 255, 255);
  /* font-weight: 900; */
  transition: all 300ms cubic-bezier(0.445, 0.05, 0.55, 0.95);
  border-radius: 50%;
}

.star--1 {
  top: 5px;
  left: 17.5px;
  z-index: 0;
  width: 15px;
  height: 1.5px;
}

.star--2 {
  top: 9px;
  left: 14px;
  z-index: 1;
  width: 15px;
  height: 1.5px;
}

.star--3 {
  top: 13.5px;
  left: 20px;
  z-index: 0;
  width: 15px;
  height: 1.5px;
}

.star--4, .star--5, .star--6 {
  opacity: 0;
  transition: all 300ms 0 cubic-bezier(0.445, 0.05, 0.55, 0.95);
}

.star--4 {
  top: 8px;
  left: 5.5px;
  z-index: 0;
  width: 1px;
  height: 1px;
  transform: translate3d(3px, 0, 0);
}

.star--5 {
  top: 16px;
  left: 8.5px;
  z-index: 0;
  width: 1.5px;
  height: 1.5px;
  transform: translate3d(3px, 0, 0);
}

.star--6 {
  top: 18px;
  left: 14px;
  z-index: 0;
  width: 1px;
  height: 1px;
  transform: translate3d(3px, 0, 0);
}

input:checked + .toggle {
  background-color: #475668;
}

input:checked + .toggle:before {
  color: #475668;
}

input:checked + .toggle:after {
  color: #fff;
}

input:checked + .toggle .toggle__handler {
  background-color: #ffe5b5;
  transform: translate3d(17px, 0, 0) rotate(0);
}

input:checked + .toggle .toggle__handler .crater {
  opacity: 1;
}

input:checked + .toggle .star--1 {
  width: 1px;
  height: 1px;
}

input:checked + .toggle .star--2 {
  width: 2px;
  height: 2px;
  transform: translate3d(-5px, 0, 0);
}

input:checked + .toggle .star--3 {
  width: 2px;
  height: 2px;
  transform: translate3d(-7px, 0, 0);
}

input:checked + .toggle .star--4, input:checked + .toggle .star--5, input:checked + .toggle .star--6 {
  opacity: 1;
  transform: translate3d(0, 0, 0);
}

input:checked + .toggle .star--4 {
  transition: all 300ms 200ms cubic-bezier(0.445, 0.05, 0.55, 0.95);
}

input:checked + .toggle .star--5 {
  transition: all 300ms 300ms cubic-bezier(0.445, 0.05, 0.55, 0.95);
}

input:checked + .toggle .star--6 {
  transition: all 300ms 400ms cubic-bezier(0.445, 0.05, 0.55, 0.95);
}
 
</style>