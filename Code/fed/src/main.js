import { computed, createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from './Pages/Dashboard.vue'
import { createStore } from 'vuex'
import axios from 'axios'
import VueCookies from 'vue-cookies'

const app = createApp(App)
const store = createStore({
    state() {
        return {
            user: {},
            count: 0,
            subjects: [],
            quizzes: []
        }
    },
    mutations: {
        setUser(state, payload) {
            state.user = payload
        },
        setSubjects(state, payload) {
            state.subjects = payload
        }
    },
    getters: {
        getUser(state) {
            return state.user
        },
        getSubjects(state) {
            return state.subjects
        }
    }

})

if (VueCookies.get("access_token") != null) {
    await axios.get("http://localhost:5000/getuser", { withCredentials: true }).then((data) => store.commit('setUser', data.data), (err) => console.log(err.response.data))
}
export const GetSubjects = async () => {
    await axios.get('http://localhost:5000/api/subjects', { withCredentials: true }).then((data) => store.commit('setSubjects', data.data.data), (err) => console.log(err.response.data))
}

export const ApiService = () => axios.create({
    baseURL: 'http://localhost:5000/api',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    }
})
GetSubjects();
const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: "/", component: Dashboard },
        { path: "/quiz", component: () => import('./Pages/QuizManagement.vue') },
        { path: "/scores", component: () => import('./Pages/Scores.vue') },
        { path: '/summary', component: () => import('./Pages/Summary.vue') }
    ],
});
app.use(router);
app.use(store);
app.mount("#app");