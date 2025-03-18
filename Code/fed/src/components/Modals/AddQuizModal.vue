<script setup>
import axios from "axios";
import { computed, ref } from "vue";
import { useToast } from "vue-toastification";
import { useStore } from "vuex";
import { GetQuizes } from "../../main";

const store = useStore();
const toast = useToast();

const subjects = computed(() => store.state.subjects);

const AddQuizModalOpen = ref(false);

const chapters = ref("");
const subject = ref("");
const chapterId = ref("");
const timeDuration = ref("");
const quizDate = ref("");

const handleAddQuiz = async (e) => {
  e.preventDefault();
  await axios
    .post(
      "http://localhost:5000/api/quiz",
      {
        chapter_id: chapterId.value,
        time_duration: timeDuration.value,
        date: quizDate.value,
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
        toast.success("Quiz Created  successfully");
        GetQuizes();
      },
      () => {
        toast.error("Error adding Quiz");
      }
    );
  closeAddQuizModal();
};
const closeAddQuizModal = () => {
  chapters.value = "";
  subject.value = "";
  quizDate.value = "";
  chapterId.value = "";
  timeDuration.value = "";
  AddQuizModalOpen.value = false;
};
</script>
<template>
  <div>
    <button
      class="fs-3 px-4 btn bg-white text-black rounded-pill"
      @click="() => (AddQuizModalOpen = true)"
    >
      Add Quiz
    </button>
    <div class="modal-wrapper" v-if="AddQuizModalOpen">
      <div class="modal-inner">
        <button class="btn btn-close" @click="closeAddQuizModal"></button>
        <div class="modal-body">
          <form
            class="d-flex flex-column mt-5 mb-4 px-4 gap-4"
            @submit="handleAddQuiz"
          >
            <select
              class="fs-4 p-2 border-0 border-bottom border-dark"
              @input="
                (e) => {
                  subject = e.target.value;
                  chapters = Array.from(subjects).filter(
                    (sub) => sub.id == e.target.value
                  )[0].chapters;
                }
              "
              :value="subject"
            >
              <option value="" hidden>Select Subject</option>
              <option
                v-for="subject in subjects"
                :value="subject.id"
                v-bind:key="subject.id"
              >
                {{ subject.name }}
              </option>
            </select>
            <select
              v-if="chapters"
              class="fs-4 p-2 border-0 border-bottom border-dark"
              @input="
                (e) => {
                  chapterId = e.target.value;
                }
              "
              :value="chapterId"
            >
              <option value="" hidden>Select Chapter</option>

              <option
                v-for="chapter in chapters"
                :value="chapter.id"
                v-bind:key="chapter.id"
              >
                {{ chapter.name }}
              </option>
            </select>

            <input
              class="fs-3"
              type="text"
              accept="number"
              placeholder="Time Duration in Minutes"
              @input="
                (e) => {
                  timeDuration = e.target.value;
                }
              "
              :value="timeDuration"
            />
            <input
              type="datetime-local"
              class="datetimepicker"
              @input="
                (e) => {
                  quizDate = e.target.value;
                }
              "
              :value="quizDate"
            />
            <button
              type="submit"
              class="fs-4 w-50 align-self-center btn bg-dark text-white rounded-pill"
            >
              Add Quiz
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
select:focus {
  outline: none;
}
</style>
