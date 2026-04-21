import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import LogoutView from '../views/LogoutView.vue'
import PlayView from '../views/PlayView.vue'
import FAQView from '../views/FAQView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/log-in',
      name: 'login',
      component: LoginView
    },
    {
      path: '/log-out',
      name: 'logout',
      component: LogoutView
    },
    {
      path: '/songs/:id',
      name: 'play',
      component: PlayView
    },
    {
      path: '/faq',
      name: 'faq',
      component: FAQView
    }
  ]
})

export default router
