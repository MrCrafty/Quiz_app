<script setup>
import { computed } from "vue";
import { useStore } from "vuex";
import AddQuizModal from "../components/Modals/AddQuizModal.vue";
import AddQuestionModal from "../components/Modals/AddQuestionModal.vue";
import { GetChapters } from "../main";
import axios from "axios";
import { useToast } from "vue-toastification";

const toast = useToast();
const store = useStore();
const quizzes = computed(() => store.state.quizzes);
const chapters = computed(() => store.state.chapters);

const handleQuestionDelete = (e) => {
  if (confirm("Do you want to delete the question ?")) {
    axios
      .delete("http://localhost:5000/api/question/" + e, {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      })
      .then(
        () => {
          toast.success("Question deleted successfully!");
          GetChapters();
        },
        () => {
          toast.error("Error in Deleting question");
        }
      );
  }
};
</script>
<template>
  <div class="container">
    <div class="row my-4 gap-4">
      <div class="col-12 pb-2 text-white d-flex justify-content-between">
        <h2 class="fs-1">Quizzes</h2>
        <AddQuizModal />
      </div>
      <div
        class="col-12 quiz-list rounded-4 py-3 px-2"
        v-for="quiz in quizzes"
        v-bind:key="quiz.id"
      >
        <div class="card">
          <div
            class="card-header d-flex align-items-center justify-content-between"
          >
            <div class="card-title fs-1">
              Chapter :
              {{
                Array.from(chapters).find((data) => data.id == quiz.chapter_id)
                  ?.name
              }}
            </div>
            <div class="quiz-date fs-3">
              {{
                `Time : ${new Date(quiz.date).getDate()}/${new Date(
                  quiz.date
                ).getMonth()}/${new Date(quiz.date).getFullYear()}@${new Date(
                  quiz.date
                ).getUTCHours()}:${new Date(quiz.date).getMinutes()} `
              }}
            </div>
          </div>
          <div class="card-body">
            <div
              class="border-bottom pb-2 mb-3 d-flex justify-content-between align-self-center"
            >
              <div class="fs-3 d-flex align-self-center">Questions</div>
              <AddQuestionModal :chapterId="quiz.chapter_id" />
            </div>
            <div
              v-for="ques in Array.from(chapters).find(
                (data) => data.id == quiz.chapter_id
              )?.questions"
              v-bind:key="ques.id"
              class="card-questions d-flex justify-content-between gap-4 mb-4 align-items-center"
            >
              <div class="question-title w-75">{{ ques.question }}</div>
              <div
                class="question-cta-button w-25 d-flex gap-1 justify-content-end"
              >
                <button class="btn btn-light text-success">Edit</button>
                <button
                  class="btn btn-light text-danger"
                  @click="
                    () => {
                      handleQuestionDelete(ques.id);
                    }
                  "
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped lang="css">
.btn {
  line-height: 1rem;
}
.quiz-list {
  background-color: #171717;
  color: white;
}
.card {
  background-color: #171717;
  color: aliceblue;
  height: 100%;
  border: none;
}
.card-questions {
  padding-bottom: 1rem;
  padding-inline: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.325);
}
.card-questions:last-child {
  border: none;
}
</style>
