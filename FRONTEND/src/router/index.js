import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)
const router = new VueRouter({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: () => import('../components/Login')
    },
    {
      path: '/index',
      name: 'Index',
      component: () => import('../components/Index')
    },
    {
      path: '/upload',
      name: 'Uploade',
      component: () => import('../components/Uploader')
    },
    {
      path: '/:catchAll(.*)',
      name: '404',
      component: () => import('../views/404.vue')
    }
  ]
})

export default router
