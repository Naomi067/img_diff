import Vue from 'vue'
import App from './App.vue'
import { syncSession$ } from './mixins/session'
import request from "./api/request"
import router from './router'
import store from './store'


Vue.config.productionTip = false
Vue.prototype.$http = request

syncSession$().then(() => {
    new Vue({
        router,
        store,
        render: (h) => h(App)
    }).$mount('#app')
})