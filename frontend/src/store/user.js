import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    username: null,
    role: null,
    isLoggedIn: false
  }),
  actions: {
    login(userData) {
      this.username = userData.username
      this.role = userData.role
      this.isLoggedIn = true
    },
    logout() {
      this.username = null
      this.role = null
      this.isLoggedIn = false
    }
  }
})