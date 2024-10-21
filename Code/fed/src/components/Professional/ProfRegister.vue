<script setup>
import { useStore } from "vuex/dist/vuex.cjs.js";
import { computed, ref } from "vue";

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
const confirmPassword = ref("");
const name = ref("");
const address = ref("");
const pincode = ref();
const experience = ref();
const selectedServ = ref();
const services = computed(() => store.state.services);
const handleSubmit = async (e) => {
  e.preventDefault();
  if (password.value != confirmPassword.value) {
    alert("Passwords do not match");
    return;
  }
  await axios
    .post(
      "http://localhost:5000/register",
      JSON.stringify({
        email: email.value,
        password: password.value,
        role: "professional",
        xp: {
          name: name.value,
          address: address.value,
          pincode: pincode.value,
          service: selectedServ.value,
          experience: experience.value,
          status: "pending",
        },
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
      <button class="modal-close btn btn-danger" @click="props.CloseModal">
        X
      </button>
      <h3 class="my-4 fs-2 text-white">Professional Register</h3>
      <form @submit="handleSubmit" class="login-form">
        <div class="input-wrapper text-white">
          <input
            type="email"
            placeholder="Email"
            name="email"
            class="input input-email"
            :value="email"
            @change="(e) => (email = e.target.value)"
            required
          />
          <input
            type="text"
            placeholder="Full Name"
            name="name"
            class="input input-name"
            :value="name"
            @change="(e) => (name = e.target.value)"
            required
          />
          <select
            name="services"
            class="input services-dropdown bg-transparent"
            required
            @change="(e) => (selectedServ = e.target.value)"
          >
            <option value="">Please select a service</option>
            <option v-for="service in services" :value="service.Id">
              {{ service.Name }}
            </option>
          </select>
          <input
            type="number"
            placeholder="pincode"
            name="pincode"
            class="input input-pincode"
            :value="pincode"
            required
            @change="(e) => (pincode = e.target.value)"
            maxlength="6"
          />
          <textarea
            name="address"
            :value="address"
            class="input input-address bg-transparent"
            placeholder="Enter your address"
            maxlength="250"
            required
            @change="(e) => (address = e.target.value)"
          ></textarea>
          <input
            type="number"
            placeholder="Experience in Years"
            name="experience"
            class="input input-experience"
            :value="experience"
            required
            @change="(e) => (experience = e.target.value)"
          />

          <input
            type="password"
            minlength="6"
            placeholder="Password"
            name="password"
            class="input input-password"
            :value="password"
            required
            @change="(e) => (password = e.target.value)"
          />
          <input
            type="text"
            minlength="6"
            placeholder="Confirm Password"
            name="confirmPassword"
            class="input input-confirm-password"
            :value="confirmPassword"
            required
            @change="(e) => (confirmPassword = e.target.value)"
          />
        </div>
        <button type="submit" class="login-button btn btn-secondary">
          Register
        </button>
      </form>
      <div class="mt-3 d-flex gap-3">
        <button class="btn text-warning" @click="props.LoginOpen">
          Have an account? Login
        </button>
        <button
          class="prof-register btn text-info"
          @click="props.UserRegisterOpen"
        >
          Register as User
        </button>
      </div>
    </div>
  </div>
</template>
<style lang="css">
/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type="number"] {
  -moz-appearance: textfield;
}
.input {
  background: transparent;
  border: none;
  border-bottom: 1px solid white;
  color: whitesmoke;
  padding: 0.5rem;
  width: 20rem;
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
  position: absolute;
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
  padding-inline: 3rem;
  padding-block-end: 2rem;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  backdrop-filter: blur(150px);
  font-size: 1.2rem;
}
.login-logo {
  width: 7rem;
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
  width: 100%;
}
</style>
