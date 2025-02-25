<script setup>
import { useStore } from "vuex/dist/vuex.cjs.js";
import { computed, ref } from "vue";
import axios from "axios";

const store = useStore();
const props = defineProps({
  closeModal: Function,
  service: Number,
});
const professionals = computed(() =>
  store.state.professionals.filter(
    (x) => JSON.parse(x.xp).service == props.service
  )
);
</script>
<template lang="html">
  <div class="login">
    <div class="login-modal bg-dark">
      <button
        class="modal-close btn btn-close text-bg-danger"
        @click="props.closeModal"
      ></button>
      <h3 class="my-4 fs-1 text-white">Book a Service</h3>
      <ul class="d-flex flex-column gap-3">
        <li
          class="list-unstyled"
          v-for="(prof, index) in professionals"
          :key="index"
        >
          <div class="d-flex">
            <div>{{ JSON.parse(prof.xp).name }}</div>
          </div>
        </li>
      </ul>
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
.category-dropdown option {
  color: black;
}
</style>
