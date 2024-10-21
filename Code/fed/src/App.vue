<script setup>
import Header from "./components/Global/Header.vue";
import Footer from "./components/Global/Footer.vue";
</script>

<template>
  <div>
    <header><Header /></header>
    <main class="bg-secondary">
      <router-view></router-view>
    </main>
    <footer><Footer /></footer>
  </div>
</template>

<style scoped></style>
