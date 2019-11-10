import Vue from 'vue'
import App from './App.vue'
import router from './router'
// import VueResource from 'vue-resource';
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
import G2 from '@antv/g2';
import axios from 'axios';
// import VueAxios from 'vue-axios'
import preview from 'vue-photo-preview'
import 'vue-photo-preview/dist/skin.css'



Vue.use(G2)
Vue.use(Antd)
// Vue.use(VueResource)
Vue.use(axios)
Vue.use(preview)
Vue.config.productionTip = false
// axios.defaults.baseURL = 'http://172.18.49.18:8585/';
axios.defaults.baseURL = 'http://192.168.1.57:8585/';


new Vue({
  router,
  // VueResource,
  axios,
  render: h => h(App)
}).$mount('#app')
