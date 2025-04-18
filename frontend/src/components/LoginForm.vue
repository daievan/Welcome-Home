<template>
  <div class="login-container">
    <div class="login-box">
      <img src="/static/logo.png" alt="Logo" class="logo" />
      <h2>Welcome Home</h2>
      <form @submit.prevent="login">
        <input v-model="username" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Sign In</button>
      </form>
      <div class="signup-tip">
        Don't have an account? <router-link to="/register">Sign Up</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    async login() {
      try {
        const res = await axios.post('http://127.0.0.1:5001/api/login', {
          username: this.username,
          password: this.password
        })
        if (res.status === 200) {
          localStorage.setItem('user', JSON.stringify(res.data))
          alert('Login successful!')
          this.$router.push('/')
        }
      } catch (err) {
        alert(err.response?.data?.error || 'Login failed.')
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f3f4f6;
}

.login-box {
  background: #ffffff;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  width: 400px;
  text-align: center;
}

.logo {
  width: 60px;
  margin-bottom: 16px;
}

h2 {
  font-size: 22px;
  color: #1f2937;
  margin-bottom: 24px;
}

input {
  width: 100%;
  padding: 12px;
  margin-top: 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 15px;
  transition: border-color 0.3s;
}

input:focus {
  border-color: #6366f1;
  outline: none;
}

button {
  width: 100%;
  padding: 12px;
  margin-top: 20px;
  background-color: #2b3a55;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #1f2a40;
}

.signup-tip {
  margin-top: 20px;
  font-size: 14px;
  color: #6b7280;
}

.signup-tip a {
  color: #3b82f6;
  text-decoration: none;
}
</style>
