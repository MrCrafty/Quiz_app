<script setup>
import axios from "axios";
import { computed, ref } from "vue";
import { useStore } from "vuex";
import AddService from "../Global/AddService.vue";
import EditService from "../Global/EditService.vue";
const store = useStore();

const services = computed(() => store.state.services);
const professionals = computed(() => store.state.professionals);
const serviceRequest = computed(() => store.state.serviceRequests);
const addServiceModal = ref(false);
const editServiceModal = ref(false);
const editService = ref(null);
const handleDeleteService = async (id) => {
  if (confirm("Are you sure you want to delete this service?")) {
    console.log("Delete Service");
    await axios
      .post(
        "http://localhost:5000/api/deleteService",
        JSON.stringify({ service_id: id }),
        {
          headers: {
            "Content-Type": "application/json",
          },
          withCredentials: true,
        }
      )
      .then(
        async (data) => {
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
          alert("Some error occurred, please check the logs");
          console.log(data);
        }
      );
  }
};
const closeeditServiceModal = () => {
  editServiceModal.value = false;
  editService.value = null;
};
const closeaddServiceModal = () => {
  addServiceModal.value = false;
};
</script>
<template>
  <div class="container">
    <AddService
      v-if="addServiceModal"
      :closeaddServiceModal="closeaddServiceModal"
    />
    <EditService
      v-if="editServiceModal"
      :serviceId="editService"
      :closeeditServiceModal="closeeditServiceModal"
    />
    <div class="row text-light">
      <div class="col-12 services-wrapper bg-dark py-5 px-5 my-4">
        <h2 class="section-header">Services</h2>
        <hr />
        <table v-if="services && services.length > 0" class="services-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Service Name</th>
              <th>Base Price</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody class="service-tbody">
            <tr v-for="(service, index) in services" v-bind:key="index">
              <td>{{ index }}</td>
              <td>{{ service.name }}</td>
              <td>{{ service.price }}</td>
              <td class="action-btns d-flex justify-content-around w-50 m-auto">
                <button
                  class="btn btn-info"
                  @click="
                    () => {
                      editService = service.id;
                      editServiceModal = !editServiceModal;
                    }
                  "
                >
                  Edit</button
                ><button
                  class="btn btn-danger"
                  @click="handleDeleteService(service.id)"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <h3 v-else>No data to show. Please add Services</h3>
        <button
          class="add-service-btn btn btn-outline-danger fs-6"
          @click="() => (addServiceModal = !addServiceModal)"
        >
          + Add Service
        </button>
      </div>
      <div class="col-12 prof-wrapper bg-dark py-5 px-5 my-4">
        <h2 class="prof-header">Professionals</h2>
        <hr />
        <table
          v-if="professionals && professionals.length > 0"
          class="prof-table fs-5"
        >
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Years of Experience</th>
              <th>Service Name</th>
              <th>Action</th>
            </tr>
          </thead>
        </table>
        <h3 v-else>No data to show</h3>
      </div>
      <div class="col-12 ser-req-wrapper bg-dark py-5 px-5 my-4">
        <h2 class="ser-req-header">Service Requests</h2>
        <hr />
        <table
          v-if="serviceRequest && serviceRequest.length > 0"
          class="ser-req-table fs-5"
        >
          <thead>
            <tr>
              <th>ID</th>
              <th>Service Name</th>
              <th>Assigned Professional</th>
              <th>Requested Date</th>
              <th>Status</th>
            </tr>
          </thead>
        </table>
        <h3 v-else>No data to show</h3>
      </div>
    </div>
  </div>
</template>

<style scoped>
.service-tbody tr:last-child {
  border-bottom: 0;
}
.service-tbody tr {
  border-bottom: 1px white solid;
}
.action-btns {
  font-family: poppins-light;
}
.add-service-btn {
  position: absolute;
  right: 1rem;
  padding: 1.2rem;
  top: 1rem;
  border-radius: 100px;
  line-height: 1rem;
  transition: all 0.2s ease-in-out;
  font-family: poppins-light;
}
.services-table th:last-child,
.prof-table th:last-child,
.ser-req-table th:last-child {
  border-inline-end: none !important;
}
.services-table,
.prof-table,
.ser-req-table {
  width: 100%;
}
.services-table th,
.prof-table th,
.ser-req-table th {
  border-inline-end: 1px solid white;
  text-align: center;
  background-color: black;
  padding-block: 5px;
}
.services-table td,
.prof-table td,
.ser-req-table td {
  /* border-inline-end: 1px solid white; */
  padding-block: 1rem;
  text-align: center;
}
.services-wrapper,
.prof-wrapper,
.ser-req-wrapper {
  border-radius: 10px;
  font-family: poppins-thin;
  position: relative;
}
.section-header,
.prof-header,
.ser-req-header {
  font-family: poppins-light;
}
</style>
