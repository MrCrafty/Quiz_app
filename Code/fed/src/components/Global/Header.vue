<script setup>
//imports
import { useStore } from "vuex";
import { computed, ref } from "vue";
import Login from "./Login.vue";
import VueCookies from "vue-cookies";
import axios from "axios";

//variables
const store = useStore();
const user = computed(() => store.state.user);
const isLoggedIn = VueCookies.get("access_token") != null;
const xp = isLoggedIn ? JSON.parse(store.state.user.xp) : "";
</script>
<template lang="html">
  <div class="container header-wrapper py-3 mt-2">
    <div class="row rounded-pill header px-4">
      <div class="d-flex justify-content-between align-items-center py-2">
        <span class="logo h2"
          ><router-link class="text-white">ScaleUpQuiz</router-link></span
        >
        <ul class="nav align-items-center">
          <li class="nav-link"><router-link to="/">Home</router-link></li>
          <li
            v-if="isLoggedIn && store.state.user.role == 'admin'"
            class="nav-link"
          >
            <router-link to="/quiz" class="me-3">Quiz</router-link>
          </li>
          <li
            v-if="isLoggedIn && store.state.user.role == 'user'"
            class="nav-link"
          >
            <router-link to="/scores" class="me-3">Scores</router-link>
          </li>
          <li v-if="isLoggedIn">
            <router-link
              class="profile-btn btn rounded-pill border-1 border-white text-white"
              to="/profile"
              >Profile</router-link
            >
          </li>
          <Login />
        </ul>
      </div>
    </div>
    <div>
      <div
        v-if="isLoggedIn && user.role == 'admin'"
        class="w-auto text-white rounded-pill py-3 px-5 fs-4 user-name"
      >
        Hello, Admin
      </div>
      <div
        class="w-auto text-white rounded-pill py-3 px-5 fs-4 user-name"
        v-if="isLoggedIn && user.role == 'user'"
      >
        Hello, {{ xp.name }}
      </div>
    </div>
  </div>
</template>
<style scoped lang="css">
li {
  color: wheat;
  list-style: none;
}
a {
  text-decoration: none;
  color: white;
}
.nav-link {
  font-size: 1.2rem;
}
.header,
.user-name {
  background-color: #171717;
}
.user-name {
  text-wrap: nowrap;
}
.header {
  display: flex;
  width: 100%;
}
.header-wrapper {
  display: flex;
  width: 100%;
  justify-content: space-between;
  gap: 1.2rem;
}
</style>
