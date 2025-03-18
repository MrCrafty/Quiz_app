<script setup>
import axios from "axios";
import { computed, ref } from "vue";
import { useToast } from "vue-toastification";
import { useStore } from "vuex";
import { GetQuizes, GetChapters } from "../../main";

const store = useStore();
const toast = useToast();

const subjects = computed(() => store.state.subjects);

const props = defineProps({
  chapterId: Number,
});

const AddQuestionModalOpen = ref(false);

const question = ref("");
const answer = ref("");
const option1 = ref("");
const option2 = ref("");
const option3 = ref("");
const option4 = ref("");
const options = ref([]);

const handleAddQuestion = async (e) => {
  e.preventDefault();
  options.value.push(option1.value);
  options.value.push(option2.value);
  options.value.push(option3.value);
  options.value.push(option4.value);
  await axios
    .post(
      "http://localhost:5000/api/question",
      {
        chapter_id: props.chapterId,
        question: question.value,
        answer: answer.value,
        options: Array.from(options.value),
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
        toast.success("Question Added  successfully");
        GetQuizes();
        GetChapters();
      },
      () => {
        toast.error("Error adding Question");
      }
    );
  closeAddQuestionModal();
};
const closeAddQuestionModal = () => {
  AddQuestionModalOpen.value = false;
};
</script>
<template>
  <div>
    <button
      class="fs-4 px-3 btn bg-black text-info rounded-pill"
      @click="() => (AddQuestionModalOpen = true)"
    >
      Add Question
    </button>
    <div class="modal-wrapper" v-if="AddQuestionModalOpen">
      <div class="modal-inner">
        <button class="btn btn-close" @click="closeAddQuestionModal"></button>
        <div class="modal-body">
          <form
            class="d-flex flex-column mt-5 mb-4 px-4 gap-4"
            @submit="handleAddQuestion"
          >
            <input
              class="fs-3"
              type="text"
              placeholder="Enter Question"
              @input="
                (e) => {
                  question = e.target.value;
                }
              "
              :value="question"
            />
            <select
              name="answer"
              id="answer"
              class="fs-4 p-2 border-0 border-bottom border-dark"
              @input="
                (e) => {
                  answer = e.target.value;
                }
              "
              :value="answer"
            >
              <option value="" hidden>Select Answer</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
            </select>
            <div class="option-wrapper">
              <input
                class="fs-4 w-100"
                type="text"
                placeholder="Enter option 1"
                @input="
                  (e) => {
                    option1 = e.target.value;
                  }
                "
                :value="option1"
              />
              <input
                class="fs-4"
                type="text"
                placeholder="Enter option 2"
                @input="
                  (e) => {
                    option2 = e.target.value;
                  }
                "
                :value="option2"
              />
              <input
                class="fs-4"
                type="text"
                placeholder="Enter option 3"
                @input="
                  (e) => {
                    option3 = e.target.value;
                  }
                "
                :value="option3"
              />
              <input
                class="fs-4"
                type="text"
                placeholder="Enter option 4"
                @input="
                  (e) => {
                    option4 = e.target.value;
                  }
                "
                :value="option4"
              />
            </div>
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
  width: 100%;
}
input:focus {
  outline: none;
}
.option-wrapper input {
  padding: 0.4rem;
}
select:focus {
  outline: none;
}
</style>
