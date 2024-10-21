<script setup>
import AdminDashVue from "../Admin/AdminDash.vue";
import ProfDashVue from "../Professional/ProfDash.vue";
import UserDashVue from "../User/UserDash.vue";
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
  <ProfDashVue v-if="isLoggedIn && user.role == 'professional'" />
</template>
<style scoped lang="css"></style>
