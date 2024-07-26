import Vue from "vue";
import App from "./App.vue";
import VueRouter from "vue-router";
import Home from "./views/Home.vue";

Vue.config.productionTip = false;
Vue.use(VueRouter);

const routes = [{ path: "/", component: Home }];

const router = new VueRouter({
  routes,
});

new Vue({
  render: (h) => h(App),
  router,
}).$mount("#app");
