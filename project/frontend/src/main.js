import Vue from 'vue'
import App from './App.vue'
import { syncSession$ } from './mixins/session'
import request from "./api/request"
import router from './router'
import store from './store'
import ElementUI from 'element-ui'; // 2.1引入结构
import 'element-ui/lib/theme-chalk/index.css'; // 2.2引入样式
import axios from 'axios';

Vue.prototype.$axios = axios;
Vue.use(ElementUI); // 3.安装
Vue.config.productionTip = false
Vue.prototype.$http = request

syncSession$().then(() => {
    new Vue({
        router,
        store,
        render: (h) => h(App)
    }).$mount('#app')
})