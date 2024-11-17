<script setup>
import { useStore } from "vuex/dist/vuex.cjs.js";
import { ref } from "vue";

import axios from "axios";
const store = useStore();
const props = defineProps({
  closeaddServiceModal: Function,
});
const serviceName = ref("");
const serviceDescription = ref("");
const basePrice = ref();
const timeRequired = ref();
const handleSubmit = async (e) => {
  e.preventDefault();
  await axios
    .post(
      "http://localhost:5000/api/addService",
      JSON.stringify({
        name: serviceName.value,
        description: serviceDescription.value,
        price: basePrice.value,
        time_required: timeRequired.value,
      }),
      {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      }
    )
    .then(
      async (data) => {
        props.closeaddServiceModal();
        await axios
          .get("http://localhost:5000/api/getServices", {
            withCredentials: true,
          })
          .then(
            (data) => store.commit("setServices", data.data.data),
            (err) => console.log(err.response.data)
          );
      },
      (data) => {
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
        @click="props.closeaddServiceModal"
      ></button>
      <h3 class="my-4 fs-1 text-white">Add Service</h3>
      <form @submit="handleSubmit" class="service-form">
        <div class="input-wrapper">
          <input
            type="text"
            placeholder="Service Name"
            name="service-name"
            class="input input-service-name"
            :value="serviceName"
            required
            @change="(e) => (serviceName = e.target.value)"
          />
          <textarea
            name="serviceDescription"
            class="bg-transparent text-white input input-description"
            placeholder="Description"
            :value="serviceDescription"
            required
            @change="(e) => (serviceDescription = e.target.value)"
          ></textarea>
          <input
            type="text"
            placeholder="Base Price"
            name="base-price"
            required
            class="input input-base-price"
            :value="basePrice"
            @change="(e) => (basePrice = e.target.value)"
          />
          <input
            type="text"
            placeholder="Time Required(in Hours)"
            name="time-required"
            required
            class="input input-time-required"
            :value="timeRequired"
            @change="(e) => (timeRequired = e.target.value)"
          />
        </div>
        <button type="submit" class="login-button btn btn-secondary">
          Add Service
        </button>
      </form>
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
.service-form {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}
.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
