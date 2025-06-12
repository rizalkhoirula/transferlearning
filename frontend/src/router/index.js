import { createRouter, createWebHistory } from "vue-router";
import Dashboard from "../views/Dashboard.vue"; 
import Food from "../views/food.vue";
import Auth from "../views/auth.vue";
import detail from "../views/detail.vue";
import Livechat from "../views/livechat.vue";
const routes = [
  { path: "/", component: Dashboard },
  { path: "/food", component: Food },
  { path: "/auth", component: Auth },
  { path: "/detail", component: detail },
  { path: "/live-chat", component: Livechat },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
