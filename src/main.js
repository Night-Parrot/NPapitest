import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VueResource from 'vue-resource';
import { DatePicker } from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';

Vue.use(DatePicker)
Vue.use(VueResource)
Vue.config.productionTip = false



new Vue({
  router,
  VueResource,
  render: h => h(App)
}).$mount('#app')
