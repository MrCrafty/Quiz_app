<script setup>
import axios from "axios";
import { ref } from "vue";
import { GetSubjects } from "../../main";
import { useToast } from "vue-toastification";

const ChapterModalOpen = ref(false);
const toast = useToast({ duration: 2000, dismissible: true });
const props = defineProps({
  subjectId: Number,
});
const closeChapterModal = () => {
  subName.value = "";
  subDescription.value = "";
  ChapterModalOpen.value = false;
};
const subName = ref("");
const subDescription = ref("");
const handleAddChapter = async (e) => {
  e.preventDefault();
  await axios
    .post(
      "http://localhost:5000/api/chapter",
      {
        name: subName.value,
        description: subDescription.value,
        subject_id: props.subjectId,
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
        toast.success("Chapter added successfully");
        GetSubjects();
      },
      () => {
        toast.error("Error adding subject");
      }
    );
  closeChapterModal();
};
</script>
<template>
  <div>
    <button
      class="btn bg-black text-white rounded-4 add-chapter-btn"
      @click="ChapterModalOpen = true"
    >
      Add Chapter
    </button>
    <div v-if="ChapterModalOpen" class="modal-wrapper">
      <div class="modal-inner">
        <button class="btn btn-close" @click="closeChapterModal"></button>
        <div class="modal-body">
          <form
            class="d-flex flex-column my-5 px-4 gap-4"
            @submit="handleAddChapter"
          >
            <input
              class="fs-3"
              type="text"
              placeholder="Chapter Name"
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
              placeholder="Chapter Description"
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
              Add Question
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
.add-chapter-btn {
  box-shadow: rgb(101, 142, 255) 0px 0px 30px -10px;
}
</style>
