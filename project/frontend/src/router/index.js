import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/setresult/:originalVersion/:compareVersion',
        name: 'setResult',
        component: () => import('../views/SetResult.vue')
    },
    {
        path: '/getresult/:originalVersion/:compareVersion',
        name: 'getResult',
        component: () => import('../views/GetResult.vue')
    }
]

const router = new VueRouter({
    mode: 'history',
    routes
})

export default router
