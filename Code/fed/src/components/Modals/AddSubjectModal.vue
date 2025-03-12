<script setup>
import axios from "axios";
import { ref } from "vue";
import { ApiService, GetSubjects } from "../../main";
const AddSubjectModelOpen = ref(false);
const subName = ref("");
const subDescription = ref("");
const handleAddSubject = async (e) => {
  e.preventDefault();
  await axios
    .post(
      "http://localhost:5000/api/subject",
      {
        name: subName.value,
        description: subDescription.value,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      }
    )
    .then(
      () => {
        alert("Subject added successfully");
        GetSubjects();
      },
      () => {
        alert("Error adding subject");
      }
    );
  closeAddSubjectModal();
};
const closeAddSubjectModal = () => {
  subName.value = "";
  subDescription.value = "";
  AddSubjectModelOpen.value = false;
};
</script>
<template>
  <div>
    <button
      class="fs-3 px-4 btn bg-white rounded-pill"
      @click="() => (AddSubjectModelOpen = true)"
    >
      Add Subject
    </button>
    <div v-if="AddSubjectModelOpen" class="modal-wrapper">
      <div class="modal-inner">
        <button class="btn btn-close" @click="closeAddSubjectModal"></button>
        <div class="modal-body">
          <form
            class="d-flex flex-column my-5 px-4 gap-4"
            @submit="handleAddSubject"
          >
            <input
              class="fs-3"
              type="text"
              placeholder="Subject Name"
              @input="
                (e) => {
                  subName = e.target.value;
                }
              "
              :value="subName"
            />
            <input
              class="fs-3"
              type="text"
              placeholder="Subject Description"
              @input="
                (e) => {
                  subDescription = e.target.value;
                }
              "
              :value="subDescription"
            />
            <button
              type="submit"
              class="fs-4 w-50 align-self-center btn bg-dark text-white rounded-pill"
            >
              Add Subject
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.modal-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-inner {
  position: relative;
  width: 500px;
  background-color: white;
  border-radius: 10px;
}
.btn-close {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
}
input {
  border: none;
  border-bottom: 1px solid black;
  padding-block: 10px;
  padding-inline: 15px;
}
input:focus {
  outline: none;
}
.modal-body {
}
</style>
