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
      component: () => import('../components/Index'),
      children: [
        {
          path: 'file',
          name: 'CardFile',
          component: () => import('../components/CardFile')
        },
        {
          path: 'upload',
          name: 'CardUpload',
          component: () => import('../components/CardUpload')
        },
        {
          path: 'download',
          name: 'CardDownload',
          component: () => import('../components/CardDownload')
        },
        {
          path: 'search',
          name: 'CardSearch',
          component: () => import('../components/CardSearch')
        }
      ]
    },
    {
      path: '/:catchAll(.*)',
      name: '404',
      component: () => import('../views/404.vue')
    }
  ]
})

export default router
