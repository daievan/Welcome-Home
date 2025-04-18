<!-- App.vue -->
<template>
  <div>
    <NavBar
      :isAuthenticated="isLoggedIn"
      :username="username"
      @logout="logout"
    />
    <router-view />
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'

export default {
  name: 'App',
  components: { NavBar },
  data() {
    return {
      // 从 localStorage 读取一次，后面由 watcher 自动更新
      isLoggedIn: !!localStorage.getItem('user'),
      username: JSON.parse(localStorage.getItem('user') || '{}').username || ''
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('user')
      this.isLoggedIn = false
      this.username = ''
      this.$router.push('/login')
    }
  },
  watch: {
    // 每次路由变化都重新同步 localStorage
    '$route'() {
      this.isLoggedIn = !!localStorage.getItem('user')
      this.username = JSON.parse(localStorage.getItem('user') || '{}').username || ''
    }
  }
}
</script>
