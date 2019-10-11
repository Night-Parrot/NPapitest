import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import testlist from './components/test_list.vue'
import zx_list from './components/zx_list.vue'
import about from './views/About.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: about
    },
    {
      path: '/list',
      name: 'list',
      component: testlist
    },
    {
      path: '/zx_list',
      name: 'zx_list',
      component: zx_list
    }
  ]
})
