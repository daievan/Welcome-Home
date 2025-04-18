import axios from 'axios'
const API = 'http://127.0.0.1:5001/api'

export function login(username, password) {
  return axios.post(`${API}/login`, { username, password })
}

export function register(data) {
  return axios.post(`${API}/register`, data)
}
