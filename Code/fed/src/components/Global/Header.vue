<script setup>
//imports
import { useStore } from "vuex";
import { computed, ref } from "vue";
import Login from "./Login.vue";
import VueCookies from "vue-cookies";
import axios from "axios";
import UserRegister from "../User/UserRegister.vue";
import ProfRegister from "../Professional/ProfRegister.vue";

//variables
const store = useStore();
const isLoginOpen = ref(false);
const isProfRegisterOpen = ref(false);
const isUserRegisterOpen = ref(false);
const CloseModal = () => {
  isLoginOpen.value = false;
  isProfRegisterOpen.value = false;
  isUserRegisterOpen.value = false;
};
const LoginOpen = () => {
  isLoginOpen.value = !isLoginOpen.value;
  isProfRegisterOpen.value = false;
  isUserRegisterOpen.value = false;
};
const UserRegisterOpen = () => {
  isUserRegisterOpen.value = true;
  isLoginOpen.value = false;
  isProfRegisterOpen.value = false;
};
const ProfRegisterOpen = () => {
  isUserRegisterOpen.value = false;
  isLoginOpen.value = false;
  isProfRegisterOpen.value = true;
};
const user = computed(() => store.state.user);
const isLoggedIn = VueCookies.get("access_token") != null;
const xp = isLoggedIn ? JSON.parse(store.state.user.xp) : "";
//handlers
const handleLogout = async () => {
  await axios
    .get("http://localhost:5000/logout", { withCredentials: true })
    .then(() => (window.location.href = "/"));
};
</script>
<template lang="html">
  <Login
    v-if="isLoginOpen"
    :LoginOpen="LoginOpen"
    :UserRegisterOpen="UserRegisterOpen"
    :ProfRegisterOpen="ProfRegisterOpen"
    :CloseModal="CloseModal"
  />
  <UserRegister
    v-if="isUserRegisterOpen"
    :LoginOpen="LoginOpen"
    :UserRegisterOpen="UserRegisterOpen"
    :ProfRegisterOpen="ProfRegisterOpen"
    :CloseModal="CloseModal"
  />
  <ProfRegister
    v-if="isProfRegisterOpen"
    :LoginOpen="LoginOpen"
    :UserRegisterOpen="UserRegisterOpen"
    :ProfRegisterOpen="ProfRegisterOpen"
    :CloseModal="CloseModal"
  />
  <div class="container">
    <div class="row">
      <div class="d-flex justify-content-between align-items-center py-2">
        <span class="logo h2"
          ><router-link>Homestead Helpers</router-link></span
        >
        <ul class="nav align-items-center">
          <li v-if="isLoggedIn && user.role == 'admin'">Hello, Admin</li>
          <li
            v-if="
              isLoggedIn && (user.role == 'user' || user.role == 'professional')
            "
          >
            Hello, {{ xp.name }}
          </li>
          <li class="nav-link"><router-link to="/">Home</router-link></li>
          <!-- <li class="nav-link">
            <router-link to="/search">Search</router-link>
          </li>
          <li class="nav-link">
            <router-link to="/summary">Summary</router-link>
          </li> -->
          <li v-if="isLoggedIn">
            <router-link
              class="profile-btn btn btn-primary text-white"
              to="/profile"
              >Profile</router-link
            >
          </li>
          <li v-if="isLoggedIn">
            <button class="btn text-white bg-danger ms-2" @click="handleLogout">
              Logout
            </button>
          </li>
          <li v-else>
            <button class="btn text-white bg-primary" @click="LoginOpen">
              Login
            </button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
<style scoped lang="css">
li {
  list-style: none;
}
a {
  text-decoration: none;
  color: black;
}
.nav-link {
  font-size: 1.2rem;
}
body {
  font-family: "Poppins", Courier, monospace !important;
}
</style>
