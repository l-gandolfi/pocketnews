import 'bootstrap/dist/css/bootstrap.css';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import Vue from 'vue';
import App from './App.vue';
import router from './router';

import axios from 'axios';

axios.defaults.baseURL = process.env.VUE_APP_APIURL;

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);

Vue.config.productionTip = false;

Vue.prototype.$eventBus = new Vue(); 

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
