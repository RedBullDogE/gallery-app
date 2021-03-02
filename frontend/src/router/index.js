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
        path: '/picture/:id',
        name: 'Details',
        component: () => import('../views/PictureDetails.vue'),
        meta: { title: 'Drown Gallery | Picture' }
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue'),
        meta: { title: 'Drown Gallery | Sign In' }
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/Register.vue'),
        meta: { title: 'Drown Gallery | Sign Up' }
    },
    {
        path: '/create',
        name: 'Create',
        component: () => import('../views/PictureCreate.vue'),
        beforeEnter: (to, from, next) => {
            const user = localStorage.getItem('user');

            if (user) next()
            else next({ name: 'Home' })
        },
        meta: { title: 'Drown Gallery | Add picture' }
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
