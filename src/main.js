import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VueResource from 'vue-resource';
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
import G2 from '@antv/g2';
import axios from 'axios';
// import VueAxios from 'vue-axios'



Vue.use(G2)
Vue.use(Antd)
Vue.use(VueResource)
Vue.use(axios)
Vue.config.productionTip = false



new Vue({
  router,
  VueResource,
  axios,
  render: h => h(App)
}).$mount('#app')
