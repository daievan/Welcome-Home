<template>
  <div class="register-container">
    <div class="register-box">
      <h2>Create Account</h2>
      <form @submit.prevent="register">
        <input v-model="username" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <input v-model="first_name" placeholder="First Name" required />
        <input v-model="last_name" placeholder="Last Name" required />
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="phone" placeholder="Phone" required />
        <select v-model="role" required>
          <option disabled value="">Select Role</option>
          <option value="1">Staff</option>
          <option value="2">Volunteer</option>
          <option value="3">Client</option>
          <option value="4">Donor</option>
        </select>
        <button type="submit">Register</button>
        <div class="login-tip">
          Already have an account? <router-link to="/login">Log In</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      username: '',
      password: '',
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      role: ''
    }
  },
  methods: {
    async register() {
      try {
        const res = await axios.post('http://127.0.0.1:5001/api/register', {
          username: this.username,
          password: this.password,
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email,
          phone: this.phone,
          role: this.role
        })

        if (res.status === 201) {
          alert('Registration successful! Please log in.')
          this.$router.push('/login')
        }
      } catch (err) {
        alert(err.response?.data?.error || 'Registration failed.')
      }
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f3f4f6;
}

.register-box {
  background: #fff;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  width: 420px;
}

h2 {
  margin-bottom: 20px;
  text-align: center;
  color: #1f2937;
}

input, select {
  width: 100%;
  padding: 12px;
  margin-top: 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 15px;
  transition: border-color 0.3s;
}

input:focus, select:focus {
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

.login-tip {
  margin-top: 16px;
  text-align: center;
  color: #6b7280;
}

.login-tip a {
  color: #3b82f6;
  text-decoration: none;
}
</style>
