<template>
  <sidebar />

  <router-view />
</template>

<script setup>
import sidebar from "./components/sidebar.vue";
</script>

<style>
body {
  margin: 0;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
}
</style>
