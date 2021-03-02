import Vue from 'vue'
import Vuelidate from 'vuelidate'
import App from './App.vue'
import router from './router'

Vue.config.productionTip = false
Vue.use(Vuelidate)

const DEFAULT_TITLE = 'Drown Gallery';
router.afterEach((to) => {
    Vue.nextTick(() => {
        document.title = to.meta.title || DEFAULT_TITLE;
    });
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
