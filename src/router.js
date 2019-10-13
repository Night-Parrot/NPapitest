import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import testlist from './components/test_list.vue'
import xm_info from './components/xm_info.vue'
import about from './views/About.vue'
import test_page from './components/test.vue'

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
      path: '/xm_info/:xmid',
      name: 'xm_info',
      component: xm_info
    },
    {
      path: '/testpage',
      name: '测试页面',
      component: test_page
    }
  ]
})
