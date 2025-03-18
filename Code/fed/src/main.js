import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from './Pages/Dashboard.vue'
import QuizManagement from './Pages/QuizManagement.vue'
import Scores from './Pages/Scores.vue'
import Summary from './Pages/Summary.vue'
import PageNotFound from './Pages/PageNotFound.vue'
import { createStore } from 'vuex'
import axios from 'axios'
import VueCookies from 'vue-cookies'
import Toast from "vue-toastification";
import 'vue-toastification/dist/index.css';

const isLoggedIn = VueCookies.get("access_token") != null;
const app = createApp(App)

app.use(Toast, {
    timeout: 2000,
    closeOnClick: true,
    pauseOnHover: false,
    pauseOnFocusLoss: false,
})
const store = createStore({
    state() {
        return {
            user: {},
            count: 0,
            subjects: [],
            quizzes: [],
            chapters: []
        }
    },
    mutations: {
        setUser(state, payload) {
            state.user = payload
        },
        setSubjects(state, payload) {
            state.subjects = payload
        },
        setQuizzes(state, payload) {
            state.quizzes = payload
        },
        setChapters(state, payload) {
            state.chapters = payload
        }
    },
    getters: {
        getUser(state) {
            return state.user
        },
        getSubjects(state) {
            return state.subjects
        },
        getQuizzes(state) {
            return state.quizzes
        },
        getChapters(state) {
            return state.chapters
        }
    }
})

if (isLoggedIn) {
    await axios.get("http://localhost:5000/getuser", { withCredentials: true }).then((data) => store.commit('setUser', data.data), (err) => console.log(err.response.data))
}
export const GetSubjects = async () => {
    await axios.get('http://localhost:5000/api/subjects', { withCredentials: true }).then((data) => store.commit('setSubjects', data.data.data), (err) => console.log(err.response.data))
}
export const GetQuizes = async () => {
    await axios.get("http://localhost:5000/api/quizzes", { withCredentials: true }).then((data) => store.commit('setQuizzes', data.data.data), (err) => console.log(err.response.data))
}
export const GetChapters = async () => {
    await axios.get("http://localhost:5000/api/chapters", { withCredentials: true }).then((data) => store.commit('setChapters', data.data.data), (err) => console.log(err.response.data))
}
GetSubjects();
GetQuizes();
GetChapters();

const router = createRouter({
    history: createWebHistory(),
    strict: true,

    routes: [
        { path: "/", component: Dashboard },
        { path: "/quiz", component: QuizManagement },
        { path: "/scores", component: Scores },
        { path: '/summary', component: Summary },
        { path: '/:pathMatch(.*)*', component: PageNotFound },
    ],
});
app.use(router);
app.use(store);
app.mount("#app");