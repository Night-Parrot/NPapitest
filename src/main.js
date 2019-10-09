import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VueResource from 'vue-resource';
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';

Vue.use(Antd);
Vue.use(VueResource)
Vue.config.productionTip = false



new Vue({
  router,
  VueResource,
  render: h => h(App)
}).$mount('#app')
