import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";

import "../node_modules/bootstrap/dist/js/bootstrap.js";
import "../node_modules/bootstrap/dist/css/bootstrap.min.css";

import "./assets/main.css";

const app = createApp(App);

app.use(createPinia());
// app.use(router)

app.mount("#app");
