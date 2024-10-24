import { computed, createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from './components/Global/Dashboard.vue'
import { createStore } from 'vuex'
import axios from 'axios'
import VueCookies from 'vue-cookies'

const app = createApp(App)
const store = createStore({
    state() {
        return {
            user: {},
            count: 0,
            isLoginOpen: false,
            services: [],
            professionals: [],
            serviceRequests: []
        }
    },
    mutations: {
        setUser(state, payload) {
            state.user = payload
        },
        setLogin(state) {
            state.isLoginOpen = !state.isLoginOpen
        },
        setServices(state, payload) {
            state.services = payload
        },
        setProfessionals(state, payload) {
            state.professionals = payload
        },
        setServiceRequests(state, payload) {
            state.serviceRequests = payload
        }
    }

})
await axios.get("http://localhost:5000/api/getServices", { withCredentials: true }).then((data) => store.commit('setServices', data.data.data), (err) => console.log(err.response.data))
if (VueCookies.get("access_token") != null) {
    await axios.get("http://localhost:5000/getuser", { withCredentials: true }).then((data) => store.commit('setUser', data.data), (err) => console.log(err.response.data))
    await axios.get("http://localhost:5000/api/getServiceRequests", { withCredentials: true }).then((data) => console.log(data.data), (err) => console.log(err.response.data))
    await axios.get("http://localhost:5000/api/getProfessionals", { withCredentials: true }).then((data) => console.log(data.data), (err) => console.log(err.response.data))
}
const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: "/", component: Dashboard },
    ],
});
app.use(router);
app.use(store);
app.mount("#app");