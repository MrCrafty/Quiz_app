<script setup>
import AdminDashVue from "../components/Admin/AdminDash.vue";
import UserDashVue from "../components/User/UserDash.vue";
import VueCookies from "vue-cookies";
import { useStore } from "vuex";
import { computed } from "vue";
const store = useStore();
const isLoggedIn = VueCookies.get("access_token") != null;
const user = computed(() => store.state.user);
</script>
<template lang="html">
  <div v-if="!isLoggedIn">
    <h1>Please Login to continue</h1>
  </div>
  <AdminDashVue v-if="isLoggedIn && user.role == 'admin'" />
  <UserDashVue v-if="isLoggedIn && user.role == 'user'" />
</template>
<style scoped lang="css"></style>
