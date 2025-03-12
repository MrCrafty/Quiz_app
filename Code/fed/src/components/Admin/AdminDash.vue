<script setup>
import { computed, ref } from "vue";
import { useStore } from "vuex";
import AddSubjectModel from "../Modals/AddSubjectModal.vue";
import AddChapterModel from "../Modals/AddChapterModal.vue";

const store = useStore();
const subjects = computed(() => store.getters.getSubjects);
</script>
<template>
  <div
    class="container mt-4 pt-5 border border-1 border-bottom-0 border-end-0 border-start-0 border-dark"
  >
    <div class="d-flex justify-content-between">
      <h2 class="text-white fs-1">Subjects</h2>
      <AddSubjectModel />
    </div>
    <div class="row text-dark mt-0 g-4">
      <div v-for="sub in subjects" v-bind:key="sub.id" class="col-6">
        <div class="card rounded-4 py-3 px-2">
          <div class="card-title fs-1 text-center">{{ sub.name }}</div>
          <div class="card-body">
            <div class="card-description">{{ sub.description }}</div>
            <div class="card-chapters">
              <div v-for="chapter in sub.chapters" v-bind:key="chapter.id">
                {{ chapter.name }}
                {{ chapter.description }}
              </div>
            </div>
          </div>
          <div class="d-flex justify-content-end me-2">
            <AddChapterModel :subjectId="sub.id" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.card {
  background-color: #171717;
  color: aliceblue;
  height: 100%;
}
</style>
