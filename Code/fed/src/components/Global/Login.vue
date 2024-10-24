<script setup>
import { useStore } from "vuex/dist/vuex.cjs.js";
import { ref } from "vue";

import axios from "axios";
const props = defineProps({
  LoginOpen: Function,
  UserRegisterOpen: Function,
  ProfRegisterOpen: Function,
  CloseModal: Function,
});

const store = useStore();
const email = ref("");
const password = ref("");
const handleSubmit = async (e) => {
  e.preventDefault();
  await axios
    .post(
      "http://localhost:5000/login",
      JSON.stringify({
        email: email.value,
        password: password.value,
      }),
      {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      }
    )
    .then(
      (data) => {
        props.CloseModal();
        window.location.reload();
      },
      (data) => {
        email.value = "";
        password.value = "";
        alert(data.response.data.error);
      }
    );
};
</script>
<template lang="html">
  <div class="login">
    <div class="login-modal bg-dark">
      <button
        class="modal-close btn btn-close text-bg-danger"
        @click="props.CloseModal"
      ></button>
      <h3 class="mt-4 fs-1 text-white">Login</h3>
      <img src="/login.png" class="login-logo" />
      <form @submit="handleSubmit" class="login-form">
        <div class="input-wrapper">
          <input
            type="email"
            placeholder="Email"
            name="email"
            class="input input-email"
            :value="email"
            required
            @change="(e) => (email = e.target.value)"
          />
          <input
            type="password"
            minlength="6"
            placeholder="Password"
            name="password"
            required
            class="input input-password"
            :value="password"
            @change="(e) => (password = e.target.value)"
          />
        </div>
        <button type="submit" class="login-button btn btn-secondary">
          Login
        </button>
      </form>
      <div class="mt-3 d-flex gap-3">
        <button class="btn text-warning" @click="props.UserRegisterOpen">
          Register as User
        </button>
        <button
          class="prof-register btn text-info"
          @click="props.ProfRegisterOpen"
        >
          Register as Professional
        </button>
      </div>
    </div>
  </div>
</template>
<style scoped lang="css">
.input {
  background: transparent;
  border: none;
  border-bottom: 1px solid white;
  color: whitesmoke;
  padding: 0.5rem;
}
.input:focus {
  outline: none;
}
.modal-close {
  position: absolute;
  right: 1rem;
  top: 1rem;
  font-size: larger;
}
.login {
  position: fixed;
  left: 0;
  top: 0;
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1;
}
.login-modal {
  border: 2px solid white;
  border-radius: 10px;
  padding-inline: 2rem;
  padding-block-end: 2rem;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  backdrop-filter: blur(150px);
}
.login-logo {
  width: 8rem;
}
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
