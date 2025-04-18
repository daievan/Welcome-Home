<template>
  <nav class="navbar">
    <div class="nav-left">
      <router-link to="/" class="logo-link">
        <img src="/static/logo.png" alt="Logo" class="logo" />
        <span class="title">WelcomeHome</span>
      </router-link>
    </div>
    <ul class="nav-right">
      <template v-if="isAuthenticated">
        <li class="nav-item username">{{ username }}</li>
        <li class="nav-item">
          <a href="#" @click.prevent="logout" class="nav-button">Log Out</a>
        </li>
      </template>
      <template v-else>
        <li class="nav-item">
          <router-link to="/login" class="nav-button">Log In</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/register" class="nav-button">Register</router-link>
        </li>
      </template>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  props: {
    isAuthenticated: Boolean,
    username: String
  },
  methods: {
    logout() {
      this.$emit('logout')
    }
  }
}
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 24px;
  background-color: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
  font-family: 'Helvetica Neue', Arial, sans-serif;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #111827;
}

.logo {
  height: 30px;
  margin-right: 10px;
}

.title {
  font-size: 20px;
  font-weight: bold;
  color: #111827;
}

.nav-right {
  display: flex;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 20px;
}

.nav-item {
  font-size: 15px;
  font-weight: 500;
}

.username {
  color: #374151;
}

.nav-button {
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 6px;
  background-color: transparent;
  color: #374151;
  transition: all 0.2s ease;
}

.nav-button:hover {
  background-color: #f3f4f6;
  color: #111827;
}
</style>
