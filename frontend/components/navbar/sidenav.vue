<script lang="ts">
// import menu-icon from element-plus
import { ElMenu, ElMenuItem } from 'element-plus';

export default {
    data() {
        return {
        isCollapse: false
        }
    },
    methods: {
        handleOpen(key: string, keyPath: string) {
        console.log(key, keyPath);
        },
        handleClose(key: string, keyPath: string) {
        console.log(key, keyPath);
        }
    }
}
</script>

<template>
    <!-- <el-menu
    class="el-menu-vertical-demo sidenav"
    @open="handleOpen"
    @close="handleClose"
  >
    <el-sub-item index="1">
        <el-icon><icon-menu /></el-icon>
        <template #title>Navigator Two</template>
    </el-sub-item>
    <el-menu-item index="2">
      <el-icon><icon-menu /></el-icon>
      <template #title>Navigator Two</template>
    </el-menu-item>
    <el-menu-item index="3" disabled>
      <el-icon><document /></el-icon>
      <template #title>Navigator Three</template>
    </el-menu-item>
    <el-menu-item index="4">
      <el-icon><setting /></el-icon>
      <template #title>Navigator Four</template>
    </el-menu-item>
  </el-menu> -->
  <el-menu>
    <el-menu-item index="2">
      <!-- <el-icon><icon-menu /></el-icon> -->
      <template #title>Navigator Two</template>
    </el-menu-item>
  </el-menu>
</template>


<style scoped lang="scss">
    .sidenav {
        height: 100%;
        width: 100%;
    }
</style>