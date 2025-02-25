<script setup>
import { computed, ref } from "vue";
import { useStore } from "vuex";
import UserBookServiceModal from "./UserBookServiceModal.vue";
const servicesModal = ref({
  isOpen: false,
  service: null,
});
const store = useStore();
const services = computed(() => store.state.services);
</script>
<template>
  <div class="container text-white py-5">
    <h2 class="text-uppercase">Services we offer</h2>
    <hr />
    <div class="row g-3">
      <div class="col-6" v-for="(service, index) in services" :key="index">
        <div class="bg-dark p-3 py-5 fs-2 rounded-2 text-center">
          {{ service.name }}
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped></style>
