// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Login from '../components/LoginForm.vue'
import Register from '../components/RegisterForm.vue'
import AcceptDonation from '../components/AcceptDonation.vue'
import AddToOrder from '../components/AddToOrder.vue'
import FindOrderItems from '../components/FindOrderItems.vue'
import FindSingleItem from '../components/FindSingleItem.vue'
import MyOrders from '../components/MyOrders.vue'
import PrepareOrder from '../components/PrepareOrder.vue'
import StartOrder from '../components/StartOrder.vue'

const routes = [
  { path: '/', name: 'Home', component: Home, meta: { requiresAuth: true } },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/accept-donation', component: AcceptDonation, meta: { requiresAuth: true } },
  { path: '/add-to-order', component: AddToOrder, meta: { requiresAuth: true } },
  { path: '/find-order-items', component: FindOrderItems, meta: { requiresAuth: true } },
  { path: '/find-single-item', component: FindSingleItem, meta: { requiresAuth: true } },
  { path: '/my-orders', component: MyOrders, meta: { requiresAuth: true } },
  { path: '/prepare-order', component: PrepareOrder, meta: { requiresAuth: true } },
  { path: '/start-order', component: StartOrder, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('user')
  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router